import { useState } from 'react'
import axios from 'axios'

// Use direct backend URL for uploads to bypass Vite proxy issues with multipart/form-data
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export function useUpload() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setError(null)
    setUploadResult(null)
  }

  const uploadCSV = async (e) => {
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
      const response = await axios.post(`${BACKEND_URL}/api/v1/upload/csv`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setUploadResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return { file, setFile: handleFileChange, uploading, uploadResult, error, uploadCSV }
}