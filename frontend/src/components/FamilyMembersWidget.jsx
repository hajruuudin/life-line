import React, { useState } from 'react'
import { FiUsers, FiEdit2, FiTrash2, FiInfo } from 'react-icons/fi'
import { familyMembersService } from '../services/familyMembers'
import EditFamilyMemberModal from './modals/EditFamilyMemberModal'
import toast from 'react-hot-toast'
import './FamilyMembersWidget.css'

function FamilyMembersWidget({ familyMembers, onDataChange }) {
  const [editingMember, setEditingMember] = useState(null)
  const [deleting, setDeleting] = useState(null)
  const [expandedMember, setExpandedMember] = useState(null)

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete ${name}?`)) {
      return
    }
    setDeleting(id)
    try {
      await familyMembersService.delete(id)
      toast.success('Family member deleted')
      onDataChange()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to delete family member')
    } finally {
      setDeleting(null)
    }
  }

  const handleEditClose = () => {
    setEditingMember(null)
    onDataChange()
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  const calculateAge = (dateOfBirth) => {
    if (!dateOfBirth) return '-'
    const today = new Date()
    const birth = new Date(dateOfBirth)
    let age = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    return age
  }

  const formatGender = (gender) => {
    if (!gender) return '-'
    return gender.charAt(0).toUpperCase() + gender.slice(1)
  }

  const toggleExpand = (memberId) => {
    setExpandedMember(expandedMember === memberId ? null : memberId)
  }

  return (
    <div className="family-members-widget modern">
      <div className="section-header">
        <h3 className="section-title">
          <FiUsers className="section-icon" />
          Family Members
        </h3>
        <span className="member-count">{familyMembers.length} member{familyMembers.length !== 1 ? 's' : ''}</span>
      </div>

      <div className="widget-content">
        {familyMembers.length === 0 ? (
          <div className="empty-state">
            <FiUsers size={48} className="empty-state-icon" />
            <h4 className="empty-state-title">No family members</h4>
            <p className="empty-state-subtitle">
              Add family members using the button above to start tracking their health.
            </p>
          </div>
        ) : (
          <div className="members-table-container">
            <table className="members-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Gender</th>
                  <th className="text-center">Age</th>
                  <th>Profession</th>
                  <th className="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {familyMembers.map((member) => (
                  <React.Fragment key={member.id}>
                    <tr>
                      <td className="member-name">{member.name}</td>
                      <td>{formatGender(member.gender)}</td>
                      <td className="text-center">
                        <span className="age-pill">{calculateAge(member.date_of_birth)}</span>
                      </td>
                      <td className="profession-cell">{member.profession || '-'}</td>
                      <td className="text-right actions-cell">
                        {member.health_notes && (
                          <button
                            className="info-icon-button"
                            onClick={() => toggleExpand(member.id)}
                            title="View health notes"
                          >
                            <FiInfo />
                          </button>
                        )}
                        <button
                          className="edit-icon-button"
                          onClick={() => setEditingMember(member)}
                          title="Edit"
                        >
                          <FiEdit2 />
                        </button>
                        <button
                          className="delete-icon-button"
                          onClick={() => handleDelete(member.id, member.name)}
                          disabled={deleting === member.id}
                          title="Delete"
                        >
                          {deleting === member.id ? '...' : <FiTrash2 />}
                        </button>
                      </td>
                    </tr>
                    {expandedMember === member.id && member.health_notes && (
                      <tr className="health-notes-row">
                        <td colSpan="5">
                          <div className="health-notes-content">
                            <strong>Health Notes:</strong>
                            <p>{member.health_notes}</p>
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

      {editingMember && (
        <EditFamilyMemberModal
          member={editingMember}
          onClose={handleEditClose}
        />
      )}
    </div>
  )
}

export default FamilyMembersWidget
