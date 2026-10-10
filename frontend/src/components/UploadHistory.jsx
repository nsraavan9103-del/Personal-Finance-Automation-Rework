import React, { useState } from 'react'
import { useDocuments } from '../hooks/useDocuments'

export function UploadHistory({ onRefreshTransactions }) {
  const { documents, loading, error, deleteDocument, fetchDocuments } = useDocuments()
  const [confirmDeleteId, setConfirmDeleteId] = useState(null)

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this document and all its transactions? This cannot be undone.')) return
    await deleteDocument(id)
    if (onRefreshTransactions) onRefreshTransactions()
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="w-72 bg-white border-r border-gray-200 h-full flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Uploads</h3>
      </div>
      
      {error && (
        <div className="p-4 text-red-600 text-sm">{error}</div>
      )}

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4 text-center text-gray-500">Loading...</div>
        ) : documents.length === 0 ? (
          <div className="p-4 text-center text-gray-500 text-sm">No documents uploaded yet</div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {documents.map(doc => (
              <li key={doc.id} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate" title={doc.filename}>
                      {doc.filename}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {formatDate(doc.upload_date)} • {doc.transaction_count} transactions • {formatSize(doc.file_size)}
                    </p>
                    <p className="text-xs text-gray-400 mt-1 font-mono">
                      {doc.file_hash.slice(0, 16)}...
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    disabled={confirmDeleteId === doc.id}
                    className="text-red-600 hover:text-red-800 text-sm font-medium px-2 py-1 whitespace-nowrap flex-shrink-0"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}