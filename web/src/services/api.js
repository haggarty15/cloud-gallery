/**
 * API service for backend communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Get public gallery images
 */
export const getGallery = async (page = 1, limit = 20, sort = 'newest') => {
  try {
    const response = await api.get('/api/gallery', {
      params: { page, limit, sort },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch gallery');
  }
};

/**
 * Get image details
 */
export const getImage = async (imageId, token = null) => {
  try {
    const config = token
      ? { headers: { Authorization: `Bearer ${token}` } }
      : {};
    const response = await api.get(`/api/images/${imageId}`, config);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch image');
  }
};

/**
 * Upload image
 */
export const uploadImage = async (file, title, description, token) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    if (title) formData.append('title', title);
    if (description) formData.append('description', description);

    const response = await api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to upload image');
  }
};

/**
 * Get user's uploads
 */
export const getUserUploads = async (token, status = null, page = 1, limit = 20) => {
  try {
    const response = await api.get('/api/uploads', {
      params: { status, page, limit },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch uploads');
  }
};

/**
 * Delete image
 */
export const deleteImage = async (imageId, token) => {
  try {
    const response = await api.delete(`/api/images/${imageId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to delete image');
  }
};

/**
 * Get pending images (admin only)
 */
export const getPendingImages = async (token, page = 1, limit = 20) => {
  try {
    const response = await api.get('/api/admin/pending', {
      params: { page, limit },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch pending images');
  }
};

/**
 * Approve image (admin only)
 */
export const approveImage = async (imageId, token) => {
  try {
    const response = await api.post(`/api/admin/approve/${imageId}`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to approve image');
  }
};

/**
 * Reject image (admin only)
 */
export const rejectImage = async (imageId, reason, token) => {
  try {
    const response = await api.post(
      `/api/admin/reject/${imageId}`,
      { reason },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to reject image');
  }
};

export default api;
