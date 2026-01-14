# Utility Scripts

This directory contains helpful utility scripts for common tasks.

## Available Scripts

### 1. `start_api.py`
**Purpose:** Start the FastAPI server with nice output

**Usage:**
```bash
python scripts/start_api.py
```

**What it does:**
- Starts the API server on http://localhost:8000
- Shows helpful URLs for docs
- Auto-reloads on code changes

---

### 2. `run_ai_matching.py`
**Purpose:** Run AI-powered matching using Ollama

**Usage:**
```bash
python scripts/run_ai_matching.py
```

**Requirements:**
- Ollama must be installed and running
- Tenders must be in `data/tenders/available_tenders.json`
- Products must be in `data/products/our_products.json`

**What it does:**
- Loads tenders and products from files
- Uses LLM to find intelligent matches
- Saves results to `data/outputs/matched_tenders.json`

---

### 3. `run_rule_matching.py`
**Purpose:** Run rule-based matching (no AI needed)

**Usage:**
```bash
# Default minimum score (1.0)
python scripts/run_rule_matching.py

# Custom minimum score
python scripts/run_rule_matching.py 2.0
```

**What it does:**
- Loads tenders and products from files
- Uses keyword-based matching
- Saves results to `data/outputs/rule_based_matches.json`

---

### 4. `view_stats.py`
**Purpose:** View matching statistics from database

**Usage:**
```bash
python scripts/view_stats.py
```

**Requirements:**
- MongoDB must be running
- Some matches must exist in database

**What it does:**
- Shows total matches
- Breaks down matches by product
- Shows score distribution
- Displays tender count

---

## Quick Reference

```bash
# Fetch tenders
python main.py

# Start API server
python scripts/start_api.py

# Run rule-based matching
python scripts/run_rule_matching.py

# Run AI matching
python scripts/run_ai_matching.py

# View statistics
python scripts/view_stats.py
```

---

## Notes

- All scripts assume you're running them from the project root directory
- Make sure to set `MONGO_URI` environment variable before running
- For AI matching, Ollama must be installed and running
