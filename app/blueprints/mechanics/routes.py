from app.utils.util import token_required
from .schemas import mechanic_schema, mechanics_schema
from app.models import Mechanic
from marshmallow import ValidationError
from flask import request, jsonify
from app.models import db
from sqlalchemy import select
from . import mechanics_bp
from app.extensions import limiter, cache

# Create a new mechanic
@mechanics_bp.route("/", methods=['POST'])
#@limiter.limit("5 per day")
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({"error": "mechanic with this email already exists."}), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

# Get all mechanics
@mechanics_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_mechanics():
    query= select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200

# Get specific mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "mechanic not found."}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

# Delete a mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(customer_id, mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "mechanic not found."}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'mechanic id: {mechanic_id}, successfully deleted.'}), 200

@mechanics_bp.route("/service-leaderboard", methods=['GET'])
def service_leaderboard():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    # # update the assignments mapped column from the relationship count, persist to DB
    # for mech in mechanics:
    #     mech.assignments = len(mech.service_tickets) if mech.service_tickets else 0
    # db.session.commit()

    mechanics.sort(key=lambda mechanic: mechanic.assignments, reverse=True )

    return mechanics_schema.jsonify(mechanics), 200