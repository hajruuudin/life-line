import api from './api'

export const medicationUsageService = {
  async logUsage(data) {
    const response = await api.post('/medication-usage', data)
    return response.data
  },

  async getAll() {
    const response = await api.get('/medication-usage')
    return response.data
  },
}

