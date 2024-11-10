import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from chromadab import vector_store

_ = load_dotenv()

llm = ChatOpenAI()
retriver = vector_store.as_retriever(search_kwargs={"k": 3})
string_parser = StrOutputParser()


def app(question):
    system_prompt = "You are a helpfull Assistant. Your task is to answer user questions only from the provided context. context:{context}."
    main_prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", "{question}")])

    retrivalChain = {"context": retriver,

                     "question": RunnablePassthrough()}

    main_chain = retrivalChain | main_prompt | llm | string_parser

    answer = main_chain.invoke(question)

    print(answer)


user_question = "give me a summary about  odebede's life"
app(user_question)
