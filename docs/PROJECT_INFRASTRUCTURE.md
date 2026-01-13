# LifeLine - Project Infrastructure & Architecture Documentation

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Project Type:** Full-Stack Monorepo Web Application

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack & Library Versions](#2-technology-stack--library-versions)
3. [Architecture Overview](#3-architecture-overview)
4. [Backend Architecture](#4-backend-architecture)
5. [Frontend Architecture](#5-frontend-architecture)
6. [Database Architecture](#6-database-architecture)
7. [Authentication & Authorization](#7-authentication--authorization)
8. [API Reference](#8-api-reference)
9. [External Integrations](#9-external-integrations)
10. [N8N Automation Workflow](#10-n8n-automation-workflow)
11. [Testing Strategy](#11-testing-strategy)
12. [CI/CD Pipeline](#12-cicd-pipeline)
13. [Deployment Architecture](#13-deployment-architecture)
14. [Environment Configuration](#14-environment-configuration)
15. [Security Considerations](#15-security-considerations)
16. [Code Style & Conventions](#16-code-style--conventions)
17. [Future Considerations](#17-future-considerations)

---

## 1. Project Overview

**LifeLine** is a family health tracking web application designed to help users manage medications, track family member health, store medical documents, and schedule health-related events. The application integrates with Google services (Drive, Calendar) and features an AI-powered chatbot for medical assistance.

### Core Features

- **Family Member Management**: Track health information for multiple family members
- **Medication Inventory**: Manage medication stock with expiration tracking
- **Medication Usage Logging**: Record when medications are used by family members
- **Illness Timeline**: Track illness history for each family member
- **Google Drive Integration**: Store and manage medical documents in a dedicated folder
- **Google Calendar Integration**: Schedule medical appointments and reminders
- **AI Chatbot**: N8N-powered assistant for medical queries with RAG capabilities
- **Automated Email Summaries**: Receive email summaries when uploading medical documents

### Project Structure

```
life-line/
├── backend/                 # FastAPI Python backend
│   ├── app/                 # Application source code
│   │   ├── controllers/     # API route handlers
│   │   ├── services/        # Business logic layer
│   │   ├── dao/             # Data access objects
│   │   ├── models/          # Pydantic models
│   │   └── utils/           # Utilities (JWT, dependencies)
│   ├── alembic/             # Database migrations
│   ├── tests/               # Unit tests
│   ├── Dockerfile           # Container configuration
│   └── requirements.txt     # Python dependencies
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Route-level pages
│   │   ├── services/        # API communication layer
│   │   ├── utils/           # Utility functions
│   │   ├── styles/          # Global styles
│   │   └── __tests__/       # Unit tests
│   ├── tests/               # E2E tests (Playwright)
│   └── package.json         # Node dependencies
├── database/                # Database schema exports
├── n8n-script/              # N8N workflow configuration
└── *.md                     # Documentation files
```

---

## 2. Technology Stack & Library Versions

### Backend Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| **FastAPI** | 0.115.6 | Web framework with auto OpenAPI docs |
| **Pydantic** | 2.10.3 | Data validation and settings |
| **Pydantic Settings** | 2.6.1 | Environment configuration |
| **Uvicorn** | 0.32.1 | ASGI server |
| **Gunicorn** | latest | Production WSGI server |
| **psycopg2-binary** | 2.9.10 | PostgreSQL adapter |
| **Alembic** | latest | Database migrations |
| **python-jose** | 3.3.0 | JWT token handling |
| **google-api-python-client** | 2.154.0 | Google APIs integration |
| **google-auth** | 2.36.0 | Google authentication |
| **google-auth-oauthlib** | 1.2.1 | OAuth 2.0 for Google |
| **requests** | 2.32.5 | HTTP client |
| **httpx** | 0.27.2 | Async HTTP client |
| **pytest** | 7.4.4 | Testing framework |
| **pytest-asyncio** | 0.23.3 | Async test support |
| **pytest-cov** | 4.1.0 | Coverage reporting |
| **pytest-mock** | 3.12.0 | Mocking utilities |
| **freezegun** | 1.5.1 | Time mocking |

### Frontend Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| **React** | 19.0.0 | UI framework |
| **React DOM** | 19.0.0 | DOM rendering |
| **React Router DOM** | 7.1.3 | Client-side routing |
| **Axios** | 1.7.9 | HTTP client |
| **React Icons** | 5.5.0 | Icon library |
| **React Dropzone** | 14.3.8 | File upload component |
| **@n8n/chat** | 1.2.1 | N8N chat widget |
| **Vite** | 6.0.5 | Build tool |
| **Vitest** | 1.2.2 | Unit testing |
| **@testing-library/react** | 16.0.1 | React testing utilities |
| **@testing-library/jest-dom** | 6.1.5 | DOM assertions |
| **@testing-library/user-event** | 14.5.2 | User interaction simulation |
| **Playwright** | 1.57.0 | E2E testing |
| **jsdom** | 24.0.0 | DOM simulation |

### Runtime Versions

- **Python**: 3.11+ (Docker uses 3.11-slim-buster)
- **Node.js**: 18+ (LTS recommended)
- **PostgreSQL**: 14+

---

## 3. Architecture Overview

The application follows a **three-tier architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │  Pages   │ │Components│ │ Services │ │     Utilities    │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTPS │
                              ▼       ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND (FastAPI)                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │Controllers │→│  Services  │→│    DAOs    │→│  Database  │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│                       │                                          │
│                       ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              External Integrations                          │ │
│  │  Google Drive │ Google Calendar │ N8N Webhooks             │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     N8N AUTOMATION                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ File Summary │ │ RAG Chatbot  │ │ Email Notifications      │ │
│  │   Workflow   │ │   Workflow   │ │ (Gmail Integration)      │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────┘ │
│                       │                                          │
│                       ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  PGVector Store │ HuggingFace Embeddings │ Gemini LLM     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Backend Architecture

### Layered Architecture Pattern

```
HTTP Request → Controller → Service → DAO → Database
                   │            │
                   ▼            ▼
              Validation    Business
              (Pydantic)     Logic
```

### Controllers (`app/controllers/`)

Route handlers that validate requests and delegate to services.

| File | Prefix | Description |
|------|--------|-------------|
| `auth.py` | `/auth` | Google OAuth authentication |
| `family_members.py` | `/family-members` | Family member CRUD |
| `medications.py` | `/medications` | Medication inventory CRUD |
| `medication_usage.py` | `/medication-usage` | Usage tracking |
| `illness_logs.py` | `/illness-logs` | Illness history tracking |
| `google_drive.py` | `/drive` | Drive file operations |
| `google_calendar.py` | `/calendar` | Calendar event operations |
| `n8n_controller.py` | `/n8n` | N8N webhook integration |

### Services (`app/services/`)

Business logic layer that coordinates DAOs and external services.

| File | Description |
|------|-------------|
| `auth_service.py` | OAuth flow, JWT generation, user creation |
| `family_member_service.py` | Family member business logic |
| `medication_service.py` | Medication inventory with duplicate handling |
| `medication_usage_service.py` | Usage logging with inventory decrement |
| `illness_log_service.py` | Illness tracking logic |
| `google_drive_service.py` | Drive API integration |
| `google_calendar_service.py` | Calendar API integration |
| `n8n_service.py` | N8N webhook triggering |

### DAOs (`app/dao/`)

Data Access Objects with parameterized SQL queries.

| File | Table | Description |
|------|-------|-------------|
| `user_dao.py` | `users` | User account operations |
| `family_member_dao.py` | `family_members` | Family member data access |
| `medication_dao.py` | `medications` | Medication inventory data |
| `medication_usage_dao.py` | `medication_usage` | Usage log data |
| `illness_log_dao.py` | `illness_logs` | Illness history data |
| `google_credentials_dao.py` | `user_google_credentials` | OAuth token storage |

### Models (`app/models/`)

Pydantic models for request/response validation.

| File | Models |
|------|--------|
| `auth.py` | `Token` |
| `user.py` | `UserResponse` |
| `family_member.py` | `FamilyMemberCreate`, `FamilyMemberUpdate`, `FamilyMemberResponse` |
| `medication.py` | `MedicationCreate`, `MedicationUpdate`, `MedicationResponse` |
| `medication_usage.py` | `MedicationUsageCreate`, `MedicationUsageResponse` |
| `illness_log.py` | `IllnessLogCreate`, `IllnessLogUpdate`, `IllnessLogResponse` |

### Utilities (`app/utils/`)

| File | Description |
|------|-------------|
| `jwt.py` | JWT token creation and verification |
| `dependencies.py` | FastAPI dependencies (`get_current_user`, `get_user_by_api_key`) |

---

## 5. Frontend Architecture

### Component-Based Architecture

```
App.jsx
├── Pages (Route-level)
│   ├── LoginPage.jsx
│   ├── GoogleCallbackPage.jsx
│   └── HomePage.jsx
│
├── Components (Reusable UI)
│   ├── Header.jsx
│   ├── Hero.jsx
│   ├── ActionGrid.jsx
│   ├── DataDashboard.jsx
│   ├── InventoryTable.jsx
│   ├── CalendarOverview.jsx
│   ├── DriveSection.jsx
│   ├── IllnessTimeline.jsx
│   ├── ChatWidget.jsx
│   └── modals/
│       ├── Modal.jsx
│       ├── FamilyMemberModal.jsx
│       ├── InventoryModal.jsx
│       ├── LogUsageModal.jsx
│       ├── ScheduleEventModal.jsx
│       ├── IllnessLogModal.jsx
│       ├── EventDetailModal.jsx
│       └── DeleteFileModal.jsx
│
└── Services (API Layer)
    ├── api.js (Axios instance)
    ├── auth.js
    ├── familyMembers.js
    ├── medications.js
    ├── medicationUsage.js
    ├── illnessLogs.js
    ├── googleCalendar.js
    ├── googleDrive.js
    └── n8n.js
```

### Pages

| Page | Route | Description |
|------|-------|-------------|
| `LoginPage.jsx` | `/login` | Google OAuth login button |
| `GoogleCallbackPage.jsx` | `/auth/google/callback` | OAuth callback handler |
| `HomePage.jsx` | `/` | Main dashboard (protected) |

### Key Components

| Component | Purpose |
|-----------|---------|
| `Header` | Navigation with user info and logout |
| `Hero` | Welcome banner with quick actions |
| `ActionGrid` | Quick action buttons for main features |
| `DataDashboard` | Family members overview |
| `InventoryTable` | Medication inventory display |
| `CalendarOverview` | Upcoming calendar events |
| `DriveSection` | Medical documents from Google Drive |
| `IllnessTimeline` | Historical illness tracking |
| `ChatWidget` | N8N-powered AI chatbot |

### Services Layer

The `api.js` creates a configured Axios instance with:
- Base URL from environment
- Automatic JWT token injection
- 401 response handling with logout (excluding Google API errors)

---

## 6. Database Architecture

### Entity Relationship Diagram

```
┌──────────────────────┐
│        users         │
├──────────────────────┤
│ id (PK)              │
│ email (UNIQUE)       │
│ name                 │
│ google_id (UNIQUE)   │
│ google_oauth_token   │
│ google_refresh_token │
│ drive_folder_id      │
│ created_at           │
│ updated_at           │
└──────────┬───────────┘
           │
           │ 1:N
           ▼
┌──────────────────────┐     ┌──────────────────────────────┐
│   family_members     │     │   user_google_credentials    │
├──────────────────────┤     ├──────────────────────────────┤
│ id (PK)              │     │ id (PK)                      │
│ user_id (FK)         │◄────┤ user_id (FK, UNIQUE)         │
│ name                 │     │ access_token                 │
│ date_of_birth        │     │ refresh_token                │
│ created_at           │     │ token_expiry                 │
│ updated_at           │     │ created_at                   │
└──────────┬───────────┘     │ updated_at                   │
           │                 └──────────────────────────────┘
           │ 1:N
           ▼
┌──────────────────────┐     ┌──────────────────────────────┐
│   illness_logs       │     │       medications            │
├──────────────────────┤     ├──────────────────────────────┤
│ id (PK)              │     │ id (PK)                      │
│ family_member_id (FK)│     │ user_id (FK)                 │
│ illness_name         │     │ name                         │
│ start_date           │     │ quantity                     │
│ end_date             │     │ expiration_date              │
│ notes                │     │ created_at                   │
│ created_at           │     │ updated_at                   │
│ updated_at           │     └──────────────┬───────────────┘
└──────────────────────┘                    │
           │                                │
           │ N:1                            │ N:1
           ▼                                ▼
┌──────────────────────────────────────────────────────────┐
│                    medication_usage                       │
├──────────────────────────────────────────────────────────┤
│ id (PK)                                                   │
│ family_member_id (FK)                                     │
│ medication_id (FK)                                        │
│ used_at                                                   │
│ quantity_used                                             │
│ created_at                                                │
│ updated_at                                                │
└──────────────────────────────────────────────────────────┘

N8N Tables:
┌──────────────────────┐     ┌──────────────────────────────┐
│  n8n_chat_histories  │     │       n8n_vectors            │
├──────────────────────┤     ├──────────────────────────────┤
│ id (PK)              │     │ (PGVector managed)           │
│ session_id           │     │ Embeddings for RAG           │
│ message (JSONB)      │     └──────────────────────────────┘
└──────────────────────┘
```

### Database Migrations (Alembic)

| Revision | Description |
|----------|-------------|
| `2236f2a63b38` | Initial schema (users, family_members, medications, medication_usage, user_google_credentials) |
| `77c08d9cfbad` | N8N chat history table for chatbot memory |
| `a1b2c3d4e5f6` | Illness logs table for health tracking |

### Indexes

- `idx_family_members_user_id` on `family_members(user_id)`
- `idx_medications_user_id` on `medications(user_id)`
- `idx_medication_usage_family_member_id` on `medication_usage(family_member_id)`
- `idx_medication_usage_medication_id` on `medication_usage(medication_id)`
- `idx_user_google_credentials_user_id` on `user_google_credentials(user_id)`
- `idx_illness_logs_family_member_id` on `illness_logs(family_member_id)`
- `idx_illness_logs_start_date` on `illness_logs(start_date)`

---

## 7. Authentication & Authorization

### OAuth 2.0 Flow with Google

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Browser │    │Frontend │    │ Backend │    │ Google  │
└────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
     │              │              │              │
     │ Click Login  │              │              │
     │──────────────>              │              │
     │              │ GET /auth/google-login      │
     │              │──────────────>              │
     │              │   Auth URL   │              │
     │              │<──────────────              │
     │  Redirect    │              │              │
     │<─────────────               │              │
     │              │              │              │
     │──────────────────────────────────────────>│
     │              │    Google OAuth Consent    │
     │<──────────────────────────────────────────│
     │              │              │              │
     │ Callback with code          │              │
     │──────────────>              │              │
     │              │ POST /auth/callback         │
     │              │──────────────>              │
     │              │              │ Exchange Code│
     │              │              │──────────────>
     │              │              │ User Info +  │
     │              │              │ Tokens       │
     │              │              │<─────────────│
     │              │              │              │
     │              │ JWT + User   │              │
     │              │<──────────────              │
     │  Store JWT   │              │              │
     │<─────────────               │              │
     │              │              │              │
```

### JWT Token Structure

```json
{
  "sub": "user_id",
  "exp": "expiration_timestamp"
}
```

- Algorithm: HS256
- Default expiration: 24 hours (1440 minutes)

### Protected Routes

All API endpoints except `/auth/*` and `/health` require valid JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Scopes Requested

```python
scopes = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar",
]
```

---

## 8. API Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/google-login` | Get Google OAuth URL |
| POST | `/auth/callback` | Exchange auth code for JWT |

### Family Members

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/family-members` | List all family members |
| POST | `/family-members` | Create family member |
| GET | `/family-members/{id}` | Get family member by ID |
| PUT | `/family-members/{id}` | Update family member |
| DELETE | `/family-members/{id}` | Delete family member |

### Medications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/medications` | List all medications |
| POST | `/medications` | Create/update medication (upsert by name) |
| GET | `/medications/{id}` | Get medication by ID |
| PUT | `/medications/{id}` | Update medication |
| DELETE | `/medications/{id}` | Delete medication |

### Medication Usage

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/medication-usage` | List usage logs (optional filters) |
| POST | `/medication-usage` | Log medication usage |
| GET | `/medication-usage/{id}` | Get usage log by ID |
| DELETE | `/medication-usage/{id}` | Delete usage log |

### Illness Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/illness-logs` | List illness logs (optional family_member_id filter) |
| POST | `/illness-logs` | Create illness log |
| GET | `/illness-logs/{id}` | Get illness log by ID |
| PUT | `/illness-logs/{id}` | Update illness log |
| DELETE | `/illness-logs/{id}` | Delete illness log |

### Google Drive

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/drive/files` | List files from LifeLine Records folder |
| POST | `/drive/upload` | Upload file (triggers N8N summary) |
| DELETE | `/drive/files/{file_id}` | Delete file |

### Google Calendar

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/calendar/upcoming` | Get upcoming events (7 days, max 3/day) |
| POST | `/calendar/events` | Create calendar event |

### Health & System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint (API info) |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc documentation |

---

## 9. External Integrations

### Google Drive Integration

- **Purpose**: Store medical documents (prescriptions, lab results, etc.)
- **Folder**: "LifeLine Records" (auto-created on first login)
- **Features**: 
  - List files
  - Upload files (triggers N8N workflow)
  - Delete files
- **Token Refresh**: Automatic when credentials expire

### Google Calendar Integration

- **Purpose**: Schedule medical appointments and reminders
- **Calendar**: "LIFELINE" (auto-created on first login)
- **Features**:
  - List upcoming events (grouped by date)
  - Create events with title, description, start/end times

### N8N Integration

The backend triggers N8N webhooks for:
1. **File Upload Summary**: When a file is uploaded to Drive, sends file content to N8N for AI summarization and email notification
2. **Chatbot Queries**: The frontend ChatWidget connects directly to N8N webhook for AI responses

---

## 10. N8N Automation Workflow

### Workflow Overview

The N8N workflow (`n8n-script/n8n-workflow.json`) contains three main flows:

### Flow 1: File Summary & Email

```
Webhook (File Upload) → Extract Text from PDF → 
    ├── Gemini Agent (Summarize) → Send Email (Gmail)
    └── PGVector Store (Embeddings)
```

**Purpose**: When a medical document is uploaded:
1. Extract text from PDF
2. Generate AI summary using Gemini
3. Send formatted email summary to user
4. Store document embeddings for RAG

### Flow 2: RAG Embeddings

```
Extracted Text → Text Splitter (500 chars, 50 overlap) → 
    HuggingFace Embeddings → PGVector Store
```

**Purpose**: Chunk and embed medical documents for semantic search.

### Flow 3: AI Chatbot

```
Chat Trigger → Chatbot Agent (Gemini) → Response
                    ↑
    PGVector Tool ──┘ (RAG retrieval)
    Chat Memory ──────┘ (Conversation history)
```

**Purpose**: AI assistant with:
- General medical knowledge (Gemini LLM)
- Personal medical context (RAG from uploaded documents)
- Conversation memory (PostgreSQL storage)

### N8N Components Used

| Component | Purpose |
|-----------|---------|
| `Webhook` | Receive file upload trigger |
| `extractFromFile` | PDF text extraction |
| `agent` | AI reasoning (Gemini-powered) |
| `gmail` | Send email notifications |
| `vectorStorePGVector` | Vector embeddings storage |
| `embeddingsHuggingFaceInference` | Generate embeddings |
| `textSplitterRecursiveCharacterTextSplitter` | Document chunking |
| `memoryPostgresChat` | Conversation memory |
| `chatTrigger` | Chatbot webhook endpoint |
| `lmChatGoogleGemini` | LLM for responses |

---

## 11. Testing Strategy

### Backend Unit Tests

**Location**: `backend/tests/`

| Test File | Coverage |
|-----------|----------|
| `test_01_basic_endpoints.py` | Root and API structure |
| `test_02_health_endpoint.py` | Health check endpoint |
| `test_03_jwt_token_creation.py` | JWT utilities |
| `test_04_family_member_service.py` | Family member business logic |
| `test_05_medication_service.py` | Medication business logic |
| `test_06_medication_usage_service.py` | Usage logging logic |
| `test_07_protected_endpoints.py` | Authentication guards |

**Running Tests**:
```bash
cd backend
pytest -v --cov=app
```

### Frontend Unit Tests

**Location**: `frontend/src/__tests__/components/`

| Test File | Component Tested |
|-----------|------------------|
| `ActionGrid.test.jsx` | Action buttons |
| `ChatWidget.test.jsx` | N8N chat integration |
| `DataDashboard.test.jsx` | Family member display |
| `DriveSection.test.jsx` | Google Drive files |
| `Header.test.jsx` | Navigation header |
| `Hero.test.jsx` | Welcome banner |
| `InventoryTable.test.jsx` | Medication inventory |

**Running Tests**:
```bash
cd frontend
npm run test:unit
```

### E2E Tests (Playwright)

**Location**: `frontend/tests/`

**Configuration**: `playwright.config.cjs`
- Browser: Firefox (Desktop)
- Base URL: http://localhost:4200
- Auto-starts dev server

**Running Tests**:
```bash
cd frontend
npm run test:e2e
```

### Test Configuration Files

| File | Purpose |
|------|---------|
| `backend/pytest.ini` | Pytest settings |
| `frontend/vitest.config.js` | Vitest configuration |
| `frontend/playwright.config.cjs` | Playwright E2E config |
| `frontend/src/test/setup.js` | Test setup (mocks) |

---

## 12. CI/CD Pipeline

### Containerization

**Backend Dockerfile**:
```dockerfile
FROM python:3.11-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "app.main:app"]
```

### Deployment Targets

| Component | Platform | Configuration |
|-----------|----------|---------------|
| Frontend | Vercel | `vercel.json` (SPA rewrites) |
| Backend | Docker-compatible (GCP, AWS, etc.) | Dockerfile |
| Database | Supabase PostgreSQL | Connection string in env |
| N8N | Self-hosted | Dedicated server |

---

## 13. Deployment Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                          INTERNET                               │
└───────────────────┬───────────────────┬────────────────────────┘
                    │                   │
                    ▼                   ▼
         ┌──────────────────┐  ┌──────────────────┐
         │     Vercel       │  │  Docker Host     │
         │  (Frontend)      │  │  (Backend)       │
         │  - React SPA     │  │  - FastAPI       │
         │  - CDN cached    │  │  - Gunicorn      │
         └────────┬─────────┘  └────────┬─────────┘
                  │                     │
                  │                     │
                  └──────────┬──────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │    Supabase      │
                   │   PostgreSQL     │
                   │  - Main DB       │
                   │  - PGVector      │
                   └──────────────────┘
                             │
                             │
                             ▼
                   ┌──────────────────┐
                   │      N8N         │
                   │  - Workflows     │
                   │  - AI Agents     │
                   └──────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │          External Services             │
         │  - Google APIs (Drive, Calendar)       │
         │  - Google Gemini (AI)                  │
         │  - HuggingFace (Embeddings)           │
         │  - Gmail (Notifications)               │
         └───────────────────────────────────────┘
```

---

## 14. Environment Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
MIGRATION_URL=postgresql://user:pass@host:5432/dbname

# Google OAuth 2.0
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://your-backend.com/auth/callback

# JWT Configuration
JWT_SECRET_KEY=your-secure-random-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Server
BACKEND_PORT=8080
FRONTEND_URL=https://your-frontend.vercel.app

# Environment
ENVIRONMENT=production

# N8N Integration
N8N_URL=https://your-n8n.xyz
N8N_API_KEY=your-n8n-api-key
N8N_WEBHOOK_AUTH_KEY=your-webhook-auth-key
```

### Frontend Environment Variables

```env
VITE_API_BASE_URL=https://your-backend.com
```

### Files Structure

- `backend/env.example` - Template for backend env
- `backend/.env` - Actual backend config (gitignored)
- `frontend/.env` - Frontend config (gitignored)

---

## 15. Security Considerations

### Implemented Security Measures

| Measure | Implementation |
|---------|----------------|
| **SQL Injection Prevention** | Parameterized queries in all DAOs |
| **XSS Protection** | React's built-in escaping |
| **CORS** | Configured for specific frontend origin |
| **Authentication** | OAuth 2.0 + JWT tokens |
| **Authorization** | User-scoped data access in all endpoints |
| **Secrets Management** | Environment variables (not in code) |
| **Token Expiration** | 24-hour JWT expiration |
| **Credential Refresh** | Automatic Google token refresh |

### Security Best Practices Followed

1. **No secrets in code**: All credentials via environment variables
2. **Gitignored sensitive files**: `.env`, `venv/`, `node_modules/`
3. **User isolation**: All queries include `user_id` checks
4. **Input validation**: Pydantic models validate all inputs
5. **Error handling**: Generic error messages (no stack traces to client)
6. **HTTPS**: Required for OAuth and production

### Areas for Future Enhancement

1. Consider httpOnly cookies for JWT (vs localStorage)
2. Add rate limiting for API endpoints
3. Implement CSRF protection
4. Add security headers (CSP, HSTS, etc.)
5. Consider refresh tokens for longer sessions

---

## 16. Code Style & Conventions

### Python (Backend)

- **Style Guide**: PEP 8
- **File Naming**: snake_case (`user_dao.py`)
- **Class Naming**: PascalCase (`UserDAO`)
- **Function Naming**: snake_case (`get_user_by_id`)
- **Constants**: UPPER_SNAKE_CASE (`LIFELINE_CALENDAR_NAME`)
- **Type Hints**: Used throughout for function signatures
- **Docstrings**: Triple-quoted strings for all public methods

### JavaScript/React (Frontend)

- **Style**: Modern ES6+ syntax
- **Components**: Functional components with hooks
- **File Naming**: PascalCase for components (`Header.jsx`), camelCase for utilities
- **Exports**: Default exports for components
- **State Management**: React hooks (useState, useEffect)
- **Comments**: Minimal, self-documenting code preferred

### CSS

- **File Naming**: Component-matched (`Header.css` for `Header.jsx`)
- **Naming**: BEM-like conventions where applicable
- **Variables**: CSS custom properties for theming

---

## 17. Future Considerations

### Scalability

- Database connection pooling (current: single connection per request)
- Redis caching for frequently accessed data
- CDN for static assets
- Horizontal scaling with load balancer

### Feature Enhancements

- MCP (Model Context Protocol) integration for intelligent scheduling
- Medication reminder notifications
- Multi-language support (i18n)
- Mobile application (React Native)
- Family sharing/multi-user households
- Export/import medical records

### Technical Debt

- Add SQLAlchemy ORM for more robust database layer
- Implement proper logging aggregation
- Add monitoring and alerting (Sentry, Prometheus)
- Improve test coverage (aim for 80%+)

---

*Document generated for LifeLine v1.1.0 - 12th January 2026*

