import api from './api'

export const medicationsService = {
  async getAll() {
    const response = await api.get('/medications')
    return response.data
  },

  async create(data) {
    const response = await api.post('/medications', data)
    return response.data
  },

  async update(id, data) {
    const response = await api.put(`/medications/${id}`, data)
    return response.data
  },

  async delete(id) {
    await api.delete(`/medications/${id}`)
  },
}

