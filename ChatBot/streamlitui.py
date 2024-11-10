# Import necessary libraries
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from chromadab import vector_store
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, WikipediaLoader, YoutubeLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables
_ = load_dotenv()

# Initialize components
# Set up the OpenAI client
client = ChatOpenAI(api_key=st.secrets["OPENAI_API_KEY"])
llm = ChatOpenAI()
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
string_parser = StrOutputParser()

# Initialize Vector Store for embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(collection_name="my_chroma",
                      embedding_function=embeddings,
                      persist_directory="./chroma_sfbu")

# Define splitters and loaders
splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=1000,
                                          chunk_overlap=200, length_function=len, is_separator_regex=False)


def load_documents(file_path, loader_type="pdf"):
    if loader_type == "pdf":
        loader = PyPDFLoader(file_path)
    elif loader_type == "text":
        loader = TextLoader(file_path, encoding='utf-8')
    elif loader_type == "web":
        loader = WebBaseLoader(file_path)
    elif loader_type == "wiki":
        loader = WikipediaLoader(query=file_path, load_max_docs=2)
    elif loader_type == "youtube":
        loader = YoutubeLoader.from_youtube_url(file_path)
    else:
        raise ValueError("Unsupported loader type.")

    loaded_docs = loader.load()
    return splitter.split_documents(loaded_docs)


def embed_documents(docs):
    vector_store.add_documents(documents=docs)
    print("Documents embedded in vector store.")


def rag_chatbot_app(question):
    system_prompt = "You are a helpful Assistant. Answer user questions only from the provided context. Context: {context}."
    main_prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", "{question}")])

    retrieval_chain = {"context": retriever, "question": RunnablePassthrough()}
    main_chain = retrieval_chain | main_prompt | llm | string_parser
    return main_chain.invoke(question)


# Streamlit UI Setup
st.title("SFBU RAG Chatbot")

# Upload Documents section at the top
st.markdown("### Upload Documents")
if st.button("Upload Documents"):
    doc_type = st.selectbox("Select Document Type", [
                            "PDF", "Text", "Web", "Wikipedia", "YouTube"])
    if doc_type == "PDF":
        file_path = st.file_uploader("Upload a PDF file", type="pdf")
        if file_path:
            docs = load_documents(file_path, loader_type="pdf")
            embed_documents(docs)
    elif doc_type == "Text":
        file_path = st.file_uploader("Upload a Text file", type="txt")
        if file_path:
            docs = load_documents(file_path, loader_type="text")
            embed_documents(docs)
    elif doc_type == "Web":
        url = st.text_input("Enter a webpage URL:")
        if url:
            docs = load_documents(url, loader_type="web")
            embed_documents(docs)
    elif doc_type == "Wikipedia":
        query = st.text_input("Enter Wikipedia search query:")
        if query:
            docs = load_documents(query, loader_type="wiki")
            embed_documents(docs)
    elif doc_type == "YouTube":
        youtube_url = st.text_input("Enter YouTube video URL:")
        if youtube_url:
            docs = load_documents(youtube_url, loader_type="youtube")
            embed_documents(docs)

# Chat interface below the document upload section
st.markdown("---")
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything based on the documents..."):
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant's response
    with st.chat_message("assistant"):
        # Generate response from the RAG chatbot
        response = rag_chatbot_app(prompt)
        st.markdown(response)

    # Append assistant's response
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
