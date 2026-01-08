import React, { useState } from 'react'
import { FiPlus, FiTrash2, FiAlertTriangle, FiArchive } from 'react-icons/fi'
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

  const isExpired = (date) => {
    return new Date(date) < new Date()
  }

  if (medications.length === 0) {
    return (
      <div className="inventory-section modern">
        <div className="section-header new-header">
          <h3 className="section-title">Inventory</h3>
        </div>
        <div className="empty-state">
          <FiArchive size={48} className="empty-state-icon" />
          <h4 className="empty-state-title">Inventory is empty</h4>
          <p className="empty-state-subtitle">Add your first medication to get started.</p>
          <button className="add-button-styled" onClick={() => setShowModal(true)}>
            <FiPlus />
            Add Medication
          </button>
        </div>
        {showModal && (
          <InventoryModal
            onClose={() => {
              setShowModal(false)
              onDataChange()
            }}
          />
        )}
      </div>
    )
  }

  return (
    <div className="inventory-section modern">
      <div className="section-header new-header">
        <h3 className="section-title">Inventory</h3>
        <button className="add-button-styled" onClick={() => setShowModal(true)}>
          <FiPlus />
          Add Item
        </button>
      </div>
      <div className="table-container">
        <table className="inventory-table-modern">
          <thead>
            <tr>
              <th>Name</th>
              <th className="text-center">Quantity</th>
              <th className="text-center">Status</th>
              <th className="hide-on-mobile">Expiration</th>
              <th className="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {medications.map((med) => (
              <tr key={med.id}>
                <td>{med.name}</td>
                <td className="text-center">
                  <span
                    className={`quantity-pill ${
                      med.quantity < 10 ? 'low' : ''
                    }`}
                  >
                    {med.quantity}
                  </span>
                </td>
                <td className="text-center">
                  {isExpired(med.expiration_date) ? (
                    <span className="status-pill expired">
                      <FiAlertTriangle /> Expired
                    </span>
                  ) : med.quantity < 10 ? (
                    <span className="status-pill low-stock">
                      <FiAlertTriangle /> Low Stock
                    </span>
                  ) : (
                    <span className="status-pill in-stock">In Stock</span>
                  )}
                </td>
                <td className="hide-on-mobile">{new Date(med.expiration_date).toLocaleDateString()}</td>
                <td className="text-right">
                  <button
                    className="delete-icon-button"
                    onClick={() => handleDelete(med.id)}
                    disabled={deleting === med.id}
                  >
                    {deleting === med.id ? '...' : <FiTrash2 />}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {showModal && (
        <InventoryModal
          onClose={() => {
            setShowModal(false)
            onDataChange()
          }}
        />
      )}
    </div>
  )
}

export default InventoryTable
