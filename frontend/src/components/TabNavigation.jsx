import React, { useState } from 'react'

function TabNavigation({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'debits', label: 'Expenses (Debits)', icon: '💸' },
    { id: 'credits', label: 'Payments (Credits)', icon: '💰' }
  ]

  return (
    <div className="mb-6">
      <div className="flex gap-2 bg-gray-100 rounded-lg p-1">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex items-center gap-2 px-5 py-3 rounded-lg font-medium text-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
              activeTab === tab.id
                ? 'bg-white shadow-md text-blue-700 shadow-sm'
                : 'text-gray-600 hover:bg-white hover:text-gray-900'
            }`}
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