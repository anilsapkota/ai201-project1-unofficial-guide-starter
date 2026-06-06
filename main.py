from dotenv import load_dotenv
load_dotenv()


from pathlib import Path 
import chromadb
from openai import OpenAI 



#load the documents
def load_documents():
    """ Load all .txt rule documents from the docs folder """

    documents = []

    for filename in sorted(os.lisdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            topic_name = filename.replace(".txt","").replace("_"," ").title()

            documents.append({
                "topic": topic_name,
                "filename":filename,
                "text":text, 
            })

#chunking the text
def chunk_document(text, topic_name):
    chunk_size = 1000
    overlap = 200
    min_length = 50

    chunks = []
    prefix = topic_name.lower().replace(" ","_")
    counter = 0

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip() 

        if len(chunk_text) >= min_length:
            chunk.append({
                "text":chunk_text,
                "topic_name":topic_name,
                "chunk_id":f"{prefix}_{counter}",
            })
            
            counter +=1
        
        #advance by (chunk_size-overlap) so that the next chunk shares
        # `overlap` characters with the tail of this one
        start += chunk_size - overlap

    return chunks 


def main():
    print("Hello from ai201-project1-unofficial-guide-starter!")


if __name__ == "__main__":
    main()
