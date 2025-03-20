// src/components/ItemTooltip/ItemTooltip.jsx
import React from 'react';
import './styles.css';

const ItemTooltip = ({ item, loading }) => {
  if (loading) {
    return (
      <div className="item-tooltip loading">
        <div className="tooltip-loading">Loading item details...</div>
      </div>
    );
  }
  
  // Clean the size property to remove "None"
  const cleanSize = (sizeValue) => {
    if (!sizeValue) return 'Small';
    return sizeValue.toString().replace(/\s*None\s*/g, '').trim() || 'Small';
  };
  
  const displaySize = cleanSize(item.size);
  
  return (
    <div className="item-tooltip">
      <div className="tooltip-header">
        <h3 className="tooltip-title">{item.name}</h3>
      </div>
      
      <div className="tooltip-body">
        <div className="tooltip-row">
          <span className="tooltip-label">Type:</span>
          <span className="tooltip-value">{displaySize}</span>
        </div>
        
        {item.cooldown && (
          <div className="tooltip-row">
            <span className="tooltip-label">Cooldown:</span>
            <span className="tooltip-value">{item.cooldown} seconds</span>
          </div>
        )}
        
        {item.effect && (
          <div className="tooltip-row">
            <span className="tooltip-label">Effect:</span>
            <span className="tooltip-value">{item.effect}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ItemTooltip;