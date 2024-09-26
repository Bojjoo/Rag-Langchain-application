#Chatbot
MODEL_LLM="gpt-4o"
TEMPERATURE= 0
MODEL_EMBEDDING="text-embedding-3-large"
PROMPT_TEMPLATE="""
        You are an AI chatbot that answers questions based on context retrieved below. Follow the rules below:
        1. **If relevant data is available:**
        - Use the context to provide an informative and accurate answer. Be concise and direct in your response and just use the information in the context below!
        2. **If the relevant data is not needed to answer:**
        - Respond in a friendly, casual, and conversational manner. You can greet the user or share light-hearted, positive thoughts.
        3. **If no relevant data is available:**
        - Apologize politely and explain that you do not have enough information to answer the question at this time.You can ONLY uses information contained in the context below and does not hallucinate.
        \nContext:
        {context}\n
        Answer the question based on the above context: {question}"""

REGENERATE_QUESTION_PROMPT="""
        You are a helpful assistant that reformulates user questions based on prior conversation history. 
        Given the following chat history and the latest user question, create a standalone question that includes all necessary context from the chat history. 
        Ensure that the question can be fully understood without needing to refer back to the previous conversation.
        If the latest user input is a greeting, casual remark, or social communication(e.g.,"hi","nice to meet you","how are you"), return the input unchanged.
        If the user asks about information from the previous chat (e.g., their own name or details they provided earlier), 
        include that information in the reformulated question(as a hint in parentheses) based on the conversation history."""
#Retriever
MODEL_RERANK="ms-marco-MiniLM-L-12-v2" 
SEARCH_KWARGS={'k': 25, 'score_threshold': 0.1,'sorted': True}
SEARCH_TYPE="similarity_score_threshold"

#Vector database
SYSTEM_DATABASE="./vectorstores/db_faiss"
USER_DATABASE="./vectorstores/db_faiss_for_user"

SYSTEM_DOCUMENT="./data/data_system"
USER_DOCUMENT="./data/data_user"

#Load data
CHUNK_SIZE=1000
CHUNK_OVERLAP=200  

#History chat secsion
URL = "https://quality-sunbeam-22641.upstash.io"
TOKEN = "AVhxAAIjcDE4MmNkZjZmZDM3M2E0NDgwOTNlMDk1ZmEwYTJkYjE3N3AxMA"