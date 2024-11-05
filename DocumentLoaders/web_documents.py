from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, NotionDBLoader, YoutubeLoader

webdocs = WebBaseLoader("https://www.sfbu.edu/student-health-insurance")
webdocs_loaded = webdocs.load()
print(webdocs_loaded)
