## DAY 3 

## 11. Embeddings

Embeddings are numerical representations of data that capture meaning and relationships. In film terms, embeddings convert scenes into coordinates so similar scenes appear closer together. This allows machines to compare meaning instead of exact words. Similar texts have similar embeddings.
Real-time example: finding similar movie descriptions.
Use cases: semantic search, recommendation systems, RAG pipelines. 
## Scenario:
In a grocery store like Dmart or Vijetha, items are organized into clearly defined sections such as fruits, drinks, and cosmetics
. Each section is assigned a specific aisle number; for example, aisle 1 may represent the fruits section. 
Within that aisle, every item is given its own position number, such as apple being assigned number 5 and banana being assigned number 6.
As a result, an apple can be represented by the coordinates (1,5) and a banana by (1,6). In the same way, all items in the store have unique coordinates
based on their section and position. This coordinate-based system makes it easy to track items, find similar products, manage inventory,
and quickly match customer searches to exact products. In Generative AI, embeddings work in a similar way by converting words, sentences,
or data into numerical coordinates so that related items are placed closer together, making searching, matching, and recommendations faster
and more accurate. 

## Common Embedding Models and Their Dimensions
OpenAI Embedding Models

text-embedding-3-small → 1536 dimensions
Used for lightweight search and basic similarity matching.
Film analogy: describing a movie using main genre and storyline only.

text-embedding-3-large → 3072 dimensions
High-quality semantic understanding.
Film analogy: describing a movie using genre, emotions, character arcs, pacing, and symbolism.

## Use cases:

Semantic search

RAG (Retrieval Augmented Generation)

Recommendation systems

Google Embedding Models

Gecko / Gemini embeddings → 768 to 1024 dimensions
Balanced performance and efficiency.
Film analogy: understanding the story and emotions but not every cinematic detail.

## Use cases:

Search

Question answering

Document similarity

Sentence Transformers (Open Source)

MiniLM → 384 dimensions
Very fast and lightweight.
Film analogy: quick movie summary.

MPNet / BERT-based models → 768 dimensions
Deeper understanding.
Film analogy: full plot + character analysis.

Use cases:

Chatbots

Local vector search

Low-cost embedding systems

Cohere Embedding Models

embed-english-v3 → 1024 dimensions
Strong semantic grouping.
Film analogy: grouping similar movies by theme and mood.

Use cases:

Enterprise search

Content clustering

Recommendation engines
