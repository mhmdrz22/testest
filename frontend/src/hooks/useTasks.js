import { useState, useEffect } from 'react'
import { taskAPI } from '../services/api'

export const useTasks = () => {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchTasks = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await taskAPI.getTasks()
      setTasks(response.data)
    } catch (err) {
      setError(err.message || 'Failed to fetch tasks')
    } finally {
      setLoading(false)
    }
  }

  const addTask = async (taskData) => {
    try {
      const response = await taskAPI.createTask(taskData)
      setTasks([...tasks, response.data])
      return response.data
    } catch (err) {
      setError(err.message || 'Failed to create task')
      throw err
    }
  }

  const updateTask = async (id, updates) => {
    try {
      const response = await taskAPI.updateTask(id, updates)
      setTasks(tasks.map((task) => (task.id === id ? response.data : task)))
      return response.data
    } catch (err) {
      setError(err.message || 'Failed to update task')
      throw err
    }
  }

  const deleteTask = async (id) => {
    try {
      await taskAPI.deleteTask(id)
      setTasks(tasks.filter((task) => task.id !== id))
    } catch (err) {
      setError(err.message || 'Failed to delete task')
      throw err
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    addTask,
    updateTask,
    deleteTask,
  }
}
