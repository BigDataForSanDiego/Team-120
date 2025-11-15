import json
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data_import/processed_data")
DEFAULT_JSON = "resource_masterfile_preview.json"

def load_json(filepath=None):
    if filepath is None:
        filepath = os.path.join(DATA_DIR, DEFAULT_JSON)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def flatten_json(y, prefix=""):
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            out.update(flatten_json(v, f"{prefix}{k}."))
    elif isinstance(y, list):
        for i, v in enumerate(y):
            out.update(flatten_json(v, f"{prefix}{i}."))
    else:
        out[prefix[:-1]] = str(y)
    return out

def build_vectordb(json_data):
    text_data = []
    if isinstance(json_data, list):
        for item in json_data:
            flat = flatten_json(item)
            text_data.append("\n".join(f"{k}: {v}" for k, v in flat.items()))
    else:
        flat = flatten_json(json_data)
        text_data.append("\n".join(f"{k}: {v}" for k, v in flat.items()))

    docs = [Document(page_content=t) for t in text_data]
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(split_docs, embeddings, persist_directory="./chroma_db")
    return vectordb

def get_chatbot(json_path=None):
    data = load_json(json_path)
    vectordb = build_vectordb(data)
    llm = ChatOpenAI(model="gpt-4o-mini")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(llm, vectordb.as_retriever(), memory=memory)
