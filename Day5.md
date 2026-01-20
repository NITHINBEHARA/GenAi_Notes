## Building a RAG Application – From Beginning
## What is a RAG Application?

RAG (Retrieval Augmented Generation) is a system where a language model does not answer from memory alone, but first retrieves relevant information from documents and then generates an answer grounded in that information.

Film analogy:
A RAG system is like an actor who first reviews the correct scenes from the script archive before delivering a dialogue, instead of improvising blindly.
## A complete RAG system has three core stages:

Ingestion – preparing knowledge (script preparation)

Retrieval – finding relevant knowledge (scene selection)

Generation – answering with context (dialogue delivery)
## STAGE 1: INGESTION PIPELINE (Knowledge Preparation)
What is the Ingestion Pipeline?

The ingestion pipeline is the process of taking raw documents (PDFs, text files, notes, web data), cleaning and breaking them into smaller pieces, converting those pieces into embeddings, and storing them in a vector database so they can be retrieved later during question answering.
## Why Ingestion is Mandatory in RAG

LLMs do not read files directly.
They only work with:

Tokens

Vectors (embeddings)

So before asking questions:

Knowledge must be converted into embeddings

Stored in a searchable vector database
## Step-by-step Explanation
## 1. Document Loading

Loads .txt files from the docs/ folder

Each file becomes a Document object

Film analogy:
Collecting all scripts, notes, and reference material before shooting starts.

## 2. Chunking

Uses CharacterTextSplitter

Splits long documents into smaller chunks

Why needed:
LLMs and embeddings cannot handle huge documents at once.

Film analogy:
Breaking a long movie script into individual scenes.

## 3. Embedding Creation

Uses text-embedding-3-small

Converts each chunk into a vector

Meaning:
Text → numbers that represent meaning

Film analogy:
Creating a unique fingerprint for every scene so similar scenes can be matched later.

## 4. Vector Storage (ChromaDB)

Stores embeddings persistently in db/chroma_db

Uses cosine similarity

Film analogy:
Storing all scene fingerprints in a digital film archive.

## Output of Ingestion Stage

Your documents are now searchable by meaning

This step is done once, not for every question
## STAGE 2: CHUNKING STRATEGIES (Improving Retrieval Quality)

Chunking quality directly affects RAG accuracy.


## Problem with Basic Chunking

Simple chunking may:

Cut sentences mid-way

Break logical meaning

Film analogy:
Cutting a scene in the middle of a dialogue.

## Recursive Character Splitter

Tries multiple separators

Preserves meaning better

Film analogy:
Cutting scenes only at natural breaks.

## Semantic Chunking

Uses embeddings to split text by meaning

Groups related sentences together

Film analogy:
Grouping scenes by theme instead of page length.

## Agentic Chunking

Uses an LLM to decide chunk boundaries

Most intelligent chunking method

Film analogy:
Letting the director decide where scenes should end.

## Stage 3  : Basic Retrieval Pipeline (Finding Relevant Context)
Purpose:
Retrieve relevant chunks from the vector database.

How it Works:

User query → embedding

Compare query embedding with stored embeddings

Return top-k most similar chunks

Film analogy:
Assistant director searching the archive for relevant scenes.
## STAGE 4: ANSWER GENERATION (RAG Core)

Purpose: 
Generate a grounded answer using retrieved documents.

Steps: 

Combine user query + retrieved chunks

Pass them to the LLM

Restrict answers to retrieved content

Film analogy:
Actor reads relevant scenes before delivering dialogues.

## STAGE 5: CONVERSATION-AWARE RAG

Problem: 

Follow-up questions lose context.

Solution: 

Convert follow-up questions into standalone queries

Use conversation history

Film analogy:
Continuity editor ensuring story consistency across scenes.

## STAGE 6: ADVANCED RETRIEVAL TECHNIQUES

Retrieval Methods are : 

## Similarity Search

Pure relevance

## Score Threshold

Removes weak matches

## MMR

Balances relevance and diversity

Film analogy:
Avoid showing the same scene repeatedly from the same angle.


## Multi-Query Retrieval

LLM generates multiple variations of the same question

Improves coverage

Film analogy:
Asking multiple assistant directors the same question to get better scene selection.


## Reciprocal Rank Fusion (RRF)
## Problem: 

Different queries return different results.

## Solution: 

Merge rankings

Boost chunks appearing across multiple queries

Film analogy:
Scenes repeatedly recommended by multiple editors get priority.
## STAGE 7: HYBRID & RERANKING

## Hybrid Search

Combines keyword search (BM25) + vector search

Film analogy:
Searching scenes by both title and emotional similarity.


## Reranking

Uses a stronger model to reorder retrieved chunks

Improves final answer quality

Film analogy:
Final editor selecting the best scenes before release.
