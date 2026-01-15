import React, { useState } from 'react'
import toast from 'react-hot-toast'
import { illnessLogsService } from '../../services/illnessLogs'
import './Modal.css'

function IllnessLogModal({ familyMembers, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    family_member_id: '',
    illness_name: '',
    start_date: '',
    end_date: '',
    notes: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await illnessLogsService.create({
        family_member_id: parseInt(formData.family_member_id),
        illness_name: formData.illness_name,
        start_date: formData.start_date,
        end_date: formData.end_date || null,
        notes: formData.notes || null,
      })
      toast.success('Illness logged successfully!')
      if (onSuccess) onSuccess()
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to log illness')
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
          <h2 className="modal-title">Log Illness</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}
            <div className="form-group">
              <label className="form-label">Family Member</label>
              <select
                name="family_member_id"
                className="form-select"
                value={formData.family_member_id}
                onChange={handleChange}
                required
              >
                <option value="">Select a family member</option>
                {familyMembers.map(member => (
                  <option key={member.id} value={member.id}>{member.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Illness Name</label>
              <input
                type="text"
                name="illness_name"
                className="form-input"
                value={formData.illness_name}
                onChange={handleChange}
                placeholder="e.g., Flu, Cold, Fever"
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Start Date</label>
              <input
                type="date"
                name="start_date"
                className="form-input"
                value={formData.start_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">End Date (Optional)</label>
              <input
                type="date"
                name="end_date"
                className="form-input"
                value={formData.end_date}
                onChange={handleChange}
                min={formData.start_date}
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                Leave empty if still ongoing
              </small>
            </div>
            <div className="form-group">
              <label className="form-label">Notes (Optional)</label>
              <textarea
                name="notes"
                className="form-textarea"
                value={formData.notes}
                onChange={handleChange}
                placeholder="Any additional details..."
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="button-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="button-primary" disabled={loading}>
              {loading ? 'Logging...' : 'Log Illness'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default IllnessLogModal
