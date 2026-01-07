import React, { useEffect, useState } from 'react'
import { authService } from '../services/auth'
import './LoginPage.css'

function LoginPage({ setIsAuthenticated }) {
  const [backgroundPosition, setBackgroundPosition] = useState('center');

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

  const handleMouseMove = (e) => {
    const { clientX, clientY } = e;
    const x = (clientX / window.innerWidth) * 1 - 10;
    const y = (clientY / window.innerHeight) * 1 - 10;
    setBackgroundPosition(`${50 + x}% ${50 + y}%`);
  };

  return (
    <div className="login-page" onMouseMove={handleMouseMove} style={{ backgroundPosition }}>
      <div className="login-container">
        <h1 className="login-logo">LIFELINE</h1>
        <p className="login-subtitle">Your family's health, organized and accessible. Track medications, appointments, and important documents with ease.</p>
        <button className="login-button" onClick={handleGoogleLogin}>
          Sign in with Google
        </button>
      </div>
    </div>
  )
}

export default LoginPage;