import React, { useState } from 'react'
import InventoryModal from './modals/InventoryModal'
import FamilyMemberModal from './modals/FamilyMemberModal'
import ScheduleEventModal from './modals/ScheduleEventModal'
import LogUsageModal from './modals/LogUsageModal'
import './ActionGrid.css'

function ActionGrid({ familyMembers, medications, onDataChange }) {
  const [activeModal, setActiveModal] = useState(null)

  const closeModal = () => {
    setActiveModal(null)
  }

  const handleModalClose = () => {
    closeModal()
    onDataChange()
  }

  return (
    <section className="action-grid-section">
      <div className="action-grid">
        <button 
          className="action-button"
          onClick={() => setActiveModal('inventory')}
        >
          Add/Update Inventory
        </button>
        <button 
          className="action-button"
          onClick={() => setActiveModal('family-member')}
        >
          Add Family Member
        </button>
        <button 
          className="action-button"
          onClick={() => setActiveModal('schedule-event')}
        >
          Schedule Event
        </button>
        <button 
          className="action-button"
          onClick={() => setActiveModal('log-usage')}
          disabled={familyMembers.length === 0 || medications.length === 0}
        >
          Log Usage
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
    </section>
  )
}

export default ActionGrid

