import os 
from dotenv import load_dotenv


load_dotenv() 

#--LLM--
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

#--Embeddings---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"



