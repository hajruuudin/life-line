import React, { useState, useEffect, forwardRef } from 'react'
import CalendarOverview from './CalendarOverview'
import DriveSection from './DriveSection'
import InventoryTable from './InventoryTable'
import FamilyMembersWidget from './FamilyMembersWidget'
import MedicationUsageWidget from './MedicationUsageWidget'
import { medicationsService } from '../services/medications'
import './DataDashboard.css'

const DataDashboard = forwardRef(function DataDashboard({ medications, familyMembers, onDataChange, aiDriveEnabled = true }, ref) {
  return (
    <section className="data-dashboard">
      <CalendarOverview ref={ref} />
      <div className="dashboard-row">
        <div className="dashboard-column">
          <DriveSection aiDriveEnabled={aiDriveEnabled} />
        </div>
        <div className="dashboard-column">
          <InventoryTable medications={medications} onDataChange={onDataChange} />
        </div>
      </div>
      <div className="dashboard-row">
        <div className="dashboard-column">
          <FamilyMembersWidget familyMembers={familyMembers} onDataChange={onDataChange} />
        </div>
        <div className="dashboard-column">
          <MedicationUsageWidget familyMembers={familyMembers} />
        </div>
      </div>
    </section>
  )
})

export default DataDashboard

