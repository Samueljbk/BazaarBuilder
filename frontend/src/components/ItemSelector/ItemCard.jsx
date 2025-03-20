// src/components/ItemSelector/ItemCard.jsx
import React from 'react';
import { getItemImagePath } from '../../utils/imageUtils';
import './styles.css';

const ItemCard = ({ item, onItemSelect }) => {
  const imagePath = getItemImagePath(item.name);

  const handleImageError = (e) => {
    // Fallback to default image if the specific one fails to load
    e.target.src = '/assets/images/items/default.avif';
    // If default.avif doesn't exist, provide a PNG fallback
    e.target.onerror = () => {
      e.target.src = '/assets/images/items/default.png';
      e.target.onerror = null; // Prevent infinite error loop
    };
  };

  const handleCardClick = () => {
    // Log that the card was clicked
    console.log('ItemCard clicked:', item.name);
    // Call the onItemSelect prop with the item
    onItemSelect(item);
  };

  return (
    <div 
      className="item-card" 
      onClick={handleCardClick}
      role="button"
      tabIndex={0}
    >
      <div className="item-image-container">
        <img 
          src={imagePath} 
          alt={item.name}
          onError={handleImageError}
          className="item-image"
        />
      </div>
      <div className="item-details">
        <h3 className="item-name">{item.name}</h3>
      </div>
    </div>
  );
};

export default ItemCard;