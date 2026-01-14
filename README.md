# SalesAgent 🤖📋

**Intelligent Government Tender Matching System**

Automatically find and match government tenders from GeM (Government e-Marketplace) with your company's products and services using AI.

---

## 🎯 What Does This Do?

This system helps you:
1. **Fetch** government tenders from GeM automatically
2. **Match** them with your products using AI or rule-based algorithms
3. **Get results** via a simple web API or command line

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Python

Make sure you have Python 3.12 or higher installed.

**Check your Python version:**
```bash
python3 --version
```

If you don't have Python, download it from [python.org](https://www.python.org/downloads/)

---

### Step 2: Download the Project

```bash
# Clone or download this repository
cd SalesAgent
```

---

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

**What gets installed:**
- FastAPI - For the web API
- Pydantic - For data validation
- PyMongo - For MongoDB database
- Requests - For API calls
- Ollama - For AI matching (optional)

---

### Step 4: Set Up MongoDB

You need a MongoDB database to store tenders.

**Option A: Use MongoDB Atlas (Free Cloud Database)**

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a free cluster
4. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
5. Set it as an environment variable:

```bash
export MONGO_URI="mongodb+srv://your-username:your-password@your-cluster.mongodb.net/"
```

**Option B: Use Local MongoDB**

If you have MongoDB installed locally:
```bash
export MONGO_URI="mongodb://localhost:27017/"
```

---

### Step 5: Add Your Products

Edit the file `data/products/our_products.json` with your company's products:

```json
{
  "company_name": "Your Company Name",
  "offerings": [
    {
      "name": "Your Product Name",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "category": "your-category"
    }
  ]
}
```

**Example:**
```json
{
  "company_name": "Acme Tech Services",
  "offerings": [
    {
      "name": "3D Printing Service",
      "keywords": ["3d printing", "additive manufacturing", "rapid prototyping"],
      "category": "manufacturing"
    },
    {
      "name": "AI Consulting",
      "keywords": ["artificial intelligence", "machine learning", "ai"],
      "category": "it"
    }
  ]
}
```

---

## 🎮 How to Use

### Method 1: Fetch Tenders (Command Line)

Fetch the latest tenders from GeM and store them in your database:

```bash
python run_cli.py
```

**What happens:**
- Connects to GeM API
- Downloads active tenders
- Saves them to MongoDB
- Or saves to file if TENDER_DATA_SOURCE=file

**Output:**
```
🚀 Starting GEM API → MongoDB pipeline
📡 Fetching data from API...
✅ Successfully stored 25 tenders in MongoDB
```

---

### Method 2: Use the Web API (Recommended)

Start the API server:

```bash
python run_api.py
```

**What happens:**
- API server starts on http://localhost:8000
- You can access it from your browser or any programming language
- Automatically loads configuration from app/.env

**Access the interactive documentation:**
Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see a beautiful interactive interface where you can:
- Click on any endpoint
- Try it out directly from your browser
- See example requests and responses

---

## 📡 Using the API

### 1. Fetch Fresh Tenders

**In your browser or using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/tenders/fetch"
```

**Response:**
```json
{
  "success": true,
  "message": "Fetched and stored 25 tenders",
  "total_tenders": 25
}
```

---

### 2. Run Matching (Rule-Based)

Find matches between tenders and your products:

```bash
curl -X POST "http://localhost:8000/api/v1/match" \
  -H "Content-Type: application/json" \
  -d '{"use_ai": false, "min_score": 1.0}'
```

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

---

### 3. Run AI Matching (Optional - Requires Ollama)

For smarter, context-aware matching:

**First, install Ollama:**
```bash
# On macOS
brew install ollama

# Start Ollama
ollama serve

# In another terminal, pull the model
ollama pull llama3.2/<your chosen model>
```

**Then run AI matching:**
```bash
curl -X POST "http://localhost:8000/api/v1/match" \
  -H "Content-Type: application/json" \
  -d '{"use_ai": true, "min_score": 50}'
```

---

### 4. Get Your Matches

Retrieve all matches found:

```bash
curl "http://localhost:8000/api/v1/matches"
```

**Get top 10 matches:**
```bash
curl "http://localhost:8000/api/v1/matches?limit=10"
```

**Filter by score:**
```bash
curl "http://localhost:8000/api/v1/matches?min_score=5.0"
```

---

### 5. View Statistics

See how many matches you have:

```bash
curl "http://localhost:8000/api/v1/stats"
```

**Response:**
```json
{
  "total_matches": 15,
  "by_product": {
    "3D Printing Service": 5,
    "AI Consulting": 4,
    "IT Services": 6
  },
  "score_distribution": {
    "0-25": 2,
    "26-50": 3,
    "51-75": 5,
    "76-100": 5
  }
}
```

---

## 🌐 Using from Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Fetch tenders
response = requests.post(f"{BASE_URL}/api/v1/tenders/fetch")
print(response.json())

# Run matching
response = requests.post(
    f"{BASE_URL}/api/v1/match",
    json={"use_ai": False, "min_score": 1.0}
)
matches = response.json()
print(f"Found {matches['total_matches']} matches!")

# Get statistics
stats = requests.get(f"{BASE_URL}/api/v1/stats").json()
print(f"Total matches: {stats['total_matches']}")
```

---

## 🌐 Using from JavaScript

