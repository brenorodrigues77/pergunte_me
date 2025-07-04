import streamlit as st
from load_files import load_files
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


modelos_ai = {
    'OpenAI':  {'modelos': ['gpt-4', 'GPT-4.1 nano', 'o4-mini'], 'chat': ChatOpenAI},
    'Groq': {'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile', 'meta-llama/llama-guard-4-12b', 'qwen-qwq-32b'], 'chat': ChatGroq},
}


def load_model(modelos, modelos_selecionado, api_key, tipos_de_arquivos, file):

    document = load_files(tipos_de_arquivos, file)

    system_message = ''''Você é um assistente amigável chamado Oráculo.
            Você possui acesso às seguintes informações vindas
            de um documento {}:

            ####
            {}
            ####

            Utilize as informações fornecidas para basear as suas respostas.

            Sempre que houver $ na sua saída, substita por S.

            Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue"
            sugira ao usuário carregar novamente o Oráculo!'''.format(tipos_de_arquivos, document)

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')]
    )
    chat = modelos_ai[modelos]['chat'](
        model=modelos_selecionado, api_key=api_key)

    chain = template | chat

    st.session_state['chain'] = chain
