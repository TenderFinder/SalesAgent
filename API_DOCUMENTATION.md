# SalesAgent API Documentation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Set MongoDB URI (required)
export MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net/"

# Optional: Set other configs
export OLLAMA_MODEL="llama3.2"
export MIN_MATCH_SCORE="1.0"
```

### 3. Start the API Server
```bash
# Option 1: Using the startup script
python start_api.py

# Option 2: Using uvicorn directly
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API Endpoints

### Health & Status

#### `GET /`
Get API status and version.

**Response:**
```json
{
  "status": "running",
  "version": "2.0.0",
  "service": "SalesAgent Matching API"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "salesagent"
}
```

---

### Matching Operations

#### `POST /api/v1/match`
Run tender-product matching (synchronous).

**Request Body:**
```json
{
  "use_ai": false,
  "min_score": 1.0,
  "save_results": true
}
```

**Parameters:**
- `use_ai` (boolean): Use AI-powered matching (requires Ollama). Default: `false`
- `min_score` (float): Minimum match score threshold. Default: `1.0`
- `save_results` (boolean): Save results to database. Default: `true`

**Response:**
```json
{
  "success": true,
  "message": "Matching complete. Found 5 matches.",
  "total_matches": 5,
  "matches": [
    {
      "tender_id": "services_home_3d22084507",
      "tender_name": "3D Printing Service",
      "matched_product": "3D Printing Service",
      "score": 6.0,
      "reasons": ["Keyword '3d printing' found in tender tags"],
      "market_url": "https://mkp.gem.gov.in/...",
      "match_type": "rule-based"
    }
  ]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/match" \
  -H "Content-Type: application/json" \
  -d '{"use_ai": false, "min_score": 1.0, "save_results": true}'
```

#### `POST /api/v1/match/async`
Run matching in background (asynchronous).

**Request Body:** Same as `/api/v1/match`

**Response:**
```json
{
  "success": true,
  "message": "Matching started in background",
  "status": "processing"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/match/async" \
  -H "Content-Type: application/json" \
  -d '{"use_ai": true, "min_score": 2.0}'
```

---

### Retrieve Matches

#### `GET /api/v1/matches`
Get stored matches from database.

**Query Parameters:**
- `min_score` (float, optional): Filter by minimum score
- `product` (string, optional): Filter by product name
- `limit` (int, optional): Maximum results. Default: `100`

**Response:**
```json
[
  {
    "tender_id": "services_home_3d22084507",
    "tender_name": "3D Printing Service",
    "matched_product": "3D Printing Service",
    "score": 6.0,
    "reasons": ["Keyword match"],
    "market_url": "https://...",
    "match_type": "rule-based"
  }
]
```

**Examples:**
```bash
# Get all matches
curl "http://localhost:8000/api/v1/matches"

# Get matches with score >= 5.0
curl "http://localhost:8000/api/v1/matches?min_score=5.0"

# Get matches for specific product
curl "http://localhost:8000/api/v1/matches?product=3D%20Printing%20Service"

# Get top 10 matches
curl "http://localhost:8000/api/v1/matches?limit=10"
```

---

### Statistics

#### `GET /api/v1/stats`
Get matching statistics.

**Response:**
```json
{
  "total_matches": 15,
  "by_product": {
    "3D Printing Service": 5,
    "AI & Machine Learning": 4,
    "IT Consulting & Development": 6
  },
  "score_distribution": {
    "0-25": 2,
    "26-50": 3,
    "51-75": 5,
    "76-100": 5
  }
}
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/stats"
```

---

### Tender Operations

#### `GET /api/v1/tenders/count`
Get total number of tenders in database.

**Response:**
```json
{
  "total_tenders": 150
}
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/tenders/count"
```

#### `POST /api/v1/tenders/fetch`
Fetch fresh tenders from GeM API and store in database.

**Response:**
```json
{
  "success": true,
  "message": "Fetched and stored 25 tenders",
  "total_tenders": 25
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/tenders/fetch"
```

---

## Usage Examples

### Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Run rule-based matching
response = requests.post(
    f"{BASE_URL}/api/v1/match",
    json={
        "use_ai": False,
        "min_score": 1.0,
        "save_results": True
    }
)
result = response.json()
print(f"Found {result['total_matches']} matches")

# Run AI matching
response = requests.post(
    f"{BASE_URL}/api/v1/match",
    json={
        "use_ai": True,
        "min_score": 50,
        "save_results": True
    }
)

# Get statistics
stats = requests.get(f"{BASE_URL}/api/v1/stats").json()
print(f"Total matches: {stats['total_matches']}")

# Get matches for a specific product
matches = requests.get(
    f"{BASE_URL}/api/v1/matches",
    params={"product": "3D Printing Service", "limit": 10}
).json()
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Run matching
async function runMatching() {
  const response = await axios.post(`${BASE_URL}/api/v1/match`, {
    use_ai: false,
    min_score: 1.0,
    save_results: true
  });
  
  console.log(`Found ${response.data.total_matches} matches`);
  return response.data.matches;
}

// Get statistics
async function getStats() {
  const response = await axios.get(`${BASE_URL}/api/v1/stats`);
  console.log('Statistics:', response.data);
}

runMatching().then(matches => {
  console.log('Matches:', matches);
});
```

### cURL

```bash
# Run rule-based matching
curl -X POST "http://localhost:8000/api/v1/match" \
  -H "Content-Type: application/json" \
  -d '{"use_ai": false, "min_score": 1.0}'

# Run AI matching
curl -X POST "http://localhost:8000/api/v1/match" \
  -H "Content-Type: application/json" \
  -d '{"use_ai": true, "min_score": 50}'

# Get all matches
curl "http://localhost:8000/api/v1/matches"

# Get statistics
curl "http://localhost:8000/api/v1/stats"

# Fetch fresh tenders
curl -X POST "http://localhost:8000/api/v1/tenders/fetch"
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

### Swagger UI
Visit http://localhost:8000/docs for interactive API testing.

Features:
- Try out endpoints directly from browser
- See request/response schemas
- View example requests and responses

### ReDoc
Visit http://localhost:8000/redoc for alternative documentation view.

Features:
- Clean, readable documentation
- Detailed schema information
- Code examples

---

## Configuration

### Environment Variables

```bash
# MongoDB (Required)
export MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net/"
export MONGO_DB_NAME="gem_database"

# LLM (Optional - for AI matching)
export OLLAMA_MODEL="llama3.2"

# Matching (Optional)
export MIN_MATCH_SCORE="1.0"

# File Paths (Optional)
export PRODUCTS_FILE="data/products/our_products.json"
```

### Using .env File

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/
MONGO_DB_NAME=gem_database
OLLAMA_MODEL=llama3.2
MIN_MATCH_SCORE=1.0
```

---

## Deployment

### Local Development
```bash
python start_api.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Future)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Troubleshooting

### API won't start
- Check if port 8000 is available
- Verify MongoDB connection
- Check Python version (3.12+ required)

### Matching fails
- Verify MongoDB is accessible
- Check if product catalog exists
- For AI matching, ensure Ollama is running

### No matches found
- Lower `min_score` threshold
- Verify product keywords match tender tags
- Check if tenders are in database

---

## Support

For issues or questions:
1. Check the interactive docs at `/docs`
2. Review this documentation
3. Check application logs
4. Open an issue on GitHub

---

**API Version:** 2.0.0  
**Last Updated:** 2026-01-10
