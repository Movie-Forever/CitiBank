# 🏦 Banking Management System - Full Stack Application

A complete, production-ready banking application with **React frontend**, **Flask REST API**, and **MongoDB Cloud Atlas** database.

![Banking App](https://img.shields.io/badge/Status-Complete-brightgreen) ![React](https://img.shields.io/badge/Frontend-React%2018-blue) ![Flask](https://img.shields.io/badge/Backend-Flask%202.3-red) ![MongoDB](https://img.shields.io/badge/Database-MongoDB%20Atlas-green)

## 🎯 Features

### ✅ Fully Implemented
- **Customers Management**: Create, Read, Update, Delete customers
- **Accounts Management**: Create, Read, Update, Delete accounts  
- **Search Functionality**: Search customers by name, search accounts by customer
- **Premium Filter**: View customers with balance > $10,000
- **Real-time Data**: Connected to MongoDB Atlas Cloud Database
- **REST API**: Fully documented with Swagger/OpenAPI
- **CORS Support**: Frontend-backend communication enabled
- **Responsive UI**: Modern, mobile-friendly interface
- **Seed Data**: 4 sample customers + 6 sample accounts pre-loaded

## 📁 Project Structure

```
g:\Citibank\
├── BankAPI/                    ← Backend (Flask)
│   ├── app.py                  Main Flask application with CORS
│   ├── data_store.py           MongoDB connection & queries
│   ├── models.py               Data models
│   ├── requirements.txt        Python dependencies
│   ├── .env                    MongoDB credentials
│   └── routes/
│       ├── customers.py        Customer endpoints
│       └── accounts.py         Account endpoints
│
├── frontend/                   ← Frontend (React + Vite)
│   ├── src/
│   │   ├── App.jsx             Main component
│   │   ├── components/
│   │   │   ├── Customers.jsx   Customer management UI
│   │   │   └── Accounts.jsx    Account management UI
│   │   ├── services/
│   │   │   └── api.js          Axios API client
│   │   └── styles/             CSS styling
│   ├── package.json            Node dependencies
│   ├── vite.config.js          Vite configuration
│   └── index.html              HTML template
│
├── SETUP_GUIDE.md              Comprehensive setup instructions
├── START_ALL.ps1               Quick start script (Windows)
└── CHECK_STATUS.py             Configuration checker
```

## 🚀 Quick Start (5 minutes)

### Option 1: Automated Start (Windows PowerShell)
```powershell
# From g:\Citibank directory
.\START_ALL.ps1
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd g:\Citibank\BankAPI
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd g:\Citibank\frontend
npm install
npm run dev
```

**Then open browser:**
```
http://localhost:3000
```

## ✨ What You Can Do

### Customers Tab
- 👥 **View all customers** with their total account balance
- 🔍 **Search customers** by name (live search)
- ⭐ **Filter premium customers** (balance > $10,000)
- ➕ **Create new customer** with name and email
- ✏️ **Edit customer** details
- 🗑️ **Delete customer** (cascades to associated accounts)

### Accounts Tab
- 💰 **View all accounts** (Savings/Checking types)
- 🔍 **Search accounts** by customer name
- ➕ **Create new account** linked to a customer
- ✏️ **Edit account** (type, balance, account number)
- 🗑️ **Delete account** (removes from customer)

## 📊 Sample Data

### Customers
| Name | Email | Total Balance | Status |
|------|-------|---------------|--------|
| John Doe | john.doe@example.com | $30,000 | Premium ⭐ |
| Jane Smith | jane.smith@example.com | $18,000 | Premium ⭐ |
| Robert Johnson | robert.j@example.com | $8,000 | Standard |
| Emily Chen | emily.chen@example.com | $2,000 | Standard |

### Accounts
- ACC001 (Savings, $25,000) → John Doe
- ACC002 (Checking, $5,000) → John Doe
- ACC003 (Savings, $15,000) → Jane Smith
- ACC004 (Checking, $3,000) → Jane Smith
- ACC005 (Savings, $8,000) → Robert Johnson
- ACC006 (Checking, $2,000) → Emily Chen

## 🔌 API Endpoints

### Customers
```
GET    /api/customers              # Get all customers
GET    /api/customers/:id          # Get customer by ID
GET    /api/customers/search?name= # Search by name
GET    /api/customers/premium      # Premium customers only
POST   /api/customers              # Create customer
PUT    /api/customers/:id          # Update customer
DELETE /api/customers/:id          # Delete customer
```

### Accounts
```
GET    /api/accounts               # Get all accounts
GET    /api/accounts/:id           # Get account by ID
GET    /api/accounts/search?name=  # Search by customer name
POST   /api/accounts               # Create account
PUT    /api/accounts/:id           # Update account
DELETE /api/accounts/:id           # Delete account
```

### Documentation
```
GET /apidocs                        # Swagger UI
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI library
- **Vite 4** - Build tool & dev server
- **Axios** - HTTP client
- **CSS3** - Styling
- **Node.js 16+** - Runtime

### Backend
- **Flask 2.3** - Web framework
- **Flask-CORS 4.0** - CORS support
- **pymongo 4.6** - MongoDB driver
- **Flasgger 0.9** - API documentation
- **python-dotenv 1.0** - Environment config
- **Python 3.8+** - Runtime

### Database
- **MongoDB Atlas** - Cloud database
- **BankCluster** - Cloud cluster
- Collections: `customers`, `accounts`

## 🔧 Verification Checklist

Run the status checker:
```bash
python CHECK_STATUS.py
```

This will verify:
- ✅ All files present
- ✅ Python packages installed
- ✅ Node packages installed
- ✅ MongoDB connection
- ✅ Backend running
- ✅ Frontend running

## 🐛 Troubleshooting

### Backend won't start
```bash
# 1. Check Python version
python --version   # Should be 3.8+

# 2. Install dependencies
pip install -r BankAPI/requirements.txt

# 3. Check MongoDB connection
python -c "from pymongo import MongoClient; client = MongoClient(...); print('Connected')"
```

### Frontend won't start
```bash
# 1. Check Node version
node --version    # Should be 16+

# 2. Clear cache and reinstall
cd frontend
rm -r node_modules package-lock.json
npm install
npm run dev
```

### CORS errors
- Ensure Flask-CORS is installed: `pip install Flask-CORS`
- Check `app.py` has CORS enabled
- Restart Flask server

### Port already in use
```bash
# Backend on different port
# In BankAPI/app.py, change: app.run(..., port=5001)

# Frontend on different port  
# In frontend/vite.config.js, change: port: 3001
```

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Comprehensive setup instructions
- [BankAPI/README.md](BankAPI/README.md) - Backend documentation
- [frontend/README.md](frontend/README.md) - Frontend documentation
- [frontend/BRANCH_INFO.md](frontend/BRANCH_INFO.md) - Frontend branch info

## 🚀 Deployment

For production deployment with a Vercel frontend and Render backend, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Build Frontend
```bash
cd frontend
npm run build
# Creates dist/ folder for hosting on Vercel/Netlify
```

### Deploy Backend
- Deploy Flask app to Heroku, AWS, DigitalOcean, or similar
- Update `.env` with production MongoDB URI
- Update frontend API URL in `.env`

### Options
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Backend**: Heroku, AWS Lambda, DigitalOcean, Railway
- **Database**: Already on MongoDB Atlas (cloud-hosted)

## 📝 Environment Configuration

### Backend (.env)
```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/?appName=BankCluster
MONGODB_DB_NAME=BankCluster
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
FLASK_ENV=production
SEED_DATABASE=false
```

### Frontend (.env)
```
VITE_API_URL=https://your-render-service.onrender.com/api
```

## ✅ Validation

### All Features Implemented ✓
- ✅ GET (retrieve all records)
- ✅ GET by ID (retrieve single record)
- ✅ POST (create record)
- ✅ PUT (update record)
- ✅ DELETE (delete record)
- ✅ Search functionality
- ✅ Filter functionality
- ✅ CORS support
- ✅ MongoDB integration
- ✅ UI display of all data
- ✅ Error handling
- ✅ Loading states
- ✅ Form validation

## 📞 Support

For issues:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
2. Run `CHECK_STATUS.py` to diagnose
3. Check terminal outputs for error messages
4. Review browser console (F12) for frontend errors

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🎉 Summary

This is a **complete, production-ready banking application** with:
- ✅ **Fully functional frontend** with React
- ✅ **Fully functional backend** with Flask
- ✅ **MongoDB Cloud database** integration
- ✅ **All CRUD operations** implemented
- ✅ **Search & filter** features
- ✅ **CORS support** for full-stack communication
- ✅ **Beautiful UI** with responsive design
- ✅ **Sample data** pre-loaded
- ✅ **API documentation** with Swagger

**Everything is ready to use!** 🚀

---

**Last Updated**: 2024
**Status**: ✅ Complete & Production Ready
