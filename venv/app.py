from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

print(os.urandom(24).hex())

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# MongoDB configuration
client = MongoClient(os.getenv('MONGO_URI'))
db = client['customer_management']
customers_collection = db['customers']

# Routes

@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    # Perform data validation (e.g., check required fields, unique email/phone)
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    customer = {
        'name': data['name'],
        'email': data['email'],
        'phone': data.get('phone', ''),
        'address': data.get('address', '')
    }
    customers_collection.insert_one(customer)
    return jsonify({'message': 'Customer added successfully'}), 201

@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = list(customers_collection.find())
    for customer in customers:
        customer['_id'] = str(customer['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(customers), 200

@app.route('/api/customers/<string:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    # Perform data validation here if needed
    update_data = {
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'address': data.get('address')
    }
    result = customers_collection.update_one(
        {'_id': ObjectId(customer_id)}, 
        {'$set': update_data}
    )
    if result.matched_count == 0:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify({'message': 'Customer updated successfully'}), 200

@app.route('/api/customers/<string:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    result = customers_collection.delete_one({'_id': ObjectId(customer_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify({'message': 'Customer deleted successfully'}), 200

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
