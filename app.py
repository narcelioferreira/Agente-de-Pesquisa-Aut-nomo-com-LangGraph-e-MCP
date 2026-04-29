import streamlit as st
import os
from dotenv import load_dotenv
from agent import run_research
from langchain_core.messages import HumanMessage, AIMessage

# Configuração da Página
st.set_page_config(
    page_title="Especialista em IA - Análise de Mercado",
    page_icon="🤖",
    layout="wide"
)

# Carregar variáveis de ambiente
load_dotenv()

# Sidebar com informações técnicas (Para o Recrutador)
with st.sidebar:
    st.title("🛠️ Stack Técnica")
    st.markdown("""
    Este projeto demonstra competências avançadas em Engenharia de IA:
    
    - **Orquestração:** LangGraph (Fluxos Cíclicos)
    - **LLM:** GPT-4o-mini
    - **Ferramentas:** MCP + Tavily Search
    - **Framework:** LangChain / Pydantic
    - **Interface:** Streamlit
    
    ---
    **Desenvolvido por:** [Seu Nome]
    *Formação Engenheiro de IA - Scoras Academy*
    """)
    
    if st.button("Limpar Histórico"):
        st.session_state.messages = []
        st.rerun()

# Título Principal
st.title("🤖 Agente Especialista em Tendências de IA")
st.subheader("Análises profundas de mercado e tecnologia em tempo real.")

# Inicializar histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do Usuário
if prompt := st.chat_input("Sobre qual tendência de IA você quer saber hoje?"):
    # Adicionar mensagem do usuário ao chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do Agente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Iniciando pesquisa profunda e análise de mercado...*")
        
        try:
            # Executar a lógica do LangGraph
            # Nota: Em produção, você usaria streaming para uma melhor UX
            response = run_research(prompt)
            
            message_placeholder.markdown(response)
            
            # Adicionar resposta ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Ocorreu um erro na pesquisa: {str(e)}")
            message_placeholder.markdown("Desculpe, tive um problema ao acessar as ferramentas de pesquisa. Verifique suas chaves de API.")

# Rodapé informativo
st.markdown("---")
st.caption("Nota: Este agente utiliza LangGraph para realizar múltiplas iterações de pesquisa antes de entregar o relatório final.")
