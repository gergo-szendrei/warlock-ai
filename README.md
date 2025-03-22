## Setup

### For Full Stack development
- docker compose -f compose/docker-compose-fs.yml up -d

### For Data Science development
- docker compose -f compose/docker-compose-ds.yml up -d

## Features
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
