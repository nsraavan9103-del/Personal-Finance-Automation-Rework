import React, { useState, useEffect } from 'react'
import { useDocuments } from '../hooks/useDocuments'
import { useTransactions } from '../context/TransactionContext'

export function UploadHistory() {
  const { documents, loading, error, deleteDocument, fetchDocuments } = useDocuments()
  const { refreshData } = useTransactions()
  const [confirmDeleteId, setConfirmDeleteId] = useState(null)

  // ponytail: DOM-event sync from FileUpload; lift documents into TransactionContext
  // if more components ever need to share this list.
  useEffect(() => {
    const handler = () => fetchDocuments()
    window.addEventListener('refresh-documents', handler)
    return () => window.removeEventListener('refresh-documents', handler)
  }, [])

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this document and all its transactions? This cannot be undone.')) return
    await deleteDocument(id)
    refreshData()
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
    <div className="w-72 bg-ink-800 border-r border-ink-600 h-full flex flex-col">
      <div className="p-4 border-b border-ink-600">
        <h3 className="text-lg font-semibold text-mist-100">Uploads</h3>
      </div>
      
      {error && (
        <div className="p-4 text-rose-300 text-sm">{error}</div>
      )}

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4 text-center text-mist-500">Loading...</div>
        ) : documents.length === 0 ? (
          <div className="p-4 text-center text-mist-500 text-sm">No documents uploaded yet</div>
        ) : (
          <ul className="divide-y divide-ink-600">
            {documents.map(doc => (
              <li key={doc.id} className="p-4 hover:bg-ink-900 transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-mist-100 truncate" title={doc.filename}>
                      {doc.filename}
                    </p>
                    <p className="text-xs text-mist-500 mt-1">
                      {formatDate(doc.upload_date)} • {doc.transaction_count} transactions • {formatSize(doc.file_size)}
                    </p>
                    <p className="text-xs text-mist-600 mt-1 font-mono">
                      {doc.file_hash.slice(0, 16)}...
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    disabled={confirmDeleteId === doc.id}
                    className="text-rose-400 hover:text-rose-300 focus-visible:ring-2 focus-visible:ring-rose-500 focus-visible:ring-offset-2 focus-visible:ring-offset-ink-800 rounded text-sm font-medium px-2 py-1 whitespace-nowrap flex-shrink-0"
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