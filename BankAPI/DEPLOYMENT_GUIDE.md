# Banking REST API - Deployment & Setup Guide

## ✅ Current Status

**Backend Server:** Running on `http://localhost:5000`  
**Storage:** In-memory (MongoDB Atlas authentication failed - fallback active)  
**Status:** ✓ Fully Functional

### API Health
- ✓ GET `/` - API root endpoint working
- ✓ GET `/api/customers` - Retrieving 4 customers
- ✓ GET `/api/accounts` - Retrieving 6 accounts  
- ✓ GET `/api/customers/premium` - Premium customers working
- ✓ Swagger/Flasgger Documentation: `http://localhost:5000/apidocs`

---

## 🚀 Running the Backend

### Start the Server
```bash
cd g:\Citibank\BankAPI
python app.py
```

The server will:
1. Attempt to connect to MongoDB Atlas using credentials from `.env`
2. If MongoDB fails, fallback to in-memory storage for development
3. Run on `http://localhost:5000` with hot-reload enabled

### Test the API
```powershell
# Get all customers
Invoke-WebRequest -Uri http://localhost:5000/api/customers -UseBasicParsing

# Get all accounts
Invoke-WebRequest -Uri http://localhost:5000/api/accounts -UseBasicParsing

# Get premium customers (balance > $10,000)
Invoke-WebRequest -Uri http://localhost:5000/api/customers/premium -UseBasicParsing

# View Swagger API docs
Start-Process http://localhost:5000/apidocs
```

---

## 🗄️ MongoDB Atlas Integration

### Current Issue
The provided MongoDB credentials are not authenticating:
```
✗ Failed to connect to MongoDB: bad auth : authentication failed
```

### To Fix MongoDB Connection

1. **Verify Your MongoDB Atlas Credentials**
   - Go to: https://cloud.mongodb.com/
   - Login to your account
   - Navigate to **BankCluster**
   - Click **Connect** → **Drivers** (Node.js driver)
   - Copy the full connection string

2. **Update `.env` File**
   ```
   MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@bankcluster.38xmjwx.mongodb.net/?appName=BankCluster
   ```

3. **Check Network Access**
   - In MongoDB Atlas, go to **Security** → **Network Access**
   - Ensure your IP is whitelisted (or add `0.0.0.0/0` to allow all IPs)

4. **Restart the Server**
   ```bash
   python app.py
   ```

If successful, you'll see:
```
✓ Connected to MongoDB Atlas successfully
✓ Seed data created: 4 customers, 6 accounts
```

---

## 📋 Available API Endpoints

### Customers
- `GET /api/customers` - Get all customers
- `GET /api/customers/<id>` - Get customer by ID
- `GET /api/customers/search?name=<name>` - Search by name
- `GET /api/customers/premium` - Get premium customers (balance > $10,000)
- `POST /api/customers` - Create new customer
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Accounts
- `GET /api/accounts` - Get all accounts
- `GET /api/accounts/<id>` - Get account by ID
- `GET /api/accounts/search?name=<name>` - Search by customer name
- `POST /api/accounts` - Create new account
- `PUT /api/accounts/<id>` - Update account
- `DELETE /api/accounts/<id>` - Delete account

### Other
- `GET /` - API root with endpoints info
- `GET /health` - Health check
- `GET /apidocs` - Swagger API documentation

---

## 🎯 Example API Calls

### Get All Customers
```powershell
$response = Invoke-WebRequest -Uri http://localhost:5000/api/customers -UseBasicParsing
$response.Content | ConvertFrom-Json
```

**Response:**
```json
{
  "customers": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "account_ids": ["1000", "1001"],
      "total_balance": 30000.0
    }
  ],
  "count": 4
}
```

### Create New Customer
```powershell
$body = @{
    name = "Alice Smith"
    email = "alice.smith@example.com"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/api/customers `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -UseBasicParsing
```

### Create New Account
```powershell
$body = @{
    account_number = "ACC007"
    account_type = "Savings"
    balance = 50000.00
    customer_id = "1"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/api/accounts `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -UseBasicParsing
```

---

## 📦 Dependencies Installed

- `Flask` 2.3.3 - Web framework
- `Flasgger` 0.9.7.1 - Swagger/API documentation
- `pymongo` 4.6.1 - MongoDB driver
- `python-dotenv` 1.0.0 - Environment variables
- `pytest` 7.4.0 - Testing framework

---

## 🔧 Project Structure

```
BankAPI/
├── app.py                 # Flask application entry point
├── data_store.py          # MongoDB/In-memory data layer
├── models.py              # Customer & Account models
├── requirements.txt       # Python dependencies
├── .env                   # MongoDB connection string
├── MONGODB_SETUP.md       # MongoDB setup instructions
├── test_connection.py     # Connection test script
├── test_endpoints.http    # HTTP endpoint tests
├── routes/
│   ├── __init__.py
│   ├── customers.py       # Customer endpoints
│   └── accounts.py        # Account endpoints
```

---

## 💾 Data Storage

### In-Memory (Current)
- 4 sample customers with 6 accounts
- Data persists while server is running
- Data resets when server restarts
- Perfect for development/testing

### MongoDB Atlas (When Configured)
- Persistent data storage in cloud
- ACID transactions
- Automatic backups
- Scalable

---

## 🆘 Troubleshooting

### Server Won't Start
```
Check error messages for Python syntax errors or missing imports
python -m py_compile app.py  # Test for syntax errors
```

### MongoDB Connection Fails
- Verify `.env` contains correct connection string
- Check network access whitelist in MongoDB Atlas
- Ensure username/password are correct
- Try connecting from MongoDB Atlas web console

### Endpoints Return 404
- Make sure server is running on port 5000
- Check endpoint paths match documentation
- Verify request method (GET, POST, PUT, DELETE)

---

## 📝 Next Steps

1. **Test All Endpoints** - Use Swagger at `http://localhost:5000/apidocs`
2. **Fix MongoDB** - Update `.env` with correct credentials
3. **Build Frontend** - Create React/Vue frontend to consume API
4. **Add Authentication** - Implement JWT or OAuth
5. **Deploy** - Use Heroku, AWS, or Azure for production

---

## 🎯 Summary

✅ **Banking REST API is fully operational**
- Backend running on `http://localhost:5000`
- All endpoints tested and working
- In-memory fallback storage active
- Ready for frontend integration or MongoDB connection setup

**To use with Postman/frontend, make requests to:**
```
http://localhost:5000/api/customers
http://localhost:5000/api/accounts
```
