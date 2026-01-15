export const auth = {
  getToken() {
    return localStorage.getItem('token')
  },

  getUserId() {
    return localStorage.getItem('userId')
  },

  getUserEmail() {
    return localStorage.getItem('userEmail')
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  },

  login(token, userId, userEmail) {
    localStorage.setItem('token', token)
    if (userId) localStorage.setItem('userId', userId)
    if (userEmail) localStorage.setItem('userEmail', userEmail)
  },

  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
    localStorage.removeItem('userEmail')
  }
}
