# Warlock AI
Langchain based agentic AI solution to support an engineering student's everyday university life.

## Reason behind project
- To test / showcase langchain based approach in solving some LLM scenarios.

## Features
1. General QA
   - LLM based chatbot functionality
   - Agentic support for coding (building, running, checking output) related queries via Python REPL
   - Agentic support for solving code error (bug, warnings, errors) related queries via StackOverFlow
   - Agentic support for queries with search engine requirement via DuckDuckGo
   - Blocking inappropriate (politics, terrorism, pornography) queries
2. Document Ingestion
   - Upload PDF or HTML documents into specific subject and topic to serve as context for future queries
   - User specific document handling
3. Document QA
   - LLM based chatbot functionality with context support based on subject and topic
   - User specific context handling

## Arhitecture
The application is following a 3 service structure:
- warlock-ai-service -> Only AI related functions ("this repository")
- warlock-backend-service -> Classical backend related functions (looking for contributor due to time shortage)
- warlock-frontend-service -> Anything that is frontend (looking for contributor due to time shortage)

## Current state
- This repository's scope is only to deliver the **warlock-ai-service**
- Functionality that should be implemented in **warlock-backend-service** is currently mocked by hardcoded values
- **warlock-frontend-service** is being mocked via CURL terminal calls
- Therefore, some features may be either missing (for example: chat history) or incomplete (like: validation, authentication, etc.)

## Setup
### To develop warlock-backend-service / warlock-frontend-service
- docker compose -f compose/docker-compose-fs.yml up -d

### To develop warlock-ai-service
- docker compose -f compose/docker-compose-ds.yml up -d

## Examples
1. General QA
   1. Block political, terrorism and pornographic queries
      - curl -X POST http://127.0.0.1:8123/api/python/v1/general_qa -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "Was Bush a great president?", "warlock_api_key": "EMPTY"}' -N 
   2. Trigger Coding Agent
      - curl -X POST http://127.0.0.1:8123/api/python/v1/general_qa -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "What is the length of the final array, when you create an empty array and append numbers [1, 2, 3] to it?", "warlock_api_key": "EMPTY"}' -N
   3. Trigger StackOverFlow Agent 
      - curl -X POST http://127.0.0.1:8123/api/python/v1/general_qa -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "How to solve error: TypeError: can only concatenate str (not int) to str?", "warlock_api_key": "EMPTY"}' -N
   4. Trigger DuckDuckGo Agent
      - curl -X POST http://127.0.0.1:8123/api/python/v1/general_qa -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "Which date is Independence Day on?", "warlock_api_key": "EMPTY"}' -N
   5. Trigger vanilla LLM
      - curl -X POST http://127.0.0.1:8123/api/python/v1/general_qa -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "What is my name?", "warlock_api_key": "EMPTY"}' -N 

2. Document Ingestion
   1. PDF
      - curl -X POST http://127.0.0.1:8123/api/python/v1/document_ingestion -H "accept: application/json" -H "Content-Type: application/json" -d '{"user_id": "user_10001", "subject_id": 1, "topic_id": 11, "document_path": "/Users/mac.username/Documents/document_ingestion_test.pdf", "document_id": 101, "document_type": 1}' &
   2. HTML
      - curl -X POST http://127.0.0.1:8123/api/python/v1/document_ingestion -H "accept: application/json" -H "Content-Type: application/json" -d '{"user_id": "user_10001", "subject_id": 1, "topic_id": 11, "document_path": "http://car-database-bucket.s3-website-eu-west-1.amazonaws.com", "document_id": 102, "document_type": 2}' &
