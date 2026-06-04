import React, { useState } from 'react'
import Customers from './components/Customers'
import Accounts from './components/Accounts'
import './styles/App.css'

function App() {
  const [activeTab, setActiveTab] = useState('customers')

  return (
    <div className="app">
      <nav className="app-nav" aria-label="View selector">
        <button
          className={`nav-btn ${activeTab === 'customers' ? 'active' : ''}`}
          onClick={() => setActiveTab('customers')}
        >
          Customers
        </button>
        <button
          className={`nav-btn ${activeTab === 'accounts' ? 'active' : ''}`}
          onClick={() => setActiveTab('accounts')}
        >
          Accounts
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'customers' && <Customers />}
        {activeTab === 'accounts' && <Accounts />}
      </main>

      <footer className="app-footer">
        <p>Banking REST API | React + Flask + MongoDB Atlas</p>
      </footer>
    </div>
  )
}

export default App
