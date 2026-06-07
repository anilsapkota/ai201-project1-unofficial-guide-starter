import chromadb
from sentence_transformers import SentenceTransformer
from ingest import fetch_and_clean, chunk_text, SOURCES 
import os 
from dotenv import load_dotenv
load_dotenv() 
from openai import OpenAI
from config import OPENAI_API_KEY


EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "geospatial_guide"
TOP_K = 5 

model = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path="./chroma_db")

openai_client = OpenAI() 



#--LLM--
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 


def build_vector_store():

    #delete existing collection if rebuilding
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass 

    collection = client.create_collection(COLLECTION_NAME)

    #ingesting all chunks
    all_chunks = []
    for source in SOURCES:
        print(f"Ingesting : {source['name']}..")
        try:
            text = fetch_and_clean(source["url"])
            chunks = chunk_text(text, source= source["name"])
            all_chunks.extend(chunks)
            print(f"-> {len(chunks)} chunks")
        except Exception as e:
            print(f" -> FAILED: {e}")
    print(f"\nTotal chunks ready to embed: {len(all_chunks)}")
    
    texts = [c["text"]for c in all_chunks]
    sources = [c["source"] for c in all_chunks]
    ids = [f"chunk_{i}"for i in range(len(all_chunks))]

    print(f"Embedding {len(all_chunks)} chunks...")
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        documents = texts,   #the raw text of each chunk(stored so you can read it later)
        embeddings=embeddings, # the vectors used for similiarity text
        metadatas=[{"source": s}for s in sources],  #metadata is used for citation 
        ids = ids
    )
    
    print(f"Done! {len(all_chunks)} chunks stored in ChromaDB.")

def query(question: str):
    collection = client.get_collection(COLLECTION_NAME)
    question_embedding = model.encode(question).tolist() 

    results = collection.query(
        query_embeddings= [question_embedding],
        n_results = TOP_K,
        include=["documents","metadatas","distances"]
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text":doc,
            "source":meta["source"],
            "distance": round(dist,4)
        })
    
    return chunks 


def generate(question: str, chunks: list):
    context = "\n\n".join([
        f"Source: {c['source']}\n{c['text']}"
        for c in chunks
    ])

    prompt = f""" You are helpful geospatial learning assistant.
    Answer the questions using ONLY the information provided in the sources below.
    Do NOT use any outside knowledge or training data.
    Do NOT recommend resources not mentioned in the sources.
    If the sources don't contain enough information to answer, say "I don't know the answer"
    Always mention the source your answer comes from 

    Sources:
    {context}

    Question: {question}

     """
    
    response = openai_client.responses.create(
        model = 'gpt-5.4-mini',
        input = prompt
    
    )

    return response.output_text
    
    
    
    
   

if __name__ == "__main__":
    #build_vector_store()
   
    test_questions = [
        "How do i reproject a layer in QGIS?",
        "How do i filter images by date in Google Earth Engine?",
        "What is a choropleth map?"
    ]

    for question in test_questions:
        print(f"Q: {question}")
        chunks = query(question)
        answer = generate(question, chunks)
        print(f"A {answer}")
        print()
