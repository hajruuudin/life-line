import React from 'react'
import { FiCalendar, FiClock, FiMapPin, FiFileText, FiExternalLink } from 'react-icons/fi'
import './Modal.css'

function EventDetailModal({ event, onClose }) {
  const formatDateTime = (dateTimeObj) => {
    if (!dateTimeObj) return 'Not specified'
    
    const dateStr = dateTimeObj.dateTime || dateTimeObj.date
    if (!dateStr) return 'Not specified'
    
    // All-day event
    if (dateTimeObj.date && !dateTimeObj.dateTime) {
      const date = new Date(dateStr + 'T00:00:00')
      return date.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      }) + ' (All day)'
    }
    
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }

  const handleOpenInCalendar = () => {
    if (event.htmlLink) {
      window.open(event.htmlLink, '_blank', 'noopener,noreferrer')
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content event-detail-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-container">
            <span className="modal-icon"><FiCalendar /></span>
            <h2 className="modal-title">Event Details</h2>
          </div>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="modal-body event-detail-body">
          <div className="event-detail-title">
            {event.summary || 'Untitled Event'}
          </div>
          
          <div className="event-detail-row">
            <FiClock className="event-detail-icon" />
            <div className="event-detail-content">
              <span className="event-detail-label">Start</span>
              <span className="event-detail-value">{formatDateTime(event.start)}</span>
            </div>
          </div>
          
          <div className="event-detail-row">
            <FiClock className="event-detail-icon" />
            <div className="event-detail-content">
              <span className="event-detail-label">End</span>
              <span className="event-detail-value">{formatDateTime(event.end)}</span>
            </div>
          </div>
          
          {event.location && (
            <div className="event-detail-row">
              <FiMapPin className="event-detail-icon" />
              <div className="event-detail-content">
                <span className="event-detail-label">Location</span>
                <span className="event-detail-value">{event.location}</span>
              </div>
            </div>
          )}
          
          {event.description && (
            <div className="event-detail-row">
              <FiFileText className="event-detail-icon" />
              <div className="event-detail-content">
                <span className="event-detail-label">Description</span>
                <span className="event-detail-value description">{event.description}</span>
              </div>
            </div>
          )}
        </div>
        
        <div className="modal-footer">
          <button className="button-secondary" onClick={onClose}>
            Close
          </button>
          {event.htmlLink && (
            <button className="button-primary" onClick={handleOpenInCalendar}>
              <FiExternalLink style={{ marginRight: '0.5rem' }} />
              Open in Calendar
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default EventDetailModal
