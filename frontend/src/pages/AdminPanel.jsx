import React, { useState, useEffect } from 'react'
import { adminAPI, userAPI } from '../services/api'
import './AdminPanel.css'

function AdminPanel() {
  const [users, setUsers] = useState([])
  const [emailData, setEmailData] = useState({
    subject: '',
    body: '',
    recipients: [],
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await userAPI.getUsers()
      setUsers(response.data)
    } catch (err) {
      setError('Failed to fetch users')
    }
  }

  const handleEmailChange = (e) => {
    const { name, value } = e.target
    setEmailData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleRecipientToggle = (userId) => {
    setEmailData((prev) => ({
      ...prev,
      recipients: prev.recipients.includes(userId)
        ? prev.recipients.filter((id) => id !== userId)
        : [...prev.recipients, userId],
    }))
  }

  const handleSendEmail = async (e) => {
    e.preventDefault()
    if (emailData.recipients.length === 0) {
      setError('Please select at least one recipient')
      return
    }

    setLoading(true)
    setError('')
    setMessage('')

    try {
      await adminAPI.sendNotification(emailData)
      setMessage('Email sent successfully!')
      setEmailData({ subject: '', body: '', recipients: [] })
      setTimeout(() => setMessage(''), 3000)
    } catch (err) {
      setError('Failed to send email')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main>
      <div className="admin-header">
        <h2>🔐 Admin Panel</h2>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {message && <div className="alert alert-success">{message}</div>}

      <div className="admin-grid">
        {/* Users Section */}
        <div className="card">
          <div className="card-header">
            <h3>👥 Users ({users.length})</h3>
          </div>
          <div className="card-body">
            {users.length === 0 ? (
              <p>No users found</p>
            ) : (
              <ul className="users-list">
                {users.map((user) => (
                  <li key={user.id} className="user-item">
                    <span className="user-name">{user.username || user.email}</span>
                    <span className="user-email">{user.email}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Email Sender Section */}
        <div className="card">
          <div className="card-header">
            <h3>✉️ Send Email Notification</h3>
          </div>
          <div className="card-body">
            <form onSubmit={handleSendEmail}>
              <div className="form-group">
                <label className="form-label">Subject</label>
                <input
                  type="text"
                  name="subject"
                  className="form-input"
                  value={emailData.subject}
                  onChange={handleEmailChange}
                  placeholder="Email subject"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Message Body</label>
                <textarea
                  name="body"
                  className="form-textarea"
                  value={emailData.body}
                  onChange={handleEmailChange}
                  placeholder="Write your message here..."
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Recipients</label>
                <div className="recipients-list">
                  {users.length === 0 ? (
                    <p>No users available</p>
                  ) : (
                    users.map((user) => (
                      <label key={user.id} className="checkbox-item">
                        <input
                          type="checkbox"
                          checked={emailData.recipients.includes(user.id)}
                          onChange={() => handleRecipientToggle(user.id)}
                        />
                        <span>{user.username || user.email}</span>
                      </label>
                    ))
                  )}
                </div>
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Sending...' : 'Send Email'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </main>
  )
}

export default AdminPanel
