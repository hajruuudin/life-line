# LifeLine - Family Health Tracking Application

A comprehensive web application for tracking family health, managing medication inventory, and organizing health records. Built with React 19 and FastAPI, featuring Google OAuth authentication and Google Drive/Calendar integration.

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **Node.js 18+** and npm
- **PostgreSQL 12+**
- **Google Cloud Console Account** (for OAuth credentials)

### Installation

1. **Clone the repository**
   ```bash
   cd life-line
   ```

2. **Set up the database**
   ```bash
   # Create database
   createdb lifeline

   # Run schema
   psql lifeline < database/database_schema.sql
   ```

3. **Backend Setup**
   ```bash
   cd backend

   # Create virtual environment
   python3.13 -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Create .env file (copy from env.example template in backend directory)
   # Create backend/.env file with the following variables:
   # DATABASE_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, JWT_SECRET_KEY, etc.
   # See Environment Variables section below for full list
   ```

4. **Frontend Setup**
   ```bash
   cd frontend

   # Install dependencies
   npm install

   # Copy environment variables template
   cp .env.example .env

   # Edit .env with your backend URL (if different from default)
   ```

5. **Configure Google OAuth**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google+ API, Google Drive API, and Google Calendar API
   - Create OAuth 2.0 credentials (Web application)
   - Add authorized redirect URI: `http://localhost:8080/auth/google/callback`
   - Copy Client ID and Client Secret to backend `.env`

### Running the Application

1. **Start the backend** (from `backend/` directory)
   ```bash
   uvicorn app.main:app --reload --port 8080
   ```
   Backend will be available at: http://localhost:8080
   API Documentation: http://localhost:8080/docs

2. **Start the frontend** (from `frontend/` directory)
   ```bash
   npm run dev
   ```
   Frontend will be available at: http://localhost:4200

3. **Access the application**
   - Open http://localhost:4200 in your browser
   - Click "Sign in with Google"
   - Complete OAuth flow
   - Start using LifeLine!

## 📁 Project Structure

```
life-line/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── controllers/    # API route handlers
│   │   ├── services/       # Business logic layer
│   │   ├── dao/            # Data access objects
│   │   ├── models/         # Pydantic DTOs
│   │   ├── utils/          # Utilities (JWT, dependencies)
│   │   ├── config.py       # Configuration settings
│   │   ├── database.py     # Database connection
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   ├── styles/         # CSS styles
│   │   ├── App.jsx         # Root component
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node dependencies
│   └── .env.example        # Environment variables template
├── database/
│   └── database_schema.sql # Database schema
├── PROJECT_INFRASTRUCTURE.md # Architecture documentation
└── README.md               # This file
```

## 🎯 Features

### Core Features
- ✅ Google OAuth 2.0 authentication
- ✅ Family member management
- ✅ Medication inventory tracking
- ✅ Medication usage logging
- ✅ Google Drive file listing
- ✅ PDF upload to Google Drive
- ✅ Google Calendar event scheduling

### UI Features
- ✅ Dark mode with Cyan-Blue color palette
- ✅ Responsive design (mobile-friendly)
- ✅ Modal-based forms
- ✅ Real-time inventory updates
- ✅ Empty state handling

## 🔌 API Endpoints

### Authentication
- `GET /auth/google-login` - Get Google OAuth URL
- `GET /auth/callback` or `GET /auth/google/callback` - Handle OAuth callback (redirects to frontend)

### Family Members
- `GET /family-members` - List all family members
- `POST /family-members` - Create family member
- `GET /family-members/{id}` - Get specific member
- `PUT /family-members/{id}` - Update member
- `DELETE /family-members/{id}` - Delete member

### Medications
- `GET /medications` - List all medications
- `POST /medications` - Create/update medication (increments quantity if exists)
- `GET /medications/{id}` - Get specific medication
- `PUT /medications/{id}` - Update medication
- `DELETE /medications/{id}` - Delete medication

### Medication Usage
- `POST /medication-usage` - Log medication usage
- `GET /medication-usage` - List usage logs

### Google Drive
- `GET /drive/files` - List Drive files
- `POST /drive/upload` - Upload PDF to Drive

### Google Calendar
- `POST /calendar/events` - Create calendar event

See full API documentation at http://localhost:8080/docs (when backend is running)

## 🛠️ Technology Stack

### Backend
- **Python 3.13**
- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Google APIs** - Drive and Calendar integration

### Frontend
- **React 19** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client

## 🔮 Future Integrations

The codebase includes structured placeholders for future integrations:

### N8N Workflow Automation
- **Location**: `backend/app/services/google_calendar_service.py`
- **Purpose**: Trigger automated workflows for medication reminders and health tracking
- **Implementation**: Add webhook calls to N8N server after event creation

### RAG (Retrieval-Augmented Generation)
- **Location**: `backend/app/services/google_drive_service.py`
- **Purpose**: Extract text from PDFs, generate embeddings, enable semantic search
- **Implementation**: 
  1. Add PDF text extraction library
  2. Integrate vector database (Pinecone, Weaviate, Chroma)
  3. Generate embeddings (OpenAI, HuggingFace)
  4. Create search/query endpoints

### MCP (Model Context Protocol)
- **Location**: `backend/app/services/google_calendar_service.py`
- **Purpose**: Intelligent event scheduling and medication reminders
- **Implementation**: 
  1. Set up MCP server
  2. Integrate MCP client
  3. Use for smart scheduling suggestions

See `PROJECT_INFRASTRUCTURE.md` for detailed integration guidelines.

## 🔐 Security Notes

- JWT tokens stored in localStorage (consider httpOnly cookies for production)
- SQL injection prevented via parameterized queries
- CORS configured for specific origins
- Environment variables for all secrets
- Never commit `.env` files

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/lifeline
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_PORT=8080
FRONTEND_URL=http://localhost:4200
ENVIRONMENT=development
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8080
```

## 🐛 Troubleshooting

### Backend Issues

1. **Database connection error**
   - Verify PostgreSQL is running
   - Check `DATABASE_URL` in `.env`
   - Ensure database `lifeline` exists

2. **OAuth errors**
   - Verify Google Cloud Console credentials
   - Check redirect URI matches exactly
   - Ensure APIs are enabled (Drive, Calendar)

3. **Import errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again

### Frontend Issues

1. **API connection error**
   - Verify backend is running on port 8080
   - Check `VITE_API_BASE_URL` in `.env`
   - Check browser console for CORS errors

2. **Build errors**
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

## 📄 License

This project is private and proprietary.

## 👥 Contributing

This is a private project. For questions or issues, contact the development team.

## 📚 Additional Documentation

- [PROJECT_INFRASTRUCTURE.md](./PROJECT_INFRASTRUCTURE.md) - Detailed architecture and design decisions
- API Documentation: http://localhost:8080/docs (when backend is running)

