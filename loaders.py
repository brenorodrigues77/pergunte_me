from dotenv import load_dotenv
import os
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader, CSVLoader, TextLoader

load_dotenv()


def page_loader(url):
    loader = WebBaseLoader(url)
    document_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in document_list])
    return document

# FUNÇÃO PARA CORREÇÃO TODO


def youtube_loader(video_id):
    loader = YoutubeLoader(video_id, add_video_info=False, language=['pt'])
    document_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in document_list])
    return document


def pdf_loader(path):
    loader = PyPDFLoader(path)
    document_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in document_list])
    return document


def csv_loader(path):
    loader = CSVLoader(path)
    document_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in document_list])
    return document


def txt_loader(path):
    loader = TextLoader(path)
    document_list = loader.load()
    document = '\n\n'.join([doc.page_content for doc in document_list])
    return document
