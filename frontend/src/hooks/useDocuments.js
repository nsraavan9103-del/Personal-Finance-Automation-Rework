import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

export function useDocuments() {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchDocuments = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE}/documents`)
      setDocuments(response.data)
    } catch (err) {
      setError('Failed to load documents')
    } finally {
      setLoading(false)
    }
  }

  const deleteDocument = async (id) => {
    try {
      await axios.delete(`${API_BASE}/documents/${id}`)
      fetchDocuments()
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Failed to delete document')
    }
  }

  useEffect(() => {
    fetchDocuments()
  }, [])

  return { documents, loading, error, fetchDocuments, deleteDocument }
}