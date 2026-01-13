from app.extensions import limiter, cache
from .schemas import customer_schema, customers_schema, login_schema
from app.models import Customer
from marshmallow import ValidationError
from flask import request, jsonify
from app.models import db
from sqlalchemy import select
from . import customers_bp
from app.utils.util import encode_token, token_required

@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email= credentials['email']
        password= credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "Successfully logged in.",
            "token": token
        }

        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password."}), 401


# Create a new customer
@customers_bp.route("/", methods=['POST'])
#@limiter.limit("5 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Customer with this email already exists."}), 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# Get all customers
@customers_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page', 8))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        query= select(Customer)
        customers = db.session.execute(query).scalars().all()
        return customers_schema.jsonify(customers), 200

# Update a Customer
@customers_bp.route("/", methods=['PUT'])
@token_required
@limiter.limit("5 per month")
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

#DELETE SPECIFIC CUSTOMER
@customers_bp.route("/", methods=['DELETE'])
@token_required
@limiter.limit("5 per day")
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted user {customer_id}"})

#GET SPECIFIC CUSTOMER
# @customers_bp.route("/<int:customer_id>", methods=['GET'])
# def get_customer(customer_id):
#     customer = db.session.get(Customer, customer_id)

#     if customer:
#         return customer_schema.jsonify(customer), 200
#     return jsonify({"error": "Customer not found."}), 404