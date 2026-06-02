"""
In-Memory Data Store for Banking API
"""
from models import Customer, Account


class DataStore:
    """Simulated database with in-memory collections"""
    customers = []
    accounts = []
    
    @classmethod
    def initialize(cls):
        """Initialize with seed data"""
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
    
    @classmethod
    def get_customer_by_id(cls, customer_id):
        """Get customer by ID"""
        for customer in cls.customers:
            if customer.id == customer_id:
                return customer
        return None
    
    @classmethod
    def get_account_by_id(cls, account_id):
        """Get account by ID"""
        for account in cls.accounts:
            if account.id == account_id:
                return account
        return None
    
    @classmethod
    def get_total_balance(cls, customer_id):
        """Calculate total balance for a customer across all accounts"""
        total = 0.0
        for account in cls.accounts:
            if account.customer_id == customer_id:
                total += account.balance
        return total
