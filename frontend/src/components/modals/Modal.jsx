import React from 'react';
import './Modal.css';

const Modal = ({ title, icon, children, confirmText, onConfirm, onCancel }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <div className="modal-title-container">
            {icon && <span className="modal-icon">{icon}</span>}
            <h2 className="modal-title">{title}</h2>
          </div>
          <button onClick={onCancel} className="modal-close-button">
            &times;
          </button>
        </div>
        <div className="modal-body">
          {children}
        </div>
        <div className="modal-footer">
          <button onClick={onCancel} className="button-secondary">
            Cancel
          </button>
          <button onClick={onConfirm} className="button-primary">
            {confirmText || 'Confirm'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;
