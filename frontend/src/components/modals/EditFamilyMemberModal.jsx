import React, { useState } from 'react'
import toast from 'react-hot-toast'
import { familyMembersService } from '../../services/familyMembers'
import './Modal.css'

function EditFamilyMemberModal({ member, onClose }) {
  const [formData, setFormData] = useState({
    name: member.name || '',
    date_of_birth: member.date_of_birth || '',
    gender: member.gender || '',
    profession: member.profession || '',
    health_notes: member.health_notes || '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await familyMembersService.update(member.id, {
        name: formData.name,
        date_of_birth: formData.date_of_birth || null,
        gender: formData.gender || null,
        profession: formData.profession || null,
        health_notes: formData.health_notes || null,
      })
      toast.success('Family member updated successfully!')
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update family member')
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
          <h2 className="modal-title">Edit Family Member</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}
            <div className="form-group">
              <label className="form-label">Name *</label>
              <input
                type="text"
                name="name"
                className="form-input"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Date of Birth</label>
                <input
                  type="date"
                  name="date_of_birth"
                  className="form-input"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Gender</label>
                <select
                  name="gender"
                  className="form-input"
                  value={formData.gender}
                  onChange={handleChange}
                >
                  <option value="">Select...</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Profession</label>
              <input
                type="text"
                name="profession"
                className="form-input"
                value={formData.profession}
                onChange={handleChange}
                placeholder="e.g. Teacher, Engineer, Student..."
              />
            </div>
            <div className="form-group">
              <label className="form-label">Health Notes</label>
              <textarea
                name="health_notes"
                className="form-input form-textarea"
                value={formData.health_notes}
                onChange={handleChange}
                placeholder="Any allergies, chronic conditions, or special health considerations..."
                rows={3}
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="button-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="button-primary" disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EditFamilyMemberModal
