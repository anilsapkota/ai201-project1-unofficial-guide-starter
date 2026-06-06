import requests 
from bs4 import BeautifulSoup 
import nltk 
nltk.download('punkt_tab', quiet=True)
from nltk.tokenize import sent_tokenize 
from collections import Counter
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

    #Fix the fragemented code blocks join lines inside <pre> and <code> tags
    for code_tag in soup.find_all(["pre", "code"]):
    # Replace the tag with its text joined on spaces instead of newlines
        code_text = code_tag.get_text(separator=" ")
        code_tag.replace_with(code_text)

    text = main.get_text(separator= "\n")

    #Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines()]
    clean = "\n".join(line for line in lines if line)

    return clean 

#buidling sentence aware 500 characters, 2 sentence overlaps chunking
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
    
#all the sources in the list here

SOURCES = [
    {"url": "https://courses.spatialthoughts.com/introduction-to-qgis.html", "name": "introduction-to-qgis"},
    {"url": "https://courses.spatialthoughts.com/advanced-qgis.html", "name": "advanced-qgis"},
    {"url": "https://courses.spatialthoughts.com/pyqgis-masterclass.html", "name": "pyqgis-masterclass"},
    {"url": "https://courses.spatialthoughts.com/python-foundation.html", "name": "python-foundation"},
    {"url": "https://courses.spatialthoughts.com/python-dataviz.html", "name": "python-dataviz"},
    {"url": "https://courses.spatialthoughts.com/python-remote-sensing.html", "name": "python-remote-sensing"},
    {"url": "https://courses.spatialthoughts.com/gdal-tools.html", "name": "mastering-gdal"},
    {"url": "https://courses.spatialthoughts.com/end-to-end-gee.html", "name": "end-to-end-gee"},
    {"url": "https://courses.spatialthoughts.com/gee-charts.html", "name": "gee-charts"},
    {"url": "https://courses.spatialthoughts.com/gee-water-resources-management.html", "name": "gee-water-resources"},
]

if __name__ =="__main__":
    all_chunks = []

    for source in SOURCES:
        print(f"Fetching :{source['name']} ..")
        try:
            text = fetch_and_clean(source["url"])
            chunks = chunk_text(text, source=source["name"])
            all_chunks.extend(chunks)
            print(f" -> {len(chunks)} chunks")
        except Exception as e:
            print(f"FAILED:{e}")
    # Check per-source breakdown
    
    source_counts = Counter(chunk["source"] for chunk in all_chunks)
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        print(f"{source}: {count} chunks")
    
    gee_chunks = [c for c in all_chunks if c["source"] == "end-to-end-gee"]
    for i in [0, 50, 100, 300, 600]:
        print(f"--- Chunk {i} ---")
        print(gee_chunks[i]["text"])
        print()

    print(f"Total Chunks : {len(all_chunks)}\n")

    