import api from './api'

export const authService = {
  async getGoogleAuthUrl() {
    const response = await api.get('/auth/google-login')
    return response.data.auth_url
  },

  async handleCallback(code) {
    const response = await api.post('/auth/callback', { code })
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
      if (response.data.user) {
        localStorage.setItem('userId', response.data.user.id)
        localStorage.setItem('userEmail', response.data.user.email)
      }
      return response.data
    }
    throw new Error('No token received')
  },
}

