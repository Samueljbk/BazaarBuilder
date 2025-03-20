// src/utils/imageUtils.js

/**
 * Converts an item name to the corresponding image filename
 * @param {string} itemName - The name of the item (e.g. "Agility Boots")
 * @returns {string} - The image filename (e.g. "AgilityBoots.avif")
 */
export const getItemImageFilename = (itemName) => {
  if (!itemName) return 'default.avif';
  
  // Remove spaces and special characters
  return itemName
    .replace(/[^a-zA-Z0-9]/g, '') // Remove special characters
    .replace(/\s+/g, '') // Remove spaces
    + '.avif';
};

/**
 * Gets the full image path for an item
 * @param {string} itemName - The name of the item
 * @returns {string} - The full image path
 */
export const getItemImagePath = (itemName) => {
  const filename = getItemImageFilename(itemName);
  return `/assets/images/items/${filename}`;
};