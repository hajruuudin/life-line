import React, { useState } from 'react'
import toast from 'react-hot-toast'
import { medicationUsageService } from '../../services/medicationUsage'
import './Modal.css'

function LogUsageModal({ familyMembers, medications, onClose }) {
  const [formData, setFormData] = useState({
    family_member_id: '',
    medication_id: '',
    quantity_used: 1,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await medicationUsageService.logUsage({
        family_member_id: parseInt(formData.family_member_id),
        medication_id: parseInt(formData.medication_id),
        quantity_used: parseInt(formData.quantity_used),
      })
      toast.success('Medication usage logged successfully!')
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to log usage')
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

  const selectedMedication = medications.find(m => m.id === parseInt(formData.medication_id))

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Log Medication Usage</h2>
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
              <label className="form-label">Medication</label>
              <select
                name="medication_id"
                className="form-select"
                value={formData.medication_id}
                onChange={handleChange}
                required
              >
                <option value="">Select a medication</option>
                {medications.map(med => (
                  <option key={med.id} value={med.id}>
                    {med.name} (Available: {med.quantity})
                  </option>
                ))}
              </select>
            </div>
            {selectedMedication && (
              <div style={{ 
                padding: '0.75rem', 
                backgroundColor: 'var(--bg-dark)', 
                borderRadius: '0.5rem',
                marginBottom: '1rem',
                fontSize: '0.9rem',
                color: 'var(--text-secondary)'
              }}>
                Available quantity: {selectedMedication.quantity}
              </div>
            )}
            <div className="form-group">
              <label className="form-label">Quantity Used</label>
              <input
                type="number"
                name="quantity_used"
                className="form-input"
                value={formData.quantity_used}
                onChange={handleChange}
                min="1"
                max={selectedMedication?.quantity || 1}
                required
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="button-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="button-primary" disabled={loading}>
              {loading ? 'Logging...' : 'Log Usage'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default LogUsageModal

