# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Geospatial analysis — specifically, practical application of tools like QGIS, GDAL, Google Earth Engine, and Python geospatial libraries. This knowledge is valuable because official documentation covers API references and theory but rarely teaches how to chain tools together on real data. The sources I collected are full applied courses from Spatial Thoughts that focus on doing rather than defining, which makes them hard to search through official channels — there is no single authoritative index of what each course covers step by step.


---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/introduction-to-qgis.html |
| 2 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/advanced-qgis.html |
| 3 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/pyqgis-masterclass.html |
| 4 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/python-foundation.html |
| 5 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/python-dataviz.html |
| 6 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/python-remote-sensing.html |
| 7 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/gdal-tools.html |
| 8 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/end-to-end-gee.html |
| 9 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/gee-charts.html |
| 10 | Spatial Thoughts | Course | https://courses.spatialthoughts.com/gee-water-resources-management.html |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters

**Overlap:** 2 sentences

**Why these choices fit your documents:** The sources are practical tutorial courses containing step-by-step instructions, code snippets, and concept explanations. Sentence-aware chunking (via `nltk sent_tokenize`) was chosen over fixed-size character splitting because it waits for a sentence to complete before starting a new chunk, avoiding mid-sentence breaks that would be meaningless to retrieve. A 500-character limit keeps each chunk focused on a single idea without blending unrelated topics. Two sentences of overlap ensure that information spanning a chunk boundary is still captured fully in at least one chunk.

**Final chunk count:** <!-- fill in after running ingestion -->

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Production tradeoff reflection:**
The current model is a general-purpose English embedding model that works well for everyday prose. In production I would weigh two tradeoffs:

1. **Domain-specific accuracy:** Geospatial tutorials contain technical terms like EPSG codes, GEE API calls, and GDAL commands. A general model may not embed these precisely, potentially returning weaker matches for technical queries. A model fine-tuned on code or scientific text would improve retrieval accuracy for these cases.

