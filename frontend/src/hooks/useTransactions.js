import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

export function useTransactions() {
  const [transactions, setTransactions] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({
    debitCredit: 'Debit',
    dateFrom: null,
    dateTo: null,
  })

  useEffect(() => {
    fetchData()
  }, [filters])

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const transactionParams = new URLSearchParams()
      if (filters.debitCredit) transactionParams.append('debit_credit', filters.debitCredit)
      if (filters.dateFrom) transactionParams.append('date_from', filters.dateFrom)
      if (filters.dateTo) transactionParams.append('date_to', filters.dateTo)
      
      const [transactionsResponse, categoriesResponse] = await Promise.all([
        axios.get(`${API_BASE}/transactions?${transactionParams.toString()}`),
        axios.get(`${API_BASE}/categories`)
      ])
      
      setTransactions(transactionsResponse.data)
      setCategories(categoriesResponse.data)
    } catch (err) {
      setError('Failed to load transactions')
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const updateTransactionCategory = async (transactionId, categoryId) => {
    try {
      await axios.put(`${API_BASE}/transactions/${transactionId}/category`, { category_id: categoryId })
      // Refresh transactions to show updated categorization
      fetchData()
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Failed to update category')
    }
  }

  return { transactions, categories, loading, error, filters, setFilters: handleFilterChange, updateTransactionCategory }
}