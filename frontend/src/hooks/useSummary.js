import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

export function useSummary() {
  const [summary, setSummary] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSummary()
  }, [])

  const fetchSummary = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.get(`${API_BASE}/transactions/summary`)
      setSummary(response.data)
    } catch (err) {
      setError('Failed to load summary')
    } finally {
      setLoading(false)
    }
  }

  return { summary, loading, error, refetch: fetchSummary }
}