2. **Multilingual support:** QGIS and Google Earth Engine are used globally. A production system serving non-English speakers would need a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2`, which `all-MiniLM-L6-v2` does not support.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt instructs the model to answer only from the provided context chunks and to explicitly state when information is not present in the retrieved documents rather than drawing on general knowledge. The instruction reads approximately: *"You are a geospatial analysis assistant. Answer the user's question using only the context provided below. If the answer is not contained in the context, say so — do not use outside knowledge."*

**How source attribution is surfaced in the response:**
Each retrieved chunk is passed to the model with its source URL attached. The model is instructed to cite the source document at the end of its answer so users can trace the response back to the specific Spatial Thoughts course page it came from.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How do I reproject a layer in QGIS? | Use Vector general → Reproject layer in Processing Toolbox, select target CRS | <!-- fill in --> | <!-- fill in --> | <!-- fill in --> |
| 2 | How do I filter images by date in Google Earth Engine? | Use `ee.Filter.date(startDate, endDate)` | <!-- fill in --> | <!-- fill in --> | <!-- fill in --> |
| 3 | What is a choropleth map? | A map where polygons are colored based on a data column value | <!-- fill in --> | <!-- fill in --> | <!-- fill in --> |
| 4 | How do you merge tiles in GDAL? | Create a text file listing all `.hgt` files and run `gdalbuildvrt` | <!-- fill in --> | <!-- fill in --> | <!-- fill in --> |
| 5 | What is XArray? | A Python library for gridded raster datasets that natively handles time-series data, useful for remote sensing | <!-- fill in --> | <!-- fill in --> | <!-- fill in --> |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "How do I use Python for geospatial analysis?"

**What the system returned:** An answer that included references to external resources (University of Helsinki course, Kaggle) as if they were part of the knowledge base, which could mislead users.

**Root cause (tied to a specific pipeline stage):** This is a retrieval + chunking issue. The `python-foundation` source document itself contains links to external courses within its introductory section. The chunking strategy does not filter or strip outbound links from content, so those references were embedded into chunks and retrieved as relevant context. The LLM then faithfully reported them as part of the answer.

**What you would change to fix it:** Add a preprocessing step during ingestion that strips anchor tags and outbound URLs before chunking, so external references are never embedded into the vector store. Alternatively, narrow the query scope by instructing users to ask more specific questions rather than broad "how do I start" prompts that land on introductory pages.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The chunking strategy section of planning.md gave me a concrete target — 500 characters, sentence-aware, 2-sentence overlap — before I wrote any code. When I asked Claude to implement `chunk_text()`, I could hand it those exact parameters instead of describing a vague idea. The result was a function that matched my intent on the first pass, and I only needed to verify the output rather than redirect from scratch.

**One way your implementation diverged from the spec, and why:**
The spec did not anticipate the HTML structure of the Spatial Thoughts pages, specifically that code snippets are rendered with each token in a separate `<span>` tag. When extracted, this produced fragmented text like `"addLayer \n (admin2 \n , \n {"` that the embedding model could not interpret. I added a BeautifulSoup preprocessing step to collapse or strip those code blocks before chunking — something not mentioned in the original document sources or chunking strategy sections.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — Ingestion and chunking**

- *What I gave the AI:* A description of the domain (geospatial tutorial content from Spatial Thoughts) and the chunking strategy from planning.md — 500-character limit, sentence-aware splitting, 2-sentence overlap.
- *What it produced:* A `fetch_and_clean()` function using `requests` + `BeautifulSoup` and a `chunk_text()` function using `nltk sent_tokenize` with the specified parameters.
- *What I changed or overrode:* I added a preprocessing step to handle fragmented code blocks caused by per-token `<span>` tags in the source HTML — Claude's initial version did not account for this because the issue only appeared when running against real pages.

**Instance 2 — Generation with the OpenAI Responses API**

- *What I gave the AI:* The architecture diagram from planning.md showing `gpt-4o-mini` as the generation model, plus a request to implement the `generate()` function using the OpenAI Responses API.
- *What it produced:* An initial implementation using an outdated method signature (`openai.ChatCompletion.create`) that no longer matched the current SDK.
- *What I changed or overrode:* I pushed Claude to look up the current Responses API documentation. The corrected version used `client.responses.create` with the proper `input` parameter structure. I also added explicit source citation formatting to the system prompt, which was not in Claude's first draft.

## Evaluation Report

| # | Question | Expected Answer | System Response | Judgment |
|---|----------|-----------------|-----------------|----------|
| 1 | How do I reproject a layer in QGIS? | Use Vector general → Reproject layer in Processing Toolbox, select target CRS | Correct step-by-step instructions, cited introduction-to-qgis | ✅ Accurate |
| 2 | How do I filter images by date in Google Earth Engine? | Use ee.Filter.date(startDate, endDate) | Correct with code examples, cited end-to-end-gee and gee-charts | ✅ Accurate |
| 3 | What is a choropleth map? | A map where polygons are colored based on a data column value | Correct definition with source quote, cited python-dataviz | ✅ Accurate |
| 4 | How to merge tiles in GDAL? | Create text files with *.hgt files and run gdalbuildvrt command | Correct about Virtual Raster and gdalbuildvrt but missing *.hgt specific detail | ⚠️ Partially Accurate |
| 5 | What is XArray? | Python library for gridded raster datasets with native time-series support | Correct, added dask parallel computing detail, cited python-remote-sensing | ✅ Accurate |

### Failure Case Analysis

**Question 4 — How to merge tiles in GDAL?**

The system correctly retrieved chunks from `mastering-gdal` and identified the 
`gdalbuildvrt` command and Virtual Raster approach. However, the specific detail 
about creating a text file listing `*.hgt` format files was missing from the 
retrieved chunks. This is a chunk boundary failure — the specific `*.hgt` detail 
likely appeared in a different part of the page that was split into a separate 
chunk which ranked below the top-5 retrieved results. Increasing TOP_K or chunk 
size might surface this detail.