import tempfile
from loaders import *


def load_files(tipos_de_arquivos, file):

    if tipos_de_arquivos == 'Site':
        document = page_loader(file)
    if tipos_de_arquivos == 'Youtube':
        document = youtube_loader(file)
    if tipos_de_arquivos == 'Pdf':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(file.read())
            name_file = temp.name
        document = pdf_loader(name_file)
    if tipos_de_arquivos == 'Csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(file.read())
            name_file = temp.name
        document = csv_loader(name_file)
    if tipos_de_arquivos == 'Txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(file.read())
            name_file = temp.name
        document = txt_loader(name_file)
    return document
