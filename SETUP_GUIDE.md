# 🏦 Banking Management System - Full Stack Setup Guide

## Project Overview

Complete full-stack Banking application with React frontend and Flask backend connected to MongoDB Atlas Cloud Database.

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)                │
│  - Customers Management (CRUD + Search)                      │
│  - Accounts Management (CRUD + Search)                       │
│  - Premium Customers Filter                                  │
│  - Responsive Dashboard UI                                   │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API (Axios)
                           │ CORS Enabled
┌──────────────────────────▼──────────────────────────────────┐
│              Flask Backend API (Port 5000)                   │
│  - Customers Endpoints (GET, GET/:id, POST, PUT, DELETE)    │
│  - Accounts Endpoints (GET, GET/:id, POST, PUT, DELETE)     │
│  - Search & Filter Endpoints                                │
│  - Swagger Documentation (/apidocs)                         │
└──────────────────────────┬──────────────────────────────────┘
                           │ MongoDB Driver (pymongo)
┌──────────────────────────▼──────────────────────────────────┐
│          MongoDB Atlas Cloud Database                        │
│  - BankCluster (Cloud-hosted)                               │
│  - Collections: customers, accounts                         │
│  - Seed Data: 4 customers + 6 accounts                      │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Node.js** 16+ (for frontend)
- **Python** 3.8+ (for backend)
- **npm** or **yarn** (Node package manager)
- **MongoDB Atlas Account** (already configured)
- **Git** (optional, for version control)

## Directory Structure

```
g:\Citibank\
├── BankAPI/                          # Backend (Flask)
│   ├── app.py                        # Main Flask app (CORS enabled)
│   ├── data_store.py                 # MongoDB connection & queries
│   ├── models.py                     # Data models
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # MongoDB credentials
│   ├── routes/
│   │   ├── customers.py              # Customer endpoints
│   │   ├── accounts.py               # Account endpoints
│   │   └── __init__.py
│   ├── test_api.py                   # API tests
│   └── test_endpoints.http           # HTTP test file
│
├── frontend/                         # Frontend (React + Vite)
│   ├── src/
│   │   ├── App.jsx                   # Main app component
│   │   ├── main.jsx                  # Entry point
│   │   ├── components/
│   │   │   ├── Customers.jsx         # Customer CRUD UI
│   │   │   └── Accounts.jsx          # Account CRUD UI
│   │   ├── services/
│   │   │   └── api.js                # Axios API client
│   │   └── styles/
│   │       ├── App.css
│   │       ├── Customers.css
│   │       ├── Accounts.css
│   │       └── index.css
│   ├── index.html                    # HTML template
│   ├── vite.config.js                # Vite config with proxy
│   ├── package.json                  # Node dependencies
│   ├── .env                          # Environment config
│   └── README.md
│
└── SETUP_GUIDE.md                    # This file
```

## Installation & Running

### Step 1: Backend Setup

#### 1.1 Navigate to backend directory
```bash
cd g:\Citibank\BankAPI
```

#### 1.2 Create Python virtual environment (recommended)
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Or if using Command Prompt
python -m venv venv
venv\Scripts\activate.bat
```

#### 1.3 Install dependencies
```bash
pip install -r requirements.txt
```

#### 1.4 Verify MongoDB connection (optional)
```bash
python test_connection.py
```

#### 1.5 Start Flask server
```bash
python app.py
```

Expected output:
```
✓ Connected to MongoDB Atlas successfully
✓ Seed data created: 4 customers, 6 accounts
Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

**Backend is now running on:** http://localhost:5000

Available endpoints:
- Swagger UI: http://localhost:5000/apidocs
- Root: http://localhost:5000/
- Customers: http://localhost:5000/api/customers
- Accounts: http://localhost:5000/api/accounts

### Step 2: Frontend Setup

#### 2.1 Open new terminal/PowerShell window and navigate to frontend
```bash
cd g:\Citibank\frontend
```

#### 2.2 Install Node dependencies
```bash
npm install
```

This will install:
- `react` - UI framework
- `react-dom` - React DOM rendering
- `axios` - HTTP client for API calls
- `vite` - Build tool
- `@vitejs/plugin-react` - React plugin for Vite

#### 2.3 Start development server
```bash
npm run dev
```

