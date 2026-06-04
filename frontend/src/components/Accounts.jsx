import React, { useState, useEffect } from 'react'
import { accountsAPI, customersAPI } from '../services/api'
import '../styles/Accounts.css'

export default function Accounts() {
  const [accounts, setAccounts] = useState([])
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({ 
    account_number: '', 
    account_type: 'Savings', 
    balance: '', 
    customer_id: '' 
  })
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchAccounts()
    fetchCustomers()
  }, [])

  const fetchAccounts = async () => {
    setLoading(true)
    try {
      const response = await accountsAPI.getAll()
      setAccounts(response.data.accounts || [])
    } catch (error) {
      console.error('Error fetching accounts:', error)
      alert('Failed to fetch accounts')
    }
    setLoading(false)
  }

  const fetchCustomers = async () => {
    try {
      const response = await customersAPI.getAll()
      setCustomers(response.data.customers || [])
    } catch (error) {
      console.error('Error fetching customers:', error)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchTerm.trim()) {
      fetchAccounts()
      return
    }
    setLoading(true)
    try {
      const response = await accountsAPI.search(searchTerm)
      setAccounts(response.data.accounts || [])
    } catch (error) {
      console.error('Error searching:', error)
      alert('Search failed')
    }
    setLoading(false)
  }

  const handleAddNew = () => {
    setEditingId(null)
    setFormData({ account_number: '', account_type: 'Savings', balance: '', customer_id: '' })
    setShowForm(true)
  }

  const handleEdit = (account) => {
    setEditingId(account.id)
    setFormData({
      account_number: account.account_number,
      account_type: account.account_type,
      balance: account.balance,
      customer_id: account.customer_id
    })
    setShowForm(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.account_number || !formData.balance || !formData.customer_id) {
      alert('Please fill in all fields')
      return
    }
    try {
      const submitData = {
        ...formData,
        balance: parseFloat(formData.balance)
      }
      if (editingId) {
        await accountsAPI.update(editingId, submitData)
        alert('Account updated successfully')
      } else {
        await accountsAPI.create(submitData)
        alert('Account created successfully')
      }
      setShowForm(false)
      fetchAccounts()
    } catch (error) {
      console.error('Error saving:', error)
      alert('Failed to save account')
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this account?')) {
      try {
        await accountsAPI.delete(id)
        alert('Account deleted successfully')
        fetchAccounts()
      } catch (error) {
        console.error('Error deleting:', error)
        alert('Failed to delete account')
      }
    }
  }

  const getCustomerName = (customerId) => {
    const customer = customers.find(c => c.id == customerId)
    return customer ? customer.name : `Customer ${customerId}`
  }

  return (
    <div className="accounts-container">
      <h2>Accounts Management</h2>
      
      <div className="controls">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="Search by customer name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button type="submit">Search</button>
        </form>

        <button onClick={handleAddNew} className="btn-primary">
          + Add Account
        </button>
      </div>

      {showForm && (
        <div className="form-modal">
          <div className="form-container">
            <h3>{editingId ? 'Edit Account' : 'Add New Account'}</h3>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Account Number"
                value={formData.account_number}
                onChange={(e) => setFormData({...formData, account_number: e.target.value})}
                required
              />
              <select
                value={formData.account_type}
                onChange={(e) => setFormData({...formData, account_type: e.target.value})}
                required
              >
                <option value="Savings">Savings</option>
                <option value="Checking">Checking</option>
              </select>
              <input
                type="number"
                placeholder="Balance"
                value={formData.balance}
                onChange={(e) => setFormData({...formData, balance: e.target.value})}
                step="0.01"
                min="0"
                required
              />
              <select
                value={formData.customer_id}
                onChange={(e) => setFormData({...formData, customer_id: e.target.value})}
                required
              >
                <option value="">Select Customer</option>
                {customers.map(c => (
                  <option key={c.id} value={c.id}>{c.name} (ID: {c.id})</option>
                ))}
              </select>
              <div className="form-buttons">
                <button type="submit" className="btn-primary">Save</button>
                <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="accounts-table">
          <table>
            <thead>
              <tr>
                <th>Account #</th>
                <th>Type</th>
                <th>Balance</th>
                <th>Customer</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map(account => (
                <tr key={account.id}>
                  <td data-label="Account #">{account.account_number}</td>
                  <td data-label="Type">{account.account_type}</td>
                  <td data-label="Balance">${account.balance.toFixed(2)}</td>
                  <td data-label="Customer">{getCustomerName(account.customer_id)}</td>
                  <td data-label="Actions">
                    <button onClick={() => handleEdit(account)} className="btn-edit">Edit</button>
                    <button onClick={() => handleDelete(account.id)} className="btn-delete">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
