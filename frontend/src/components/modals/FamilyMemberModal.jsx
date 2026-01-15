import React, { useState } from 'react'
import toast from 'react-hot-toast'
import { familyMembersService } from '../../services/familyMembers'
import './Modal.css'

function FamilyMemberModal({ onClose }) {
  const [formData, setFormData] = useState({
    name: '',
    date_of_birth: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await familyMembersService.create({
        name: formData.name,
        date_of_birth: formData.date_of_birth || null,
      })
      toast.success('Family member added successfully!')
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add family member')
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
          <h2 className="modal-title">Add Family Member</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}
            <div className="form-group">
              <label className="form-label">Name</label>
              <input
                type="text"
                name="name"
                className="form-input"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Date of Birth (Optional)</label>
              <input
                type="date"
                name="date_of_birth"
                className="form-input"
                value={formData.date_of_birth}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="button-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="button-primary" disabled={loading}>
              {loading ? 'Adding...' : 'Add Member'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default FamilyMemberModal

