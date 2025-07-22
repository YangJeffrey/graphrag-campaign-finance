# GraphRAG/LLMs for Campaign Finance Data

GraphRAG agent leveraging Neo4j's graph DB architecture to uncover hidden patterns in FEC contribution data through natural language queries. Combines LangChain's Cypher translation with Anthropic's Claude LLM to detect PEPs, bundling networks, and influence clusters across millions of interconnected donor-committee-employer relationships.

## Prerequisites

### 1. FEC Data Download

Download the "Contributions by Individuals" dataset from the [FEC Bulk Data portal](https://www.fec.gov/data/browse-data/?tab=bulk-data). This will provide you with the `itcont.txt` file containing individual contribution records.

### 2. Data Conversion

Use the included `txt_to_csv.py` script to convert the pipe-delimited `itcont.txt` file to CSV format:

```bash
python txt_to_csv.py
```

### 3. Neo4j Database Setup

Import the converted CSV data into your local Neo4j instance and run the Cypher query:

```sql
LOAD CSV WITH HEADERS FROM 'file:///itcont.csv' AS row
WITH row
SKIP 0 LIMIT 10000  // Adjust for batch loading

WITH
  trim(row.NAME) AS name,
  trim(row.CITY) AS city,
  trim(row.EMPLOYER) AS employer,
  trim(row.OCCUPATION) AS occupation,
  trim(row.STATE) AS state,
  trim(row.ZIP_CODE) AS zip,
  trim(row.CMTE_ID) AS cmte_id,
  toFloat(row.TRANSACTION_AMT) AS amount,
  toString(row.TRANSACTION_DT) AS date,
  // ... whatever data points you want

WHERE name IS NOT NULL AND cmte_id IS NOT NULL AND amount IS NOT NULL

// Create or update Donor node
MERGE (donor:Donor { name: name })
SET donor.city = city,
    donor.employer = employer,
    donor.occupation = occupation,
    donor.state = state,
    donor.zip = zip

// Create or update Committee node
MERGE (committee:Committee { cmte_id: cmte_id })

// Create DONATED relationship
MERGE (donor)-[:DONATED {
  amount: amount,
  date: date,
  type: type
}]->(committee);
```

## Neo4j GraphRAG API (`api.py`)

A FastAPI-based service that provides natural language querying capabilities for a Neo4j graph database containing donor information. The API uses Anthropic's Claude model to generate Cypher queries and provide human-readable answers.

### API Endpoints

- `GET /` - Root endpoint with API status
- `GET /health` - Health check for Neo4j and Anthropic connections
- `GET /query?q=<question>` - Query the graph database with natural language

### Setup

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

### Usage Example

```bash
curl -X 'GET' \
  'http://0.0.0.0:8000/query?q=Who%20are%20the%20top%2010%20donors%20by%20amount%3F' \
  -H 'accept: application/json'
```
