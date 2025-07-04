import streamlit as st
import tempfile
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from loaders import *
from load_files import *
from load_models import *


st.set_page_config(page_title='Pergunte-me',
                   page_icon=':robot_face:', layout='wide')

tipo_de_arquivo = [
    'Site', 'Youtube', 'Pdf', 'Csv', 'Txt']

modelos_ai = {
    'OpenAI':  {'modelos': ['gpt-4', 'GPT-4.1 nano', 'o4-mini'], 'chat': ChatOpenAI},
    'Groq': {'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile', 'meta-llama/llama-guard-4-12b', 'qwen-qwq-32b'], 'chat': ChatGroq},
}

MEMORIA = ConversationBufferMemory()


def page_chat():

    st.header('😃 Bem vindo ao Pergunte-me!', divider=True)
    chain = st.session_state.get('chain')

    if chain is None:
        st.write('Por favor, Clique em "carregar Pergunta-me"')
        st.stop()

    mensseger = st.session_state.get('memoria', MEMORIA)

    for mensagem in mensseger.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_user = st.chat_input('Pergunte-me algo!')

    if input_user:
        mensseger.chat_memory.add_user_message(input_user)
        chat = st.chat_message('human')
        chat.markdown(input_user)

        chat = st.chat_message('ai')
        response = chat.write_stream(chain.stream(
            {'input': input_user,
             'chat_history': mensseger.buffer_as_messages}))

        mensseger.chat_memory.add_ai_message(response)

        st.session_state['memoria'] = mensseger


def sidebar():
    table = st.tabs(['Suba seus arquivos', 'Selecione seus modelos'])
    with table[0]:
        tipos_de_arquivos = st.selectbox('Suba seus arquivos', tipo_de_arquivo)
        if tipos_de_arquivos == 'Site':
            file = st.text_input('Copie e cole o link do site')
        if tipos_de_arquivos == 'Youtube':
            file = st.text_input('Copie e cole o link do video')
        if tipos_de_arquivos == 'Pdf':
            file = st.file_uploader('suba seu pdf', type=['.pdf'])
        if tipos_de_arquivos == 'Csv':
            file = st.file_uploader('Suba seu csv', type=['.csv'])
        if tipos_de_arquivos == 'Txt':
            file = st.file_uploader('Suba seu txt', type=['.txt'])

    with table[1]:
        modelos = st.selectbox('Selecione seus modelos', modelos_ai.keys())
        modelos_selecionado = st.selectbox(
            'Selecione seus modelos', modelos_ai[modelos]['modelos'])
        api_key = st.text_input(
            f'Copie e cole sua api key, {modelos}',
            value=st.session_state.get(f'api_key {modelos}'),
            type='password')

        st.session_state[f'api_key {modelos}'] = api_key

    if st.button('Carregar Pergunta-me', use_container_width=True):
        load_model(modelos, modelos_selecionado,
                   api_key, tipos_de_arquivos, file)


def main():
    with st.sidebar:
        sidebar()
    page_chat()


if __name__ == "__main__":
    main()
