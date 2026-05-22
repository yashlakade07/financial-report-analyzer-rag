import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Global variable to hold our vector store in memory
vector_store = None

def get_llm():
    return ChatOllama(
        model="qwen2.5:7b",
        temperature=0,
        base_url="http://host.docker.internal:11434"
    )

def get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://host.docker.internal:11434"
    )

def process_pdf(file_path: str):
    global vector_store
    
    # 1. Load the PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 2. Split the text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # 3. Create Embeddings and store them in FAISS (Vector DB)
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(splits, embeddings)
    
    return len(splits)

def ask_question(question: str):
    global vector_store
    if not vector_store:
        raise ValueError("No document has been processed yet. Please upload a PDF.")

    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    system_prompt = (
        "You are an expert financial analyst. Use the following pieces of retrieved context to "
        "answer the user's question. If you don't know the answer based on the context, say that "
        "you don't know. Keep the answer concise and professional.\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": question})
    
    # Extract source pages
    sources = [f"Page {doc.metadata.get('page', 'Unknown')}" for doc in response["context"]]
    
    return {
        "answer": response["answer"],
        "sources": list(set(sources)) # Remove duplicates
    }