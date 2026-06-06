import chromadb
from sentence_transformers import SentenceTransformer
from ingest import fetch_and_clean, chunk_text, SOURCES 

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "geospatial_guide"
TOP_K = 5 

model = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path="./chroma_db")


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


if __name__ == "__main__":
    build_vector_store()
