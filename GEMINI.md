# Project Overview: Life-Line

This document outlines the architecture and key components of the Life-Line project, which consists of a FastAPI backend and a React frontend.

## Backend (FastAPI)

The backend is built with FastAPI and follows a layered architecture, promoting separation of concerns and maintainability.

### Key Components:

*   **`main.py`**: The main entry point for the FastAPI application. It initializes the app, configures middleware, and includes all API routers.
*   **`controllers/`**: This directory contains the API endpoints, organized by resource. Each file typically defines the routes and handles incoming requests, often delegating business logic to the services layer.
    *   `auth.py`: Handles authentication-related endpoints, including Google OAuth2 callback.
    *   `family_members.py`: Manages endpoints for family member operations.
    *   `medications.py`: Manages endpoints for medication-related operations.
    *   `medication_usage.py`: Manages endpoints for tracking medication usage.
    *   `google_calendar.py` & `google_drive.py`: Controllers for Google Calendar and Drive integrations.
*   **`services/`**: This layer encapsulates the business logic. Services interact with DAOs to perform operations and coordinate between different parts of the application.
    *   `auth_service.py`: Contains the core logic for Google OAuth2 authentication, including exchanging auth codes, creating/updating users, and generating JWTs.
    *   `family_member_service.py`: Business logic for family member management.
    *   `medication_service.py`: Business logic for medication management.
    *   `medication_usage_service.py`: Business logic for medication usage tracking.
    *   `google_calendar_service.py` & `google_drive_service.py`: Services for interacting with Google Calendar and Drive APIs.
*   **`dao/` (Data Access Objects)**: This layer is responsible for direct interaction with the database. Each DAO typically handles CRUD (Create, Read, Update, Delete) operations for a specific model. The investigation indicates direct SQL interaction.
    *   `user_dao.py`: Handles database operations for user accounts.
    *   `google_credentials_dao.py`: Manages storage and retrieval of Google API credentials.
    *   `family_member_dao.py`: Handles database operations for family members.
    *   `medication_dao.py`: Handles database operations for medications.
*   **`models/`**: Defines the data models (Pydantic models for request/response validation and SQLAlchemy models for database schema).
*   **`utils/`**: Contains utility functions and dependencies.
    *   `dependencies.py`: Defines dependencies used across the application, notably `get_current_user` for authentication and authorization.
    *   `jwt.py`: Handles JSON Web Token (JWT) creation and validation.
    *   `database.py`: Database connection and session management.
    *   `config.py`: Application configuration settings.

### Authentication Flow:

The application uses Google OAuth2 for authentication. The general flow is:
1.  Frontend initiates Google OAuth2 login.
2.  Google redirects back to a backend endpoint (`auth.py`).
3.  The backend (`auth_service.py`) exchanges the Google auth code for user information and Google API credentials.
4.  A local user record is created or updated in the database (`user_dao.py`, `google_credentials_dao.py`).
5.  The backend issues its own JWT to the frontend for securing subsequent API calls.
6.  API endpoints are protected using `get_current_user` dependency (`dependencies.py`), which validates the JWT and retrieves the authenticated user.

## Frontend (React)

The frontend is a React application. While a detailed analysis was not completed, the structure suggests a typical React application setup.

### Key Components (Hypothesized based on structure):

*   **`src/App.jsx`**: The main application component.
*   **`src/main.jsx`**: Entry point for the React application.
*   **`src/pages/`**: Contains different pages of the application.
    *   `HomePage.jsx`
    *   `LoginPage.jsx`
    *   `GoogleCallbackPage.jsx`: Likely handles the redirect after Google OAuth2 authentication.
*   **`src/components/`**: Reusable UI components.
    *   `ActionGrid.jsx`, `DataDashboard.jsx`, `DriveSection.jsx`, `Header.jsx`, `Hero.jsx`, `InventoryTable.jsx`.
    *   `modals/`: Contains various modal components (e.g., `FamilyMemberModal.jsx`, `InventoryModal.jsx`, `LogUsageModal.jsx`, `ScheduleEventModal.jsx`).
*   **`src/services/`**: This directory is crucial for understanding frontend-backend interaction. It is expected to contain modules for making API calls to the FastAPI backend.
    *   `api.js`: Likely a central place for API configurations or an Axios/fetch instance.
    *   `auth.js`: Handles authentication-related API calls (e.g., login, token refresh).
    *   `familyMembers.js`, `googleCalendar.js`, `googleDrive.js`, `medications.js`, `medicationUsage.js`: Modules for interacting with respective backend services.
*   **`src/utils/`**: Utility functions for the frontend.
    *   `auth.util.js`: Likely contains client-side authentication utilities.

## Shared Elements and Configuration

*   **`.env` / `env.example`**: Environment variable configurations for both backend and frontend.
*   **`requirements.txt`**: Python dependencies for the backend.
*   **`package.json`**: Node.js dependencies for the frontend.
*   **`database/database_schema.sql`**: Defines the relational database schema used by the backend.

This overview provides a foundational understanding of the Life-Line project's architecture. Further investigation into the frontend components and their interaction with the backend would provide a more complete picture.