```javascript
const BASE_URL = 'http://localhost:8000';

// Fetch tenders
fetch(`${BASE_URL}/api/v1/tenders/fetch`, { method: 'POST' })
  .then(res => res.json())
  .then(data => console.log(data));

// Run matching
fetch(`${BASE_URL}/api/v1/match`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ use_ai: false, min_score: 1.0 })
})
  .then(res => res.json())
  .then(data => console.log(`Found ${data.total_matches} matches!`));
```

---

## 📁 Project Structure

```
SalesAgent/
├── run_cli.py           # Fetch tenders script
├── run_api.py           # Web API application
├── requirements.txt     # Python packages needed
│
├── app/                 # Core application code
│   ├── .env            # Configuration file
│   ├── main.py         # App factory
│   ├── routes/         # API endpoints
│   ├── models/         # Data structures
│   ├── repositories/   # Database operations
│   ├── agents/         # Matching algorithms
│   ├── services/       # Business logic
│   └── config/         # Settings
│
└── data/               # Your data
    ├── products/       # Your products (EDIT THIS!)
    ├── tenders/        # Downloaded tenders
    └── outputs/        # Match results
```

---

## ⚙️ Configuration

### Environment Variables & .env File

The application uses a `.env` file located at `app/.env` for configuration.

**Configuration Options:**

1. **Data Source:**
   ```env
   # Load from local files (Default, good for testing)
   TENDER_DATA_SOURCE=file
   PRODUCT_DATA_SOURCE=file
   
   # Load from MongoDB (Good for production)
   # TENDER_DATA_SOURCE=mongodb
   ```

2. **MongoDB Settings (Required if source is mongodb):**
   ```env
   MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/
   MONGO_DB_NAME=gem_database
   ```

3. **AI Settings:**
   ```env
   OLLAMA_MODEL=llama3.2
   ```

4. **Matching Settings:**
   ```env
   MIN_MATCH_SCORE=1.0
   ```

**To Setup:**
Copy `.env.example` to `app/.env` and edit it:
```bash
cp .env.example app/.env
# Edit app/.env with your settings
```

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

---

### Problem: "MongoDB connection error"

**Solution:** Check your MongoDB URI in `app/.env`
```bash
# Make sure MONGO_URI is set correctly in app/.env
# Verify connection string format
```

**For MongoDB Atlas:**
- Check your IP is whitelisted (add `0.0.0.0/0` for testing)
- Verify username and password are correct

---

### Problem: "Port 8000 already in use"

**Solution:** Use a different port
```bash
uvicorn app.main:app --reload --port 8001
```

---

### Problem: "No matches found"

**Solutions:**
- Lower the `min_score` threshold: `{"min_score": 0.5}`
- Check your product keywords match tender descriptions
- Make sure tenders are in the database (run `python run_cli.py` first)

---

### Problem: "AI matching not working"

**Solution:** Install and start Ollama
```bash
# Install Ollama
brew install ollama  # macOS
# or download from ollama.com

# Start Ollama service
ollama serve

# Pull the model (in another terminal)
ollama pull llama3.2
```

---

## 📖 API Documentation

For complete API documentation with all endpoints and examples, see:
- **Interactive Docs:** http://localhost:8000/docs (after starting the server)
- **API Documentation:** See `API_DOCUMENTATION.md` file

---

## 🎯 Common Use Cases

### Use Case 1: Daily Tender Check

Run this daily to get fresh tenders:
```bash
python run_cli.py
```

### Use Case 2: Find Matches for New Products

1. Add your product to `data/products/our_products.json`
2. Run matching:
```bash
curl -X POST http://localhost:8000/api/v1/match \
  -H "Content-Type: application/json" \
  -d '{"use_ai": false, "min_score": 1.0}'
```

### Use Case 3: Integrate with Your Website

Use the API endpoints from your website:
```javascript
// Fetch and display matches
fetch('http://localhost:8000/api/v1/matches?limit=10')
  .then(res => res.json())
  .then(matches => {
    // Display matches on your website
    matches.forEach(match => {
      console.log(`${match.tender_name} - Score: ${match.score}`);
    });
  });
```

---

## 🚀 Next Steps

1. ✅ **Set up Configuration** - Create `app/.env`
2. ✅ **Add your products** - Edit `data/products/our_products.json`
3. ✅ **Fetch tenders** - Run `python run_cli.py`
4. ✅ **Start the API** - Run `python run_api.py`
5. ✅ **Try matching** - Visit http://localhost:8000/docs

---

## 💡 Tips

- **Start simple:** Use rule-based matching first (no AI needed)
- **Test with the docs:** The interactive docs at `/docs` are the easiest way to test
- **Check logs:** The API shows helpful error messages
- **Lower min_score:** If you're not getting matches, try `min_score: 0.5`

---

## 🤝 Need Help?

1. Check the **Troubleshooting** section above
2. Look at the interactive API docs: http://localhost:8000/docs
3. Read the detailed API documentation: `API_DOCUMENTATION.md`

---

## 📝 License

This project is for internal use. Add your license here if needed.

---

## 🎉 You're Ready!

The system is simple:
1. **Fetch** tenders → `python run_cli.py`
2. **Match** them → Use the API
3. **Get results** → Check the matches

**Start the API and visit http://localhost:8000/docs to try it out!** 🚀

---

**Made with ❤️ for smarter government tender discovery**
