# SalesAgent Restructuring Guide

## Overview

This document guides you through the restructuring of SalesAgent from a simple script-based application to a professional, industry-standard Agentic AI system following MVC and layered architecture patterns.

---

## What Changed?

### Architecture Transformation

**Before (v1.0):**
```
SalesAgent/
├── main.py              # Simple pipeline script
├── api_client.py        # API wrapper
├── mongo_client.py      # MongoDB helper
├── matcher.py           # Matching logic
├── SaleAgent.py         # LLM script
├── scorer.py            # Scoring function
├── config.py            # Hardcoded config
└── data/
    └── our_products.json
```

**After (v2.0):**
```
SalesAgent/
├── app/                          # Main application package
│   ├── models/                   # Data models (Pydantic)
│   ├── repositories/             # Data access layer
│   ├── agents/                   # AI agents
│   │   └── scoring/             # Scoring algorithms
│   ├── services/                 # Business logic
│   ├── controllers/              # Request handlers
│   ├── utils/                    # Utilities (logging, etc.)
│   └── config/                   # Configuration management
├── data/                         # Organized data files
│   ├── products/
│   ├── tenders/
│   └── outputs/
├── tests/                        # Test suite
├── scripts/                      # Utility scripts
├── docs/                         # Documentation
└── main.py                       # New CLI entry point
```

---

## Migration Steps

### Step 1: Install New Dependencies

```bash
# Backup old requirements
cp requirements.txt requirements_old.txt

# Install new dependencies
pip install -r requirements_new.txt

# Or use the new requirements file
mv requirements_new.txt requirements.txt
pip install -r requirements.txt
```

**New Dependencies:**
- `pydantic==2.10.5` - Data validation
- `pydantic-settings==2.7.1` - Configuration management
- `python-dotenv==1.0.1` - Environment variables

### Step 2: Set Up Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Important:** Set your MongoDB URI in `.env`:
```bash
MONGO_URI=mongodb+srv://your_user:your_password@your_cluster.mongodb.net/
```

### Step 3: Migrate Data Files

Data files are now organized in subdirectories:

```bash
# Products
# Already moved: data/our_products.json → data/products/our_products.json

# Tenders (if you have local copies)
# Already moved: available_tenders.json → data/tenders/available_tenders.json

# Outputs will go to
# data/outputs/matched_tenders_*.json
```

### Step 4: Update Your Workflow

#### Old Way (v1.0):
```bash
# Fetch tenders
python main.py

# Run rule-based matching
python -c "from matcher import TenderMatchingAgent; ..."

# Run AI matching
python SaleAgent.py
```

#### New Way (v2.0):
```bash
# Run rule-based matching
python main_new.py match

# Run AI-powered matching
python main_new.py match --ai

# Run with custom score threshold
python main_new.py match --min-score 2.0

# View statistics
python main_new.py stats

# Get help
python main_new.py --help
```

### Step 5: Test the New System

```bash
# Test rule-based matching
python main_new.py match

# Expected output:
# 🚀 Starting SalesAgent Matching System
# ============================================================
# 📊 Mode: Rule-Based
# 🎯 Minimum Score: 1.0
# ============================================================
# ✅ Matching Complete!
# 📈 Found X matches
```

---

## Key Improvements

### 1. **Separation of Concerns**

**Models** (`app/models/`)
- Pure data structures
- Pydantic validation
- Type safety
- No business logic

**Repositories** (`app/repositories/`)
- Data access only
- Database operations
- API integration
- No business logic

**Agents** (`app/agents/`)
- AI-specific logic
- Pluggable architecture
- Reusable components

**Services** (`app/services/`)
- Business logic orchestration
- Workflow coordination
- Transaction management

**Controllers** (`app/controllers/`)
- User interface handling
- Input validation
- Response formatting

### 2. **Configuration Management**

**Old:**
```python
# config.py
MONGO_URI = "mongodb+srv://user:password@..."  # ❌ Hardcoded
```

**New:**
```python
# app/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str  # ✅ From environment
    
    class Config:
        env_file = ".env"
```

### 3. **Logging**

**Old:**
```python
print("🚀 Starting...")  # ❌ No structured logging
```

**New:**
```python
from app.utils import get_logger

logger = get_logger(__name__)
logger.info("Starting matching workflow")  # ✅ Structured logging
```

### 4. **Error Handling**

**Old:**
```python
try:
    data = fetch_data(url)
except:
    print("Failed")  # ❌ Poor error handling
```

