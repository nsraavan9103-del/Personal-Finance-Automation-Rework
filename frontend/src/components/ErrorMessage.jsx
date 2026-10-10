import React from 'react'

function ErrorMessage({ message, onDismiss, className = '' }) {
  if (!message) return null

  return (
    <div className={`p-4 bg-red-50 border border-red-200 rounded-lg ${className}`} role="alert">
      <div className="flex items-start gap-3">
        <svg className="w-5 h-5 flex-shrink-0 text-red-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L10.586 10l-1.707 1.707a1 1 0 001.414 1.414L10 11.414l1.707 1.707a1 1 0 001.414-1.414L11.414 10l1.707-1.707a1 1 0 00-1.414-1.414L10 8.586 8.293 6.854a1 1 0 00-1.414 0L10 6.586 8.293 5.146a1 1 0 00-1.414 1.414L8.586 10 6.854 11.707a1 1 0 000 1.414z" clipRule="evenodd" />
        </svg>
        <div className="flex-1">
          <p className="text-red-800 font-medium">{message}</p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-red-500 hover:text-red-700 transition-colors p-1"
            aria-label="Dismiss error"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
    </div>
  )
}

export default ErrorMessage