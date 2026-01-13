![Screenshot](./docs/images/banner.png)

# LifeLine
**Family Health Tracking Application**

LifeLine is a comprehensive web application designed to help families manage their health. Track medications, log illnesses, store medical documents, schedule appointments, and get AI-powered medical assistance—all in one place.

## 🌐 Live Deployment

**A fully deployed version of LifeLine is available as of January 12th, 2026.** `https://life-line-flax.vercel.app`


## ✨ What is LifeLine?

LifeLine helps you:

| Feature | Description |
|---------|-------------|
| 👨‍👩‍👧‍👦 **Family Members** | Add and manage health profiles for your entire family |
| 💊 **Medication Inventory** | Track medications, quantities, and expiration dates |
| 📝 **Usage Logging** | Record when medications are taken and by whom |
| 🤒 **Illness Timeline** | Keep a history of illnesses for each family member |
| 📁 **Medical Documents** | Upload and store prescriptions, lab results, etc. to Google Drive |
| 📅 **Appointments** | Schedule medical events on a dedicated Google Calendar |
| 🤖 **AI Assistant** | Chat with an AI that knows your medical history (RAG-powered) |
| 📧 **Email Summaries** | Receive AI-generated summaries when uploading documents |

## 🏗️ Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  PostgreSQL │
│   (React)   │     │  (FastAPI)  │     │  (Supabase) │
│   Vercel    │     │   Docker    │     │             │
└─────────────┘     └──────┬──────┘     └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │     N8N     │
                   │ (Automation)│
                   └──────┬──────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
      ┌──────────┐ ┌──────────┐ ┌──────────┐
      │  Gemini  │ │  Gmail   │ │ PGVector │
      │   (AI)   │ │ (Email)  │ │  (RAG)   │
      └──────────┘ └──────────┘ └──────────┘
```

**Tech Stack:**
- **Frontend**: React 19, Vite, React Router 7
- **Backend**: Python 3.11, FastAPI, Pydantic
- **Database**: PostgreSQL with PGVector extension
- **Auth**: Google OAuth 2.0 + JWT
- **Integrations**: Google Drive, Google Calendar, N8N, Gemini AI

For detailed architecture documentation, see [PROJECT_INFRASTRUCTURE.md](./PROJECT_INFRASTRUCTURE.md).

## 🚀 Self-Hosting Guide

Want to run LifeLine yourself? Follow these steps to deploy all components. It's a bit of a process, so take your time

### Prerequisites

- **Docker** and **Docker Compose** (for containerized deployment)
- **Node.js 18+** and npm (for frontend development)
- **Python 3.11+** (for backend development)
- **PostgreSQL 14+** with PGVector extension
- **Google Cloud Console** account (for OAuth and APIs)
- **N8N instance** (self-hosted or cloud)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd life-line
```

### Step 2: Set Up PostgreSQL Database

You can use a local PostgreSQL instance or a cloud provider like Supabase.

**Option A: Local PostgreSQL**
```bash
# Create database
createdb lifeline

# Enable PGVector extension (required for AI features)
psql lifeline -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Run initial migration
cd backend
alembic upgrade head
```

