import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { Toaster } from "react-hot-toast";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import GoogleCallbackPage from "./pages/GoogleCallbackPage";
import { auth } from "../src/utils/auth.util";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(auth.isAuthenticated())

  useEffect(() => {
    // Check localStorage on mount
    const authenticated = auth.isAuthenticated()
    setIsAuthenticated(authenticated)

    // Listen for storage changes (updates from other tabs or same tab)
    const handleStorageChange = () => {
      const authenticated = auth.isAuthenticated()
      setIsAuthenticated(authenticated)
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [])

  return (
    <Router>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'var(--bg-card)',
            color: 'var(--text-primary)',
            border: '1px solid var(--border-color)',
            borderRadius: '8px',
            padding: '12px 16px',
          },
          success: {
            iconTheme: {
              primary: 'var(--success)',
              secondary: 'var(--bg-card)',
            },
          },
          error: {
            iconTheme: {
              primary: 'var(--error)',
              secondary: 'var(--bg-card)',
            },
          },
        }}
      />
      <Routes>
        <Route path="/auth/google/callback" element={<GoogleCallbackPage />} />

        <Route
          path="/login"
          element={
            isAuthenticated
              ? <Navigate to="/" replace />
              : <LoginPage />
          }
        />

        <Route
          path="/"
          element={
            isAuthenticated
              ? <HomePage setIsAuthenticated={setIsAuthenticated} />
              : <Navigate to="/login" replace />
          }
        />
      </Routes>
    </Router>
  )
}


export default App;
