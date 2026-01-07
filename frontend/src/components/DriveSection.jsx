import React, { useState, useEffect, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { googleDriveService } from '../services/googleDrive'
import DeleteFileModal from './modals/DeleteFileModal'
import { FiFile, FiTrash2, FiUploadCloud, FiZap, FiXCircle, FiPlus } from 'react-icons/fi'
import './DriveSection.css'

function DriveSection() {
  const [files, setFiles] = useState([])
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [fileToDelete, setFileToDelete] = useState(null)

  const loadFiles = useCallback(async () => {
    setLoading(true)
    try {
      const data = await googleDriveService.listFiles()
      setFiles(data.files || [])
      setConnected(data.connected)
    } catch (error) {
      setConnected(false)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadFiles()
  }, [loadFiles])

  const onDrop = useCallback(
    async (acceptedFiles) => {
      if (!acceptedFiles.length) return
      setUploading(true)
      try {
        await googleDriveService.uploadFile(acceptedFiles[0])
        loadFiles()
      } catch (error) {
        alert(error.response?.data?.detail || 'Failed to upload file')
      } finally {
        setUploading(false)
      }
    },
    [loadFiles]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    noClick: true,
    noKeyboard: true,
    multiple: false,
  })

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
      loadFiles()
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to delete file')
    } finally {
      closeModal()
    }
  }

  const renderFileIcon = (mimeType) => {
    if (mimeType.includes('image')) return <FiFile className="file-icon image" />
    if (mimeType.includes('pdf')) return <FiFile className="file-icon pdf" />
    return <FiFile className="file-icon" />
  }

  if (loading) {
    return (
      <div className="drive-section modern">
        <h3 className="section-title">Google Drive</h3>
        <div className="loading-state">Loading files...</div>
      </div>
    )
  }

  if (!connected) {
    return (
      <div className="drive-section modern not-connected">
        <div className="empty-state">
          <FiZap size={48} className="empty-state-icon" />
          <h4 className="empty-state-title">Connect to Google Drive</h4>
          <p className="empty-state-subtitle">
            Link your Google account to manage and access your files directly.
          </p>
          <button className="setup-button" onClick={loadFiles}>
            <FiZap />
            Connect Now
          </button>
        </div>
      </div>
    )
  }

  return (
    <div {...getRootProps({ className: `drive-section modern ${isDragActive ? 'drag-active' : ''}` })}>
      <input {...getInputProps()} />
      <div className="section-header">
        <h3 className="section-title">Google Drive</h3>
        <button className="add-new-file-button" onClick={() => document.getElementById('drive-file-input').click()}>
          {uploading ? 'Uploading...' :<><FiPlus /> Add File</>}
        </button>
        <input
          id="drive-file-input"
          type="file"
          style={{ display: 'none' }}
          onChange={(e) => onDrop(Array.from(e.target.files))}
        />
      </div>

      {files.length === 0 ? (
        <div className="empty-state">
          <FiUploadCloud size={48} className="empty-state-icon" />
          <h4 className="empty-state-title">Drag & drop to upload</h4>
          <p className="empty-state-subtitle">or click the button to select a file</p>
          <label className="upload-button-styled">
            <input type="file" onChange={(e) => onDrop(Array.from(e.target.files))} />
            {uploading ? 'Uploading...' : 'Browse Files'}
          </label>
        </div>
      ) : (
        <>
          <div className="files-grid">
            {files.map((file) => (
              <div key={file.id} className="file-card">
                <div className="file-card-header">
                  {renderFileIcon(file.mimeType)}
                  <span className="file-name">{file.name}</span>
                </div>
                <div className="file-card-footer">
                  <span className="file-type">{file.mimeType}</span>
                  <button onClick={() => handleDeleteClick(file)} className="delete-icon-button">
                    <FiTrash2 />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {isDragActive && (
        <div className="drag-overlay">
          <FiUploadCloud size={64} />
          <p>Drop file to upload</p>
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

export default DriveSection;
