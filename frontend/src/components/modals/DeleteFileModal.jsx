import React from 'react'
import './DeleteFileModal.css'

function DeleteFileModal({ fileName, onConfirm, onCancel }) {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2 className="modal-title">Confirm Deletion</h2>
        <p>
          Are you sure you want to delete the file: <strong>{fileName}</strong>?
        </p>
        <div className="modal-actions">
          <button onClick={onCancel} className="cancel-button">
            Cancel
          </button>
          <button onClick={onConfirm} className="confirm-button">
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}

export default DeleteFileModal
