import React, { useState, useEffect } from 'react'
import { googleDriveService } from '../services/googleDrive'
import DeleteFileModal from './modals/DeleteFileModal'
import './DriveSection.css'

function DriveSection() {
  const [files, setFiles] = useState([])
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [fileToDelete, setFileToDelete] = useState(null)

  useEffect(() => {
    loadFiles()
  }, [])

  const loadFiles = async () => {
    setLoading(true)
    try {
      const data = await googleDriveService.listFiles()
      setFiles(data.files || [])
      setConnected(data.connected)
    } catch (error) {
      if (error.response?.status === 401) {
        setConnected(false)
      } else {
        setConnected(false)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploading(true)
    try {
      await googleDriveService.uploadFile(file)
      alert('File uploaded successfully!')
      loadFiles()
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to upload file')
    } finally {
      setUploading(false)
      e.target.value = ''
    }
  }

  const handleDeleteClick = (file) => {
    setFileToDelete(file)
    setIsDeleteModalOpen(true)
  }

  const closeModal = () => {
    setIsDeleteModalOpen(false)
    setFileToDelete(null)
  }

  const handleConfirmDelete = async () => {
    if (!fileToDelete) return

    try {
      await googleDriveService.deleteFile(fileToDelete.id)
      alert('File deleted successfully!')
      loadFiles()
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to delete file')
    } finally {
      closeModal()
    }
  }

  if (loading) {
    return (
      <div className="drive-section">
        <h3 className="section-title">Google Drive</h3>
        <div className="loading-state">Loading...</div>
      </div>
    )
  }

  if (!connected) {
    return (
      <div className="drive-section">
        <h3 className="section-title">Google Drive</h3>
        <div className="empty-state">
          <p>Google Drive not connected</p>
          <p className="empty-state-subtitle">Connect your Google account to access files</p>
          <button className="setup-button" onClick={loadFiles}>
            Setup
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="drive-section">
      <div className="section-header">
        <h3 className="section-title">Google Drive</h3>
        <label className="upload-button">
          <input
            type="file"
            onChange={handleFileUpload}
            disabled={uploading}
            style={{ display: 'none' }}
          />
          {uploading ? 'Uploading...' : 'Upload File'}
        </label>
      </div>
      {files.length === 0 ? (
        <div className="empty-state">
          <p>No files found</p>
        </div>
      ) : (
        <div className="files-list">
          {files.map((file) => (
            <div key={file.id} className="file-item">
              <span className="file-name">{file.name}</span>
              <span className="file-type">{file.mimeType}</span>
              <button onClick={() => handleDeleteClick(file)} className="delete-button">
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
      {isDeleteModalOpen && (
        <DeleteFileModal
          fileName={fileToDelete?.name}
          onConfirm={handleConfirmDelete}
          onCancel={closeModal}
        />
      )}
    </div>
  )
}

export default DriveSection

