"""
Customer Routes for Banking API
"""
from flask import Blueprint, request, jsonify
from models import Customer
from data_store import DataStore

customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')


# GET /api/customers - Retrieve all customers
@customers_bp.route('', methods=['GET'])
def get_all_customers():
    """
    Get all bank customers
    ---
    tags:
      - Customers
    responses:
      200:
        description: List of all customers
        schema:
          type: object
          properties:
            customers:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: John Doe
                  email:
                    type: string
                    example: john.doe@example.com
                  account_ids:
                    type: array
                    items:
                      type: integer
                    example: [1000, 1001]
                  created_at:
                    type: string
                    example: "2026-06-02T10:42:50.165410"
            count:
              type: integer
              example: 4
    """
    customers = [customer.to_dict(include_accounts=True) for customer in DataStore.customers]
    return jsonify({'customers': customers, 'count': len(customers)}), 200


# GET /api/customers/{id} - Retrieve customer by ID
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    """Get customer by ID"""
    customer = DataStore.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer.to_dict(include_accounts=True)), 200


# GET /api/customers/search?name={name} - Search customers by name
@customers_bp.route('/search', methods=['GET'])
def get_customer_by_name():
    """Search customers by name"""
    name = request.args.get('name', '').strip().lower()
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400
    
    matches = [
        customer.to_dict(include_accounts=True) 
        for customer in DataStore.customers 
        if name in customer.name.lower()
    ]
    return jsonify({'customers': matches, 'count': len(matches)}), 200


# GET /api/customers/premium - Get premium customers (total balance > $10,000)
@customers_bp.route('/premium', methods=['GET'])
def get_all_premium_customers():
    """
    Get premium customers with total balance above threshold
    ---
    tags:
      - Customers
    responses:
      200:
        description: List of premium customers (total balance > $10,000)
        schema:
          type: object
          properties:
            premium_customers:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: John Doe
                  email:
                    type: string
                    example: john.doe@example.com
                  account_ids:
                    type: array
                    items:
                      type: integer
                    example: [1000, 1001]
                  total_balance:
                    type: number
                    example: 30000.0
            count:
              type: integer
              example: 2
            threshold:
              type: number
              example: 10000.0
    """
    premium_threshold = 10000.0
    premium_customers = []
    
    for customer in DataStore.customers:
        total_balance = DataStore.get_total_balance(customer.id)
        if total_balance > premium_threshold:
            customer_dict = customer.to_dict(include_accounts=True)
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
    
    # Validation
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Create new customer
    new_customer = Customer(name, email)
    DataStore.customers.append(new_customer)
    
    return jsonify(new_customer.to_dict(include_accounts=True)), 201


# PUT /api/customers/{id} - Update customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update an existing customer"""
    customer = DataStore.get_customer_by_id(customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Update fields if provided
    if 'name' in data and data['name'].strip():
        customer.name = data['name'].strip()
    if 'email' in data and data['email'].strip():
        customer.email = data['email'].strip()
    
    return jsonify(customer.to_dict(include_accounts=True)), 200


# DELETE /api/customers/{id} - Delete customer and associated accounts
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer and their associated accounts"""
    customer = DataStore.get_customer_by_id(customer_id)
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # Delete all associated accounts
    DataStore.accounts = [
        account for account in DataStore.accounts 
        if account.customer_id != customer_id
    ]
    
    # Delete customer
    DataStore.customers.remove(customer)
    
    return jsonify({'message': f'Customer {customer_id} deleted successfully'}), 200
