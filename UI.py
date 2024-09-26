import os
import requests
import streamlit as st
import time


# Kiểm tra nếu chưa có ID, yêu cầu người dùng nhập ID trước

if "user_id" not in st.session_state:
    id_input = st.text_input("Please enter your User_ID to start chatting:")
    if id_input:
        st.session_state["user_id"] = id_input

if "user_id" in st.session_state:
    st.write(f"Your user id is: {st.session_state['user_id']}")
#id = st.text_input("Please enter your User_ID to start chatting:")

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://127.0.0.1:8000/get_answer/")
def response_generator(text):
    for word in text.strip():
        yield word + ""
        time.sleep(0.01)

def handler_input(prompt: str):
    data = {
    "question": prompt,
    "id": st.session_state['user_id']
}
    
    try:
        # Gửi yêu cầu POST đến endpoint FastAPI
        response = requests.post(url=CHATBOT_URL, json=data)
        
        # Kiểm tra xem yêu cầu có thành công hay không
        if response.status_code == 200:
            # Trả về nội dung phản hồi
            return response.json()
        else:
            # Nếu có lỗi, trả về thông báo lỗi
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        # Bắt lỗi trong quá trình gọi API
        return f"Error: {str(e)}"

#CHATBOT_URL = os.getenv("CHATBOT_URL", "http://127.0.0.1:8000/get_answer/")
with st.sidebar:
    st.header("About")

st.title("Hello This is Rag Langchain application on FastAPI")
st.info(
    "Nice to meet you."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Chill out..."):
        response = handler_input(prompt)


    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(response))

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": response,
        }
    )


#st.write(st.session_state.messages)