import requests 
from bs4 import BeautifulSoup 
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

#temporarily testing the python

if __name__ =="__main__":
    url = "http://courses.spatialthoughts.com/introduction-to-qgis.html"
    text = fetch_and_clean(url)
    print(text[:2000])
    print(f"\n\nTotal length: {len(text)} characters")