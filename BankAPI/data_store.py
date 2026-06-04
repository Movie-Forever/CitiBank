"""
MongoDB Data Store for Banking API (with fallback to in-memory)
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from models import Customer, Account

# Load environment variables
load_dotenv()


class DataStore:
    """MongoDB-based data store with in-memory fallback"""
    client = None
    db = None
    customers_collection = None
    accounts_collection = None
    
    # In-memory fallback
    customers = []
    accounts = []
    use_mongodb = False
    
    @classmethod
    def initialize(cls):
        """Initialize MongoDB connection and create seed data"""
        try:
            # MongoDB Connection String from environment
            mongo_uri = os.getenv('MONGODB_URI')
            if not mongo_uri:
                raise ValueError("MONGODB_URI environment variable not set")
            
            cls.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Verify connection
            cls.client.admin.command('ping')
            print("[OK] Connected to MongoDB Atlas successfully")
            
            # Access database and collections
            database_name = os.getenv('MONGODB_DB_NAME', 'BankCluster')
            cls.db = cls.client[database_name]
            cls.customers_collection = cls.db['customers']
            cls.accounts_collection = cls.db['accounts']
            
            cls.use_mongodb = True
            seed_database = os.getenv('SEED_DATABASE', 'false').lower() == 'true'
            if seed_database and cls.customers_collection.count_documents({}) == 0:
                cls._create_seed_data()
            
        except Exception as e:
            print(f"[ERROR] Failed to connect to MongoDB: {e}")
            if os.getenv('FLASK_ENV') == 'production':
                raise
            print("[INFO] Falling back to in-memory storage")
            cls.use_mongodb = False
            cls._initialize_in_memory()
    
    @classmethod
    def _initialize_in_memory(cls):
        """Initialize with in-memory seed data"""
        # Create sample customers
        customer1 = Customer("John Doe", "john.doe@example.com")
        customer2 = Customer("Jane Smith", "jane.smith@example.com")
        customer3 = Customer("Robert Johnson", "robert.j@example.com")
        customer4 = Customer("Emily Chen", "emily.chen@example.com")
        
        cls.customers = [customer1, customer2, customer3, customer4]
        
        # Create sample accounts
        account1 = Account("ACC001", "Savings", 25000.00, customer1.id)
        account2 = Account("ACC002", "Checking", 5000.00, customer1.id)
        account3 = Account("ACC003", "Savings", 15000.00, customer2.id)
        account4 = Account("ACC004", "Checking", 3000.00, customer2.id)
        account5 = Account("ACC005", "Savings", 8000.00, customer3.id)
        account6 = Account("ACC006", "Checking", 2000.00, customer4.id)
        
        cls.accounts = [account1, account2, account3, account4, account5, account6]
        
        # Link accounts to customers
        customer1.accounts = [account1.id, account2.id]
        customer2.accounts = [account3.id, account4.id]
        customer3.accounts = [account5.id]
        customer4.accounts = [account6.id]
        
        print("[OK] Using in-memory storage for development")
    
    @classmethod
    def _create_seed_data(cls):
        """Create initial seed data in MongoDB"""
        # Create sample customers
        customers_data = [
            {"name": "John Doe", "email": "john.doe@example.com", "accounts": []},
            {"name": "Jane Smith", "email": "jane.smith@example.com", "accounts": []},
            {"name": "Robert Johnson", "email": "robert.j@example.com", "accounts": []},
            {"name": "Emily Chen", "email": "emily.chen@example.com", "accounts": []}
        ]
        
        result = cls.customers_collection.insert_many(customers_data)
        customer_ids = result.inserted_ids
        
        # Create sample accounts
        accounts_data = [
            {"account_number": "ACC001", "account_type": "Savings", "balance": 25000.00, "customer_id": str(customer_ids[0])},
            {"account_number": "ACC002", "account_type": "Checking", "balance": 5000.00, "customer_id": str(customer_ids[0])},
            {"account_number": "ACC003", "account_type": "Savings", "balance": 15000.00, "customer_id": str(customer_ids[1])},
            {"account_number": "ACC004", "account_type": "Checking", "balance": 3000.00, "customer_id": str(customer_ids[1])},
            {"account_number": "ACC005", "account_type": "Savings", "balance": 8000.00, "customer_id": str(customer_ids[2])},
            {"account_number": "ACC006", "account_type": "Checking", "balance": 2000.00, "customer_id": str(customer_ids[3])}
        ]
        
        result = cls.accounts_collection.insert_many(accounts_data)
        account_ids = result.inserted_ids
        
        # Update customers with account references
        for i, customer_id in enumerate(customer_ids):
            accounts_for_customer = []
            if i == 0:
                accounts_for_customer = [str(account_ids[0]), str(account_ids[1])]
            elif i == 1:
                accounts_for_customer = [str(account_ids[2]), str(account_ids[3])]
            elif i == 2:
                accounts_for_customer = [str(account_ids[4])]
            elif i == 3:
                accounts_for_customer = [str(account_ids[5])]
            
            cls.customers_collection.update_one(
                {"_id": customer_id},
                {"$set": {"accounts": accounts_for_customer}}
            )
        
        print(f"[OK] Seed data created: {len(customer_ids)} customers, {len(account_ids)} accounts")
    
    @classmethod
    def get_all_customers(cls):
        """Get all customers"""
        if cls.use_mongodb:
            try:
                return list(cls.customers_collection.find())
            except Exception as e:
                print(f"Error getting customers: {e}")
                return []
        else:
            return [c.to_dict(include_accounts=True) for c in cls.customers]
    
    @classmethod
    def get_all_accounts(cls):
        """Get all accounts"""
        if cls.use_mongodb:
            try:
                return list(cls.accounts_collection.find())
            except Exception as e:
                print(f"Error getting accounts: {e}")
                return []
        else:
            return [a.to_dict() for a in cls.accounts]
    
    @classmethod
    def get_customer_by_id(cls, customer_id):
        """Get customer by ID"""
        if cls.use_mongodb:
            try:
                return cls.customers_collection.find_one({"_id": ObjectId(customer_id)})
            except Exception as e:
                print(f"Error getting customer: {e}")
                return None
        else:
            try:
                cid = int(customer_id)
                for c in cls.customers:
                    if c.id == cid:
                        return c
                return None
            except:
                return None
    
    @classmethod
    def get_account_by_id(cls, account_id):
        """Get account by ID"""
        if cls.use_mongodb:
            try:
                return cls.accounts_collection.find_one({"_id": ObjectId(account_id)})
            except Exception as e:
                print(f"Error getting account: {e}")
                return None
        else:
            try:
                aid = int(account_id)
                for a in cls.accounts:
                    if a.id == aid:
                        return a
                return None
            except:
                return None
    
    @classmethod
    def get_accounts_by_customer_id(cls, customer_id):
        """Get all accounts for a customer"""
        if cls.use_mongodb:
            try:
                return list(cls.accounts_collection.find({"customer_id": customer_id}))
            except Exception as e:
                print(f"Error getting accounts: {e}")
                return []
        else:
            try:
                cid = int(customer_id)
                return [a.to_dict() for a in cls.accounts if a.customer_id == cid]
            except:
                return []
    
    @classmethod
    def get_total_balance(cls, customer_id):
        """Calculate total balance for a customer across all accounts"""
        try:
            accounts = cls.get_accounts_by_customer_id(customer_id)
            if cls.use_mongodb:
                return sum(account.get('balance', 0) for account in accounts)
            else:
                return sum(account['balance'] for account in accounts)
        except Exception as e:
            print(f"Error calculating balance: {e}")
            return 0.0
    
    @classmethod
    def create_customer(cls, name, email):
        """Create a new customer"""
        if cls.use_mongodb:
            try:
                customer = {"name": name, "email": email, "accounts": []}
                result = cls.customers_collection.insert_one(customer)
                customer["_id"] = result.inserted_id
                return customer
            except Exception as e:
                print(f"Error creating customer: {e}")
                return None
        else:
            new_customer = Customer(name, email)
            cls.customers.append(new_customer)
            return new_customer.to_dict(include_accounts=True)
    
    @classmethod
    def create_account(cls, account_number, account_type, balance, customer_id):
        """Create a new account"""
        if cls.use_mongodb:
            try:
                account = {
                    "account_number": account_number,
                    "account_type": account_type,
                    "balance": balance,
                    "customer_id": customer_id
                }
                result = cls.accounts_collection.insert_one(account)
                account["_id"] = result.inserted_id
                return account
            except Exception as e:
                print(f"Error creating account: {e}")
                return None
        else:
            try:
                cid = int(customer_id)
                new_account = Account(account_number, account_type, balance, cid)
                cls.accounts.append(new_account)
                return new_account.to_dict()
            except:
                return None
    
    @classmethod
    def update_account_balance(cls, account_id, new_balance):
        """Update account balance"""
        if cls.use_mongodb:
            try:
                result = cls.accounts_collection.update_one(
                    {"_id": ObjectId(account_id)},
                    {"$set": {"balance": new_balance}}
                )
                return result.modified_count > 0
            except Exception as e:
                print(f"Error updating account: {e}")
                return False
        else:
            try:
                aid = int(account_id)
                for a in cls.accounts:
                    if a.id == aid:
                        a.balance = new_balance
                        return True
                return False
            except:
                return False
