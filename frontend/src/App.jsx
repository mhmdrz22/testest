import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import AdminPanel from './pages/AdminPanel'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState(null)

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token')
    if (token) {
      setIsLoggedIn(true)
      // Fetch user info
      const userName = localStorage.getItem('username')
      setUser(userName)
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setIsLoggedIn(false)
    setUser(null)
  }

  return (
    <BrowserRouter>
      <div className="app">
        <nav className="navbar">
          <div className="navbar-brand">
            <h1>📋 Task Board</h1>
          </div>
          <div className="navbar-menu">
            {isLoggedIn && (
              <>
                <span className="user-info">👤 {user}</span>
                <button className="logout-btn" onClick={handleLogout}>
                  خروج
                </button>
              </>
            )}
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
