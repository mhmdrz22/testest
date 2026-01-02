import React, { useState, useEffect } from 'react';
import './AdminPanel.css';

function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState(new Set());
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchUserOverview();
  }, []);

  async function fetchUserOverview() {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/overview/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      if (!response.ok) throw new Error('Failed to fetch users');
      const data = await response.json();
      setUsers(data);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function toggleUser(userId) {
    const newSelected = new Set(selectedUsers);
    if (newSelected.has(userId)) {
      newSelected.delete(userId);
    } else {
      newSelected.add(userId);
    }
    setSelectedUsers(newSelected);
  }

  function selectAll() {
    if (selectedUsers.size === users.length) {
      setSelectedUsers(new Set());
    } else {
      setSelectedUsers(new Set(users.map(u => u.id)));
    }
  }

  async function handleSendEmail() {
    if (selectedUsers.size === 0) {
      setError('Please select at least one user');
      return;
    }
    if (!message.trim()) {
      setError('Please enter a message');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setSuccess('');
      
      const recipients = users
        .filter(u => selectedUsers.has(u.id))
        .map(u => u.email);

      const response = await fetch('/api/admin/notify/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          recipients,
          message: message.trim(),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send email');
      }

      const data = await response.json();
      setSuccess(`Email queued successfully! Job ID: ${data.job_id}`);
      setMessage('');
      setSelectedUsers(new Set());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="admin-panel">
      <header className="admin-header">
        <h1>Admin Panel</h1>
        <p>Manage users and send email notifications</p>
      </header>

      {error && <div className="error-box">{error}</div>}
      {success && <div className="success-box">{success}</div>}

      <section className="panel">
        <div className="panel-head">
          <h2 className="panel-title">Users Overview</h2>
          <p className="panel-subtitle">
            {selectedUsers.size} of {users.length} users selected
          </p>
        </div>

        {loading && !users.length ? (
          <div className="info-box">Loading users...</div>
        ) : (
          <div className="table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>
                    <input
                      type="checkbox"
                      checked={selectedUsers.size === users.length && users.length > 0}
                      onChange={selectAll}
                    />
                  </th>
                  <th>Email</th>
                  <th>Username</th>
                  <th>Open Tasks</th>
                  <th>Total Tasks</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id} className={selectedUsers.has(user.id) ? 'selected' : ''}>
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedUsers.has(user.id)}
                        onChange={() => toggleUser(user.id)}
                      />
                    </td>
                    <td>{user.email}</td>
                    <td>{user.username}</td>
                    <td>{user.open_tasks || 0}</td>
                    <td>{user.total_tasks || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="panel">
        <div className="panel-head">
          <h2 className="panel-title">Send Email Notification</h2>
          <p className="panel-subtitle">Compose message using Markdown</p>
        </div>

        <div className="form-field full-width">
          <label>Message (Markdown supported)</label>
          <textarea
            className="markdown-editor"
            rows="10"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="# Hello!\n\nThis is a reminder about your open tasks...\n\n- Task 1\n- Task 2"
          />
        </div>

        <div className="form-actions">
          <button
            onClick={handleSendEmail}
            disabled={loading || selectedUsers.size === 0 || !message.trim()}
          >
            {loading ? 'Sending...' : 'Send Email to Selected Users'}
          </button>
        </div>
      </section>
    </div>
  );
}

export default AdminPanel;
