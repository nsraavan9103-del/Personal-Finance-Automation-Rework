import React, { useState, useEffect, useMemo } from 'react'
import { useTransactions } from '../context/TransactionContext'

function TransactionTable({ initialDebitCredit = 'Debit' }) {
  const { transactions, setTransactions, categories, setCategories, refreshKey, fetchTransactions, fetchCategories, updateTransactionCategory } = useTransactions()
  const [debitCreditFilter, setDebitCreditFilter] = useState(initialDebitCredit)
  const [dateFrom, setDateFrom] = useState(null)
  const [dateTo, setDateTo] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchData()
  }, [debitCreditFilter, dateFrom, dateTo, refreshKey])

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const transactionParams = new URLSearchParams()
      if (debitCreditFilter) transactionParams.append('debit_credit', debitCreditFilter)
      if (dateFrom) transactionParams.append('date_from', dateFrom)
      if (dateTo) transactionParams.append('date_to', dateTo)
      
      const [transactionsResponse, categoriesResponse] = await Promise.all([
        fetchTransactions({ debitCredit: debitCreditFilter, dateFrom, dateTo }),
        fetchCategories()
      ])
      
      setTransactions(transactionsResponse)
      setCategories(categoriesResponse)
    } catch (err) {
      setError('Failed to load transactions')
    } finally {
      setLoading(false)
    }
  }

  const handleDebitCreditChange = (e) => {
    setDebitCreditFilter(e.target.value)
  }

  const handleDateChange = (type, date) => {
    if (type === 'from') setDateFrom(date)
    else setDateTo(date)
  }

  const handleCategoryChange = async (transactionId, categoryId) => {
    try {
      await updateTransactionCategory(transactionId, categoryId)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update category')
    }
  }

  // Filter transactions based on search query
  const filteredTransactions = useMemo(() => {
    if (!searchQuery.trim()) return transactions
    const query = searchQuery.toLowerCase().trim()
    return transactions.filter(transaction => 
      transaction.details.toLowerCase().includes(query)
    )
  }, [transactions, searchQuery])

  const uncategorizedCategoryId = useMemo(() => {
    const cat = categories.find(c => c.name === 'Uncategorized')
    return cat?.id
  }, [categories])
  
  const formatDate = (dateString) => {
    if (!dateString) return ''
    return new Date(dateString).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
  }

  const formatCurrency = (amount, currency = 'AED') => {
    return currency + ' ' + parseFloat(amount).toFixed(2)
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 gap-4">
        <h2 className="text-xl font-bold text-gray-900">Transactions</h2>
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2 flex-1 sm:flex-none max-w-md">
            <label className="sr-only">Search transactions</label>
            <div className="relative">
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search transactions..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                placeholder="Search by name..."
              />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">Type:</label>
            <select
              value={debitCreditFilter}
              onChange={handleDebitCreditChange}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            >
              <option value="Debit">Expenses (Debits)</option>
              <option value="Credit">Payments (Credits)</option>
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">From:</label>
            <input
              type="date"
              value={dateFrom || ''}
              onChange={(e) => handleDateChange('from', e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">To:</label>
            <input
              type="date"
              value={dateTo || ''}
              onChange={(e) => handleDateChange('to', e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
        </div>
      </div>
      
      {/* Error Message */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg" role="alert">
          <div className="flex items-center gap-3 text-red-800">
            <svg className="w-5 h-5 flex-shrink-0 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L10.586 10l-1.707 1.707a1 1 0 001.414 1.414L10 11.414l1.707 1.707a1 1 0 001.414-1.414L11.414 10l1.707-1.707a1 1 0 00-1.414-1.414L10 8.586 8.293 6.854a1 1 0 00-1.414 0L10 6.586 8.293 5.146a1 1 0 00-1.414 1.414L8.586 10 6.854 11.707a1 1 0 000 1.414z" clipRule="evenodd" />
            </svg>
            <p className="text-red-800 font-medium">{error}</p>
          </div>
        </div>
      )}
      
      {/* Loading State */}
      {loading && (
        <div className="py-12 text-center">
          <div className="flex items-center justify-center gap-3 text-gray-600">
            <svg className="animate-spin h-6 w-6 text-blue-600" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <span>Loading transactions...</span>
          </div>
        </div>
      )}
      
      {/* Transactions Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Details</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredTransactions.length > 0 ? (
              filteredTransactions.map(transaction => (
                <tr key={transaction.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate(transaction.date)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 max-w-xs truncate" title={transaction.details}>
                    {transaction.details}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                    {formatCurrency(transaction.amount, transaction.currency)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <select
                      value={transaction.category_id || ''}
                      onChange={(e) => handleCategoryChange(transaction.id, parseInt(e.target.value))}
                      className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white"
                    >
                      <option value="">Select Category</option>
                      {categories.map(category => (
                        <option key={category.id} value={category.id}>
                          {category.name}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {transaction.category_id && transaction.category_id !== uncategorizedCategoryId ? (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5" />
            Categorized
          </span>
        ) : (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            <span className="w-1.5 h-1.5 bg-yellow-500 rounded-full mr-1.5" />
            Uncategorized
          </span>
        )}
      </td>
                </tr>
              ))
            ) : (
              <tr>
                <td className="px-6 py-12 text-center text-gray-500" colSpan={5}>
                  <div className="flex flex-col items-center gap-3">
                    <svg className="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 012-2h2a2 2 0 012 2v2m-6 9l3 3m0 0l3-3m-3 3V4" />
                    </svg>
                    <p className="text-gray-500">
                      {searchQuery.trim() 
                        ? 'No transactions match your search' 
                        : 'No transactions found'}
                    </p>
                    <p className="text-sm text-gray-400">
                      {searchQuery.trim() 
                        ? 'Try a different search term' 
                        : 'Try adjusting your filters or upload a bank statement'}
                      </p>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default TransactionTable