import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

tipo_de_arquivo = ['site', 'youtube', 'pdf', 'csv', 'txt']

modelos_ai = {
    'OpenAI':  {'modelos': ['gpt-4', 'GPT-4.1 nano', 'o4-mini'], 'chat': ChatOpenAI},
    'Groq': {'modelos': ['gemma2-9b-it', 'llama-3.3-70b-versatile', 'meta-llama/llama-guard-4-12b', 'qwen-qwq-32b'], 'chat': ChatGroq},
}

MEMORIA = ConversationBufferMemory()


def load_modelo(modelos, modelos_selecionado, api_key):
    chat = modelos_ai[modelos]['chat'](
        model=modelos_selecionado,
        api_key=api_key)

    st.session_state['chat'] = chat


def page_chat():

    st.set_page_config(page_title='Pergunte-me',
                       page_icon=':robot_face:', layout='wide')

    st.header('😃 Bem vindo ao Pergunte-me!', divider=True)

    mensseger = st.session_state.get('memoria', MEMORIA)

    chat_model = st.session_state.get('chat')
    for mensagem in mensseger.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_user = st.chat_input('Pergunte-me algo!')

    if input_user:
        mensseger.chat_memory.add_user_message(input_user)
        chat = st.chat_message('human')
        chat.markdown(input_user)

        chat = st.chat_message('ai')
        response = chat.write_stream(chat_model.stream(input_user))
        mensseger.chat_memory.add_ai_message(response)

        st.session_state['memoria'] = mensseger


def sidebar():
    table = st.tabs(['suba seus arquivos', 'selecione seus modelos'])
    with table[0]:
        tipos_de_arquivos = st.selectbox('suba seus arquivos', tipo_de_arquivo)
        if tipos_de_arquivos == 'site':
            link = st.text_input('copie e cole o link do site')
        if tipos_de_arquivos == 'youtube':
            link = st.text_input('copie e cole o link do video')
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
        load_modelo(modelos, modelos_selecionado, api_key)


def main():
    page_chat()
    with st.sidebar:
        sidebar()


if __name__ == "__main__":
    main()
