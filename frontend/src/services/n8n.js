import api from './api';

export const n8nService = {
  async getAuthorizationUrl() {
    const response = await api.get('/api/n8n/auth-url');
    return response.data.authorization_url;
  },
};
