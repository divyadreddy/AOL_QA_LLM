__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from PIL import Image

from elements import headAndCss, title, desc, img_to_html
from LLM import create_llm
from collections import deque 

# Website
st.set_page_config(
    page_icon=Image.open('./imgs/title_icon.png'),
    initial_sidebar_state="expanded",
    page_title='Ask Gurudev', 
    layout="centered" 
)

# Helper funtions
rag_chain =create_llm()

# Streamed response emulator
def ask_sri_sri(question, history):
    # return "HELLO"
    response =rag_chain.invoke({"input": question, "chat_history": history})

    answer =response['answer']

    # for word in answer.split():
    #     yield word + " "
    #     time.sleep(0.05)
    return answer


st.markdown(headAndCss, unsafe_allow_html=True)

icon ={"user":"./imgs/user.png", "assistant":"./imgs/sri_sri_face.png"}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = deque([])
elif len(st.session_state.messages) > 10:
    st.session_state.messages.popleft()

with st.sidebar:
    # st.markdown(img_to_html('./imgs/aol.png'), unsafe_allow_html=True)
    st.markdown(title, unsafe_allow_html=True)
    st.divider()
    st.image('./imgs/sri_sri.png', use_column_width=True)
    st.markdown(desc, unsafe_allow_html=True)


for message in st.session_state.messages:
    st.chat_message(message["role"], avatar=icon[message["role"]]).write(message["content"])

if question := st.chat_input("Ask Gurudev...", key="chat_input_placeholder"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message in chat message container
    with st.chat_message("user", avatar=icon["user"]):
        st.markdown(question)

    answer = ask_sri_sri(question, list(st.session_state.messages))
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=icon["assistant"]):
        st.markdown(answer)
        # answer =st.write_stream(ask_sri_sri(question, st.session_state.messages))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Remove the default header and footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       header {visibility: hidden; }
       footer {visibility: hidden; }
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)