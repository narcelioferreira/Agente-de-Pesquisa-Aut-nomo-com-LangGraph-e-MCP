# Agente Especialista em Análise de Mercado (LangGraph + MCP)

Este projeto foi desenvolvido como parte do meu portfólio de Engenheiro de IA, aplicando conceitos avançados de sistemas multi-agentes e fluxos de trabalho cíclicos.

## 🚀 Tecnologias Utilizadas
- **LangGraph**: Orquestração de estados e loops de pesquisa.
- **OpenAI GPT-4o-mini**: Cérebro do agente para tomada de decisão.
- **Tavily Search**: Ferramenta de busca otimizada para LLMs.
- **Streamlit**: Interface de usuário interativa.
- **MCP (Model Context Protocol)**: Integração padronizada de ferramentas.

## 🧠 Arquitetura do Agente
O agente utiliza um grafo cíclico onde:
1. Analisa a pergunta do usuário.
2. Decide se precisa de informações externas.
3. Executa buscas via ferramentas de pesquisa.
4. Sintetiza os dados e avalia se a resposta está completa.
5. Gera um relatório final estruturado.

## 🛠️ Como Executar
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Configure suas chaves no arquivo `.env`.
4. Execute o app: `streamlit run src/app.py`.
