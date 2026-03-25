import json
import os
import math
from flask import Flask, jsonify, request

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/customers', methods=['GET'])
def get_customers():
    data = load_data()
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    if page < 1 or limit < 1:
        return jsonify({"error": "Page and limit must be positive integers"}), 400

    start = (page - 1) * limit
    end = start + limit
    paginated_data = data[start:end]

    return jsonify({
        "data": paginated_data,
        "total": len(data),
        "page": page,
        "limit": limit
    })

@app.route('/api/customers/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    data = load_data()
    customer = next((c for c in data if c['customer_id'] == customer_id), None)
    if customer:
        return jsonify(customer)
    return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
