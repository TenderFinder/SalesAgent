# SalesAgent 🤖📋

**An intelligent toolkit for government tender discovery and matching**

Automatically fetch government tenders from GeM (Government e-Marketplace), store them in MongoDB, and intelligently match them against your company's product offerings using both rule-based algorithms and AI-powered analysis.

---

## 🌟 Features

- **🔄 Automated Data Pipeline**: Fetch tenders from GeM API and persist to MongoDB
- **🎯 Smart Matching**: Rule-based tender-to-product matching with scoring
- **🤖 AI-Powered Analysis**: LLM-driven bulk analysis using Ollama for deeper insights
- **📊 JSON-Based Integration**: Easy-to-read inputs/outputs for seamless integration
- **🔐 Secure Configuration**: Environment-based configuration management
- **📈 Scalable Architecture**: Modular design for easy extension and customization

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture Overview](#-architecture-overview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Data Formats](#-data-formats)
- [Troubleshooting](#-troubleshooting)
- [Security Best Practices](#-security-best-practices)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd SalesAgent

# 2. Set up Python environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (IMPORTANT!)
export MONGO_URI="your_mongodb_connection_string"

# 5. Run the pipeline
python main.py

# 6. Run AI analysis (requires Ollama)
python SaleAgent.py
```

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│   GeM API       │
│ (Tenders Data)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   api_client.py │─────▶│   MongoDB        │
│  (Fetch Data)   │      │ (Tender Storage) │
└─────────────────┘      └──────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌──────────────────┐
│    main.py      │      │   matcher.py     │
│  (Orchestrator) │      │ (Rule Matching)  │
└─────────────────┘      └──────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  SaleAgent.py    │
                         │  (AI Analysis)   │
                         └──────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ matched_tenders  │
                         │     .json        │
                         └──────────────────┘
```

### Component Breakdown

| Component | Purpose | Dependencies |
|-----------|---------|--------------|
| `main.py` | Orchestrates the data pipeline | `api_client`, `mongo_client`, `config` |
| `api_client.py` | Fetches tender data from GeM API | `requests` |
| `mongo_client.py` | Handles MongoDB operations | `pymongo` |
| `matcher.py` | Rule-based matching engine | `scorer` (⚠️ **Missing - see Known Issues**) |
| `SaleAgent.py` | AI-powered analysis using LLMs | `ollama` |
| `config.py` | Configuration constants | None |

---

## ⚙️ Prerequisites

### Required
- **Python 3.12+** (specified in `Pipfile`)
- **MongoDB** instance (MongoDB Atlas or self-hosted)
  - Free tier Atlas cluster: [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- **Git** for version control

### Optional (for AI Analysis)
- **Ollama** for LLM-powered analysis
  - Installation: [ollama.com](https://ollama.com)
  - Recommended model: `llama3.2`

---

## 📦 Installation

### Option 1: Using pipenv (Recommended)

```bash
# Install pipenv
pip install pipenv

# Install dependencies and create virtual environment
pipenv install

# Activate the virtual environment
pipenv shell
```

### Option 2: Using venv + pip

```bash
# Create virtual environment
python3.12 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import pymongo, requests, ollama; print('✅ All dependencies installed')"
```

---

## 🔧 Configuration

### Environment Variables (Recommended)

**⚠️ CRITICAL: Never commit credentials to version control!**

```bash
# Set MongoDB connection string
export MONGO_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/"

# Optional: Override default database/collection
export DB_NAME="gem_database"
export COLLECTION_NAME="services"
```

### Configuration File

Edit `config.py` for development only. **Remove credentials before committing!**

```python
# config.py
import os

API_URL = "https://mkp.gem.gov.in/cms/others/api/services/list.json?search%5Bstatus_in%5D%5B%5D=active&_ln=en"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "gem_database")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "services")
```

### Product Catalog Configuration

Edit `data/our_products.json` to define your company's offerings:

```json
{
  "company_name": "Your Company Name",
  "offerings": [
    {
      "name": "Your Product/Service",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "category": "category_name"
    }
  ]
}
```

---

## 💻 Usage

### 1️⃣ Fetch and Store Tenders

Retrieves tenders from GeM API and stores them in MongoDB.

```bash
python main.py
```

**Expected Output:**
```
🚀 Starting GEM API → MongoDB pipeline
📡 Fetching data from API...
🗄️ Connecting to MongoDB...
✅ Data saved to MongoDB successfully
```

### 2️⃣ Rule-Based Matching

**⚠️ Known Issue**: `matcher.py` requires `scorer.py` which is currently missing from the repository.

**Workaround**: Create `scorer.py` with the following implementation:

```python
# scorer.py
def score_match(offering, tender):
    """
    Calculate match score between an offering and a tender.
    
    Args:
        offering: Dict with 'keywords' and 'name'
        tender: Dict with 'search_tags', 'display_name', 'description'
    
    Returns:
        Tuple of (score: float, reasons: list)
    """
    score = 0.0
    reasons = []
    
    # Get keywords and tags
    keywords = [k.lower() for k in offering.get('keywords', [])]
    tags = [t.lower() for t in tender.get('search_tags', [])]
    tender_text = (tender.get('display_name', '') + ' ' + 
                   tender.get('description', '')).lower()
    
    # Check keyword matches in tags
    for keyword in keywords:
        if keyword in tags:
            score += 2.0
            reasons.append(f"Keyword '{keyword}' found in tender tags")
        elif keyword in tender_text:
            score += 1.0
            reasons.append(f"Keyword '{keyword}' found in tender description")
    
    return score, reasons
```

**Then run matching:**

```bash
# Command-line usage
python -c "from matcher import TenderMatchingAgent; \
m = TenderMatchingAgent('data/our_products.json', 'available_tenders.json'); \
import json; print(json.dumps(m.find_matches(min_score=1.0), indent=2))"
```

**Programmatic usage:**

```python
from matcher import TenderMatchingAgent

matcher = TenderMatchingAgent(
    product_file='data/our_products.json',
    tender_file='available_tenders.json'
)

matches = matcher.find_matches(min_score=1.0)
for match in matches:
    print(f"Tender: {match['tender_name']}")
    print(f"Product: {match['matched_offering']}")
    print(f"Score: {match['score']}")
    print(f"Reason: {match['reason']}")
    print(f"URL: {match['market_url']}\n")
```

### 3️⃣ AI-Powered Analysis (Ollama)

Uses LLM to perform intelligent matching with contextual understanding.

**Prerequisites:**
```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama service
ollama serve

# Pull the model (in another terminal)
ollama pull llama3.2
```

**Run analysis:**
```bash
python SaleAgent.py
```

**Expected Output:**
```
🚀 Starting Sales Agent Analysis with Ollama (Bulk Mode)...
📡 Loaded 6 tenders and 4 products.
🧠 Analyze matches contextually (Bulk)...
DEBUG LLM RAW: [...]
✅ Analysis Complete. Found 3 matches:
[
  {
    "tender_id": "services_home_3d22084507",
    "tender_title": "3D Printing Service",
    "matched_product": "3D Printing Service",
    "matching_score": 95,
    "customization_possibility": "Minimal customization needed",
    "reasoning": "Direct match on service type and keywords"
  }
]
💾 Saved results to matched_tenders.json
```

---

## 📄 Data Formats

### Input: Product Catalog (`data/our_products.json`)

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
      "name": "AI & Machine Learning",
      "keywords": ["ai", "artificial intelligence", "machine learning"],
      "category": "it"
    }
  ]
}
```

### Input: Tenders (`available_tenders.json`)

```json
{
  "total_count": 6,
  "source": "GeM Services",
  "services": [
    {
      "id": "services_home_3d22084507",
      "type": "OfferPriceOnlyInBidService",
      "display_name": "3D Printing Service",
      "description": "<p>3D Printing or Additive Manufacturing...</p>",
      "sla": "<p>Service STC requirements...</p>",
      "market_url": "https://mkp.gem.gov.in/services#!/browse/...",
      "search_tags": ["Additive Manufacturing", "3D Printing", "Rapid Prototyping"],
      "status": "active"
    }
  ]
}
```

### Output: Matched Tenders (`matched_tenders.json`)

```json
[
  {
    "tender_id": "services_home_3d22084507",
    "tender_title": "3D Printing Service",
    "matched_product": "3D Printing Service",
    "matching_score": 95,
    "customization_possibility": "Minimal customization needed",
    "reasoning": "Direct match on service type and keywords"
  }
]
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error

**Error:** `pymongo.errors.ServerSelectionTimeoutError`

**Solutions:**
- Verify `MONGO_URI` is correctly set
- Check MongoDB Atlas IP whitelist (add `0.0.0.0/0` for testing)
- Ensure network connectivity
- Verify credentials are correct

```bash
# Test connection
python -c "from pymongo import MongoClient; \
client = MongoClient('$MONGO_URI'); \
print(client.server_info())"
```

#### 2. Missing `scorer.py`

**Error:** `ModuleNotFoundError: No module named 'scorer'`

**Solution:** Create `scorer.py` as shown in the [Rule-Based Matching](#2️⃣-rule-based-matching) section.

#### 3. Ollama Connection Error

**Error:** `ollama.exceptions.ConnectionError`

**Solutions:**
- Start Ollama service: `ollama serve`
- Verify model is installed: `ollama list`
- Pull model if missing: `ollama pull llama3.2`

#### 4. API Fetch Failure

**Error:** `❌ Failed to fetch data`

**Solutions:**
- Check internet connectivity
- Verify API URL is accessible
- Check for API rate limiting
- Try with a browser to confirm API is working

#### 5. Empty Match Results

**Issue:** No matches found despite relevant products

**Solutions:**
- Lower `min_score` threshold in matcher
- Verify keywords in `our_products.json` match tender tags
- Check tender data format in `available_tenders.json`
- Review `scorer.py` logic

---

## 🔐 Security Best Practices

### ⚠️ Critical Security Issues

**The current repository has exposed credentials in `config.py`!**

### Immediate Actions Required

1. **Remove credentials from `config.py`:**
   ```python
   # ❌ NEVER DO THIS
   MONGO_URI = "mongodb+srv://user:password@cluster.mongodb.net/"
   
   # ✅ DO THIS INSTEAD
   MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
   ```

2. **Rotate exposed credentials:**
   - Change MongoDB password immediately
   - Update connection string
   - Review access logs for unauthorized access

3. **Use environment variables:**
   ```bash
   # .env file (add to .gitignore!)
   MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/
   DB_NAME=gem_database
   COLLECTION_NAME=services
   ```

4. **Update `.gitignore`:**
   ```gitignore
   # Environment variables
   .env
   .env.local
   
   # Credentials
   config_local.py
   secrets/
   
   # Output files with sensitive data
   matched_tenders.json
   available_tenders.json
   ```

### Additional Security Recommendations

- **Use MongoDB Atlas IP Whitelist**: Restrict access to known IPs
- **Enable MongoDB Authentication**: Use strong passwords
- **Implement API Rate Limiting**: Prevent abuse of GeM API
- **Sanitize LLM Inputs**: Prevent prompt injection attacks
- **Audit Logs**: Monitor MongoDB access and API usage
- **Data Privacy**: Ensure tender data handling complies with regulations

---

## 📊 Repository Structure

```
SalesAgent/
├── main.py                    # Main pipeline orchestrator
├── api_client.py              # GeM API client
├── mongo_client.py            # MongoDB operations
├── matcher.py                 # Rule-based matching engine
├── SaleAgent.py              # AI-powered analysis
├── config.py                  # Configuration (⚠️ remove credentials!)
├── scorer.py                  # ⚠️ MISSING - needs to be created
├── requirements.txt           # Python dependencies
├── Pipfile                    # Pipenv configuration
├── Pipfile.lock              # Locked dependencies
├── available_tenders.json     # Sample tender data
├── matched_tenders.json       # Output from AI analysis
├── data/
│   └── our_products.json     # Product catalog
└── README.md                  # This file
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues

- Use GitHub Issues for bug reports
- Include error messages, logs, and steps to reproduce
- Specify your environment (OS, Python version, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages: `git commit -m "Add: feature description"`
6. Push to your fork: `git push origin feature/your-feature`
7. Open a Pull Request

### Development Priorities

- [ ] Create `scorer.py` with robust matching algorithm
- [ ] Implement environment variable configuration
- [ ] Add unit tests for all components
- [ ] Create CLI interface for easier usage
- [ ] Add logging framework
- [ ] Implement error handling and retry logic
- [ ] Add data validation for JSON inputs
- [ ] Create Docker containerization
- [ ] Add CI/CD pipeline
- [ ] Improve documentation with examples

---

## 📝 License

This repository does not currently include a license file.

**Recommended actions:**
- Add an appropriate open-source license (MIT, Apache-2.0, GPL-3.0)
- Consider your use case:
  - **MIT**: Permissive, allows commercial use
  - **Apache-2.0**: Permissive with patent protection
  - **GPL-3.0**: Copyleft, requires derivative works to be open-source

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Documentation**: This README and inline code comments

---

## 🎯 Roadmap

### Version 1.1 (Next Release)
- ✅ Fix missing `scorer.py` dependency
- ✅ Implement environment-based configuration
- ✅ Add comprehensive error handling
- ⬜ Create CLI interface
- ⬜ Add unit tests

### Version 2.0 (Future)
- ⬜ Web dashboard for match visualization
- ⬜ Real-time tender monitoring
- ⬜ Email notifications for new matches
- ⬜ Multi-source tender aggregation
- ⬜ Advanced ML-based scoring

---

## 🙏 Acknowledgments

- **GeM (Government e-Marketplace)** for providing the tender API
- **Ollama** for local LLM capabilities
- **MongoDB** for flexible data storage

---

**Made with ❤️ for smarter government tender discovery**
