import React, { useState, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react'
import { googleCalendarService } from '../services/googleCalendar'
import EventDetailModal from './modals/EventDetailModal'
import { FiCalendar, FiAlertCircle } from 'react-icons/fi'
import './CalendarOverview.css'

const CalendarOverview = forwardRef(function CalendarOverview(props, ref) {
  const [eventsByDate, setEventsByDate] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [noAccess, setNoAccess] = useState(false)
  const [selectedEvent, setSelectedEvent] = useState(null)

  const loadEvents = useCallback(async () => {
    setLoading(true)
    setError(null)
    setNoAccess(false)
    try {
      const data = await googleCalendarService.getUpcomingEvents()
      setEventsByDate(data.events || {})
    } catch (err) {
      if (err.response?.status === 403) {
        setNoAccess(true)
      } else {
        setError(err.response?.data?.detail || 'Failed to load calendar events')
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadEvents()
  }, [loadEvents])

  useImperativeHandle(ref, () => ({
    refresh: loadEvents
  }))

  // Generate next 7 days
  const getNext7Days = () => {
    const days = []
    const today = new Date()
    for (let i = 0; i < 7; i++) {
      const date = new Date(today)
      date.setDate(today.getDate() + i)
      days.push(date)
    }
    return days
  }

  const formatDateKey = (date) => {
    return date.toISOString().split('T')[0]
  }

  const formatDayName = (date) => {
    const today = new Date()
    const tomorrow = new Date(today)
    tomorrow.setDate(today.getDate() + 1)

    if (formatDateKey(date) === formatDateKey(today)) return 'Today'
    if (formatDateKey(date) === formatDateKey(tomorrow)) return 'Tomorrow'
    return date.toLocaleDateString('en-US', { weekday: 'short' })
  }

  const formatDayNumber = (date) => {
    return date.getDate()
  }

  const formatMonth = (date) => {
    return date.toLocaleDateString('en-US', { month: 'short' })
  }

  const formatEventTime = (event) => {
    const start = event.start?.dateTime || event.start?.date
    if (!start) return ''
    
    if (event.start?.date && !event.start?.dateTime) {
      return 'All day'
    }
    
    const date = new Date(start)
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
  }

  const days = getNext7Days()

  if (loading) {
    return (
      <div className="calendar-overview modern">
        <div className="section-header">
          <h3 className="section-title">
            <FiCalendar className="section-icon" />
            Upcoming Appointments
          </h3>
        </div>
        <div className="loading-state">Loading calendar...</div>
      </div>
    )
  }

  if (noAccess) {
    return (
      <div className="calendar-overview modern no-access">
        <div className="section-header">
          <h3 className="section-title">
            <FiCalendar className="section-icon" />
            Upcoming Appointments
          </h3>
        </div>
        <div className="no-access-message">
          <FiAlertCircle size={32} className="no-access-icon" />
          <p>Calendar access not granted.</p>
          <p className="no-access-hint">Please re-login and allow calendar access to use this feature.</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="calendar-overview modern">
        <div className="section-header">
          <h3 className="section-title">
            <FiCalendar className="section-icon" />
            Upcoming Appointments
          </h3>
        </div>
        <div className="error-state">{error}</div>
      </div>
    )
  }

  return (
    <div className="calendar-overview modern">
      <div className="section-header">
        <h3 className="section-title">
          <FiCalendar className="section-icon" />
          Upcoming Appointments
        </h3>
      </div>
      
      <div className="calendar-scroll-container">
        <div className="days-grid">
          {days.map((date) => {
            const dateKey = formatDateKey(date)
            const dayEvents = eventsByDate[dateKey] || []
            const isToday = formatDateKey(date) === formatDateKey(new Date())
            
            return (
              <div key={dateKey} className={`day-column ${isToday ? 'today' : ''}`}>
                <div className="day-header">
                  <span className="day-name">{formatDayName(date)}</span>
                  <span className="day-number">{formatDayNumber(date)}</span>
                  <span className="day-month">{formatMonth(date)}</span>
                </div>
                <div className="day-events">
                  {dayEvents.length === 0 ? (
                    <div className="no-events">No appointments</div>
                  ) : (
                    dayEvents.map((event) => (
                      <div 
                        key={event.id} 
                        className="event-card"
                        onClick={() => setSelectedEvent(event)}
                      >
                        <span className="event-time">{formatEventTime(event)}</span>
                        <span className="event-title">{event.summary}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {selectedEvent && (
        <EventDetailModal 
          event={selectedEvent} 
          onClose={() => setSelectedEvent(null)} 
        />
      )}
    </div>
  )
})

export default CalendarOverview
