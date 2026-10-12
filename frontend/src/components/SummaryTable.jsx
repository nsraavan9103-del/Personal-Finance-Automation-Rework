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
    <div className="bg-ink-800 border border-ink-600 rounded-xl p-6">
      <h2 className="font-display text-xl font-bold mb-4 text-mist-100">Expense Summary</h2>
      
      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-rose-500/10 border border-rose-500/20 text-rose-300 rounded">
          {error}
        </div>
      )}
      
      {/* Summary Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-ink-600">
          <thead className="bg-ink-900">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-mist-500 uppercase tracking-wider">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-mist-500 uppercase tracking-wider">Amount</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-ink-600">
            {summary.length > 0 ? (
              summary.map(item => (
                <tr key={item.category} className="hover:bg-ink-900">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-mist-100">
                    {item.category}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap font-display text-sm text-brass-300 tnum">
                    AED {parseFloat(item.total_amount).toFixed(2)}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td className="px-6 py-4 text-center text-mist-500" colSpan={2}>
                  No expense data found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {/* Total Expenses */}
      <div className="mt-4 pt-4 border-t border-ink-600">
        <p className="font-display text-lg font-bold text-right text-brass-300 tnum">
          Total Expenses: AED {summary.reduce((sum, item) => sum + parseFloat(item.total_amount), 0).toFixed(2)}
        </p>
      </div>
    </div>
  )
}

export default SummaryTable