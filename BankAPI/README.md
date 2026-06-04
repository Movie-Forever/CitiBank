# Banking REST API - Part 1

A secure, standard Banking REST API built with Flask following the MVC design pattern.

## Project Structure

```
BankAPI/
├── app.py              # Main Flask application entry point
├── models.py           # Customer and Account data models
├── data_store.py       # In-memory data storage with seed data
├── requirements.txt    # Python dependencies
├── routes/
│   ├── __init__.py
│   ├── customers.py    # Customer endpoints
│   └── accounts.py     # Account endpoints
└── README.md           # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` from `.env.example` and set real values locally or in your host dashboard:

```text
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?appName=BankCluster
MONGODB_DB_NAME=BankCluster
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
FLASK_ENV=production
SEED_DATABASE=false
```

### 3. Run the Application

```bash
python app.py
```

The API will start on the configured `PORT`, defaulting to `5000` for local development.

### Production Start Command

Use Gunicorn on Render or another Python host:

```bash
gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

## API Endpoints

### Customer Endpoints

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| GetAllCustomers | GET | `/api/customers` | Retrieves all customers |
| GetCustomerById | GET | `/api/customers/{id}` | Get customer by ID |
| GetCustomerByName | GET | `/api/customers/search?name={name}` | Search customers by name |
| GetAllPremiumCustomers | GET | `/api/customers/premium` | Get customers with balance > $10,000 |
| CreateCustomer | POST | `/api/customers` | Create new customer |
| UpdateCustomer | PUT | `/api/customers/{id}` | Update customer details |
| DeleteCustomer | DELETE | `/api/customers/{id}` | Delete customer and accounts |

### Account Endpoints

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| GetAllAccounts | GET | `/api/accounts` | Retrieves all accounts |
| GetAccountById | GET | `/api/accounts/{id}` | Get account by ID |
| GetAccountByName | GET | `/api/accounts/search?name={name}` | Get accounts by customer name |
| CreateAccount | POST | `/api/accounts` | Create new account |
| UpdateAccount | PUT | `/api/accounts/{id}` | Update account details |
| DeleteAccount | DELETE | `/api/accounts/{id}` | Delete account |

## Sample Data

On startup, the API initializes with:
- 4 Sample Customers
- 6 Sample Accounts

### Sample Customers:
- John Doe (ID: 1) - john.doe@example.com
- Jane Smith (ID: 2) - jane.smith@example.com
- Robert Johnson (ID: 3) - robert.j@example.com
- Emily Chen (ID: 4) - emily.chen@example.com

### Sample Accounts:
- ACC001, ACC002, ACC003, ACC004, ACC005, ACC006

## Request/Response Examples

### Get All Customers
```
GET /api/customers
Response: 200 OK
{
  "customers": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "account_ids": [1001, 1002],
      "created_at": "2024-01-01T10:00:00"
    }
  ],
  "count": 4
}
```

### Create Customer
```
POST /api/customers
Content-Type: application/json

{
  "name": "Alice Williams",
  "email": "alice.w@example.com"
}

Response: 201 Created
```

### Create Account
```
POST /api/accounts
Content-Type: application/json

{
  "account_number": "ACC007",
  "account_type": "Savings",
  "balance": 50000.00,
  "customer_id": 1
}

Response: 201 Created
```

## Features

- ✅ MVC Architecture (Controllers via Blueprints, Models, Data Store)
- ✅ RESTful HTTP Methods (GET, POST, PUT, DELETE)
- ✅ Proper HTTP Status Codes (200, 201, 404, 400, 500)
- ✅ In-memory data storage
- ✅ Input validation
- ✅ Error handling
- ✅ Seed data initialization

## Testing

Use the `test_endpoints.http` file with REST Client extension in VS Code, or import into Postman.

## Notes

- MongoDB data is preserved on application restart unless `SEED_DATABASE=true` is set for an empty database
- Premium customer threshold: $10,000
- Account types: Savings or Checking
