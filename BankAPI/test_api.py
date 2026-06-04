"""
Test Suite for Banking REST API
Comprehensive unit and integration tests for all endpoints
"""
import pytest
import json
from app import create_app
from data_store import DataStore


@pytest.fixture
def client():
    """Create test client with fresh data store"""
    app = create_app()
    app.config['TESTING'] = True
    
    # Reset ID counters before each test
    from models import Customer, Account
    Customer._id_counter = 1
    Account._id_counter = 1000
    
    DataStore.initialize()
    return app.test_client()


class TestCustomerEndpoints:
    """Test suite for all customer endpoints"""
    
    def test_get_all_customers_success(self, client):
        """Test: GET /api/customers returns all customers with 200"""
        response = client.get('/api/customers')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'customers' in data
        assert 'count' in data
        assert data['count'] == 4
        assert data['customers'][0]['name'] == 'John Doe'
    
    def test_get_all_customers_contains_accounts(self, client):
        """Test: Customer response includes account_ids"""
        response = client.get('/api/customers')
        data = json.loads(response.data)
        customer = data['customers'][0]
        assert 'account_ids' in customer
        assert len(customer['account_ids']) > 0
    
    def test_get_customer_by_id_success(self, client):
        """Test: GET /api/customers/1 returns customer with 200"""
        response = client.get('/api/customers/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['name'] == 'John Doe'
        assert data['email'] == 'john.doe@example.com'
    
    def test_get_customer_by_id_not_found(self, client):
        """Test: GET /api/customers/999 returns 404"""
        response = client.get('/api/customers/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Customer not found'
    
    def test_get_customer_by_name_success(self, client):
        """Test: GET /api/customers/search?name=John returns matching customers"""
        response = client.get('/api/customers/search?name=John')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2  # John Doe and Robert Johnson
        assert all('john' in c['name'].lower() for c in data['customers'])
    
    def test_get_customer_by_name_no_match(self, client):
        """Test: GET /api/customers/search?name=NonExistent returns empty list"""
        response = client.get('/api/customers/search?name=NonExistent')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
    
    def test_get_customer_by_name_missing_parameter(self, client):
        """Test: GET /api/customers/search without name returns 400"""
        response = client.get('/api/customers/search')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_premium_customers_success(self, client):
        """Test: GET /api/customers/premium returns customers with balance > $10k"""
        response = client.get('/api/customers/premium')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'premium_customers' in data
        assert 'threshold' in data
        assert data['threshold'] == 10000.0
        # John Doe (30k) and Jane Smith (18k) should be premium
        assert data['count'] == 2
        assert all(c['total_balance'] > 10000.0 for c in data['premium_customers'])
    
    def test_create_customer_success(self, client):
        """Test: POST /api/customers creates new customer with 201"""
        new_customer = {
            'name': 'Alice Williams',
            'email': 'alice@example.com'
        }
        response = client.post('/api/customers',
                              data=json.dumps(new_customer),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Alice Williams'
        assert data['email'] == 'alice@example.com'
        assert 'id' in data
        assert data['id'] == 5  # Next ID after 4 existing customers
    
    def test_create_customer_missing_name(self, client):
        """Test: POST /api/customers without name returns 400"""
        new_customer = {
            'email': 'test@example.com'
        }
        response = client.post('/api/customers',
                              data=json.dumps(new_customer),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_customer_missing_email(self, client):
        """Test: POST /api/customers without email returns 400"""
        new_customer = {
            'name': 'Test User'
        }
        response = client.post('/api/customers',
                              data=json.dumps(new_customer),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_create_customer_no_body(self, client):
        """Test: POST /api/customers without body returns 400"""
        response = client.post('/api/customers',
                              data=json.dumps(None),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_update_customer_success(self, client):
        """Test: PUT /api/customers/1 updates customer with 200"""
        update_data = {
            'name': 'John Updated',
            'email': 'john.updated@example.com'
        }
        response = client.put('/api/customers/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'John Updated'
        assert data['email'] == 'john.updated@example.com'
    
    def test_update_customer_not_found(self, client):
        """Test: PUT /api/customers/999 returns 404"""
        update_data = {'name': 'Test'}
        response = client.put('/api/customers/999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
    
    def test_update_customer_partial(self, client):
        """Test: PUT /api/customers/1 with only name updates only name"""
        update_data = {'name': 'Only Name Updated'}
        response = client.put('/api/customers/1',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Only Name Updated'
        assert data['email'] == 'john.doe@example.com'  # Email unchanged
    
    def test_delete_customer_success(self, client):
        """Test: DELETE /api/customers/1 removes customer with 200"""
        response = client.delete('/api/customers/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verify customer is deleted
        check = client.get('/api/customers/1')
        assert check.status_code == 404
    
    def test_delete_customer_cascades_accounts(self, client):
        """Test: DELETE /api/customers/1 also deletes associated accounts"""
        # Get customer's accounts before deletion
        before = client.get('/api/customers/1')
        customer_data = json.loads(before.data)
        account_ids = customer_data['account_ids']
        
        # Delete customer
        response = client.delete('/api/customers/1')
        assert response.status_code == 200
        
        # Verify all customer's accounts are deleted
        for account_id in account_ids:
            check = client.get(f'/api/accounts/{account_id}')
            assert check.status_code == 404
    
    def test_delete_customer_not_found(self, client):
        """Test: DELETE /api/customers/999 returns 404"""
        response = client.delete('/api/customers/999')
        assert response.status_code == 404


class TestAccountEndpoints:
    """Test suite for all account endpoints"""
    
    def test_get_all_accounts_success(self, client):
        """Test: GET /api/accounts returns all accounts with 200"""
        response = client.get('/api/accounts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'accounts' in data
        assert 'count' in data
        assert data['count'] == 6
    
    def test_get_all_accounts_structure(self, client):
        """Test: Account response includes all required fields"""
        response = client.get('/api/accounts')
        data = json.loads(response.data)
        account = data['accounts'][0]
        assert 'id' in account
        assert 'account_number' in account
        assert 'account_type' in account
        assert 'balance' in account
        assert 'customer_id' in account
    
    def test_get_account_by_id_success(self, client):
        """Test: GET /api/accounts/1000 returns account with 200"""
        response = client.get('/api/accounts/1000')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 1000
        assert data['account_number'] == 'ACC001'
        assert data['account_type'] == 'Savings'
        assert data['balance'] == 25000.0
    
    def test_get_account_by_id_not_found(self, client):
        """Test: GET /api/accounts/9999 returns 404"""
        response = client.get('/api/accounts/9999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_account_by_name_success(self, client):
        """Test: GET /api/accounts/search?name=Jane returns Jane's accounts"""
        response = client.get('/api/accounts/search?name=Jane')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2  # Jane has 2 accounts
        assert all(a['customer_id'] == 2 for a in data['accounts'])
    
    def test_get_account_by_name_no_match(self, client):
        """Test: GET /api/accounts/search?name=NonExistent returns empty"""
        response = client.get('/api/accounts/search?name=NonExistent')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
    
    def test_create_account_success(self, client):
        """Test: POST /api/accounts creates new account with 201"""
        new_account = {
            'account_number': 'ACC999',
            'account_type': 'Savings',
            'balance': 50000.0,
            'customer_id': 1
        }
        response = client.post('/api/accounts',
                              data=json.dumps(new_account),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['account_number'] == 'ACC999'
        assert data['account_type'] == 'Savings'
        assert data['balance'] == 50000.0
        assert 'id' in data
    
    def test_create_account_invalid_type(self, client):
        """Test: POST /api/accounts with invalid type returns 400"""
        new_account = {
            'account_number': 'ACC999',
            'account_type': 'InvalidType',
            'balance': 1000.0,
            'customer_id': 1
        }
        response = client.post('/api/accounts',
                              data=json.dumps(new_account),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_account_negative_balance(self, client):
        """Test: POST /api/accounts with negative balance returns 400"""
        new_account = {
            'account_number': 'ACC999',
            'account_type': 'Savings',
            'balance': -1000.0,
            'customer_id': 1
        }
        response = client.post('/api/accounts',
                              data=json.dumps(new_account),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_create_account_missing_required_field(self, client):
        """Test: POST /api/accounts without account_number returns 400"""
        new_account = {
            'account_type': 'Savings',
            'balance': 1000.0,
            'customer_id': 1
        }
        response = client.post('/api/accounts',
                              data=json.dumps(new_account),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_create_account_customer_not_found(self, client):
        """Test: POST /api/accounts with non-existent customer returns 404"""
        new_account = {
            'account_number': 'ACC999',
            'account_type': 'Savings',
            'balance': 1000.0,
            'customer_id': 999
        }
        response = client.post('/api/accounts',
                              data=json.dumps(new_account),
                              content_type='application/json')
        assert response.status_code == 404
    
    def test_update_account_balance_success(self, client):
        """Test: PUT /api/accounts/1000 updates balance with 200"""
        update_data = {'balance': 99999.0}
        response = client.put('/api/accounts/1000',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['balance'] == 99999.0
    
    def test_update_account_type_success(self, client):
        """Test: PUT /api/accounts/1000 updates account_type with 200"""
        update_data = {'account_type': 'Checking'}
        response = client.put('/api/accounts/1000',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['account_type'] == 'Checking'
    
    def test_update_account_invalid_type(self, client):
        """Test: PUT /api/accounts/1000 with invalid type returns 400"""
        update_data = {'account_type': 'InvalidType'}
        response = client.put('/api/accounts/1000',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_update_account_negative_balance(self, client):
        """Test: PUT /api/accounts/1000 with negative balance returns 400"""
        update_data = {'balance': -5000.0}
        response = client.put('/api/accounts/1000',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_update_account_not_found(self, client):
        """Test: PUT /api/accounts/9999 returns 404"""
        update_data = {'balance': 1000.0}
        response = client.put('/api/accounts/9999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
    
    def test_delete_account_success(self, client):
        """Test: DELETE /api/accounts/1000 removes account with 200"""
        response = client.delete('/api/accounts/1000')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verify account is deleted
        check = client.get('/api/accounts/1000')
        assert check.status_code == 404
    
    def test_delete_account_removes_from_customer(self, client):
        """Test: DELETE /api/accounts/1000 removes from customer's account list"""
        # Get customer before deletion
        before = client.get('/api/customers/1')
        customer_before = json.loads(before.data)
        assert 1000 in customer_before['account_ids']
        
        # Delete account
        response = client.delete('/api/accounts/1000')
        assert response.status_code == 200
        
        # Check customer's accounts
        after = client.get('/api/customers/1')
        customer_after = json.loads(after.data)
        assert 1000 not in customer_after['account_ids']
    
    def test_delete_account_not_found(self, client):
        """Test: DELETE /api/accounts/9999 returns 404"""
        response = client.delete('/api/accounts/9999')
        assert response.status_code == 404


class TestDataIntegrity:
    """Test suite for data integrity and relationships"""
    
    def test_customer_account_relationship(self, client):
        """Test: Customer account_ids match actual accounts"""
        customers = json.loads(client.get('/api/customers').data)['customers']
        accounts = json.loads(client.get('/api/accounts').data)['accounts']
        
        for customer in customers:
            for account_id in customer['account_ids']:
                # Account should exist in accounts list
                assert any(a['id'] == account_id for a in accounts)
    
    def test_account_customer_reference_valid(self, client):
        """Test: All accounts reference valid customers"""
        customers = json.loads(client.get('/api/customers').data)['customers']
        accounts = json.loads(client.get('/api/accounts').data)['accounts']
        
        customer_ids = {c['id'] for c in customers}
        for account in accounts:
            assert account['customer_id'] in customer_ids


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
