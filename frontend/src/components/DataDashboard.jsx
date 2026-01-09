import React, { useState, useEffect } from 'react'
import CalendarOverview from './CalendarOverview'
import DriveSection from './DriveSection'
import InventoryTable from './InventoryTable'
import { medicationsService } from '../services/medications'
import './DataDashboard.css'

function DataDashboard({ medications, onDataChange }) {
  return (
    <section className="data-dashboard">
      <CalendarOverview />
      <div className="dashboard-row">
        <div className="dashboard-column">
          <DriveSection />
        </div>
        <div className="dashboard-column">
          <InventoryTable medications={medications} onDataChange={onDataChange} />
        </div>
      </div>
    </section>
  )
}

export default DataDashboard

