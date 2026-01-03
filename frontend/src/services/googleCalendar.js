import api from './api'

export const googleCalendarService = {
  async createEvent(data) {
    const response = await api.post('/calendar/events', data)
    return response.data
  },
}

