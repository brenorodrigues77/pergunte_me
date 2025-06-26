import streamlit as st

tipo_de_arquivo = ['site', 'youtube', 'pdf', 'csv', 'txt']

mensagens_exemplo = [
    ('user', 'Oi'),
    ('assistant', 'Olá, como posso ajudar?'),
    ('user', 'tudo otimo')
]


def pagina_chat():

    st.set_page_config(page_title='Pergunte-me',
                       page_icon=':robot_face:', layout='wide')

    st.header('😃 Bem vindo ao Pergunte-me!', divider=True)

    mensseger = st.session_state.get('mensseger', mensagens_exemplo)

    for message in mensseger:
        chat = st.chat_message(message[0])
        chat.markdown(message[1])

    input_user = st.chat_input('Pergunte-me algo!')

    if input_user:
        mensseger.append(('user', input_user))
        st.session_state['mensseger'] = mensseger
        st.rerun()


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


def main():
    pagina_chat()
    with st.sidebar:
        sidebar()


if __name__ == "__main__":
    main()
