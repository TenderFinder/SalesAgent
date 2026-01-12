# SalesAgent Architecture Documentation

## Overview

This document describes the architectural design of the SalesAgent system, following industry-standard patterns for Agentic AI applications.

---

## Architecture Pattern

The project follows a **Layered Architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│  (CLI, API Routes - Future: Web Dashboard, REST API)        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    Controller Layer                          │
│     (Orchestrates requests, handles routing logic)          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                     Service Layer                            │
│  (Business Logic, Agent Orchestration, Workflows)           │
│  - TenderService: Fetch & process tenders                   │
│  - MatchingService: Coordinate matching operations          │
│  - AgentService: Manage AI agents                           │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                      Agent Layer                             │
│  (AI-Powered Components, LLM Integration)                   │
│  - RuleBasedMatchingAgent: Keyword matching                 │
│  - LLMMatchingAgent: AI-powered analysis                    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   Repository Layer                           │
│  (Data Access, External APIs, Database Operations)          │
│  - TenderRepository: GeM API integration                    │
│  - ProductRepository: Product catalog access                │
│  - MatchRepository: Match results storage                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                      Model Layer                             │
│  (Data Models, Schemas, Domain Objects)                     │
│  - Tender, Product, Match, MatchResult                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
SalesAgent/
├── app/                          # Main application package
│   ├── __init__.py              # App initialization
│   │
│   ├── models/                  # Data models (Domain objects)
│   │   ├── __init__.py
│   │   ├── tender.py           # Tender model
│   │   ├── product.py          # Product model
│   │   ├── match.py            # Match result model
│   │   └── schemas.py          # Pydantic schemas for validation
│   │
│   ├── repositories/            # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py             # Base repository interface
│   │   ├── tender_repository.py    # GeM API integration
│   │   ├── product_repository.py   # Product catalog access
│   │   └── match_repository.py     # Match storage (MongoDB)
│   │
│   ├── agents/                  # AI Agent components
│   │   ├── __init__.py
│   │   ├── base_agent.py       # Base agent interface
│   │   ├── rule_based_agent.py # Rule-based matching agent
│   │   ├── llm_agent.py        # LLM-powered matching agent
│   │   └── scoring/            # Scoring algorithms
│   │       ├── __init__.py
│   │       ├── keyword_scorer.py
│   │       └── semantic_scorer.py
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── tender_service.py   # Tender operations
│   │   ├── matching_service.py # Matching orchestration
│   │   └── agent_service.py    # Agent management
│   │
│   ├── controllers/             # Request handlers
│   │   ├── __init__.py
│   │   ├── tender_controller.py
│   │   ├── match_controller.py
│   │   └── cli_controller.py   # CLI interface
│   │
│   ├── routes/                  # API routes (future)
│   │   ├── __init__.py
│   │   ├── api_v1.py
│   │   └── health.py
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py           # Logging configuration
│   │   ├── validators.py       # Input validation
│   │   └── helpers.py          # Helper functions
│   │
│   └── config/                  # Configuration management
│       ├── __init__.py
│       ├── settings.py         # Application settings
│       └── database.py         # Database configuration
│
├── data/                        # Data files
│   ├── products/               # Product catalogs
│   │   └── our_products.json
│   ├── tenders/                # Tender data
│   │   └── available_tenders.json
│   └── outputs/                # Generated outputs
│       └── matched_tenders.json
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── unit/                   # Unit tests
│   │   ├── test_models.py
│   │   ├── test_agents.py
│   │   └── test_services.py
│   ├── integration/            # Integration tests
│   │   └── test_workflows.py
│   └── fixtures/               # Test fixtures
│       └── sample_data.py
│
├── scripts/                     # Utility scripts
│   ├── fetch_tenders.py        # Standalone tender fetcher
│   ├── run_matching.py         # Standalone matcher
│   └── migrate_data.py         # Data migration
│
├── docs/                        # Documentation
│   ├── api/                    # API documentation
│   ├── architecture/           # Architecture docs
│   └── guides/                 # User guides
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── Pipfile                      # Pipenv configuration
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## Layer Responsibilities

### 1. **Model Layer** (`app/models/`)
- Define domain objects (Tender, Product, Match)
- Data validation using Pydantic
- Type hints and schemas
- No business logic

**Example:**
```python
# app/models/tender.py
from pydantic import BaseModel, Field
from typing import List, Optional

class Tender(BaseModel):
    id: str
    display_name: str
    description: str
    search_tags: List[str]
    market_url: str
    status: str = "active"
```

### 2. **Repository Layer** (`app/repositories/`)
- Data access abstraction
- External API integration
- Database operations
- CRUD operations
- No business logic

