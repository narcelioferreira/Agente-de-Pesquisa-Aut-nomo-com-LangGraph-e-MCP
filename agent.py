import os
from typing import Annotated, TypedDict, List, Union, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import Tool

load_dotenv()

# 1. Definição do Estado do Agente (Mais robusto)
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "Histórico de mensagens"]
    steps_count: int  # Controle de iterações para evitar loops infinitos
    max_steps: int    # Limite máximo de pesquisas

# 2. Configuração das Ferramentas GRATUITAS (DuckDuckGo)
ddg_search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="duckduckgo_search",
    description="Útil para pesquisar tendências atuais na internet de forma gratuita.",
    func=ddg_search.run
)
tools = [search_tool]
tool_node = ToolNode(tools)

# 3. System Prompt Especializado
SYSTEM_PROMPT = """Você é um Engenheiro de IA Especialista em Análise de Mercado e Tendências Tecnológicas.
Sua missão é fornecer relatórios técnicos profundos, precisos e atualizados.

DIRETRIZES DE ANÁLISE:
1. PESQUISA: Sempre utilize a ferramenta de busca para validar tendências recentes (2025-2026).
2. ESTRUTURA DO RELATÓRIO:
   - # Título do Relatório
   - ## Resumo Executivo (O que é e por que importa)
   - ## Principais Players e Tecnologias (Quem está liderando)
   - ## Análise de Impacto (Prós, Contras e Riscos)
   - ## Tendências Futuras (O que esperar nos próximos 12 meses)
   - ## Fontes Consultadas (Links reais)
3. TOM DE VOZ: Profissional, técnico e imparcial.
4. CRITÉRIO DE PARADA: Se você já possui informações suficientes para preencher todas as seções acima com qualidade, finalize o relatório. Caso contrário, refine sua busca.

Importante: Se não encontrar informações sobre algo muito recente, admita a limitação, mas forneça o contexto mais próximo disponível."""

# 4. Configuração do Modelo GRATUITO (Groq - Llama 3)
# Nota: O usuário precisará de uma API Key gratuita do Groq (console.groq.com)
model = ChatGroq(
    model_name="llama-3.3-70b-versatile", 
    temperature=0.2,
    groq_api_key=os.getenv("GROQ_API_KEY")
).bind_tools(tools)

# 5. Definição dos Nós
def call_model(state: AgentState):
    messages = state['messages']
    # Adiciona o System Prompt se for a primeira mensagem
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = model.invoke(messages)
    return {
        "messages": [response],
        "steps_count": state.get("steps_count", 0) + 1
    }

def should_continue(state: AgentState) -> Literal["continue", "end"]:
    last_message = state['messages'][-1]
    
    # Se o modelo não chamou ferramentas, termina
    if not last_message.tool_calls:
        return "end"
    
    # Se atingiu o limite de passos, força o término para economizar tokens e evitar loops
    if state.get("steps_count", 0) >= state.get("max_steps", 5):
        return "end"
    
    return "continue"

# 6. Construção do Grafo
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

workflow.add_edge("action", "agent")

# Compilar o Grafo
graph = workflow.compile()

def run_research(query: str):
    """Função auxiliar para executar a pesquisa completa"""
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "steps_count": 0,
        "max_steps": 5
    }
    
    final_state = graph.invoke(initial_state)
    return final_state["messages"][-1].content

if __name__ == "__main__":
    # Teste de robustez
    print("Iniciando pesquisa robusta...")
    result = run_research("Qual o impacto do Model Context Protocol (MCP) no ecossistema de agentes em 2026?")
    print("\n--- RELATÓRIO FINAL ---\n")
    print(result)
