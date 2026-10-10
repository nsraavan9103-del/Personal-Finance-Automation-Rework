import React, { useState, useCallback } from 'react'
import axios from 'axios'
import { useTransactions } from '../context/TransactionContext'

const API_BASE = '/api'

function FileUpload() {
  const { refreshData } = useTransactions()
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = useCallback((e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      const validTypes = ['text/csv', 'application/csv', 'text/plain']
      const validExtensions = ['.csv']
      const fileExtension = '.' + selectedFile.name.split('.').pop().toLowerCase()
      
      if (!validTypes.includes(selectedFile.type) && !validExtensions.includes(fileExtension)) {
        setError('Please select a valid CSV file')
        setFile(null)
        return
      }
      
      setFile(selectedFile)
      setError(null)
      setUploadResult(null)
    }
  }, [])

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      const validTypes = ['text/csv', 'application/csv', 'text/plain']
      const validExtensions = ['.csv']
      const fileExtension = '.' + droppedFile.name.split('.').pop().toLowerCase()
      
      if (!validTypes.includes(droppedFile.type) && !validExtensions.includes(fileExtension)) {
        setError('Please drop a valid CSV file')
        return
      }
      
      setFile(droppedFile)
      setError(null)
      setUploadResult(null)
    }
  }, [])

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }
    
    setUploading(true)
    setError(null)
    
    const formData = new FormData()
    formData.append('file', file)
    
try {
        const response = await axios.post(`${API_BASE}/upload/csv`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        setUploadResult(response.data)
        setFile(null)
        refreshData()
        // Trigger document list refresh in sidebar
        window.dispatchEvent(new CustomEvent('refresh-documents'))
      } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }
  
  const clearResults = () => {
    setUploadResult(null)
    setError(null)
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4">Upload Bank Statement</h2>
      
      <form onSubmit={handleUpload} className="space-y-4">
        <div 
          className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            accept=".csv,text/csv"
            onChange={handleFileChange}
            className="hidden"
          />
          <label htmlFor="file-upload" className="cursor-pointer block">
            <div className="flex flex-col items-center gap-2">
              <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p className="text-gray-600">
                Drag and drop a CSV file here, or <span className="text-blue-600 font-medium">click to browse</span>
              </p>
              <p className="text-sm text-gray-500">CSV files only (.csv)</p>
            </div>
          </label>
          {file && (
            <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center gap-3">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 12.586 7.707 11.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <div>
                  <p className="font-medium text-green-800">{file.name}</p>
                  <p className="text-sm text-green-600">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setFile(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}
        </div>
        
        <button
          type="submit"
          disabled={uploading || !file}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-3 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          {uploading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Uploading...
            </span>
          ) : (
            'Upload Statement'
          )}
        </button>
        
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center gap-2 text-red-800">
              <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L10.586 10l-1.707 1.707a1 1 0 001.414 1.414L10 11.414l1.707 1.707a1 1 0 001.414-1.414L10 8.586 8.293 6.854a1 1 0 00-1.414 0L10 6.586 8.293 5.146a1 1 0 00-1.414 1.414L8.586 10 6.854 11.707a1 1 0 000 1.414z" clipRule="evenodd" />
              </svg>
              <p>{error}</p>
            </div>
          </div>
        )}
        
        {uploadResult && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center gap-2 text-green-800">
              <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 8.793a1 1 0 001.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <p>{uploadResult.message}</p>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white p-3 rounded">
                <p className="text-green-600 font-medium">Transactions Created</p>
                <p className="text-2xl font-bold text-green-800">{uploadResult.transactions_created}</p>
              </div>
              <div className="bg-white p-3 rounded">
                <p className="text-green-600 font-medium">Categories</p>
                <p className="text-2xl font-bold text-green-800">{uploadResult.categories.length}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={clearResults}
              className="mt-4 text-green-600 hover:text-green-800 text-sm font-medium"
            >
              Upload another file
            </button>
          </div>
        )}
      </form>
    </div>
  )
}

export default FileUpload