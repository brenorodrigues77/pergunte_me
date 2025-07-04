import os
from time import sleep
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader, CSVLoader, TextLoader
from fake_useragent import UserAgent


def page_loader(url):
    document = ''
    for i in range(3):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            document_list = loader.load()
            document = '\n\n'.join([doc.page_content for doc in document_list])
            break
        except:
            print(f'erro ao carregar pagina {i+1}')
            sleep(3)
    if document == '':
        st.error('erro ao carregar pagina')
        st.stop()
    return document


def youtube_loader(video_id):
    document = ''
    for i in range(3):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = YoutubeLoader(
                video_id, add_video_info=False, language=['pt'])
            document_list = loader.load()
            document = '\n\n'.join([doc.page_content for doc in document_list])
            break
        except:
            print(f'erro ao carregar video {i+1}')
            sleep(3)
    if document == '':
        st.error('erro ao carregar video')
        st.stop()
    return document


def pdf_loader(path):
    document = ''
    for i in range(3):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = PyPDFLoader(path)
            document_list = loader.load()
            document = '\n\n'.join([doc.page_content for doc in document_list])
            break
        except:
            print(f'erro ao carregar pdf {i+1}')
            sleep(3)
        if document == '':
            st.error('erro ao carregar pdf')
            st.stop()
    return document


def csv_loader(path):
    document = ''
    for i in range(3):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = CSVLoader(path)
            document_list = loader.load()
            document = '\n\n'.join([doc.page_content for doc in document_list])
            break
        except:
            print(f'erro ao carregar csv {i+1}')
            sleep(3)
        if document == '':
            st.error('erro ao carregar csv')
            st.stop()
    return document


def txt_loader(path):
    document = ''
    for i in range(3):
        try:
            os.environ['USER_AGENT'] = UserAgent().random
            loader = TextLoader(path)
            document_list = loader.load()
            document = '\n\n'.join([doc.page_content for doc in document_list])
            break
        except:
            print(f'erro ao carregar txt {i+1}')
            sleep(3)
        if document == '':
            st.error('erro ao carregar txt')
            st.stop()
    return document
