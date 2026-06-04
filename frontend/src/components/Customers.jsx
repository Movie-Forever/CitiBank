import React, { useState, useEffect } from 'react'
import { customersAPI } from '../services/api'
import '../styles/Customers.css'

export default function Customers() {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({ name: '', email: '' })
  const [searchTerm, setSearchTerm] = useState('')
  const [filterPremium, setFilterPremium] = useState(false)

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async (premium = filterPremium) => {
    setLoading(true)
    try {
      const response = premium 
        ? await customersAPI.getPremium()
        : await customersAPI.getAll()
      setCustomers(response.data.customers || response.data.premium_customers || [])
    } catch (error) {
      console.error('Error fetching customers:', error)
      alert('Failed to fetch customers')
    }
    setLoading(false)
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchTerm.trim()) {
      fetchCustomers()
      return
    }
    setLoading(true)
    try {
      const response = await customersAPI.search(searchTerm)
      setCustomers(response.data.customers || [])
    } catch (error) {
      console.error('Error searching:', error)
      alert('Search failed')
    }
    setLoading(false)
  }

  const handleAddNew = () => {
    setEditingId(null)
    setFormData({ name: '', email: '' })
    setShowForm(true)
  }

  const handleEdit = (customer) => {
    setEditingId(customer.id)
    setFormData({ name: customer.name, email: customer.email })
    setShowForm(true)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.name || !formData.email) {
      alert('Please fill in all fields')
      return
    }
    try {
      if (editingId) {
        await customersAPI.update(editingId, formData)
        alert('Customer updated successfully')
      } else {
        await customersAPI.create(formData)
        alert('Customer created successfully')
      }
      setShowForm(false)
      fetchCustomers()
    } catch (error) {
      console.error('Error saving:', error)
      alert('Failed to save customer')
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this customer?')) {
      try {
        await customersAPI.delete(id)
        alert('Customer deleted successfully')
        fetchCustomers()
      } catch (error) {
        console.error('Error deleting:', error)
        alert('Failed to delete customer')
      }
    }
  }

  return (
    <div className="customers-container">
      <h2>Customers Management</h2>
      
      <div className="controls">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="Search by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button type="submit">Search</button>
        </form>

        <div className="filter-buttons">
          <button 
            onClick={() => { setFilterPremium(false); fetchCustomers(false) }}
            className={!filterPremium ? 'active' : ''}
          >
            All Customers
          </button>
          <button 
            onClick={() => { setFilterPremium(true); fetchCustomers(true) }}
            className={filterPremium ? 'active' : ''}
          >
            Premium Only
          </button>
          <button onClick={handleAddNew} className="btn-primary">
            + Add Customer
          </button>
        </div>
      </div>

      {showForm && (
        <div className="form-modal">
          <div className="form-container">
            <h3>{editingId ? 'Edit Customer' : 'Add New Customer'}</h3>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Name"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
              <input
                type="email"
                placeholder="Email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
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
        <div className="customers-grid">
          {customers.map(customer => (
            <div key={customer.id} className="customer-card">
              <h4>{customer.name}</h4>
              <p><strong>Email:</strong> {customer.email}</p>
              <p><strong>ID:</strong> {customer.id}</p>
              {customer.total_balance !== undefined && (
                <p className="premium-badge"><strong>Total Balance:</strong> ${customer.total_balance.toFixed(2)}</p>
              )}
              {customer.account_ids && (
                <p><strong>Accounts:</strong> {customer.account_ids}</p>
              )}
              <div className="card-actions">
                <button onClick={() => handleEdit(customer)} className="btn-edit">Edit</button>
                <button onClick={() => handleDelete(customer.id)} className="btn-delete">Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
