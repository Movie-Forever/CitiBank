# MongoDB Atlas Setup Instructions

## Issue: Authentication Failed

The current connection is failing with "bad auth" error. Follow these steps:

### 1. Verify Your MongoDB Atlas Credentials
- Go to https://cloud.mongodb.com/
- Log in to your account
- Navigate to your **BankCluster**
- Click **Connect** → **Drivers**
- Copy the connection string (it should look like):
  ```
  mongodb+srv://<username>:<password>@bankcluster.38xmjwx.mongodb.net/?appName=BankCluster
  ```

### 2. Update the .env File
Replace the connection string in `.env`:
```
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@bankcluster.38xmjwx.mongodb.net/?appName=BankCluster
```

**Important:** 
- If your password contains special characters, they need to be URL-encoded
- Common special characters encoding:
  - `@` → `%40`
  - `:` → `%3A`
  - `#` → `%23`
  - etc.

### 3. Verify IP Whitelist in MongoDB Atlas
- Go to **Security** → **Network Access**
- Ensure your IP address is whitelisted (or add 0.0.0.0/0 to allow all IPs)

### 4. Test the Connection
```bash
python -c "from data_store import DataStore; DataStore.initialize()"
```

If successful, you should see:
```
✓ Connected to MongoDB Atlas successfully
✓ Seed data created: 4 customers, 6 accounts
```

### 5. Start the Server
```bash
python app.py
```

The server should run on `http://localhost:5000`
