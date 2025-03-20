// src/components/ItemSelector/ItemSelector.jsx
import React, { useState, useEffect } from 'react';
import ItemList from './ItemList';
import './styles.css';
import { fetchItems } from '../../api/items';

const ItemSelector = ({ onSelect, onCancel, heroId, remainingSlots }) => {
  const [items, setItems] = useState([]);
  const [filteredItems, setFilteredItems] = useState([]);
  const [selectedSize, setSelectedSize] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Size options
  const sizeOptions = ['All', 'Small', 'Medium', 'Large'];
  
  // Fetch items from the API
  useEffect(() => {
    const loadItems = async () => {
      try {
        console.log('Loading items from API...');
        setLoading(true);
        setError(null);
        
        // Construct query params
        const params = {};
        if (heroId) params.hero_id = heroId;
        
        console.log('Fetching items with params:', params);
        
        const itemsData = await fetchItems(params);
        console.log('Fetched items data:', itemsData);
        console.log('Total items fetched:', Array.isArray(itemsData) ? itemsData.length : 'Not an array');
        
        // Process the data
        let processedItems = [];
        
        // Case 1: The data itself might be nested inside a property
        if (itemsData && typeof itemsData === 'object' && !Array.isArray(itemsData)) {
          console.log('Data is an object, checking for nested arrays');
          // Check common response formats
          const possibleArrayProps = ['items', 'data', 'results', 'content'];
          for (const prop of possibleArrayProps) {
            if (Array.isArray(itemsData[prop])) {
              console.log(`Found items array in ${prop} property with ${itemsData[prop].length} items`);
              processedItems = itemsData[prop];
              break;
            }
          }
        }
        // Case 2: Standard array response
        else if (Array.isArray(itemsData)) {
          console.log(`Received ${itemsData.length} items as an array`);
          processedItems = itemsData;
        } 
        else {
          console.error('Unexpected data format:', itemsData);
          setError('Received unexpected data format from server');
          setLoading(false);
          return;
        }
        
        // Ensure we have items
        if (processedItems.length === 0) {
          console.warn('No items found in the response');
          setError('No items found. Please try again.');
          setLoading(false);
          return;
        }
        
        // Log some diagnostic information
        console.log(`Processing ${processedItems.length} items`);
        console.log('First item:', processedItems[0]);
        console.log('Available item properties:', Object.keys(processedItems[0]));
        
        // Sort items alphabetically by name
        const sortedItems = [...processedItems].sort((a, b) => {
          const nameA = (a.name || '').toLowerCase();
          const nameB = (b.name || '').toLowerCase();
          return nameA.localeCompare(nameB);
        });
        
        console.log(`Sorted ${sortedItems.length} items alphabetically`);
        console.log('First item after sorting:', sortedItems[0]?.name);
        console.log('Last item after sorting:', sortedItems[sortedItems.length - 1]?.name);
        
        setItems(sortedItems);
        setFilteredItems(sortedItems);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch items:', error);
        setError('Failed to load items. Please try again.');
        setLoading(false);
      }
    };
    
    loadItems();
  }, [heroId]);
  
  // Filter items based on selected filters
  useEffect(() => {
    if (!items || items.length === 0) return;
    
    let result = [...items];
    console.log('Starting filtering with', items.length, 'items');
    
    // Filter by size with better handling of size property
    if (selectedSize !== 'All') {
      console.log('Filtering by size:', selectedSize);
      
      // Case-insensitive comparison with fallback
      result = result.filter(item => {
        // If size is missing, default to unknown
        const itemSize = (item.size || '').toString().trim();
        const matches = itemSize.toLowerCase() === selectedSize.toLowerCase();
        return matches;
      });
      
      console.log('After size filtering:', result.length, 'items remain');
    }
    
    // Filter by search term
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(item => 
        (item.name || '').toLowerCase().includes(term) || 
        (item.description || '').toLowerCase().includes(term)
      );
      console.log('After search filtering:', result.length, 'items remain');
    }
    
    // Filter by remaining slots
    if (remainingSlots !== undefined && remainingSlots !== null) {
      const sizeMap = {
        'small': 1,
        'medium': 2,
        'large': 3,
        'Small': 1,
        'Medium': 2,
        'Large': 3
      };
      
      result = result.filter(item => {
        const itemSize = (item.size || '').toString().trim();
        const slotsRequired = sizeMap[itemSize] || 1;
        return slotsRequired <= remainingSlots;
      });
      console.log('After slots filtering:', result.length, 'items remain');
    }
    
    setFilteredItems(result);
  }, [items, selectedSize, searchTerm, remainingSlots]);
  
  // When user selects a size
  const handleSizeSelect = (size) => {
    console.log('User selected size:', size);
    setSelectedSize(size);
  };
  
  // When user selects an item - immediately add it
  const handleItemSelect = (item) => {
    console.log('Selected item:', item);
    onSelect(item);
  };
  
  return (
    <div className="item-selector-modal">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Add card</h2>
          <button className="close-button" onClick={onCancel}>×</button>
        </div>
        
        <div className="filter-controls">
          {/* Size filter buttons */}
          <div className="size-filter">
            {sizeOptions.map(size => (
              <button 
                key={size}
                className={`size-btn ${selectedSize === size ? 'selected' : ''}`}
                onClick={() => handleSizeSelect(size)}
              >
                {size}
              </button>
            ))}
          </div>
          
          {/* Search box */}
          <div className="search-box">
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
        
        {loading ? (
          <div className="loading-message">Loading items...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : filteredItems.length === 0 ? (
          <div className="no-items-message">
            No items found matching your filters.
            <br />
            <button 
              onClick={() => {
                setSelectedSize('All');
                setSearchTerm('');
              }}
              className="reset-filters-btn"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="items-container">
            <ItemList 
              items={filteredItems}
              onItemSelect={handleItemSelect}
            />
          </div>
        )}
        
        <div className="modal-footer">
          <button className="cancel-btn" onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default ItemSelector;