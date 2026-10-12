import React from 'react'
import CategoryManager from './CategoryManager'
import TransactionTable from './TransactionTable'
import SummaryTable from './SummaryTable'
import ExpensePieChart from './ExpensePieChart'

function DashboardContent({ activeTab }) {
  return (
    <div className="space-y-6">
      <CategoryManager />
      {activeTab === 'debits' && (
        <>
          <TransactionTable initialDebitCredit="Debit" />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SummaryTable />
            <ExpensePieChart />
          </div>
        </>
      )}
      {activeTab === 'credits' && (
        <>
          <div className="bg-ink-800 border border-ink-600 rounded-xl p-6 mb-6">
            <h2 className="font-display text-xl font-bold mb-4 text-mist-100">Total Payments (Credits)</h2>
            <TransactionTable initialDebitCredit="Credit" />
          </div>
        </>
      )}
    </div>
  )
}

export default DashboardContent
