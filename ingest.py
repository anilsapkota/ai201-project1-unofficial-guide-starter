import requests 
from bs4 import BeautifulSoup 
import nltk 
nltk.download('punkt_tab', quiet=True)
from nltk.tokenize import sent_tokenize 
import os 

def fetch_and_clean(url:str) ->str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")

    #Remove navigation, headers, footers - junk we don't want 

    for tag in soup(["nav", "header","footer","script","style"]):
        tag.decompose()
    
    #Remove the table of content 
    for ul in soup.find_all("ul"):
        links = ul.find_all("a",href=True)
        if links and all(a["href"].startswith("#") for a in links):
            ul.decompose()

    #Get the main content area
    main = soup.find("main") or soup.find("article") or soup.find("body")

    text = main.get_text(separator= "\n")

    #Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines()]
    clean = "\n".join(line for line in lines if line)

    return clean 


def chunk_text(text: str, source: str, chunk_size: int = 500, overlap_sentences: int= 2):
    """
    Splits text into chunks on sentence boundaries.
    - chunk_size: max characters per chunk
    - overlap_sentences: how many sentences from the previous chunk to prepend to the next one
    """


    #splits the entire cleaned text into a list of sentences.
    sentences = sent_tokenize(text)

    #
    chunks = []  
    current_sentences = []
    current_length = 0

    for sentence in sentences: 
        #checks to if we add further would it be greater than 500 characters  and do we have at least one sentence already.
        #if so we will save the current chunk 
        
        if current_length + len(sentence) > chunk_size and current_sentences: 
            chunk_text_str = " ".join(current_sentences).strip()
            if len(chunk_text_str)>50:
                chunks.append({
                    "text": chunk_text_str,
                    "source": source,
                })
            #keep last N sentences as overlap for next chunk
            current_sentences = current_sentences[-overlap_sentences:]
            current_length = sum(len(s) for s in current_sentences) 
        
        current_sentences.append(sentence)
        current_length += len(sentence)
    
    #last chunk
    if current_sentences:
        chunk_text_str = " ".join(current_sentences).strip()
        if len(chunk_text_str) >50:
            chunks.append({
                "text":chunk_text_str,
                "source":source, 
            })
    
    return chunks 
    
#temporarily testing the python

if __name__ =="__main__":
    url = "http://courses.spatialthoughts.com/introduction-to-qgis.html"
    text = fetch_and_clean(url)
    chunks = chunk_text(text,source="introduction-to-qgis")

    print(f"Total Chunks : {len(chunks)}\n")

    #print 5 sample chunks
    for i in [0,10,25,50,75]:
        print(f"Chunk {i}")
        print(chunks[i]["text"])
        print() 