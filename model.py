# ! pip install chromadb

from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage
from langchain.document_loaders import TextLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models.gigachat import GigaChat

auth = 'NTlkY2MyZmItM2Q4ZC00ZWMzLWE2NjAtNTI3MzZhOTk2ZjQzOjVhZGJiZDQxLTc0YjAtNDQxNi04YjAzLTUxZDVmYTY4NTkwNw=='


class Agent():
    def __init__(self, texts):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        if type(texts) != list:
            docs = text_splitter.create_documents([texts])
        else:
            docs = text_splitter.create_documents(texts)
        self.emb_model = GigaChatEmbeddings(credentials=auth, 
                                            verify_ssl_certs=False,
                                            scope='GIGACHAT_API_CORP')
        db = Chroma.from_documents(docs, self.emb_model)
        self.llm = GigaChat(credentials=auth,
                            model='GigaChat:latest', 
                            scope='GIGACHAT_API_CORP',
                            verify_ssl_certs=False)
        self.qa_chain = RetrievalQA.from_chain_type(self.llm, 
                                                    retriever=db.as_retriever())
        

    def __call__(self, question):
        answer = self.qa_chain({"query": question})
        return answer
  