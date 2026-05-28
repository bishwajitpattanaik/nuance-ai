import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# folder where chroma database will be stored
CHROMA_DIR = "vector_db"

# chroma collection name
COLLECTION_NAME = "meeting_transcript"

# embedding model name
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# loads huggingface embedding model
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
    )


# builds vector store from transcript
def build_vector_store(transcript: str) -> Chroma:

    print("Building Vector Store...")

    # splits transcript into smaller chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(transcript)

    # converts chunks into langchain documents
    docs = [
        Document(
            page_content=chunk,
            metadata={"chunk_index": i}
        )
        for i, chunk in enumerate(chunks)
    ]

    # loads embeddings model
    embeddings = get_embeddings()

    # creates and stores embeddings in chroma db
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )

    print(f"Stored {len(docs)} chunks in vector database")

    return vector_store


# loads existing chroma vector store
def load_vector_store() -> Chroma:

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vector_store


# creates retriever for similarity search
def get_retriever(vector_store: Chroma, k: int = 4):

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )