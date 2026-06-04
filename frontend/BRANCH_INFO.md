# Frontend Branch

This is the frontend branch for the Banking Management System.

## Backend Branch
The backend (Flask API with MongoDB) is in the main branch.

## To Run

1. **Start Backend** (from main branch):
```bash
cd BankAPI
pip install -r requirements.txt
python app.py
```

2. **Start Frontend** (this branch):
```bash
cd frontend
npm install
npm run dev
```

3. **Open Browser**:
Navigate to `http://localhost:3000`

## Stack

- **Frontend**: React 18 + Vite
- **Backend**: Flask + MongoDB Atlas
- **API Communication**: Axios
- **Styling**: CSS3
- **CORS**: Flask-CORS enabled

## Features

### Customers Tab
- View all customers
- Search by name
- Filter premium customers (balance > $10K)
- Create, read, update, delete customers

### Accounts Tab
- View all accounts
- Search by customer name
- Create, read, update, delete accounts
- Link accounts to customers

## API Integration

All requests go through `axios` instance in `src/services/api.js` with CORS support enabled on backend.
