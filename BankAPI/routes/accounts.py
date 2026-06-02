"""
Account Routes for Banking API
"""
from flask import Blueprint, request, jsonify
from models import Account
from data_store import DataStore

accounts_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')


# GET /api/accounts - Retrieve all accounts
@accounts_bp.route('', methods=['GET'])
def get_all_accounts():
    """
    Get all bank accounts
    ---
    tags:
      - Accounts
    responses:
      200:
        description: List of all accounts
        schema:
          type: object
          properties:
            accounts:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1000
                  account_number:
                    type: string
                    example: ACC001
                  account_type:
                    type: string
                    example: Savings
                  balance:
                    type: number
                    example: 25000.00
                  customer_id:
                    type: integer
                    example: 1
                  created_at:
                    type: string
                    example: "2026-06-02T10:42:50.165410"
            count:
              type: integer
              example: 6
    """
    accounts = [account.to_dict() for account in DataStore.accounts]
    return jsonify({'accounts': accounts, 'count': len(accounts)}), 200


# GET /api/accounts/{id} - Retrieve account by ID
@accounts_bp.route('/<int:account_id>', methods=['GET'])
def get_account_by_id(account_id):
    """
    Get a specific account by ID
    ---
    tags:
      - Accounts
    parameters:
      - name: account_id
        in: path
        type: integer
        required: true
        example: 1000
    responses:
      200:
        description: Account details
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1000
            account_number:
              type: string
              example: ACC001
            account_type:
              type: string
              example: Savings
            balance:
              type: number
              example: 25000.00
            customer_id:
              type: integer
              example: 1
      404:
        description: Account not found
    """
    account = DataStore.get_account_by_id(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify(account.to_dict()), 200


# GET /api/accounts/search?name={name} - Get accounts by customer name
@accounts_bp.route('/search', methods=['GET'])
def get_account_by_name():
    """Get accounts belonging to customers matching the given name"""
    name = request.args.get('name', '').strip().lower()
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400
    
    matching_customers = [
        customer for customer in DataStore.customers 
        if name in customer.name.lower()
    ]
    
    customer_ids = [customer.id for customer in matching_customers]
    
    matching_accounts = [
        account.to_dict() 
        for account in DataStore.accounts 
        if account.customer_id in customer_ids
    ]
    
    return jsonify({'accounts': matching_accounts, 'count': len(matching_accounts)}), 200


# POST /api/accounts - Create new account
@accounts_bp.route('', methods=['POST'])
def create_account():
    """
    Create a new bank account
    ---
    tags:
      - Accounts
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - account_number
            - account_type
            - customer_id
          properties:
            account_number:
              type: string
              example: ACC007
            account_type:
              type: string
              enum: [Savings, Checking]
              example: Savings
            balance:
              type: number
              example: 50000.00
            customer_id:
              type: integer
              example: 1
    responses:
      201:
        description: Account created successfully
      400:
        description: Invalid input
      404:
        description: Customer not found
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    account_number = data.get('account_number', '').strip()
    account_type = data.get('account_type', '').strip()
    balance = data.get('balance', 0.0)
    customer_id = data.get('customer_id')
    
    # Validation
    if not account_number:
        return jsonify({'error': 'Account number is required'}), 400
    if not account_type:
        return jsonify({'error': 'Account type is required'}), 400
    if account_type not in ['Savings', 'Checking']:
        return jsonify({'error': 'Account type must be Savings or Checking'}), 400
    if not isinstance(balance, (int, float)) or balance < 0:
        return jsonify({'error': 'Balance must be a non-negative number'}), 400
    if not customer_id:
        return jsonify({'error': 'Customer ID is required'}), 400
    
    # Check if customer exists
    customer = DataStore.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # Create new account
    new_account = Account(account_number, account_type, balance, customer_id)
    DataStore.accounts.append(new_account)
    
    # Add account to customer's account list
    customer.accounts.append(new_account.id)
    
    return jsonify(new_account.to_dict()), 201


# PUT /api/accounts/{id} - Update account
@accounts_bp.route('/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    """Update account properties"""
    account = DataStore.get_account_by_id(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Update fields if provided
    if 'account_type' in data:
        account_type = data['account_type'].strip()
        if account_type not in ['Savings', 'Checking']:
            return jsonify({'error': 'Account type must be Savings or Checking'}), 400
        account.account_type = account_type
    
    if 'balance' in data:
        balance = data['balance']
        if not isinstance(balance, (int, float)) or balance < 0:
            return jsonify({'error': 'Balance must be a non-negative number'}), 400
        account.balance = balance
    
    if 'account_number' in data and data['account_number'].strip():
        account.account_number = data['account_number'].strip()
    
    return jsonify(account.to_dict()), 200


# DELETE /api/accounts/{id} - Delete account
@accounts_bp.route('/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    """Delete an account from the records"""
    account = DataStore.get_account_by_id(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    # Remove account from customer's account list
    customer = DataStore.get_customer_by_id(account.customer_id)
    if customer and account.id in customer.accounts:
        customer.accounts.remove(account.id)
    
    # Delete account
    DataStore.accounts.remove(account)
    
    return jsonify({'message': f'Account {account_id} deleted successfully'}), 200
