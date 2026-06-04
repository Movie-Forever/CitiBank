# Banking App Frontend

React + Vite frontend for the Banking Management System

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Features

- ✅ Full CRUD for Customers (GET, GET by ID, POST, PUT, DELETE)
- ✅ Full CRUD for Accounts (GET, GET by ID, POST, PUT, DELETE)
- ✅ Search customers by name
- ✅ Search accounts by customer name
- ✅ Filter premium customers (balance > $10,000)
- ✅ Real-time data from MongoDB Atlas
- ✅ CORS support for frontend-backend communication
- ✅ Responsive UI with React components
- ✅ Axios for API calls

## API Endpoints

- `GET /api/customers` - All customers
- `GET /api/customers/:id` - Customer by ID
- `GET /api/customers/search?name=` - Search customers
- `GET /api/customers/premium` - Premium customers
- `POST /api/customers` - Create customer
- `PUT /api/customers/:id` - Update customer
- `DELETE /api/customers/:id` - Delete customer

- `GET /api/accounts` - All accounts
- `GET /api/accounts/:id` - Account by ID
- `GET /api/accounts/search?name=` - Search accounts
- `POST /api/accounts` - Create account
- `PUT /api/accounts/:id` - Update account
- `DELETE /api/accounts/:id` - Delete account

## Architecture

```
frontend/
├── src/
│   ├── components/
│   │   ├── Customers.jsx    # Customer management
│   │   └── Accounts.jsx     # Account management
│   ├── services/
│   │   └── api.js           # API client with Axios
│   ├── styles/
│   │   ├── App.css          # Main styles
│   │   ├── Customers.css    # Customer component styles
│   │   ├── Accounts.css     # Account component styles
│   │   └── index.css        # Global styles
│   ├── App.jsx              # Main app component
│   └── main.jsx             # Entry point
├── index.html               # HTML template
├── vite.config.js           # Vite config with proxy
├── package.json             # Dependencies
└── .env                     # Environment variables
```

## Backend Connection

The frontend reads the backend API base URL from `VITE_API_URL`.

Create a local `.env` file from `.env.example` and set the backend API URL:

```text
VITE_API_URL=https://your-render-service.onrender.com/api
```

To start backend:
```bash
cd ../BankAPI
python app.py
```

## Browser

Run `npm run dev` and open the local URL printed by Vite.
