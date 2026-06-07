# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---
GeoSpatial Analysis is the domain of my choice. I am starting to learn about geospatial analysis and want to build my own knowledge base for it. Official channels have 
lots of theory and not a practical focused content and these are applied geopstial analysis courses rather than theororitical concepts.

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Spatial Thoughts  | Intro to QGIS|https://courses.spatialthoughts.com/introduction-to-qgis.html |
| 2 |Spatial Thoughts |Advanced QGIS |https://courses.spatialthoughts.com/advanced-qgis.html |
| 3 |Spatial Thoughts |PyQGIS MasterClass |https://courses.spatialthoughts.com/pyqgis-masterclass.html |
| 4 |Spatial Thoughts |Python Foundation for Spatial Analysis |https://courses.spatialthoughts.com/python-foundation.html |
| 5 |Spatial Thoughts |Mapping and Data Visualization with Python |https://courses.spatialthoughts.com/python-dataviz.html |
| 6 |Spatial Thoughts |Cloud Native Remote Sensing with Python |https://courses.spatialthoughts.com/python-remote-sensing.html |
| 7 |Spatial Thoughts |Mastering GDAL |https://courses.spatialthoughts.com/gdal-tools.html |
| 8 |Spatial Thoughts |End to End Google Earth Engine | https://courses.spatialthoughts.com/gdal-tools.html|
| 9 |Spatial Thoughts|Creating Publication Quality Charts with GEE |https://courses.spatialthoughts.com/gee-charts.html |
| 10 |Spatial Thoughts |Google Earth Engine for Water Resources Management |https://courses.spatialthoughts.com/gee-water-resources-management.html |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

For my chunking we are using sentence based chunking strategy.

**Chunk size: 500 characters

**Overlap: 2 sentences

**Reasoning:**
The source documents are practical tutorial courses containing step-by-step 
instructions, code snippets, and concept explanations. Sentence-aware chunking 
was chosen over fixed-size character splitting because it waits until a sentence 
is complete before starting a new chunk, avoiding incomplete sentences that would 
be meaningless to retrieve. A 500 character limit keeps chunks focused on one idea 
without blending unrelated topics. Two sentences of overlap ensure that information 
spanning a chunk boundary is captured in at least one complete chunk.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:all-MiniLM-L6-v2

**Top-k: 5 

**Production tradeoff reflection:**
The current model (all-MiniLM-L6-v2) is a general-purpose embedding model that 
works well for everyday English text. In production, I would consider two tradeoffs:

1. **Domain-specific accuracy:** Geospatial tutorials contain technical terms like 
EPSG codes, GEE API calls, and GDAL commands. A general model may not embed these 
as precisely as a model trained on geospatial or code-heavy text, potentially 
returning weaker matches for technical queries.

2. **Multilingual support:** Geospatial tools like QGIS and Google Earth Engine are 
used globally. A production system serving non-English speakers would need a 
multilingual model like paraphrase-multilingual-MiniLM-L12-v2, which all-MiniLM-L6-v2 
does not support.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How do i reproject a layer in QGIS?| Use Vector general → Reproject layer in Processing Toolbox, select target CRS|
| 2 | How do I filter images by date in Google Earth Engine?|Use ee.Filter.date(startDate, endDate) |
| 3 |What is a choropleth map? | A map where polygons are colored based on a data column value|
| 4 | How to merge tiles in GDAL? | We need to create text files containing all the files we want to merge that are in *.hgt format and run gdalbuiltvrt command|
| 5 |What is XArray?  |XArray is a Python library to work with gridded raster datasets which can natively handle time-series data making for Remote Sensing data. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The table of contents appearing in ingested content posed a retrieval risk — 
TOC entries contain only topic titles without substance, so if retrieved they would 
give the LLM no useful context to answer from.

2. Code snippets on Spatial Thoughts pages are rendered with each token in a 
separate HTML span tag, which when extracted produces fragmented text like 
"addLayer \n (admin2 \n , \n {". This breaks semantic matching for code-related 
queries since the embedding model cannot interpret scattered tokens as meaningful code.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

```
URLs (Spatial Thoughts)
        ↓
[1] INGESTION — requests + BeautifulSoup
        ↓
[2] CHUNKING — nltk sent_tokenize (500 chars, 2-sentence overlap)
        ↓
[3] EMBEDDING — sentence-transformers (all-MiniLM-L6-v2)
        ↓
[4] VECTOR STORE — ChromaDB (PersistentClient)
        ↓
[5] GENERATION — OpenAI gpt-4o-mini (Responses API)
        ↓
    Answer + Source Citation
```

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


**Milestone 3 — Ingestion and chunking:**
I used Claude to guide the implementation of fetch_and_clean() and chunk_text() 
incrementally. Rather than providing the full planning.md, I described the domain 
(geospatial tutorial content from Spatial Thoughts) and asked Claude to explain 
each concept before writing code. I verified outputs at each step by printing 
sample chunks and checking for noise like TOC entries and fragmented code blocks.

**Milestone 4 — Embedding and retrieval:**
I used Claude to explain how SentenceTransformer and ChromaDB work before 
implementing them. Code was built line by line rather than generated all at once, 
which helped me understand what each piece does. I verified retrieval by checking 
distance scores and confirming returned chunks were topically relevant to each 
test question.

**Milestone 5 — Generation and interface:**
I used Claude to implement the generate() function using the OpenAI Responses API. 
I had to push Claude to find the latest API documentation since initial suggestions 
used outdated method signatures. I verified grounding by checking that answers 
cited specific source documents and matched content from retrieved chunks rather 
than general LLM knowledge.


When asking broad questions like 'How to use Python for geospatial analysis?', 
the system retrieves chunks from python-foundation that contain links to external courses (University of Helsinki, Kaggle). The LLM faithfully reports these as part of the answer, which may mislead users into thinking those resources are part of the knowledge base. This is a retrieval issue — the source document itself references external resources, and the chunking strategy does not filter them out.



