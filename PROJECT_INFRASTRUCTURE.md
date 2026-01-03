# LifeLine - Project Infrastructure

## Overview

LifeLine is a family health tracking web application built as a monolithic repository (Monorepo) with a clear separation between frontend and backend. The architecture follows strict layering principles to ensure maintainability and scalability.

## Architecture

### Backend Architecture

The backend follows a **Layered Architecture** pattern:

```
Controller (Routers) → Service Layer (Business Logic) → DAO (Data Access) → Database
```

#### Layer Breakdown:

1. **Controllers (`app/controllers/`)**
   - FastAPI routers that handle HTTP requests/responses
   - Validate request data using Pydantic models
   - Call appropriate service methods
   - Handle authentication via JWT dependency injection

2. **Services (`app/services/`)**
   - Contains all business logic
   - Coordinates between multiple DAOs when needed
   - Handles complex operations (e.g., logging usage decrements inventory)
   - Contains TODO markers for future AI/Automation integrations

3. **DAO Layer (`app/dao/`)**
   - Data Access Objects for database operations
   - Pure SQL queries using psycopg2
   - No business logic, only data access
   - Returns dictionaries (not Pydantic models)

4. **Models (`app/models/`)**
   - Pydantic models for request/response validation
   - DTOs (Data Transfer Objects)
   - Type-safe data structures

5. **Utilities (`app/utils/`)**
   - JWT token creation and verification
   - FastAPI dependencies for authentication
   - Shared utility functions

### Frontend Architecture

The frontend follows a **Component-Based Architecture**:

```
Pages → Components → Services → API
```

#### Structure:

1. **Pages (`src/pages/`)**
   - Route-level components
   - Manage state and data loading
   - Compose multiple components

2. **Components (`src/components/`)**
   - Reusable UI components
   - Stateless or minimal state
   - Styled with CSS modules

3. **Services (`src/services/`)**
   - API communication layer
   - Axios-based HTTP client
   - Handles authentication tokens

4. **Styles (`src/styles/`)**
   - Global CSS variables (Cyan-Blue palette, Dark Mode)
   - Component-specific CSS files

## Database Schema

The database uses PostgreSQL with the following tables:

- **users**: Parent account information and OAuth data
- **family_members**: Family members linked to parent user
- **medications**: Medication inventory items
- **medication_usage**: Usage logs linking members to medications
- **user_google_credentials**: Google OAuth tokens for Drive/Calendar

All tables include `created_at` and `updated_at` timestamps. Foreign keys use `ON DELETE CASCADE` to maintain referential integrity.

## Authentication Flow

1. User clicks "Sign in with Google" on frontend
2. Frontend calls `/auth/google-login` to get authorization URL
3. User redirected to Google OAuth consent screen
4. Google redirects to `/auth/google/callback` (GET request) with authorization code
5. Backend exchanges code for tokens and user info
6. Backend creates/updates user in database
7. Backend stores Google credentials for Drive/Calendar access
8. Backend generates JWT token
9. Backend redirects to frontend with JWT token in URL hash
10. Frontend extracts token from URL and stores in localStorage
11. All subsequent requests include JWT in Authorization header

## Future Integration Points

### N8N Integration

**Location**: `backend/app/services/google_calendar_service.py`

The `create_event` method contains TODO markers for N8N workflow triggers. To integrate:

1. Install N8N SDK or use HTTP webhooks
2. Add environment variables for N8N webhook URLs
3. Trigger workflows after calendar event creation
4. Support bidirectional sync (N8N → LifeLine)

### RAG (Retrieval-Augmented Generation) Integration

**Locations**: 
- `backend/app/services/google_drive_service.py` (list_files, upload_pdf methods)
- Future: `backend/app/services/rag_service.py` (to be created)

To integrate RAG:

1. Install vector database (e.g., Pinecone, Weaviate, or local Chroma)
2. Add PDF text extraction (e.g., PyPDF2, pdfplumber)
3. Implement text chunking strategy
4. Generate embeddings (e.g., OpenAI, HuggingFace)
5. Store embeddings with metadata
6. Create search endpoint for semantic queries
7. Integrate with LLM for question-answering over documents

### MCP (Model Context Protocol) Integration

**Location**: `backend/app/services/google_calendar_service.py`

The calendar service contains TODO markers for MCP server integration. To integrate:

1. Set up MCP server (separate service or embedded)
2. Add MCP client library
3. Use MCP for intelligent event scheduling suggestions
4. Support medication reminder automation via MCP
5. Add environment variables for MCP server configuration

## Environment Variables

All configuration is externalized via environment variables:

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret
- `GOOGLE_REDIRECT_URI`: OAuth callback URL
- `JWT_SECRET_KEY`: Secret for JWT token signing
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `BACKEND_PORT`: Server port (default: 8080)
- `FRONTEND_URL`: Frontend URL for CORS
- `ENVIRONMENT`: Deployment environment

### Frontend (.env)
- `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:8080)

## Dependency Management

### Backend
- Python 3.13 compatible packages
- FastAPI 0.115.6+ (OpenAPI/Swagger auto-generation)
- PostgreSQL via psycopg2-binary
- Google APIs via google-api-python-client

### Frontend
- React 19.0.0
- Vite 6.0+ for build tooling
- React Router v7 for routing
- Axios for HTTP requests

## Deployment Considerations

1. **Database**: Ensure PostgreSQL is running and accessible
2. **Environment Variables**: Set all required variables in production
3. **CORS**: Update `FRONTEND_URL` to production frontend URL
4. **Google OAuth**: Update redirect URIs in Google Cloud Console
5. **JWT Secret**: Use strong, randomly generated secret in production
6. **HTTPS**: Use HTTPS in production for OAuth and JWT security

## Development Workflow

1. **Backend**: 
   - Create virtual environment: `python -m venv venv`
   - Activate: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
   - Install: `pip install -r requirements.txt`
   - Run: `uvicorn app.main:app --reload --port 8080`

2. **Frontend**:
   - Install: `npm install`
   - Run: `npm run dev` (starts on port 4200)

3. **Database**:
   - Create database: `createdb lifeline`
   - Run schema: `psql lifeline < database/database_schema.sql`

## Code Style & Conventions

- **Python**: PEP 8 style guide
- **JavaScript**: Modern ES6+ syntax, functional components with hooks
- **Naming**: 
  - Files: snake_case (Python), PascalCase (React components), camelCase (JavaScript utilities)
  - Classes: PascalCase
  - Functions/Methods: snake_case (Python), camelCase (JavaScript)
- **Type Safety**: Pydantic models for backend, PropTypes (optional) for frontend

## Testing Strategy (Future)

- **Backend**: pytest with FastAPI TestClient
- **Frontend**: Jest + React Testing Library
- **Integration**: End-to-end tests with Playwright or Cypress

## Security Considerations

1. **JWT Tokens**: Stored in localStorage (consider httpOnly cookies for production)
2. **SQL Injection**: Prevented via parameterized queries in DAO layer
3. **XSS**: React's built-in XSS protection
4. **CORS**: Configured for specific origins
5. **OAuth**: Follows OAuth 2.0 best practices
6. **Secrets**: Never commit .env files, use environment variables

## Scalability Considerations

1. **Database**: Add connection pooling (e.g., SQLAlchemy pool)
2. **Caching**: Add Redis for session/token caching
3. **CDN**: Serve static assets via CDN
4. **Load Balancing**: Use reverse proxy (nginx) for multiple backend instances
5. **Monitoring**: Add logging, metrics, and error tracking (e.g., Sentry)

