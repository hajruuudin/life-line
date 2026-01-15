import React, { useState, useEffect, forwardRef } from 'react'
import CalendarOverview from './CalendarOverview'
import DriveSection from './DriveSection'
import InventoryTable from './InventoryTable'
import { medicationsService } from '../services/medications'
import './DataDashboard.css'

const DataDashboard = forwardRef(function DataDashboard({ medications, onDataChange }, ref) {
  return (
    <section className="data-dashboard">
      <CalendarOverview ref={ref} />
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
})

export default DataDashboard

