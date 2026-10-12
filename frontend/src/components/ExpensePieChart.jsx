import React, { useState, useEffect, useContext } from 'react'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useTransactions } from '../context/TransactionContext'

function ExpensePieChart() {
  const { refreshKey, fetchSummary } = useTransactions()
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchData()
  }, [refreshKey])

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetchSummary()
      // Convert total_amount to number for recharts
      const processedData = response.map(item => ({
        ...item,
        total_amount: parseFloat(item.total_amount)
      }))
      setData(processedData)
    } catch (err) {
      setError('Failed to load chart data')
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#00b3b6', '#d4a76a', '#f39c12', '#9b59b6', '#3498db', '#e74c3c']

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4">Expense Distribution</h2>
      
      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {/* Loading State */}
      {loading && <p className="text-center py-8">Loading chart data...</p>}
      
      {/* Pie Chart */}
      {!loading && !error && (
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="total_amount"
                nameKey="category"
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={120}
                labelLine={false}
                label={({ name, percent }) => (
                  `${name}: ${(percent * 100).toFixed(1)}%`
                )}
              >
                {data.map((entry, index) => (
                  <Cell key={`index-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `AED ${value}`} />
              <Legend verticalAlign="top" height={36} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
      
      {/* Empty State */}
      {!loading && !error && data.length === 0 && (
        <p className="text-center py-8 text-gray-500">
          No expense data to display
        </p>
      )}
    </div>
  )
}

export default ExpensePieChart