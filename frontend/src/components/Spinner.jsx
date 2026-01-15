import React from 'react'
import './Spinner.css'

function Spinner({ message = 'Loading...' }) {
  return (
    <div className="spinner-overlay">
      <div className="spinner-container">
        <div className="spinner"></div>
        <p className="spinner-message">{message}</p>
      </div>
    </div>
  )
}

export default Spinner
