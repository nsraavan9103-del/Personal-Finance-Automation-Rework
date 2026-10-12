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
      <div className="min-h-screen bg-ink-950 flex">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'w-72' : 'w-0'} overflow-hidden bg-ink-800 border-r border-ink-600 transition-all duration-300 flex-shrink-0`}>
          <UploadHistory />
        </aside>

        {/* Main content */}
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-ink-800/80 backdrop-blur border-b border-ink-600 shadow-[0_1px_24px_rgba(45,212,191,0.06)] sticky top-0 z-10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-lg text-mist-500 hover:bg-ink-700 hover:text-mist-100 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-glow"
                aria-label="Toggle uploads sidebar"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="font-display text-2xl font-bold tracking-tight text-mist-100">Personal Finance Dashboard</h1>
              <span className="hidden sm:inline-block text-xs font-display tracking-wide text-mist-600 border border-ink-600 rounded-full px-3 py-1">Dark preview</span>
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