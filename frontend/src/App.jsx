// src/App.jsx
import React from 'react';
import GameBoard from './components/GameBoard/GameBoard';
import './index.css';

const App = () => {
  return (
    <div className="app">
      <header style={{ padding: '20px', backgroundColor: 'var(--primary-color)' }}>
        <h1>The Bazaar Game Assistant</h1>
      </header>
      
      <main style={{ padding: '20px' }}>
        <div className="container">
          <h2>Build Planner</h2>
          <p>Create your build by adding items to the board below.</p>
          
          <GameBoard />
        </div>
      </main>
      
      <footer style={{ 
        padding: '15px', 
        backgroundColor: 'var(--primary-color)', 
        textAlign: 'center',
        marginTop: '20px'
      }}>
        <p>&copy; {new Date().getFullYear()} The Bazaar Game Assistant</p>
      </footer>
    </div>
  );
};

export default App;