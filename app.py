import streamlit as st
import tempfile
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from loaders import *


st.set_page_config(page_title='Pergunte-me',
                   page_icon=':robot_face:', layout='wide')

tipo_de_arquivo = ['site', 'youtube', 'pdf', 'csv', 'txt']

modelos_ai = {
    'OpenAI':  {'modelos': ['gpt-4', 'GPT-4.1 nano', 'o4-mini'], 'chat': ChatOpenAI},
    'Groq': {'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile', 'meta-llama/llama-guard-4-12b', 'qwen-qwq-32b'], 'chat': ChatGroq},
}

MEMORIA = ConversationBufferMemory()


def load_files(tipos_de_arquivos, file):

    if tipos_de_arquivos == 'site':
        document = page_loader(file)
    if tipos_de_arquivos == 'youtube':
        document = youtube_loader(file)
    if tipos_de_arquivos == 'pdf':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(file.read())
            name_file = temp.name
        document = pdf_loader(name_file)
    if tipos_de_arquivos == 'csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(file.read())
            name_file = temp.name
        document = csv_loader(name_file)
    if tipos_de_arquivos == 'txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(file.read())
            name_file = temp.name
        document = txt_loader(name_file)
    return document


def load_modelo(modelos, modelos_selecionado, api_key, tipos_de_arquivos, file):

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


def page_chat():

    st.header('😃 Bem vindo ao Pergunte-me!', divider=True)
    chain = st.session_state.get('chain')

    if chain is None:
        st.error('por favor, clique em "carregar Pergunta-me"')
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
    table = st.tabs(['suba seus arquivos', 'selecione seus modelos'])
    with table[0]:
        tipos_de_arquivos = st.selectbox('suba seus arquivos', tipo_de_arquivo)
        if tipos_de_arquivos == 'site':
            file = st.text_input('copie e cole o link do site')
        if tipos_de_arquivos == 'youtube':
            file = st.text_input('copie e cole o link do video')
        if tipos_de_arquivos == 'pdf':
            file = st.file_uploader('suba seu pdf', type=['.pdf'])
        if tipos_de_arquivos == 'csv':
            file = st.file_uploader('suba seu csv', type=['.csv'])
        if tipos_de_arquivos == 'txt':
            file = st.file_uploader('suba seu txt', type=['.txt'])

    with table[1]:
        modelos = st.selectbox('selecione seus modelos', modelos_ai.keys())
        modelos_selecionado = st.selectbox(
            'selecione seus modelos', modelos_ai[modelos]['modelos'])
        api_key = st.text_input(
            f'copie e cole sua api key, {modelos}',
            value=st.session_state.get(f'api_key {modelos}'),
            type='password')

        st.session_state[f'api_key {modelos}'] = api_key

    if st.button('carregar Pergunta-me', use_container_width=True):
        load_modelo(modelos, modelos_selecionado,
                    api_key, tipos_de_arquivos, file)


def main():
    with st.sidebar:
        sidebar()
    page_chat()


if __name__ == "__main__":
    main()
