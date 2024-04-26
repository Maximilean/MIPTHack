import io
import requests
from PyPDF2 import PdfReader


def download_file(url):
    """
    считывает текст с pdf-файла по url
    возвращает текст статьи в формате str

    :url: - str, ссылка
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers, timeout=120)
    bytes = io.BytesIO(response.content)
    pdf = PdfReader(bytes)

    raw_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        raw_text += " " + text

    full_text = preprocess(raw_text)
    return full_text


def preprocess(text):
    """
    убирает перенос слов на новую строку и разбиение на абзацы
    """
    
    text1 = text.replace("-\n", "")
    text2 = text1.replace("\n", " ")
    return text2
