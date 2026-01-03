import api from './api'

export const familyMembersService = {
  async getAll() {
    const response = await api.get('/family-members')
    return response.data
  },

  async create(data) {
    const response = await api.post('/family-members', data)
    return response.data
  },

  async update(id, data) {
    const response = await api.put(`/family-members/${id}`, data)
    return response.data
  },

  async delete(id) {
    await api.delete(`/family-members/${id}`)
  },
}

