import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
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
