import React, { useState, useEffect, useRef } from 'react'
import Header from '../components/Header'
import Hero from '../components/Hero'
import ActionGrid from '../components/ActionGrid'
import DataDashboard from '../components/DataDashboard'
import IllnessTimeline from '../components/IllnessTimeline'
import ChatWidget from '../components/ChatWidget'
import Spinner from '../components/Spinner'
import { familyMembersService } from '../services/familyMembers'
import { medicationsService } from '../services/medications'
import { featuresService } from '../services/features'
import { auth } from '../utils/auth.util'
import './HomePage.css'

function HomePage({ setIsAuthenticated }) {
  const [familyMembers, setFamilyMembers] = useState([])
  const [medications, setMedications] = useState([])
  const [initialLoading, setInitialLoading] = useState(true)
  const [featureFlags, setFeatureFlags] = useState({
    ai_chat_enabled: true,
    ai_illness_suggestions_enabled: true,
    ai_drive_enabled: true,
  })
  const illnessTimelineRef = useRef(null)
  const calendarRef = useRef(null)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      const [membersData, medicationsData, flags] = await Promise.all([
        familyMembersService.getAll(),
        medicationsService.getAll(),
        featuresService.getFeatureFlags(),
      ])
      setFamilyMembers(membersData)
      setMedications(medicationsData)
      setFeatureFlags(flags)
    } catch (error) {
      console.error('Error loading initial data:', error)
    } finally {
      setInitialLoading(false)
    }
  }

  const loadData = async () => {
    try {
      const [membersData, medicationsData] = await Promise.all([
        familyMembersService.getAll(),
        medicationsService.getAll(),
      ])
      setFamilyMembers(membersData)
      setMedications(medicationsData)
    } catch (error) {
      console.error('Error loading data:', error)
    }
  }

  const handleLogout = () => {
    auth.logout()
    setIsAuthenticated(false)
  }

  const handleIllnessRefresh = () => {
    illnessTimelineRef.current?.refresh()
  }

  const handleCalendarRefresh = () => {
    calendarRef.current?.refresh()
  }

  if (initialLoading) {
    return <Spinner message="Loading Life-Line..." />
  }

  return (
    <div className="home-page">
      <Header  onLogout={handleLogout}/>
      <div className="home-content">
        <Hero />
        <ActionGrid 
          familyMembers={familyMembers}
          medications={medications}
          onDataChange={loadData}
          onIllnessRefresh={handleIllnessRefresh}
          onCalendarRefresh={handleCalendarRefresh}
        />
        <DataDashboard 
          medications={medications}
          familyMembers={familyMembers}
          onDataChange={loadData}
          ref={calendarRef}
          aiDriveEnabled={featureFlags.ai_drive_enabled}
        />
        <IllnessTimeline 
          familyMembers={familyMembers} 
          ref={illnessTimelineRef}
          aiSuggestionsEnabled={featureFlags.ai_illness_suggestions_enabled}
        />
      </div>
      {featureFlags.ai_chat_enabled && <ChatWidget />}
    </div>
  )
}

export default HomePage
