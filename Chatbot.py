from config import *
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder

from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from flashrank import Ranker
from langchain.retrievers import ContextualCompressionRetriever

import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
#os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] =os.getenv("OPENAI_API_KEY")

class chatbot:
    def __init__(self) :
        self.model_llm=ChatOpenAI(temperature=TEMPERATURE,model= MODEL_LLM)
        self.model_embedding=OpenAIEmbeddings(model=MODEL_EMBEDDING)
        self.model_rerank=Ranker(model_name=MODEL_RERANK,max_length=5000)

    def prompt_template(self, question, context):
        template=PROMPT_TEMPLATE
        pt=ChatPromptTemplate.from_template(template)
        prompt=pt.format(context=context,question=question)
        return prompt
    
    def get_answer(self, prompt_template):
        response=self.model_llm.invoke(prompt_template)
        return response
    
    def retriever(self,question,retriever):
        compressor = FlashrankRerank(client=self.model_rerank, top_n=5)
        compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)

        compressed_docs = compression_retriever.invoke(question)

        content_text="\n\n---\n\n".join([doc.page_content for doc in compressed_docs if doc.metadata['relevance_score']>0.5])
        return compressed_docs,content_text
    

    def regenerate_question(self,question,history):
        history_chat=history.messages[-10::]
        remake_question_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", REGENERATE_QUESTION_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        question_pt=remake_question_prompt.format(chat_history=history_chat,question=question)
        new_question=self.model_llm.invoke(question_pt)
        return new_question.content


    def get_answer_with_memory(self,question,context,history):
        prompt=self.prompt_template(question,context)
        answer=self.model_llm.invoke(prompt)
        return answer
        
    
