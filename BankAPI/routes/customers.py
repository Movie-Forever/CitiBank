"""
Customer Routes for Banking API
"""
from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from data_store import DataStore

customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')


def serialize_customer(customer):
    """Convert customer document to JSON-serializable format"""
    if not customer:
        return None
    
    if DataStore.use_mongodb:
        return {
            'id': str(customer['_id']),
            'name': customer.get('name'),
            'email': customer.get('email'),
            'account_ids': customer.get('accounts', []),
            'created_at': customer.get('created_at', '')
        }
    else:
        return customer


# GET /api/customers - Retrieve all customers
@customers_bp.route('', methods=['GET'])
def get_all_customers():
    """Get all bank customers"""
    customers = DataStore.get_all_customers()
    serialized = [serialize_customer(c) for c in customers]
    return jsonify({'customers': serialized, 'count': len(serialized)}), 200


# GET /api/customers/{id} - Retrieve customer by ID
@customers_bp.route('/<customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    """Get customer by ID"""
    customer = DataStore.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    result = serialize_customer(customer)
    if DataStore.use_mongodb:
        total_balance = DataStore.get_total_balance(str(customer['_id']))
    else:
        total_balance = DataStore.get_total_balance(str(customer['id']))
    result['total_balance'] = total_balance
    
    return jsonify(result), 200


# GET /api/customers/search?name={name} - Search customers by name
@customers_bp.route('/search', methods=['GET'])
def get_customer_by_name():
    """Search customers by name"""
    name = request.args.get('name', '').strip().lower()
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400
    
    all_customers = DataStore.get_all_customers()
    if DataStore.use_mongodb:
        matches = [serialize_customer(c) for c in all_customers if name in c.get('name', '').lower()]
    else:
        matches = [serialize_customer(c) for c in all_customers if name in c['name'].lower()]
    
    return jsonify({'customers': matches, 'count': len(matches)}), 200


# GET /api/customers/premium - Get premium customers (total balance > $10,000)
@customers_bp.route('/premium', methods=['GET'])
def get_all_premium_customers():
    """Get premium customers with total balance above threshold"""
    premium_threshold = 10000.0
    premium_customers = []
    
    all_customers = DataStore.get_all_customers()
    for customer in all_customers:
        if DataStore.use_mongodb:
            customer_id = str(customer['_id'])
        else:
            customer_id = str(customer['id'])
        total_balance = DataStore.get_total_balance(customer_id)
        if total_balance > premium_threshold:
            customer_dict = serialize_customer(customer)
            customer_dict['total_balance'] = total_balance
            premium_customers.append(customer_dict)
    
    return jsonify({
        'premium_customers': premium_customers,
        'count': len(premium_customers),
        'threshold': premium_threshold
    }), 200


# POST /api/customers - Create new customer
@customers_bp.route('', methods=['POST'])
def create_customer():
    """Create a new customer"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    new_customer = DataStore.create_customer(name, email)
    if not new_customer:
        return jsonify({'error': 'Failed to create customer'}), 500
    
    return jsonify(serialize_customer(new_customer)), 201


# PUT /api/customers/{id} - Update customer
@customers_bp.route('/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update an existing customer"""
    customer = DataStore.get_customer_by_id(customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    if DataStore.use_mongodb:
        update_data = {}
        if 'name' in data and data['name'].strip():
            update_data['name'] = data['name'].strip()
        if 'email' in data and data['email'].strip():
            update_data['email'] = data['email'].strip()
        if update_data:
            DataStore.customers_collection.update_one({'_id': ObjectId(customer_id)}, {'$set': update_data})
            customer = DataStore.get_customer_by_id(customer_id)
    else:
        if 'name' in data and data['name'].strip():
            customer['name'] = data['name'].strip()
        if 'email' in data and data['email'].strip():
            customer['email'] = data['email'].strip()
    
    return jsonify(serialize_customer(customer)), 200


# DELETE /api/customers/{id} - Delete customer and associated accounts
@customers_bp.route('/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer and their associated accounts"""
    customer = DataStore.get_customer_by_id(customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    if DataStore.use_mongodb:
        DataStore.accounts_collection.delete_many({'customer_id': customer_id})
        DataStore.customers_collection.delete_one({'_id': ObjectId(customer_id)})
    else:
        try:
            cid = int(customer_id)
            DataStore.accounts = [a for a in DataStore.accounts if a.customer_id != cid]
            DataStore.customers.remove(customer)
        except:
            pass
    
    return jsonify({'message': f'Customer {customer_id} deleted successfully'}), 200
