import React, { useState } from 'react'
import { medicationsService } from '../services/medications'
import InventoryModal from './modals/InventoryModal'
import './InventoryTable.css'

function InventoryTable({ medications, onDataChange }) {
  const [showModal, setShowModal] = useState(false)
  const [deleting, setDeleting] = useState(null)

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this medication?')) {
      return
    }

    setDeleting(id)
    try {
      await medicationsService.delete(id)
      onDataChange()
    } catch (error) {
      alert('Failed to delete medication')
    } finally {
      setDeleting(null)
    }
  }

  if (medications.length === 0) {
    return (
      <div className="inventory-section">
        <h3 className="section-title">Inventory</h3>
        <div className="empty-state">
          <p>No medications in inventory</p>
          <button className="add-button" onClick={() => setShowModal(true)}>
            Add Item
          </button>
        </div>
        {showModal && (
          <InventoryModal onClose={() => {
            setShowModal(false)
            onDataChange()
          }} />
        )}
      </div>
    )
  }

  return (
    <div className="inventory-section">
      <div className="section-header">
        <h3 className="section-title">Inventory</h3>
      </div>
      <div className="table-container">
        <table className="inventory-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Quantity</th>
              <th>Expiration Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {medications.map((med) => (
              <tr key={med.id}>
                <td>{med.name}</td>
                <td>
                  <span className={med.quantity < 10 ? 'low-quantity' : ''}>
                    {med.quantity}
                  </span>
                </td>
                <td>{med.expiration_date || 'N/A'}</td>
                <td>
                  <button
                    className="delete-button"
                    onClick={() => handleDelete(med.id)}
                    disabled={deleting === med.id}
                  >
                    {deleting === med.id ? 'Deleting...' : 'Delete'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default InventoryTable

