from Chatbot import chatbot
from Load_data import Load_data
from config import *
from fastapi import FastAPI,UploadFile, File, HTTPException
import shutil
import os
from pydantic import BaseModel
from langchain_community.chat_message_histories import UpstashRedisChatMessageHistory

# Define Pydantic model to validate request body
class QuestionRequest(BaseModel):
    question: str
    id:str


data=Load_data()
bot=chatbot()
retriever_system=data.retriever_system

app=FastAPI(
    title="RAG_APP",
    description="'Hello This is Rag Langchain application on FastAPI !!!'"
)

@app.get("/")
def read_root():
    return {
        'Hello This is Rag Langchain application on FastAPI !!!'
    }

@app.post('/upload_data')
async def upload_file(file: UploadFile = File(...)):
    
    if file.filename.endswith('.pdf'):
        with open(f"{USER_DOCUMENT}/{file.filename}","wb") as buff:
            shutil.copyfileobj(file.file,buff)
        chunks = data.split_document(f"{USER_DOCUMENT}/{file.filename}")
    else:
        return {"message": "Only pdf files are supported"}
    
    # bỏ vào vectorstore mới
    new_db_for_user = data.To_vectorstore(chunks)
    try : # Nếu có db rồi
        db_user=data.check_user_db()
        data.add_to_vectorstore(new_db_for_user)
    except: #Nếu chưa có db
        new_db_for_user.save_local(f"{USER_DATABASE}")
        db_user=data.check_user_db()

    db_user_aftersave=data.db_user
    retriever_user=data.retriever_user

    return {"message": f"Successfully uploaded {file.filename}", 
            "num_splits" : len(chunks)}

@app.get("/take_relevant_data")
async def take_relevant_data(question:str):
    similar_docs,context=bot.retriever(question,retriever=retriever_system)
    if len(similar_docs)==0 :
        raise HTTPException(status_code=400,detail='Data not found!')
    else:
        return context


@app.post('/get_answer/')
async def get_response(data:QuestionRequest):
    question = data.question
    id_value = data.id
    history = UpstashRedisChatMessageHistory(
        url=URL, token=TOKEN, session_id=id_value
    )
    new_question = bot.regenerate_question(question, history)
    similar_docs, context = bot.retriever(new_question, retriever=retriever_system)
    response = bot.get_answer_with_memory(new_question, context, history)
    history.add_user_message(question)
    #history.add_user_message(new_question)
    history.add_ai_message(response)
    return response.content


@app.get('/get_answer_about_users_data/')
async def get_response(query:str):
    question=query
    try:
        similar_docs,context=bot.retriever(question,retriever=data.retriever_user)
        pt=bot.prompt_template(question=question,context=context)
        response=bot.get_answer(pt)
        return response.content
    except:
        return {"Hello, nice to meet you! Look like you have not uploaded any documents yet! Please Upload data!"}
    
@app.delete("/delete_file/")
def delete_file(file_name:str):
    try:
        data.delete_from_vectorstore(file_name=file_name)
        return {"Deleted file!"}
    except:
        return {f"The file {file_name} is not existed!"}
    

