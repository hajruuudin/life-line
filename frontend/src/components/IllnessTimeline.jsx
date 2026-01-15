import React, { useState, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react'
import { illnessLogsService } from '../services/illnessLogs'
import { FiThermometer, FiTrash2, FiFilter, FiChevronDown, FiChevronUp } from 'react-icons/fi'
import './IllnessTimeline.css'

const IllnessTimeline = forwardRef(function IllnessTimeline({ familyMembers, aiSuggestionsEnabled = true }, ref) {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filterMemberId, setFilterMemberId] = useState('')
  const [deleting, setDeleting] = useState(null)
  const [expandedRows, setExpandedRows] = useState(new Set())

  const loadLogs = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await illnessLogsService.getAll(filterMemberId || null)
      setLogs(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load illness logs')
    } finally {
      setLoading(false)
    }
  }, [filterMemberId])

  useEffect(() => {
    loadLogs()
  }, [loadLogs])

  useImperativeHandle(ref, () => ({
    refresh: loadLogs
  }))

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this illness log?')) {
      return
    }
    setDeleting(id)
    try {
      await illnessLogsService.delete(id)
      loadLogs()
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete illness log')
    } finally {
      setDeleting(null)
    }
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return 'Ongoing'
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  const calculateDuration = (startDate, endDate) => {
    const start = new Date(startDate)
    const end = endDate ? new Date(endDate) : new Date()
    const diffTime = Math.abs(end - start)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return '< 1 day'
    if (diffDays === 1) return '1 day'
    return `${diffDays} days`
  }

  const isOngoing = (endDate) => !endDate

  const toggleRow = (logId) => {
    setExpandedRows(prev => {
      const newSet = new Set(prev)
      if (newSet.has(logId)) {
        newSet.delete(logId)
      } else {
        newSet.add(logId)
      }
      return newSet
    })
  }

  if (loading) {
    return (
      <div className="illness-timeline modern">
        <div className="section-header">
          <h3 className="section-title">
            <FiThermometer className="section-icon" />
            Illness Timeline
          </h3>
        </div>
        <div className="loading-state">Loading illness history...</div>
      </div>
    )
  }

  return (
    <div className="illness-timeline modern">
      <div className="section-header">
        <h3 className="section-title">
          <FiThermometer className="section-icon" />
          Illness Timeline
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

      {error && <div className="error-state">{error}</div>}

      <div className="timeline-content">
        {logs.length === 0 ? (
          <div className="empty-state">
            <FiThermometer size={48} className="empty-state-icon" />
            <h4 className="empty-state-title">No illness records</h4>
            <p className="empty-state-subtitle">
              {filterMemberId 
                ? 'No illness records found for this family member.' 
                : 'Start tracking by logging an illness using the button above.'}
            </p>
          </div>
        ) : (
          <div className="timeline-table-container">
            <table className="timeline-table">
              <thead>
                <tr>
                  <th>Family Member</th>
                  <th>Illness</th>
                  <th>Start Date</th>
                  <th>End Date</th>
                  <th className="text-center">Duration</th>
                  {aiSuggestionsEnabled && <th className="text-center">AI Tips</th>}
                  <th className="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <React.Fragment key={log.id}>
                    <tr>
                      <td className="member-name">{log.family_member_name}</td>
                      <td className="illness-name">{log.illness_name}</td>
                      <td>{formatDate(log.start_date)}</td>
                      <td>
                        {isOngoing(log.end_date) ? (
                          <span className="status-pill ongoing">Ongoing</span>
                        ) : (
                          formatDate(log.end_date)
                        )}
                      </td>
                      <td className="text-center">
                        <span className={`duration-pill ${isOngoing(log.end_date) ? 'ongoing' : ''}`}>
                          {calculateDuration(log.start_date, log.end_date)}
                        </span>
                      </td>
                      {aiSuggestionsEnabled && (
                        <td className="text-center">
                          {log.ai_suggestion ? (
                            <button
                              className="expand-button"
                              onClick={() => toggleRow(log.id)}
                              title={expandedRows.has(log.id) ? 'Hide suggestions' : 'Show suggestions'}
                            >
                              {expandedRows.has(log.id) ? <FiChevronUp /> : <FiChevronDown />}
                            </button>
                          ) : (
                            <span className="no-suggestion">-</span>
                          )}
                        </td>
                      )}
                      <td className="text-right">
                        <button
                          className="delete-icon-button"
                          onClick={() => handleDelete(log.id)}
                          disabled={deleting === log.id}
                        >
                          {deleting === log.id ? '...' : <FiTrash2 />}
                        </button>
                      </td>
                    </tr>
                    {aiSuggestionsEnabled && expandedRows.has(log.id) && log.ai_suggestion && (
                      <tr className="suggestion-row">
                        <td colSpan="7">
                          <div className="ai-suggestion-content">
                            <strong>💡 Home Remedy Suggestions:</strong>
                            <div className="suggestion-text">{log.ai_suggestion}</div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
})

export default IllnessTimeline
