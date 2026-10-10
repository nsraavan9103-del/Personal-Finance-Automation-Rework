import React, { createContext, useContext, useState, useCallback } from 'react'
import axios from 'axios'

const API_BASE = '/api'

const TransactionContext = createContext(null)

export function TransactionProvider({ children }) {
  const [transactions, setTransactions] = useState([])
  const [categories, setCategories] = useState([])
  const [refreshKey, setRefreshKey] = useState(0)

  const fetchTransactions = useCallback(async (params = {}) => {
    try {
      const paramsObj = new URLSearchParams()
      if (params.debitCredit) paramsObj.append('debit_credit', params.debitCredit)
      if (params.dateFrom) paramsObj.append('date_from', params.dateFrom)
      if (params.dateTo) paramsObj.append('date_to', params.dateTo)

      const response = await axios.get(`${API_BASE}/transactions?${paramsObj.toString()}`)
      return response.data
    } catch (err) {
      console.error('Failed to fetch transactions:', err)
      throw err
    }
  }, [])

  const fetchCategories = useCallback(async () => {
    try {
      const response = await axios.get(`${API_BASE}/categories`)
      return response.data
    } catch (err) {
      console.error('Failed to fetch categories:', err)
      throw err
    }
  }, [])

  const fetchSummary = useCallback(async () => {
    try {
      const response = await axios.get(`${API_BASE}/transactions/summary`)
      return response.data
    } catch (err) {
      console.error('Failed to fetch summary:', err)
      throw err
    }
  }, [])

  const refreshData = useCallback(() => {
    setRefreshKey(prev => prev + 1)
  }, [])

  const updateTransactionCategory = useCallback(async (transactionId, categoryId) => {
    await axios.put(`${API_BASE}/transactions/${transactionId}/category`, null, {
      params: { category_id: categoryId }
    })
    refreshData()
  }, [refreshData])

  const value = {
    transactions,
    setTransactions,
    categories,
    setCategories,
    refreshKey,
    fetchTransactions,
    fetchCategories,
    fetchSummary,
    refreshData,
    updateTransactionCategory
  }

  return (
    <TransactionContext.Provider value={value}>
      {children}
    </TransactionContext.Provider>
  )
}

export function useTransactions() {
  const context = useContext(TransactionContext)
  if (!context) {
    throw new Error('useTransactions must be used within a TransactionProvider')
  }
  return context
}