**New:**
```python
try:
    data = self.tender_repo.fetch_from_api()
except requests.RequestException as e:
    logger.error(f"API error: {e}", exc_info=True)
    raise  # ✅ Proper error handling
```

### 5. **Testability**

**Old:**
- Hard to test
- Tight coupling
- No dependency injection

**New:**
```python
# Easy to test with mocks
def test_matching_service():
    mock_repo = Mock(TenderRepository)
    service = MatchingService(tender_repo=mock_repo)
    # Test with mocked dependencies
```

---

## Code Comparison

### Fetching Tenders

**Old (`main.py`):**
```python
from config import API_URL, MONGO_URI, DB_NAME, COLLECTION_NAME
from api_client import fetch_data
from mongo_client import save_to_mongodb

def main():
    data = fetch_data(API_URL)
    if data:
        save_to_mongodb(data, MONGO_URI, DB_NAME, COLLECTION_NAME)
```

**New (using services):**
```python
from app.services import MatchingService

service = MatchingService()
matches = service.execute_matching(use_ai=False)
```

### Matching

**Old (`matcher.py`):**
```python
class TenderMatchingAgent:
    def __init__(self, product_file, tender_file):
        with open(product_file) as f:
            self.offerings = json.load(f)["offerings"]
        # ...
```

**New (`app/agents/rule_based_agent.py`):**
```python
class RuleBasedMatchingAgent(BaseAgent):
    def analyze(self, tenders: List[Tender], products: List[Product]) -> List[Match]:
        # Type-safe, validated, testable
        matches = []
        for tender in tenders:
            # ...
        return matches
```

---

## Benefits of New Architecture

### ✅ Professional Structure
- Industry-standard patterns
- Clear separation of concerns
- Easy to understand and maintain

### ✅ Type Safety
- Pydantic models with validation
- Type hints throughout
- Catch errors early

### ✅ Configuration Management
- Environment-based configuration
- No hardcoded credentials
- Easy deployment

### ✅ Logging & Monitoring
- Structured logging
- Log levels
- File and console output

### ✅ Testability
- Dependency injection
- Mock-friendly design
- Easy unit testing

### ✅ Scalability
- Modular architecture
- Easy to add features
- Plugin-based agents

### ✅ Maintainability
- Clear code organization
- Single responsibility principle
- Easy to debug

---

## Backward Compatibility

The old scripts still work but are deprecated:

```bash
# Old scripts (deprecated but functional)
python main.py          # Still works
python SaleAgent.py     # Still works

# New unified CLI (recommended)
python main_new.py match
python main_new.py match --ai
```

**Recommendation:** Migrate to the new CLI for better features and support.

---

## Next Steps

### Immediate
1. ✅ Install new dependencies
2. ✅ Set up `.env` file
3. ✅ Test new CLI
4. ✅ Migrate workflows

### Short-term
1. Add unit tests (`tests/unit/`)
2. Add integration tests (`tests/integration/`)
3. Set up CI/CD pipeline
4. Add API layer (FastAPI)

### Long-term
1. Web dashboard
2. Real-time monitoring
3. Multi-agent collaboration
4. Advanced analytics

---

## Troubleshooting

### Issue: Import errors

**Solution:**
```bash
# Make sure you're in the project root
cd /path/to/SalesAgent

# Install dependencies
pip install -r requirements.txt

# Run from project root
python main_new.py match
```

### Issue: Configuration not found

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Edit with your settings
nano .env
```

### Issue: MongoDB connection error

**Solution:**
```bash
# Check your MONGO_URI in .env
# Make sure MongoDB is accessible
# Check IP whitelist in MongoDB Atlas
```

---

## Support

For questions or issues:
1. Check `ARCHITECTURE.md` for design details
2. Check `README.md` for usage instructions
3. Open an issue on GitHub
4. Contact the development team

---

## Summary

The restructuring transforms SalesAgent from a collection of scripts into a professional, production-ready Agentic AI system:

- **Before:** Simple scripts, hardcoded config, tight coupling
- **After:** Layered architecture, environment config, loose coupling

**The new structure is:**
- ✅ More maintainable
- ✅ More testable
- ✅ More scalable
- ✅ More professional
- ✅ Industry-standard

**Migration is straightforward:**
1. Install new dependencies
2. Set up `.env` file
3. Use new CLI commands
4. Enjoy better architecture!

---

**Welcome to SalesAgent v2.0!** 🚀
