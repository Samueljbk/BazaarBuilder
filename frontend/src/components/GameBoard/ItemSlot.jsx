// src/components/GameBoard/ItemSlot.jsx
import React from 'react';
import PlacedItem from './PlacedItem';
import './styles.css';

const ItemSlot = ({ index, item, slotsOccupied = 1, onSlotClick, onRemoveItem }) => {
  const handleClick = () => {
    if (!item) {
      onSlotClick(index);
    }
  };
  
  const slotClassName = `item-slot ${item ? 'filled' : ''} slot-width-${slotsOccupied}`;
  
  return (
    <div 
      className={slotClassName}
      onClick={handleClick}
      style={{ gridColumn: `span ${slotsOccupied}` }}
    >
      {item ? (
        <PlacedItem 
          item={item} 
          onRemove={() => onRemoveItem(index)} 
          slotsOccupied={slotsOccupied}
        />
      ) : (
        <div className="empty-slot-plus">+</div>
      )}
    </div>
  );
};

export default ItemSlot;