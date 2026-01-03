import React, { useEffect } from 'react'
import { authService } from '../services/auth'
import './LoginPage.css'

function LoginPage({ setIsAuthenticated }) {
  useEffect(() => {
    // Check for error messages from OAuth flow
    const urlParams = new URLSearchParams(window.location.search)
    const error = urlParams.get('error')
    
    if (error) {
      alert(`Authentication failed: ${error}`)
      window.history.replaceState({}, document.title, '/login')
    }
  }, [])

  const handleGoogleLogin = async () => {
    try {
      const authUrl = await authService.getGoogleAuthUrl()
      window.location.href = authUrl
    } catch (error) {
      // Login error - user will see alert
    }
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <h1 className="login-logo">LIFELINE</h1>
        <p className="login-subtitle">Family Health Tracking</p>
        <button className="login-button" onClick={handleGoogleLogin}>
          Sign in with Google
        </button>
      </div>
    </div>
  )
}

export default LoginPage;
