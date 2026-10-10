import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

export function useCategories() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.get(`${API_BASE}/categories`)
      setCategories(response.data)
    } catch (err) {
      setError('Failed to load categories')
    } finally {
      setLoading(false)
    }
  }

  const addCategory = async (name) => {
    try {
      const response = await axios.post(`${API_BASE}/categories`, { name })
      setCategories([...categories, response.data])
      return response.data
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Failed to add category')
    }
  }

  const deleteCategory = async (id) => {
    try {
      await axios.delete(`${API_BASE}/categories/${id}`)
      setCategories(categories.filter(cat => cat.id !== id))
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Failed to delete category')
    }
  }

  return { categories, loading, error, addCategory, deleteCategory }
}