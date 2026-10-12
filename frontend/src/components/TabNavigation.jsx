import React, { useState } from 'react'

function TabNavigation({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'debits', label: 'Expenses (Debits)', icon: '💸' },
    { id: 'credits', label: 'Payments (Credits)', icon: '💰' }
  ]

  return (
    <div className="mb-6">
      <div className="inline-flex gap-1 bg-ink-900 border border-ink-600 rounded-lg p-1">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-md font-display font-medium text-sm tracking-wide transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-glow ${
              activeTab === tab.id
                ? 'bg-ink-700 text-glow shadow-[0_0_16px_rgba(45,212,191,0.15)]'
                : 'text-mist-500 hover:bg-ink-800 hover:text-mist-300'
            }`}
            aria-current={activeTab === tab.id ? 'page' : undefined}
          >
            <span className="text-lg">{tab.icon}</span>
            <span className="font-medium">{tab.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default TabNavigation