from langchain_community.document_loaders import PyPDFLoader


loadpdf = PyPDFLoader(
    "C:\\Users\\H00422003\\Desktop\\SFBU\\2ndsem\\GenAI\\langchain_rag\\data\\sfbu-2024-2025-university-catalog-8-20-2024.pdf")
pdf_loaded = loadpdf.load()
print(len(pdf_loaded))
