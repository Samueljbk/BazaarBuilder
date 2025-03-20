// src/api/heroes.js
import apiClient, { handleApiError } from './index';

/**
 * Fetch all heroes
 * @returns {Promise<Array>} - List of heroes
 */
export const fetchHeroes = async () => {
  try {
    const response = await apiClient.get('/heroes/');
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};

/**
 * Fetch a single hero by ID
 * @param {number} heroId - The ID of the hero to fetch
 * @returns {Promise<Object>} - Hero data
 */
export const fetchHeroById = async (heroId) => {
  try {
    const response = await apiClient.get(`/heroes/${heroId}`);
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};