Expected output:
```
  VITE v4.x.x  ready in XX ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

**Frontend is now running on:** http://localhost:3000

### Step 3: Access the Application

1. Open your web browser
2. Navigate to: **http://localhost:3000**
3. You should see the Banking Management System dashboard

## Features Overview

### Customers Tab
- **View All Customers**: See all customers from MongoDB
- **Search Customers**: Search by name (substring match)
- **Premium Customers Filter**: View only customers with balance > $10,000
- **Add Customer**: Create new customer (name + email)
- **Edit Customer**: Update existing customer details
- **Delete Customer**: Remove customer (cascades to accounts)

### Accounts Tab
- **View All Accounts**: See all accounts from MongoDB
- **Search Accounts**: Search by customer name
- **Add Account**: Create new account (number, type, balance, customer)
- **Edit Account**: Update account details
- **Delete Account**: Remove account

### Account Types
- **Savings**: For savings accounts
- **Checking**: For checking accounts

## API Endpoints Reference

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | Get all customers |
| GET | `/api/customers/:id` | Get customer by ID |
| GET | `/api/customers/search?name=John` | Search customers by name |
| GET | `/api/customers/premium` | Get premium customers (balance > $10K) |
| POST | `/api/customers` | Create new customer |
| PUT | `/api/customers/:id` | Update customer |
| DELETE | `/api/customers/:id` | Delete customer |

### Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts` | Get all accounts |
| GET | `/api/accounts/:id` | Get account by ID |
| GET | `/api/accounts/search?name=John` | Search by customer name |
| POST | `/api/accounts` | Create new account |
| PUT | `/api/accounts/:id` | Update account |
| DELETE | `/api/accounts/:id` | Delete account |

## Seed Data

The application automatically creates sample data on startup:

### Customers (4 total)
1. John Doe (john.doe@example.com) - Total Balance: $30,000
2. Jane Smith (jane.smith@example.com) - Total Balance: $18,000
3. Robert Johnson (robert.j@example.com) - Total Balance: $8,000
4. Emily Chen (emily.chen@example.com) - Total Balance: $2,000

### Accounts (6 total)
- ACC001 (Savings, $25,000) - John Doe
- ACC002 (Checking, $5,000) - John Doe
- ACC003 (Savings, $15,000) - Jane Smith
- ACC004 (Checking, $3,000) - Jane Smith
- ACC005 (Savings, $8,000) - Robert Johnson
- ACC006 (Checking, $2,000) - Emily Chen

## Troubleshooting

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -r node_modules package-lock.json
npm install
npm run dev
```

### Backend won't connect to MongoDB
- Check .env file has correct MongoDB URI
- Verify MongoDB Atlas credentials
- Check internet connection to MongoDB Atlas

### CORS errors
- Ensure backend is running with CORS enabled (Flask-CORS installed)
- Check `app.py` has CORS initialization
- Verify backend is on port 5000

### Port already in use
```bash
# Change port in vite.config.js for frontend
# Change port in Flask app.py for backend
```

## Development Commands

### Backend
```bash
# Run with hot reload
python app.py

# Run tests
pytest test_api.py

# Test specific endpoint
python -m pytest test_api.py -v
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Production Deployment

### Frontend Build
```bash
cd frontend
npm run build
# Outputs to dist/ folder
```

### Environment Variables
Create `.env` files in both directories:

**Backend** (`BankAPI/.env`):
```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?appName=BankCluster
```

**Frontend** (`frontend/.env`):
```
VITE_API_URL=https://your-backend-domain.com/api
```

## Technology Stack

### Frontend
- **React** 18.2.0 - UI library
- **Vite** 4.3.0 - Build tool
- **Axios** 1.6.0 - HTTP client
- **CSS3** - Styling

### Backend
- **Flask** 2.3.3 - Web framework
- **Flask-CORS** 4.0.0 - CORS support
- **pymongo** 4.6.1 - MongoDB driver
- **python-dotenv** 1.0.0 - Environment management
- **Flasgger** 0.9.7.1 - Swagger documentation

### Database
- **MongoDB Atlas** - Cloud database
- **BankCluster** - Cluster name

## Contact & Support

For issues or questions:
1. Check the README.md files in backend and frontend folders
2. Review error messages in browser console (F12)
3. Check Flask server terminal for backend errors
4. Verify MongoDB connection with test script

## Next Steps

1. ✅ Backend running with MongoDB integration
2. ✅ Frontend displaying data from backend
3. ✅ All CRUD operations working
4. 🚀 Deploy to production (AWS, Heroku, Vercel, etc.)
5. 🚀 Add authentication (JWT tokens)
6. 🚀 Add data validation & error handling
7. 🚀 Add unit & integration tests

---

**Full Stack Banking System** - Complete Implementation ✅
