import React, { useState } from 'react'
import { medicationsService } from '../../services/medications'
import './Modal.css'

function InventoryModal({ onClose }) {
  const [formData, setFormData] = useState({
    name: '',
    quantity: 1,
    expiration_date: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await medicationsService.create({
        name: formData.name,
        quantity: parseInt(formData.quantity),
        expiration_date: formData.expiration_date || null,
      })
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add medication')
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
          <h2 className="modal-title">Add/Update Inventory</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}
            <div className="form-group">
              <label className="form-label">Medication Name</label>
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
              <label className="form-label">Quantity</label>
              <input
                type="number"
                name="quantity"
                className="form-input"
                value={formData.quantity}
                onChange={handleChange}
                min="1"
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Expiration Date (Optional)</label>
              <input
                type="date"
                name="expiration_date"
                className="form-input"
                value={formData.expiration_date}
                onChange={handleChange}
              />
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" className="button-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="button-primary" disabled={loading}>
              {loading ? 'Adding...' : 'Add Medication'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default InventoryModal

