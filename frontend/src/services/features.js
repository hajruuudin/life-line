import api from './api'

export const featuresService = {
  async getFeatureFlags() {
    const response = await api.get('/features')
    return response.data
  },
}
