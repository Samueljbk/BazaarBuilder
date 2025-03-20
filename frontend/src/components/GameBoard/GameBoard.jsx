// src/components/GameBoard/GameBoard.jsx
import React, { useState } from 'react';
import ItemSlot from './ItemSlot';
import ItemSelector from '../ItemSelector/ItemSelector';
import './styles.css';

const GameBoard = () => {
  const [placedItems, setPlacedItems] = useState({}); // Maps slot index to item
  const [showSelector, setShowSelector] = useState(false);
  const [currentSlot, setCurrentSlot] = useState(null);
  const totalSlots = 10;
  
  // Size map for slot calculations
  const sizeMap = {
    'small': 1, 
    'medium': 2, 
    'large': 3,
    'Small': 1, 
    'Medium': 2, 
    'Large': 3
  };
  
  // Calculate used and occupied slots
  const calculateBoardState = () => {
    let usedSlots = 0;
    const occupiedSlotIndexes = new Set();
    
    // For each item, calculate slots it occupies
    Object.entries(placedItems).forEach(([slotIndex, item]) => {
      const startSlot = parseInt(slotIndex);
      const size = item.size?.toString() || 'small';
      const slotsNeeded = sizeMap[size] || 1;
      
      usedSlots += slotsNeeded;
      
      // Mark all slots this item occupies
      for (let i = 0; i < slotsNeeded; i++) {
        occupiedSlotIndexes.add(startSlot + i);
      }
    });
    
    return { usedSlots, occupiedSlotIndexes };
  };
  
  const { usedSlots, occupiedSlotIndexes } = calculateBoardState();
  const remainingSlots = totalSlots - usedSlots;
  
  // Check if a slot can be used to place an item of a specific size
  const canPlaceItemAtSlot = (slotIndex, itemSize) => {
    const slotsNeeded = sizeMap[itemSize] || 1;
    
    // Check if any of the slots needed are already occupied
    for (let i = 0; i < slotsNeeded; i++) {
      const checkSlot = slotIndex + i;
      if (checkSlot >= totalSlots || occupiedSlotIndexes.has(checkSlot)) {
        return false;
      }
    }
    
    return true;
  };
  
  // Handler for adding an item to the board
  const handleAddItem = (item) => {
    if (currentSlot !== null) {
      const itemSize = item.size?.toString().toLowerCase() || 'small';
      
      // Check if we can place this item at the selected slot
      if (canPlaceItemAtSlot(currentSlot, itemSize)) {
        setPlacedItems(prev => ({
          ...prev,
          [currentSlot]: item
        }));
      } else {
        console.log("Can't place item here - not enough space");
        // You could add an alert or visual feedback here
      }
      
      setShowSelector(false);
      setCurrentSlot(null);
    }
  };
  
  // Handler for removing an item from the board
  const handleRemoveItem = (slotIndex) => {
    setPlacedItems(prev => {
      const newItems = { ...prev };
      delete newItems[slotIndex];
      return newItems;
    });
  };
  
  // Handler for opening the item selector
  const handleSlotClick = (index) => {
    // Only allow clicking empty slots
    if (!occupiedSlotIndexes.has(index)) {
      setCurrentSlot(index);
      setShowSelector(true);
    }
  };
  
  // Render slot components
  const renderSlots = () => {
    const slots = [];
    
    for (let i = 0; i < totalSlots; i++) {
      // Check if this slot is the starting position of an item
      const hasItemStart = placedItems[i] !== undefined;
      
      // Check if this slot is occupied by an item that starts at an earlier slot
      const isPartOfItem = occupiedSlotIndexes.has(i) && !hasItemStart;
      
      // Only render a visible slot if it's not part of another item
      if (!isPartOfItem) {
        const item = placedItems[i];
        const itemSize = item ? (item.size?.toString().toLowerCase() || 'small') : null;
        const slotsOccupied = item ? (sizeMap[itemSize] || 1) : 1;
        
        slots.push(
          <ItemSlot 
            key={i} 
            index={i}
            item={item}
            slotsOccupied={slotsOccupied}
            onSlotClick={handleSlotClick}
            onRemoveItem={handleRemoveItem}
          />
        );
      } else {
        // Add an invisible placeholder for slots that are part of larger items
        slots.push(<div key={i} className="slot-placeholder"></div>);
      }
    }
    
    return slots;
  };
  
  return (
    <div className="game-board-container">
      <h2 className="game-board-title">Game Board</h2>
      
      <div className="slots-info">
        <div className="slots-used">
          Slots Used: {usedSlots}/{totalSlots}
        </div>
        <div className="slots-remaining">
          Slots Remaining: {remainingSlots}
        </div>
      </div>
      
      <div className="game-board">
        {renderSlots()}
      </div>
      
      {showSelector && (
        <ItemSelector 
          onSelect={handleAddItem}
          onCancel={() => setShowSelector(false)}
          remainingSlots={remainingSlots}
        />
      )}
    </div>
  );
};

export default GameBoard;