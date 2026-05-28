import os

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from core.vector_store import build_vector_store, load_vector_store, get_retriever


# loads mistral language model
def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
    )


# combines retrieved documents into single context string
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


PROMPT_TEMPLATE = """You are an expert meeting assistant. Answer the user's question 
based on the meeting transcript context provided below.

Use whatever relevant information is available in the context to give 
the best possible answer. If someone is mentioned, share what you know 
about them from the transcript. Only say you cannot find information 
if the topic is completely absent from the context.

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}"""


# builds complete RAG pipeline from transcript
def build_rag_chain(transcript: str):

    vector_store = build_vector_store(transcript)

    retriever = get_retriever(vector_store, k=6)

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", PROMPT_TEMPLATE),
        ("human", "{question}"),
    ])

    # full LCEL RAG pipeline for retrieval + generation
    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# loads existing vector database and creates RAG chain
def load_rag_chain():

    vector_store = load_vector_store()

    retriever = get_retriever(vector_store, k=6)

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", PROMPT_TEMPLATE),
        ("human", "{question}"),
    ])

    # retrieval + prompt + llm response pipeline
    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# sends question to rag chain and returns final answer
def ask_question(rag_chain, question: str) -> str:
    print(f"Question : {question}")
    answer = rag_chain.invoke(question)
    print(f"answer : {answer}")
    return answer