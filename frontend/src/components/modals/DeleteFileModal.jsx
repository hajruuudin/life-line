import React from 'react';
import Modal from './Modal'; // Import the new generic Modal component

function DeleteFileModal({ fileName, onConfirm, onCancel }) {
  return (
    <Modal
      title="Confirm Deletion"
      // You can add an icon here if needed, e.g., icon={<i className="fas fa-trash-alt"></i>}
      confirmText="Delete"
      onConfirm={onConfirm}
      onCancel={onCancel}
    >
      <p>
        Are you sure you want to delete the file: <strong>{fileName}</strong>?
      </p>
    </Modal>
  );
}

export default DeleteFileModal;
