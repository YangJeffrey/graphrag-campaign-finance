# GraphRAG/LLMs for Campaign Finance Data

GraphRAG agent leveraging Neo4j's graph DB architecture to uncover hidden patterns in FEC contribution data through natural language queries. Combines LangChain's Cypher translation with Anthropic's Claude LLM to detect PEPs, bundling networks, and influence clusters across millions of interconnected donor-committee-employer relationships.

## Components

### 1. Neo4j GraphRAG API (`api.py`)

A FastAPI-based service that provides natural language querying capabilities for a Neo4j graph database containing donor information. The API uses Anthropic's Claude model to generate Cypher queries and provide human-readable answers.

#### API Endpoints

- `GET /` - Root endpoint with API status
- `GET /health` - Health check for Neo4j and Anthropic connections
- `GET /query?q=<question>` - Query the graph database with natural language

#### Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in a `.env` file:

   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_neo4j_password
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

3. Run the API:
   ```bash
   python api.py
   ```

The API will be available at `http://localhost:8000`

#### Usage Example

```bash
curl "http://localhost:8000/query?q=Who are the top 10 donors by amount?"
```

### 2. Text to CSV Converter (`txt_to_csv.py`)

A utility script that converts pipe-delimited text files to CSV format, specifically designed for processing FEC individual contribution data.

#### Setup

1. Ensure you have the required dependencies:

   ```bash
   pip install pandas
   ```

2. Place your input file (`itcont.txt`) in a `data/` directory relative to the script

#### Usage

```bash
python txt_to_csv.py
```
