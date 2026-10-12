import React, { useState, useEffect } from 'react'
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

  const COLORS = ['#E3C77F', '#2DD4BF', '#A78BFA', '#60A5FA', '#FB7185', '#34D399', '#FBBF24', '#818CF8', '#22D3EE', '#F97316']

  return (
    <div className="bg-ink-800 border border-ink-600 rounded-lg p-6">
      <h2 className="font-display text-xl font-bold mb-4 text-mist-100">Expense Distribution</h2>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-rose-500/10 border border-rose-500/20 text-rose-300 rounded">
          {error}
        </div>
      )}

      {/* Loading State */}
      {loading && <p className="text-center py-8 text-mist-500">Loading chart data...</p>}

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
                stroke="#0B0E14"
                strokeWidth={2}
                labelLine={false}
                label={({ name, percent }) => (
                  `${name}: ${(percent * 100).toFixed(1)}%`
                )}
              >
                {data.map((entry, index) => (
                  <Cell key={`index-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value) => [`AED ${value}`, null]}
                contentStyle={{
                  background: '#151B28',
                  border: '1px solid #263048',
                  borderRadius: 8,
                  color: '#ECEDF2',
                }}
                itemStyle={{ color: '#B7BECB' }}
                cursor={{ fill: 'rgba(45, 212, 191, 0.08)' }}
              />
              <Legend verticalAlign="top" height={36} iconType="circle" iconSize={8} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && data.length === 0 && (
        <p className="text-center py-8 text-mist-500">
          No expense data to display
        </p>
      )}
    </div>
  )
}

export default ExpensePieChart
