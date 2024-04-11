"""
This script is where we build the front end chatbot which hosts
the LLM model
faiss-cpu - vector store
"""
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
#from langchain_community.chat_models import ChatOpenAI
from htmlTemplate import css, bot_template, user_template
from langchain_community.llms import HuggingFaceHub

def get_pdf_texts(pdf_docs):
    """
    This function gets pdfs and return all the text contents in the pdfs
    """
    text = ""
    for pdf in pdf_docs:
        #It creates pages from the pdfs and we read through pages to get the texts
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_txt):
    text_spliiter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 500,
        chunk_overlap = 200,
        length_function = len
    )
    chunks = text_spliiter.split_text(raw_txt)
    return chunks

def get_vector_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-large")
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding= embeddings)
    #vectorstore.save_local("/Users/sahithya/Documents/Study Materials/Machine Learning/Stats_Chatbot/vectors/")
    return vectorstore

def get_conversation_chain(vector_store):
    """
    Langchain allows to create conversation chain which also allows to add memory.
    Memory is added so we can ask followup question from the previous replies.
    Chatbot gets to know the context of the question
    """
    print(vector_store)
    #llm = ChatOpenAI() vennify/t5-base-grammar-correction- poor performance
    llm = HuggingFaceHub(repo_id ="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":1024})
    print(llm)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    #chat with the vector store and have memory
    #vector_store = FAISS.load_local(folder_path = "./vectors/", embeddings = embeddings)
    retriever = vector_store.as_retriever()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = retriever,
        memory = memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question':user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i%2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Statsy and know more about Statistics", page_icon=":nerd:", layout="wide")

    #add css on the top
    st.write(css, unsafe_allow_html=True)
    #initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with Statsy :nerd_face:")
    user_question = st.text_input("Ask your question about the Statistics")
    if user_question:
        handle_userinput(user_question)

    st.write(user_template.replace("{{MSG}}", "hello robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "hello muggle"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Stats documents")
        pdf_docs = st.file_uploader(
            "Upload your Stats books and click on Process", accept_multiple_files=True)
        #Do the process only if we click on the button so we add if
        if st.button("Process"):
            with st.spinner("Processing"):
                #get pdfs
                raw_txt = get_pdf_texts(pdf_docs)
                #get text chunks
                text_chunks = get_text_chunks(raw_txt)
                #create vector store
                vector_store = get_vector_store(text_chunks)
                #create conversation chain
                #conversation is what that is going to have the result
                #session_state will not make the variable reload and persists the result
                st.session_state.conversation = get_conversation_chain(vector_store)
                print('conversation state done')


if __name__ == '__main__':
    main()