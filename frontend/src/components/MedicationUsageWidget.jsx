import React, { useState, useEffect, useCallback } from 'react'
import { FiActivity, FiFilter } from 'react-icons/fi'
import { medicationUsageService } from '../services/medicationUsage'
import './MedicationUsageWidget.css'

function MedicationUsageWidget({ familyMembers }) {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filterMemberId, setFilterMemberId] = useState('')

  const loadLogs = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await medicationUsageService.getAll()
      setLogs(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load usage logs')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadLogs()
  }, [loadLogs])

  const formatDateTime = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const filteredLogs = filterMemberId
    ? logs.filter(log => log.family_member_id === parseInt(filterMemberId))
    : logs

  if (loading) {
    return (
      <div className="medication-usage-widget modern">
        <div className="section-header">
          <h3 className="section-title">
            <FiActivity className="section-icon" />
            Medication Usage
          </h3>
        </div>
        <div className="widget-content">
          <div className="loading-state">Loading usage history...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="medication-usage-widget modern">
      <div className="section-header">
        <h3 className="section-title">
          <FiActivity className="section-icon" />
          Medication Usage
        </h3>
        <div className="filter-container">
          <FiFilter className="filter-icon" />
          <select
            className="filter-select"
            value={filterMemberId}
            onChange={(e) => setFilterMemberId(e.target.value)}
          >
            <option value="">All Members</option>
            {familyMembers.map(member => (
              <option key={member.id} value={member.id}>{member.name}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="widget-content">
        {error && <div className="error-state">{error}</div>}

        {filteredLogs.length === 0 ? (
          <div className="empty-state">
            <FiActivity size={48} className="empty-state-icon" />
            <h4 className="empty-state-title">No usage records</h4>
            <p className="empty-state-subtitle">
              {filterMemberId 
                ? 'No medication usage found for this family member.' 
                : 'Log medication usage using the button above.'}
            </p>
          </div>
        ) : (
          <div className="usage-table-container">
            <table className="usage-table">
              <thead>
                <tr>
                  <th>Family Member</th>
                  <th>Medication</th>
                  <th className="text-center">Qty</th>
                  <th>Date & Time</th>
                </tr>
              </thead>
              <tbody>
                {filteredLogs.map((log) => (
                  <tr key={log.id}>
                    <td className="member-name">{log.family_member_name}</td>
                    <td className="medication-name">{log.medication_name}</td>
                    <td className="text-center">
                      <span className="quantity-pill">{log.quantity_used}</span>
                    </td>
                    <td className="date-cell">{formatDateTime(log.used_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default MedicationUsageWidget
