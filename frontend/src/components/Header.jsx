import React from 'react'
import { n8nService } from '../services/n8n'
import './Header.css'

function Header({ onLogout }) {

  return (
    <header className="app-header">
      <div className="header-content">
        <h1 className="header-logo">LIFELINE</h1>
        <div className="header-actions">
          <button className="header-button logout-button" onClick={onLogout}>
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header

