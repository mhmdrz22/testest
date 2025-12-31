import React, { useState } from 'react'
import TaskList from '../components/TaskList'
import TaskForm from '../components/TaskForm'
import { useTasks } from '../hooks/useTasks'
import './Dashboard.css'

function Dashboard() {
  const { tasks, loading, error, addTask, updateTask, deleteTask } = useTasks()
  const [showForm, setShowForm] = useState(false)
  const [filter, setFilter] = useState('all')

  const filteredTasks = tasks.filter((task) => {
    if (filter === 'all') return true
    return task.status === filter
  })

  const handleAddTask = async (taskData) => {
    try {
      await addTask(taskData)
      setShowForm(false)
    } catch (err) {
      console.error('Failed to add task:', err)
    }
  }

  const handleUpdateTask = async (id, updates) => {
    try {
      await updateTask(id, updates)
    } catch (err) {
      console.error('Failed to update task:', err)
    }
  }

  const handleDeleteTask = async (id) => {
    try {
      await deleteTask(id)
    } catch (err) {
      console.error('Failed to delete task:', err)
    }
  }

  return (
    <main>
      <div className="dashboard-header">
        <h2>📋 Task Dashboard</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? '✕ Close' : '+ New Task'}
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {showForm && (
        <div className="form-container">
          <TaskForm onSubmit={handleAddTask} onCancel={() => setShowForm(false)} />
        </div>
      )}

      <div className="filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Tasks ({tasks.length})
        </button>
        <button
          className={`filter-btn ${filter === 'open' ? 'active' : ''}`}
          onClick={() => setFilter('open')}
        >
          Open ({tasks.filter((t) => t.status === 'open').length})
        </button>
        <button
          className={`filter-btn ${filter === 'in_progress' ? 'active' : ''}`}
          onClick={() => setFilter('in_progress')}
        >
          In Progress ({tasks.filter((t) => t.status === 'in_progress').length})
        </button>
        <button
          className={`filter-btn ${filter === 'closed' ? 'active' : ''}`}
          onClick={() => setFilter('closed')}
        >
          Closed ({tasks.filter((t) => t.status === 'closed').length})
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading tasks...</div>
      ) : filteredTasks.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">📭</div>
          <p>No tasks found</p>
        </div>
      ) : (
        <TaskList
          tasks={filteredTasks}
          onUpdateTask={handleUpdateTask}
          onDeleteTask={handleDeleteTask}
        />
      )}
    </main>
  )
}

export default Dashboard