**Option B: Supabase (Recommended for production)**
1. Create a new project at [supabase.com](https://supabase.com)
2. Enable the Vector extension in Database → Extensions
3. Copy the connection string for later use

### Step 3: Configure Google Cloud

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable these APIs:
   - Google+ API
   - Google Drive API
   - Google Calendar API
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure the OAuth consent screen
6. Add authorized redirect URIs:
   - Development: `http://localhost:8080/auth/callback`
   - Production: `https://your-backend-domain.com/auth/callback`
7. Save your **Client ID** and **Client Secret**

### Step 4: Set Up the Backend

```bash
cd backend

# Create environment file
cp env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lifeline

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/callback

# JWT (generate a secure random string)
JWT_SECRET_KEY=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Server
BACKEND_PORT=8080
FRONTEND_URL=http://localhost:4200
ENVIRONMENT=development

# N8N Integration
N8N_URL=https://your-n8n-instance.com
N8N_API_KEY=your-n8n-api-key
N8N_WEBHOOK_AUTH_KEY=your-webhook-secret
```

**Run locally (development):**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8080
```

**Run with Docker (production):**
```bash
# Build the image
docker build -t lifeline-backend .

# Run the container
docker run -d \
  --name lifeline-backend \
  -p 8080:8080 \
  --env-file .env \
  lifeline-backend
```

The API will be available at `http://localhost:8080` with documentation at `/docs`.

### Step 5: Set Up the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_BASE_URL=http://localhost:8080" > .env
```

**Run locally (development):**
```bash
npm run dev
```

The frontend will be available at `http://localhost:4200`.

**Build for production:**
```bash
npm run build
```

The built files will be in `frontend/dist/`. Deploy to Vercel, Netlify, or any static hosting:

**Deploy to Vercel:**
```bash
npm install -g vercel
vercel --prod
```

### Step 6: Set Up N8N (AI & Automation)

N8N powers the AI chatbot and email automation features. This is optional as the main functions of the application can run without this. if You opt not to use this, please either comment out or remove the applications implementation of the Chatbot Widget, as it might break the UI.

**Option A: Self-hosted with Docker**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=your-password \
  n8nio/n8n
```

**Option B: N8N Cloud**
Sign up at [n8n.io](https://n8n.io) for a managed instance.

**Import the workflow:**
1. Open your N8N instance
2. Go to **Workflows** → **Import from File**
3. Import `n8n-script/n8n-workflow.json`
4. Configure credentials:
   - **PostgreSQL**: Your database connection (for PGVector and chat memory)
   - **Gmail OAuth2**: For sending email summaries
   - **Google Gemini API**: For AI responses
   - **HuggingFace API**: For text embeddings

**N8N Workflow Features:**
- 📄 **Document Summary**: When files are uploaded, AI summarizes them and emails you
- 🧠 **RAG Chatbot**: AI assistant with access to your uploaded medical documents
- 💬 **Chat Memory**: Conversation history stored in PostgreSQL

### Step 7: Verify Everything Works

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8080/health
   # Should return: {"status": "healthy"}
   ```

2. **Frontend Access:**
   - Open `http://localhost:4200`
   - Click "Sign in with Google"
   - Complete OAuth flow

3. **Test Features:**
   - Add a family member
   - Add a medication
   - Upload a PDF document (triggers N8N workflow)
   - Try the AI chatbot

## 📁 Project Structure

```
life-line/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── controllers/        # API endpoints
│   │   ├── services/           # Business logic
│   │   ├── dao/                # Database access
│   │   ├── models/             # Pydantic schemas
│   │   └── utils/              # JWT, auth helpers
│   ├── alembic/                # Database migrations
│   ├── tests/                  # Unit tests
│   ├── Dockerfile              # Container config
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── pages/              # Route pages
│   │   ├── services/           # API client
│   │   └── __tests__/          # Component tests
│   ├── tests/                  # E2E tests (Playwright)
│   └── package.json            # Node dependencies
├── database/                   # Schema exports
├── n8n-script/                 # N8N workflow JSON
├── PROJECT_INFRASTRUCTURE.md   # Detailed architecture docs
└── README.md                   # This file
```

## 🔧 Environment Variables Reference

### Backend

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `GOOGLE_CLIENT_ID` | OAuth client ID | `xxx.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret | `GOCSPX-xxx` |
| `GOOGLE_REDIRECT_URI` | OAuth callback URL | `http://localhost:8080/auth/callback` |
| `JWT_SECRET_KEY` | Secret for signing tokens | Random 32+ char string |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `1440` (24 hours) |
| `FRONTEND_URL` | Frontend origin for CORS | `http://localhost:4200` |
| `N8N_URL` | N8N instance URL | `https://your-n8n.com` |
| `N8N_WEBHOOK_AUTH_KEY` | Webhook authentication | Random secret string |

### Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8080` |

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **OAuth redirect mismatch** | Ensure `GOOGLE_REDIRECT_URI` exactly matches Google Console config |
| **CORS errors** | Check `FRONTEND_URL` in backend `.env` matches actual frontend URL |
| **Database connection failed** | Verify PostgreSQL is running and `DATABASE_URL` is correct |
| **N8N webhook not triggering** | Check `N8N_URL` and `N8N_WEBHOOK_AUTH_KEY` are set correctly |
| **AI chatbot not responding** | Verify N8N workflow is active and credentials are configured |
| **Drive/Calendar not working** | Re-authenticate with Google (tokens may have expired) |

## 📚 Additional Documentation

- **[PROJECT_INFRASTRUCTURE.md](./PROJECT_INFRASTRUCTURE.md)** - Complete technical documentation including:
  - Detailed architecture diagrams
  - Database schema and relationships
  - API endpoint reference
  - Authentication flow
  - N8N workflow details
  - Testing strategy
  - Security considerations

- **API Documentation** - Available at `/docs` when backend is running (Swagger UI)
- **SRS Document** - https://docs.google.com/document/d/1Y_vGDxNaCAM6ZdlmlKZ-lFoHUWJWYMwTbfI3h4AU8iA/edit?usp=sharing
- **Prompts used for development** - https://docs.google.com/document/d/1_WHQp4J4ivLqGYCMGuSkqnQN0PX_OjrCJtQgFTI6OUw/edit?usp=sharing

## 📄 License

This project is open source and available under the [MIT License](./LICENSE).


