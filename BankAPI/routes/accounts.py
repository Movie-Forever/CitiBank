"""
Account Routes for Banking API
"""
from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from data_store import DataStore

accounts_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')


def serialize_account(account):
    """Convert account document to JSON-serializable format"""
    if not account:
        return None
    
    if DataStore.use_mongodb:
        return {
            'id': str(account['_id']),
            'account_number': account.get('account_number'),
            'account_type': account.get('account_type'),
            'balance': account.get('balance', 0),
            'customer_id': account.get('customer_id'),
            'created_at': account.get('created_at', '')
        }
    else:
        return account


# GET /api/accounts - Retrieve all accounts
@accounts_bp.route('', methods=['GET'])
def get_all_accounts():
    """Get all bank accounts"""
    accounts = DataStore.get_all_accounts()
    serialized = [serialize_account(a) for a in accounts]
    return jsonify({'accounts': serialized, 'count': len(serialized)}), 200


# GET /api/accounts/{id} - Retrieve account by ID
@accounts_bp.route('/<account_id>', methods=['GET'])
def get_account_by_id(account_id):
    """Get a specific account by ID"""
    account = DataStore.get_account_by_id(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify(serialize_account(account)), 200


# GET /api/accounts/search?name={name} - Get accounts by customer name
@accounts_bp.route('/search', methods=['GET'])
def get_account_by_name():
    """Get accounts belonging to customers matching the given name"""
    name = request.args.get('name', '').strip().lower()
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400
    
    all_customers = DataStore.get_all_customers()
    if DataStore.use_mongodb:
        matching_customers = [c for c in all_customers if name in c.get('name', '').lower()]
        customer_ids = [str(c['_id']) for c in matching_customers]
    else:
        matching_customers = [c for c in all_customers if name in c['name'].lower()]
        customer_ids = [str(c['id']) for c in matching_customers]
    
    all_accounts = DataStore.get_all_accounts()
    if DataStore.use_mongodb:
        matching_accounts = [serialize_account(a) for a in all_accounts if a.get('customer_id') in customer_ids]
    else:
        matching_accounts = [serialize_account(a) for a in all_accounts if a['customer_id'] in customer_ids]
    
    return jsonify({'accounts': matching_accounts, 'count': len(matching_accounts)}), 200


# POST /api/accounts - Create new account
@accounts_bp.route('', methods=['POST'])
def create_account():
    """Create a new bank account"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    account_number = data.get('account_number', '').strip()
    account_type = data.get('account_type', '').strip()
    balance = data.get('balance', 0.0)
    customer_id = data.get('customer_id')
    
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
    
    customer = DataStore.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    new_account = DataStore.create_account(account_number, account_type, balance, customer_id)
    if not new_account:
        return jsonify({'error': 'Failed to create account'}), 500
    
    if DataStore.use_mongodb:
        DataStore.customers_collection.update_one({'_id': ObjectId(customer_id)}, {'$push': {'accounts': str(new_account['_id'])}})
    else:
        try:
            cid = int(customer_id)
            for c in DataStore.customers:
                if c.id == cid:
                    c.accounts.append(new_account['id'])
                    break
        except:
            pass
    
    return jsonify(serialize_account(new_account)), 201


# PUT /api/accounts/{id} - Update account
@accounts_bp.route('/<account_id>', methods=['PUT'])
def update_account(account_id):
    """Update account properties"""
    account = DataStore.get_account_by_id(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    if DataStore.use_mongodb:
        update_data = {}
        if 'account_type' in data:
            account_type = data['account_type'].strip()
            if account_type not in ['Savings', 'Checking']:
                return jsonify({'error': 'Account type must be Savings or Checking'}), 400
            update_data['account_type'] = account_type
        if 'balance' in data:
            balance = data['balance']
            if not isinstance(balance, (int, float)) or balance < 0:
                return jsonify({'error': 'Balance must be a non-negative number'}), 400
            update_data['balance'] = balance
        if 'account_number' in data and data['account_number'].strip():
            update_data['account_number'] = data['account_number'].strip()
        if update_data:
            DataStore.accounts_collection.update_one({'_id': ObjectId(account_id)}, {'$set': update_data})
            account = DataStore.get_account_by_id(account_id)
    else:
        if 'account_type' in data:
            account_type = data['account_type'].strip()
            if account_type not in ['Savings', 'Checking']:
                return jsonify({'error': 'Account type must be Savings or Checking'}), 400
            account['account_type'] = account_type
        if 'balance' in data:
            balance = data['balance']
            if not isinstance(balance, (int, float)) or balance < 0:
                return jsonify({'error': 'Balance must be a non-negative number'}), 400
            account['balance'] = balance
        if 'account_number' in data and data['account_number'].strip():
            account['account_number'] = data['account_number'].strip()
    
    return jsonify(serialize_account(account)), 200


# DELETE /api/accounts/{id} - Delete account
@accounts_bp.route('/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    """Delete an account from the records"""
    account = DataStore.get_account_by_id(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    if DataStore.use_mongodb:
        customer_id = account.get('customer_id')
        if customer_id:
            try:
                DataStore.customers_collection.update_one({'_id': ObjectId(customer_id)}, {'$pull': {'accounts': account_id}})
            except:
                pass
        DataStore.accounts_collection.delete_one({'_id': ObjectId(account_id)})
    else:
        try:
            aid = int(account_id)
            customer_id = account['customer_id']
            cid = int(customer_id)
            for c in DataStore.customers:
                if c.id == cid and aid in c.accounts:
                    c.accounts.remove(aid)
                    break
            DataStore.accounts = [a for a in DataStore.accounts if a.id != aid]
        except:
            pass
    
    return jsonify({'message': f'Account {account_id} deleted successfully'}), 200
