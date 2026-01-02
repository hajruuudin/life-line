-- LifeLine Database Schema
-- PostgreSQL Database Schema for Family Health Tracking Application
-- No triggers or functions used

-- Users table: Stores parent account information and OAuth data
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    google_id VARCHAR(255) UNIQUE,
    google_oauth_token TEXT,
    google_refresh_token TEXT,
    drive_folder_id VARCHAR(255),
    api_key TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Family members table: Linked to parent user
CREATE TABLE IF NOT EXISTS family_members (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Medications table: Inventory items
CREATE TABLE IF NOT EXISTS medications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    expiration_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Medication usage table: Logs linked to family members and medications
CREATE TABLE IF NOT EXISTS medication_usage (
    id SERIAL PRIMARY KEY,
    family_member_id INTEGER NOT NULL REFERENCES family_members(id) ON DELETE CASCADE,
    medication_id INTEGER NOT NULL REFERENCES medications(id) ON DELETE CASCADE,
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity_used INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Google credentials table: Stores OAuth tokens for Drive/Calendar integrations
CREATE TABLE IF NOT EXISTS user_google_credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    token_expiry TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_family_members_user_id ON family_members(user_id);
CREATE INDEX IF NOT EXISTS idx_medications_user_id ON medications(user_id);
CREATE INDEX IF NOT EXISTS idx_medication_usage_family_member_id ON medication_usage(family_member_id);
CREATE INDEX IF NOT EXISTS idx_medication_usage_medication_id ON medication_usage(medication_id);
CREATE INDEX IF NOT EXISTS idx_user_google_credentials_user_id ON user_google_credentials(user_id);

