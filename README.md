## Install

### For Full Stack development
- docker compose -f compose/docker-compose-fs.yml up -d

### For Data Science development
- docker compose -f compose/docker-compose-ds.yml up -d

## Features
1. General QA
   1. curl -X POST http://127.0.0.1:8123/api/python/v1/general_qa -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "Was Bush a great president?", "warlock_api_key": "EMPTY"}' -N 
   2. curl -X POST http://127.0.0.1:8123/api/python/v1/general_qa -H "accept: application/json" -H "Content-Type: application/json" -d '{"query": "Which date is Independence Day on?", "warlock_api_key": "EMPTY"}' -N
