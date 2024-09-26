from config import *
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from Chatbot import chatbot
import os

class Load_data:
    def __init__(self):
        self.text_splitter=RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP,length_function=len)
        self.model=chatbot()
        self.db_system=FAISS.load_local(SYSTEM_DATABASE,self.model.model_embedding,allow_dangerous_deserialization=True)
        self.retriever_system=self.db_system.as_retriever(search_kwargs=SEARCH_KWARGS, search_type=SEARCH_TYPE)
    
    ## For user
    def check_user_db(self):
        self.db_user=FAISS.load_local(USER_DATABASE,self.model.model_embedding,allow_dangerous_deserialization=True)
        self.retriever_user=self.db_user.as_retriever(search_kwargs=SEARCH_KWARGS, search_type=SEARCH_TYPE)
        return self.db_user

    def split_document(self,pdf_file):
        pdf_reader=PyPDFLoader(pdf_file)
        documents=pdf_reader.load()
        chunks=self.text_splitter.split_documents(documents)
        return chunks

    def To_vectorstore(self, chunks):
        db=FAISS.from_documents(chunks, self.model.model_embedding)
        #db.save_local(USER_DATABASE)
        return db
    
    def add_to_vectorstore(self, new_db):
        self.db_user.merge_from(new_db)
        self.db_user.save_local(USER_DATABASE)

    def delete_from_vectorstore(self,file_name):
        docstore=self.db_user.docstore._dict
        key_delete=[]
        for key,values in docstore.items():
            if values.metadata['source'].endswith(f"{file_name}"):
                key_delete.append(key)
        self.db_user.delete(key_delete)
        self.db_user.save_local(USER_DATABASE)
        os.remove(f"{USER_DOCUMENT}/{file_name}")
    
    ## For system
    def create_db_from_files(self):
        loader = DirectoryLoader(SYSTEM_DOCUMENT, glob="*.pdf", loader_cls = PyPDFLoader)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)

        # Embeding
        db = FAISS.from_documents(chunks, self.model.model_embedding)
        db.save_local(SYSTEM_DATABASE)
        return db
    