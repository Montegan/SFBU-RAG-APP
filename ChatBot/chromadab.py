import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from doc_loders import pdfLoaders, text_loaders, web_loaders, youtube_loder

_ = load_dotenv()
pdfPath = "C:\\Users\\H00422003\\Desktop\\SFBU\\2ndsem\\GenAI\\langchain_rag\\data\\sfbu-2024-2025-university-catalog-8-20-2024.pdf"
textPath = "C:\\Users\\H00422003\\Desktop\\SFBU\\2ndsem\\GenAI\\langchain_rag\\data\\stateUnion.txt"
web = "https://www.sfbu.edu/student-health-insurance"
youtubeLink = "https://www.youtube.com/watch?v=kuZNIvdwnMc&ab"

docs = pdfLoaders(pdfPath)
text_docs = text_loaders(textPath)
web_docs = web_loaders(web)
youtube_docs = youtube_loder(youtubeLink)


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(collection_name="my_chroma",
                      embedding_function=embeddings,
                      persist_directory="./chroma_sfbu")


def embed_documents():
    vector_store.add_documents(documents=docs)
    vector_store.add_documents(documents=text_docs)
    vector_store.add_documents(documents=web_docs)
    vector_store.add_documents(youtube_docs)
    print("db created")
