import React, { useState } from 'react'
import { googleCalendarService } from '../../services/googleCalendar'
import './Modal.css'

function ScheduleEventModal({ onClose }) {
  const [formData, setFormData] = useState({
    summary: '',
    start_time: '',
    end_time: '',
    description: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await googleCalendarService.createEvent({
        summary: formData.summary,
        start_time: new Date(formData.start_time).toISOString(),
        end_time: new Date(formData.end_time).toISOString(),
        description: formData.description,
      })
      alert('Event scheduled successfully!')
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to schedule event')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Schedule Event</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}
            <div className="form-group">
              <label className="form-label">Event Title</label>
              <input
                type="text"
                name="summary"
                className="form-input"
                value={formData.summary}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Start Time</label>
              <input
                type="datetime-local"
                name="start_time"
                className="form-input"
                value={formData.start_time}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">End Time</label>
              <input
                type="datetime-local"
                name="end_time"
                className="form-input"
                value={formData.end_time}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Description (Optional)</label>
              <textarea
                name="description"
                className="form-textarea"
                value={formData.description}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="button-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="button-primary" disabled={loading}>
              {loading ? 'Scheduling...' : 'Schedule Event'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ScheduleEventModal

