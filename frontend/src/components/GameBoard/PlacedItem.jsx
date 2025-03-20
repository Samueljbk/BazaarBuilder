// src/components/GameBoard/PlacedItem.jsx
import React, { useState, useRef, useEffect } from 'react';
import ItemTooltip from '../ItemTooltip/ItemTooltip';
import { fetchItemById } from '../../api/items';
import { getItemImagePath } from '../../utils/imageUtils';
import './styles.css';

const PlacedItem = ({ item, onRemove, slotsOccupied = 1 }) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipStyle, setTooltipStyle] = useState({});
  const [itemDetails, setItemDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const tooltipTimeoutRef = useRef(null);
  const itemRef = useRef(null);
  
  // Fetch detailed item data when needed
  useEffect(() => {
    // Only fetch details if we don't have them and tooltip is shown
    if (showTooltip && !itemDetails && !loading) {
      const fetchDetails = async () => {
        try {
          setLoading(true);
          const details = await fetchItemById(item.id);
          console.log('Fetched item details:', details);
          setItemDetails(details);
        } catch (error) {
          console.error('Failed to fetch item details:', error);
        } finally {
          setLoading(false);
        }
      };
      
      fetchDetails();
    }
  }, [showTooltip, item.id, itemDetails, loading]);
  
  // Use either the fetched details or the original item
  const displayItem = itemDetails || item;
  
  // Clean up any size display issues
  const cleanSize = displayItem.size ? displayItem.size.toString().toLowerCase() : 'small';
  
  // Get the image path based on item name
  const imagePath = getItemImagePath(displayItem.name);
  
  // Position tooltip method - separated for clarity
  const positionTooltip = () => {
    if (!itemRef.current) return;
    
    const rect = itemRef.current.getBoundingClientRect();
    const windowHeight = window.innerHeight;
    
    // Position tooltip above the item by default
    setTooltipStyle({
      position: 'fixed',
      bottom: `${window.innerHeight - rect.top + 10}px`,
      left: `${rect.left + (rect.width / 2)}px`,
      transform: 'translateX(-50%)',
      zIndex: 2000
    });
  };
  
  // Handle tooltip visibility with debounce
  const handleMouseEnter = () => {
    clearTimeout(tooltipTimeoutRef.current);
    tooltipTimeoutRef.current = setTimeout(() => {
      setShowTooltip(true);
      // Position after a brief delay to ensure content is stable
      setTimeout(positionTooltip, 50);
    }, 100);
  };
  
  const handleMouseLeave = () => {
    clearTimeout(tooltipTimeoutRef.current);
    tooltipTimeoutRef.current = setTimeout(() => {
      setShowTooltip(false);
    }, 100);
  };
  
  // Clean up timeout on unmount
  useEffect(() => {
    return () => {
      if (tooltipTimeoutRef.current) {
        clearTimeout(tooltipTimeoutRef.current);
      }
    };
  }, []);
  
  // Set class based on slots occupied
  const itemWidthClass = `placed-item item-width-${slotsOccupied}`;
  
  return (
    <div 
      ref={itemRef}
      className={itemWidthClass}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="item-content">
        <img 
          src={displayItem.image_url || imagePath} 
          alt={displayItem.name}
          className="item-image"
          onError={(e) => {
            e.target.onerror = null;
            // Try default.avif first
            e.target.src = '/assets/images/items/default.avif';
            // If default.avif fails, fall back to default.png
            e.target.onerror = () => {
              e.target.src = '/assets/images/items/default.png';
              e.target.onerror = null;
            };
          }}
        />
        {/* Removed item name display */}
      </div>
      
      {/* Button positioned at top right */}
      <button 
        className="remove-item-btn"
        onClick={(e) => {
          e.stopPropagation();
          onRemove(displayItem.id);
        }}
      >
        ×
      </button>
      
      {showTooltip && (
        <div style={tooltipStyle} className="stable-tooltip">
          <ItemTooltip 
            item={{
              ...displayItem,
              // Fix the size display by removing "None"
              size: cleanSize
            }}
            loading={loading && !itemDetails}
          />
        </div>
      )}
    </div>
  );
};

export default PlacedItem;