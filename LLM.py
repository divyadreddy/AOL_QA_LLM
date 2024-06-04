__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders.text import TextLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st

# Creates and store data as Chroma vectorstore (DB) in ./chroma_db
def create_vectorstore():
    ### Construct retriever ###
    loader = TextLoader('./QA_data_final.txt')
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, 
                                                                persist_directory='./chroma_db',
                                                                embedding=OpenAIEmbeddings(api_key=st.secrets['openai']["OPENAI_API_KEY"]))
    vectorstore.persist()

    return vectorstore

@st.cache_resource
def create_llm():
    llm = ChatOpenAI(openai_api_key=st.secrets['openai']["OPENAI_API_KEY"], model="gpt-3.5-turbo", temperature=0)

    vectorstore =Chroma(persist_directory='./chroma_db', embedding_function=OpenAIEmbeddings(api_key=st.secrets['openai']["OPENAI_API_KEY"]))
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    ### Contextualize question ###
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    ### Answer question ###
    system_prompt = (
        "You are an assistant who would be doing question-answering tasks. "
        "You need to exactly answer like Sri Sri Ravishankar alias Gurudev, in his words."
        "Use the only the following retrieved context to answer "
        "the question. If you don't know the answer, "
        "say that you will find out from Gurudev."
        "Do not add anything which is not from the provided context."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain