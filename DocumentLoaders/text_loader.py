from langchain_community.document_loaders import TextLoader

load_text = TextLoader(
    "C:\\Users\\H00422003\\Desktop\\SFBU\\2ndsem\\GenAI\\langchain_rag\\data\\stateUnion.txt", encoding='utf-8')
text_loaded = load_text.load()
print(text_loaded)
