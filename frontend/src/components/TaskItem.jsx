import React, { useState } from 'react'
import './TaskItem.css'

function TaskItem({ task, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false)
  const [status, setStatus] = useState(task.status)

  const handleStatusChange = async (e) => {
    const newStatus = e.target.value
    setStatus(newStatus)
    try {
      await onUpdate(task.id, { status: newStatus })
      setIsEditing(false)
    } catch (err) {
      setStatus(task.status)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'open':
        return 'status-open'
      case 'in_progress':
        return 'status-progress'
      case 'closed':
        return 'status-closed'
      default:
        return 'status-open'
    }
  }

  const getStatusLabel = (status) => {
    switch (status) {
      case 'open':
        return '🔐 باز'
      case 'in_progress':
        return '⚡ در حال انجام'
      case 'closed':
        return '✓ بسته شده'
      default:
        return status
    }
  }

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' }
    return new Date(dateString).toLocaleDateString('en-US', options)
  }

  return (
    <div className="task-item card">
      <div className="task-header">
        <h3 className="task-title">{task.title}</h3>
        <span className={`task-status ${getStatusColor(task.status)}`}>
          {getStatusLabel(task.status)}
        </span>
      </div>

      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      <div className="task-meta">
        <span className="meta-item">
          <strong>Created by:</strong> {task.created_by_username}
        </span>
        <span className="meta-item">
          <strong>Date:</strong> {formatDate(task.created_at)}
        </span>
      </div>

      <div className="task-actions">
        <select
          value={status}
          onChange={handleStatusChange}
          className="form-select"
        >
          <option value="open">🔐 Open</option>
          <option value="in_progress">⚡ In Progress</option>
          <option value="closed">✓ Closed</option>
        </select>

        <button
          className="btn btn-danger"
          onClick={() => {
            if (window.confirm('Are you sure you want to delete this task?')) {
              onDelete(task.id)
            }
          }}
        >
          🗑 Delete
        </button>
      </div>
    </div>
  )
}

export default TaskItem
