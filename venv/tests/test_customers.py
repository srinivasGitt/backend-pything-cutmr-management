import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Clear the test database
            db.customers.delete_many({})
        yield client

def test_add_customer(client):
    # Test adding a new customer
    response = client.post('/api/customers', json={
        'name': 'Alice',
        'email': 'alice@example.com',
        'phone': '1234567890',
        'address': '123 Street'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['name'] == 'Alice'

def test_get_customers(client):
    # Add a customer to retrieve
    client.post('/api/customers', json={
        'name': 'Bob',
        'email': 'bob@example.com',
        'phone': '0987654321',
        'address': '456 Avenue'
    })
    
    # Test retrieving customers
    response = client.get('/api/customers')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) > 0

def test_update_customer(client):
    # Add a customer to update
    add_response = client.post('/api/customers', json={
        'name': 'Charlie',
        'email': 'charlie@example.com',
        'phone': '1112223333',
        'address': '789 Boulevard'
    })
    customer_id = add_response.get_json()['_id']

    # Update the customer
    response = client.put(f'/api/customers/{customer_id}', json={
        'name': 'Charlie Updated',
        'email': 'charlie@example.com',
        'phone': '1112223333',
        'address': '789 Boulevard'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['name'] == 'Charlie Updated'

def test_delete_customer(client):
    # Add a customer to delete
    add_response = client.post('/api/customers', json={
        'name': 'David',
        'email': 'david@example.com',
        'phone': '5556667777',
        'address': '101 Main St'
    })
    customer_id = add_response.get_json()['_id']

    # Delete the customer
    response = client.delete(f'/api/customers/{customer_id}')
    assert response.status_code == 200

    # Ensure the customer is deleted
    get_response = client.get('/api/customers')
    data = get_response.get_json()
    assert all(cust['_id'] != customer_id for cust in data)
