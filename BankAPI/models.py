"""
Data Models for Banking API
"""
from datetime import datetime


class Account:
    """Account Model"""
    _id_counter = 1000
    
    def __init__(self, account_number, account_type, balance=0.0, customer_id=None):
        self.id = Account._id_counter
        Account._id_counter += 1
        self.account_number = account_number
        self.account_type = account_type  # 'Savings', 'Checking'
        self.balance = balance
        self.customer_id = customer_id
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance,
            'customer_id': self.customer_id,
            'created_at': self.created_at
        }


class Customer:
    """Customer Model"""
    _id_counter = 1
    
    def __init__(self, name, email):
        self.id = Customer._id_counter
        Customer._id_counter += 1
        self.name = name
        self.email = email
        self.accounts = []  # List of Account IDs
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self, include_accounts=False):
        result = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }
        if include_accounts:
            result['account_ids'] = self.accounts
        return result
