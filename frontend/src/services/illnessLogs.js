import api from './api'

export const illnessLogsService = {
  async getAll(familyMemberId = null) {
    const params = familyMemberId ? { family_member_id: familyMemberId } : {}
    const response = await api.get('/illness-logs', { params })
    return response.data
  },

  async getById(id) {
    const response = await api.get(`/illness-logs/${id}`)
    return response.data
  },

  async create(data) {
    const response = await api.post('/illness-logs', data)
    return response.data
  },

  async update(id, data) {
    const response = await api.put(`/illness-logs/${id}`, data)
    return response.data
  },

  async delete(id) {
    await api.delete(`/illness-logs/${id}`)
  },
}
