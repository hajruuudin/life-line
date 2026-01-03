export const auth = {
  getToken() {
    return localStorage.getItem('token')
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  },

  login(token) {
    localStorage.setItem('token', token)
  },

  logout() {
    localStorage.removeItem('token')
  }
}
