import React, { useState } from 'react';
import InventoryModal from './modals/InventoryModal';
import FamilyMemberModal from './modals/FamilyMemberModal';
import ScheduleEventModal from './modals/ScheduleEventModal';
import LogUsageModal from './modals/LogUsageModal';
import IllnessLogModal from './modals/IllnessLogModal';
import { FaBoxOpen, FaUsers, FaCalendarAlt, FaPrescriptionBottle, FaThermometerHalf } from 'react-icons/fa';
import './ActionGrid.css';

function ActionGrid({ familyMembers, medications, onDataChange }) {
  const [activeModal, setActiveModal] = useState(null);

  const closeModal = () => {
    setActiveModal(null);
  };

  const handleModalClose = () => {
    closeModal();
    onDataChange();
  };

  return (
    <section className="action-grid-section">
      <div className="action-grid">
        <button
          className="action-button inventory"
          onClick={() => setActiveModal('inventory')}
        >
          <FaBoxOpen /> Add/Update Inventory
        </button>
        <button
          className="action-button family-member"
          onClick={() => setActiveModal('family-member')}
        >
          <FaUsers /> Add Family Member
        </button>
        <button
          className="action-button schedule-event"
          onClick={() => setActiveModal('schedule-event')}
        >
          <FaCalendarAlt /> Schedule Event
        </button>
        <button
          className="action-button log-usage"
          onClick={() => setActiveModal('log-usage')}
          disabled={familyMembers.length === 0 || medications.length === 0}
        >
          <FaPrescriptionBottle /> Log Usage
        </button>
        <button
          className="action-button log-illness"
          onClick={() => setActiveModal('log-illness')}
          disabled={familyMembers.length === 0}
        >
          <FaThermometerHalf /> Log Illness
        </button>
      </div>

      {activeModal === 'inventory' && (
        <InventoryModal onClose={handleModalClose} />
      )}
      {activeModal === 'family-member' && (
        <FamilyMemberModal onClose={handleModalClose} />
      )}
      {activeModal === 'schedule-event' && (
        <ScheduleEventModal onClose={closeModal} />
      )}
      {activeModal === 'log-usage' && (
        <LogUsageModal
          familyMembers={familyMembers}
          medications={medications}
          onClose={handleModalClose}
        />
      )}
      {activeModal === 'log-illness' && (
        <IllnessLogModal
          familyMembers={familyMembers}
          onClose={handleModalClose}
        />
      )}
    </section>
  );
}

export default ActionGrid;