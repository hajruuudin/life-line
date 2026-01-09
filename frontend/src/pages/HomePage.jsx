import React, { useState, useEffect } from 'react'
import Header from '../components/Header'
import Hero from '../components/Hero'
import ActionGrid from '../components/ActionGrid'
import DataDashboard from '../components/DataDashboard'
import IllnessTimeline from '../components/IllnessTimeline'
import ChatWidget from '../components/ChatWidget'
import { familyMembersService } from '../services/familyMembers'
import { medicationsService } from '../services/medications'
import { auth } from '../utils/auth.util'
import './HomePage.css'

function HomePage({ setIsAuthenticated }) {
  const [familyMembers, setFamilyMembers] = useState([])
  const [medications, setMedications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

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
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    auth.logout()
    setIsAuthenticated(false)
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
        />
        <DataDashboard 
          medications={medications}
          onDataChange={loadData}
        />
        <IllnessTimeline familyMembers={familyMembers} />
      </div>
      <ChatWidget />
    </div>
  )
}

export default HomePage
