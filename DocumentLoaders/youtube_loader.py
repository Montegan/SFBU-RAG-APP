from langchain_community.document_loaders import YoutubeLoader


load_youtube = YoutubeLoader.from_youtube_url(
    "https://www.youtube.com/watch?v=8OJC21T2SL4")
youtube_loaded = load_youtube.load()

print(youtube_loaded)
