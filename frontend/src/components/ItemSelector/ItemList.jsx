// src/components/ItemSelector/ItemList.jsx
import React from 'react';
import ItemCard from './ItemCard';
import './styles.css';

const ItemList = ({ items, onItemSelect }) => {
  return (
    <div className="item-list">
      {items.map((item) => (
        <ItemCard 
          key={item.id} 
          item={item} 
          onItemSelect={onItemSelect}
        />
      ))}
    </div>
  );
};

export default ItemList;