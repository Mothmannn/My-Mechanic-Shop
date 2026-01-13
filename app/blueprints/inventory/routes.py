from app.extensions import limiter, cache
from .schemas import inventory_schema, inventories_schema
from app.models import Inventory
from marshmallow import ValidationError
from flask import request, jsonify
from app.models import db
from sqlalchemy import select
from . import inventory_bp
from app.utils.util import encode_token, token_required

# Create a new part in inventory
@inventory_bp.route("/", methods=['POST'])
#@limiter.limit("5 per day")
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Inventory).where(Inventory.part_name == inventory_data['part_name'])
    existing_inventory = db.session.execute(query).scalars().all()
    if existing_inventory:
        return jsonify({"error": "Part already exists in inventory."}), 400

    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201

# Get all parts in inventory
@inventory_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_inventory():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page', 8))
        query = select(Inventory)
        inventory = db.paginate(query, page=page, per_page=per_page)
        return inventories_schema.jsonify(inventory.items), 200
    except:
        query= select(Inventory)
        inventory = db.session.execute(query).scalars().all()
        return inventories_schema.jsonify(inventory), 200

#GET SPECIFIC inventory
@inventory_bp.route("/<int:inventory_id>", methods=['GET'])
def get_inventory_by_id(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if inventory:
        return inventory_schema.jsonify(inventory), 200
    return jsonify({"error": "Part not found in inventory."}), 404

# Update a inventory
@inventory_bp.route("/<int:inventory_id>", methods=['PUT'])
@limiter.limit("5 per month")
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error": "Part not found in inventory."}), 404
    
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200

#DELETE SPECIFIC inventory
@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
@limiter.limit("5 per day")
def delete_inventory(inventory_id):
    part = db.session.get(Inventory, inventory_id)

    if not part:
        return jsonify({"error": "Part not found in inventory."}), 404

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted part {part.part_name}"})