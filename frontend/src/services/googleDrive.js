import api from './api'

export const googleDriveService = {
  async listFiles() {
    const response = await api.get('/drive/files')
    return response.data
  },

  async uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/drive/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async deleteFile(fileId) {
    const response = await api.delete(`/drive/files/${fileId}`)
    return response.data
  },
}