**Example:**
```python
# app/repositories/tender_repository.py
class TenderRepository(BaseRepository):
    def fetch_from_api(self) -> List[Tender]:
        """Fetch tenders from GeM API"""
        
    def save_to_database(self, tenders: List[Tender]) -> None:
        """Save tenders to MongoDB"""
```

### 3. **Agent Layer** (`app/agents/`)
- AI-powered components
- LLM integration
- Scoring algorithms
- Agent-specific logic
- Reusable AI capabilities

**Example:**
```python
# app/agents/llm_agent.py
class LLMMatchingAgent(BaseAgent):
    def analyze(self, tenders: List[Tender], products: List[Product]) -> List[Match]:
        """Use LLM to analyze and match"""
```

### 4. **Service Layer** (`app/services/`)
- Business logic orchestration
- Workflow coordination
- Agent management
- Transaction handling
- Error handling

**Example:**
```python
# app/services/matching_service.py
class MatchingService:
    def __init__(self, rule_agent, llm_agent, match_repo):
        self.rule_agent = rule_agent
        self.llm_agent = llm_agent
        self.match_repo = match_repo
    
    def find_matches(self, use_ai: bool = False) -> List[Match]:
        """Orchestrate matching process"""
```

### 5. **Controller Layer** (`app/controllers/`)
- Handle user requests
- Input validation
- Response formatting
- Route to appropriate services
- Error handling

**Example:**
```python
# app/controllers/match_controller.py
class MatchController:
    def execute_matching(self, request: MatchRequest) -> MatchResponse:
        """Handle matching request"""
```

### 6. **Routes Layer** (`app/routes/`)
- API endpoint definitions
- Request routing
- Middleware integration
- Future: REST API, GraphQL

---

## Design Patterns Used

### 1. **Repository Pattern**
- Abstracts data access
- Enables easy testing with mocks
- Separates data logic from business logic

### 2. **Service Pattern**
- Encapsulates business logic
- Coordinates between repositories and agents
- Manages transactions

### 3. **Agent Pattern**
- Autonomous AI components
- Pluggable architecture
- Easy to add new agents

### 4. **Dependency Injection**
- Loose coupling
- Easy testing
- Flexible configuration

### 5. **Factory Pattern**
- Create agents dynamically
- Configuration-based instantiation

---

## Data Flow

### Tender Fetching Flow
```
CLI/API Request
    ↓
TenderController
    ↓
TenderService
    ↓
TenderRepository → GeM API
    ↓
TenderRepository → MongoDB
    ↓
Response
```

### Matching Flow
```
CLI/API Request
    ↓
MatchController
    ↓
MatchingService
    ↓
├─→ RuleBasedAgent → Scoring
└─→ LLMAgent → Ollama
    ↓
MatchRepository → MongoDB
    ↓
Response
```

---

## Configuration Management

### Environment-Based Configuration
```python
# app/config/settings.py
class Settings(BaseSettings):
    # API Configuration
    gem_api_url: str
    
    # Database Configuration
    mongo_uri: str
    mongo_db_name: str
    
    # LLM Configuration
    ollama_model: str = "deepseek-r1:8b"
    
    # Application Configuration
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```

---

## Error Handling Strategy

### Layered Error Handling
```python
# Custom exceptions
class TenderServiceError(Exception): pass
class MatchingServiceError(Exception): pass
class AgentError(Exception): pass

# Error handling in layers
try:
    service.execute()
except RepositoryError as e:
    logger.error(f"Data access error: {e}")
    raise ServiceError("Failed to access data")
except AgentError as e:
    logger.error(f"Agent error: {e}")
    raise ServiceError("AI processing failed")
```

---

## Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock dependencies
- Fast execution

### Integration Tests
- Test component interactions
- Use test database
- Verify workflows

### Agent Tests
- Test AI components
- Use sample data
- Verify output quality

---

## Future Enhancements

### Phase 1: API Layer
- Add FastAPI/Flask REST API
- Implement authentication
- Add rate limiting

### Phase 2: Advanced Agents
- Multi-agent collaboration
- Agent memory/context
- Feedback loops

### Phase 3: Scalability
- Message queue integration
- Distributed processing
- Caching layer

---

## Benefits of This Architecture

✅ **Separation of Concerns**: Each layer has a clear responsibility  
✅ **Testability**: Easy to write unit and integration tests  
✅ **Maintainability**: Changes are isolated to specific layers  
✅ **Scalability**: Easy to add new features and agents  
✅ **Reusability**: Components can be reused across different contexts  
✅ **Flexibility**: Easy to swap implementations (e.g., different LLMs)  
✅ **Professional**: Follows industry best practices  

---

**This architecture provides a solid foundation for building a production-ready Agentic AI system.**
