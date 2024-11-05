from langchain_community.document_loaders import WikipediaLoader

userInput = input("enter search query: ")
load_wiki = WikipediaLoader(query=userInput, load_max_docs=2)
wiki_loaded = load_wiki.load()
print(wiki_loaded)
