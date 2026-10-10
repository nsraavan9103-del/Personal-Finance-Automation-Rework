import React, { useState } from 'react'
import { TransactionProvider } from './context/TransactionContext'
import FileUpload from './components/FileUpload'
import TabNavigation from './components/TabNavigation'
import DashboardContent from './components/DashboardContent'
import { UploadHistory } from './components/UploadHistory'

function App() {
  const [activeTab, setActiveTab] = useState('debits')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <TransactionProvider>
      <div className="min-h-screen bg-gray-50 flex">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'w-72' : 'w-0'} overflow-hidden bg-white border-r border-gray-200 transition-all duration-300 flex-shrink-0`}>
          <UploadHistory onRefreshTransactions={() => window.dispatchEvent(new CustomEvent('refresh-transactions'))} />
        </aside>

        {/* Main content */}
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
                aria-label="Toggle uploads sidebar"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-2xl font-bold text-gray-900">Personal Finance Dashboard</h1>
            </div>
          </header>
          
          <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full">
            <FileUpload />
            <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />
            <DashboardContent activeTab={activeTab} />
          </main>
        </div>
      </div>
    </TransactionProvider>
  )
}

export default App