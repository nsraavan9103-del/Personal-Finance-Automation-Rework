import React, { useState, useEffect, useContext } from 'react'
import { useTransactions } from '../context/TransactionContext'

function SummaryTable() {
  const { refreshKey, fetchSummary } = useTransactions()
  const [summary, setSummary] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSummaryData()
  }, [refreshKey])

  const fetchSummaryData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetchSummary()
      setSummary(response)
    } catch (err) {
      setError('Failed to load summary')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4">Expense Summary</h2>
      
      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {/* Summary Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {summary.length > 0 ? (
              summary.map(item => (
                <tr key={item.category} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.category}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    AED {parseFloat(item.total_amount).toFixed(2)}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td className="px-6 py-4 text-center text-gray-500" colSpan={2}>
                  No expense data found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {/* Total Expenses */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-lg font-semibold text-right">
          Total Expenses: AED {summary.reduce((sum, item) => sum + parseFloat(item.total_amount), 0).toFixed(2)}
        </p>
      </div>
    </div>
  )
}

export default SummaryTable