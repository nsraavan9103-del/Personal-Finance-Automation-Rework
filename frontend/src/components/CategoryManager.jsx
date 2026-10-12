import React, { useState, useEffect, useContext } from 'react'
import axios from 'axios'
import { useTransactions } from '../context/TransactionContext'

function CategoryManager() {
  const { categories, setCategories, refreshData } = useTransactions()
  const [newCategoryName, setNewCategoryName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [deletingId, setDeletingId] = useState(null)

  const fetchCategories = async () => {
    try {
      const response = await axios.get('/api/v1/categories')
      setCategories(response.data)
    } catch (err) {
      setError('Failed to load categories')
    }
  }

  useEffect(() => {
    fetchCategories()
  }, [])

  const handleAddCategory = async (e) => {
    e.preventDefault()
    if (!newCategoryName.trim()) return
    
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post('/api/v1/categories', { name: newCategoryName.trim() })
      setCategories([...categories, response.data])
      refreshData()
      setNewCategoryName('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add category')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteCategory = async (id) => {
    if (!window.confirm('Are you sure you want to delete this category? This cannot be undone.')) return
    
    setDeletingId(id)
    try {
      await axios.delete('/api/v1/categories/' + id)
      setCategories(categories.filter(cat => cat.id !== id))
      refreshData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete category')
    } finally {
      setDeletingId(null)
    }
  }

  const isProtected = (name) => name === 'Uncategorized'

  return (
    <div className="bg-ink-800 border border-ink-600 p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-mist-100">Category Manager</h2>
        <span className="text-sm text-mist-500">{categories.length} categories</span>
      </div>
      
      {/* Add Category Form */}
      <form onSubmit={handleAddCategory} className="mb-6 flex items-center gap-3">
        <input
          type="text"
          value={newCategoryName}
          onChange={(e) => setNewCategoryName(e.target.value)}
          placeholder="Enter new category name"
          className="flex-1 border border-ink-600 rounded-lg px-4 py-3 focus:ring-2 focus:ring-glow focus:border-glow outline-none transition-shadow"
          maxLength={100}
        />
        <button
          type="submit"
          disabled={loading || !newCategoryName.trim()}
          className="bg-glow-strong hover:bg-glow text-ink-950 disabled:bg-ink-700 disabled:text-mist-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-glow focus:ring-offset-2 whitespace-nowrap"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Adding...
            </span>
          ) : (
            'Add Category'
          )}
        </button>
      </form>
      
      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-rose-500/10 border border-rose-500/20 rounded-lg" role="alert">
          <div className="flex items-center gap-3">
            <svg className="w-5 h-5 flex-shrink-0 text-rose-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L10.586 10l-1.707 1.707a1 1 0 001.414 1.414L10 11.414l1.707 1.707a1 1 0 001.414-1.414L11.414 10l1.707-1.707a1 1 0 001.414-1.414L10 8.586 8.293 6.854a1 1 0 00-1.414 0L10 6.586 8.293 5.146a1 1 0 00-1.414 1.414L8.586 10 6.854 11.707a1 1 0 000 1.414z" clipRule="evenodd" />
            </svg>
            <p className="text-rose-300 font-medium">{error}</p>
          </div>
        </div>
      )}
      
      {/* Categories List */}
      <div className="space-y-2">
        {categories.length > 0 ? (
          categories.map(category => (
            <div 
              key={category.id} 
              className="flex items-center justify-between p-4 bg-ink-900 border border-ink-600 rounded-lg hover:bg-ink-700 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${isProtected(category.name) ? 'bg-amber-400' : 'bg-glow'}`} />
                <span className="font-medium text-mist-100">{category.name}</span>
                {isProtected(category.name) && (
                  <span className="text-xs px-2 py-0.5 bg-amber-400/10 text-amber-300 rounded-full font-medium">
                    Protected
                  </span>
                )}
              </div>
              {!isProtected(category.name) && (
                <button
                  onClick={() => handleDeleteCategory(category.id)}
                  disabled={deletingId === category.id}
                  className="text-sm text-white bg-rose-600 hover:bg-rose-500 disabled:bg-rose-800 px-4 py-2 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-rose-500 focus:ring-offset-2"
                >
                  {deletingId === category.id ? (
                    <span className="flex items-center gap-1">
                      <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      Deleting...
                    </span>
                  ) : 'Delete'}
                </button>
              )}
            </div>
          ))
        ) : (
          <div className="text-center py-12 bg-ink-900 rounded-lg">
            <svg className="w-12 h-12 mx-auto text-ink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <p className="mt-4 text-mist-500 text-center">No categories found</p>
            <p className="text-sm text-mist-600 mt-1 text-center">Create your first category above</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default CategoryManager