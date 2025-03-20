// src/api/items.js
import apiClient, { handleApiError } from './index';

/**
 * Fetch all items, with optional filtering
 * @param {Object} params - Query parameters
 * @param {number} params.hero_id - Filter by hero ID
 * @param {string} params.size - Filter by item size
 * @param {string} params.type - Filter by item type
 * @returns {Promise<Array>} - List of items
 */
export const fetchItems = async (params = {}) => {
  try {
    console.log('Fetching items with params:', params);
    
    // Make request with no pagination limits
    const response = await apiClient.get('/items/', { 
      params: {
        ...params,
        limit: 1000,  // Request a large number to ensure we get all items
      } 
    });
    
    console.log('API Response status:', response.status);
    
    // Check if we got data
    if (!response.data) {
      console.error('No data in response:', response);
      return [];
    }
    
    // Determine the shape of the data
    let items = [];
    
    if (Array.isArray(response.data)) {
      items = response.data;
    } else if (response.data.items && Array.isArray(response.data.items)) {
      items = response.data.items;
    } else if (response.data.data && Array.isArray(response.data.data)) {
      items = response.data.data;
    } else {
      // Check if any property is an array
      for (const key in response.data) {
        if (Array.isArray(response.data[key])) {
          items = response.data[key];
          break;
        }
      }
    }
    
    console.log(`Extracted ${items.length} items from response`);
    
    return items;
  } catch (error) {
    console.error('Error fetching items:', error);
    return handleApiError(error);
  }
};

/**
 * Fetch a single item by ID
 * @param {number} itemId - The ID of the item to fetch
 * @returns {Promise<Object>} - Item data
 */
export const fetchItemById = async (itemId) => {
  try {
    const response = await apiClient.get(`/items/${itemId}`);
    return response.data;
  } catch (error) {
    return handleApiError(error);
  }
};