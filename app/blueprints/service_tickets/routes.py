from .schemas import service_schema, services_schema
from app.models import Service
from marshmallow import ValidationError
from flask import request, jsonify
from app.models import db
from sqlalchemy import select
from . import services_bp
from app.models import Mechanic
from app.models import Customer

# Create a new service ticket
@services_bp.route("/", methods=['POST'])
def create_service():
    try:
        service = service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.get(Customer, service.customer_id)
    if not customer:
        return {"error": "Customer not found."}, 404
    
    existing = db.session.execute(select(Service).where(Service.VIN == service.VIN,
            Service.service_date == service.service_date)).scalar_one_or_none()
    if existing:
        return {"error": "Service ticket already exists."}, 400

    db.session.add(service)
    db.session.commit()

    return service_schema.jsonify(service), 201

# Assign a mechanic to a service ticket
@services_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service, ticket_id)
    if not ticket:
        return {"error": "Service ticket not found"}, 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"error": "Mechanic not found"}, 404
    
    if mechanic in ticket.mechanics:
        return {"error": "Mechanic already assigned to this ticket"}, 400
    
    ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_schema.jsonify(ticket), 200

# Remove a mechanic from a service ticket
@services_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service, ticket_id)
    if not ticket:
        return {"error": "Service ticket not found"}, 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return {"error": "Mechanic not found"}, 404
    
    if mechanic not in ticket.mechanics:
        return {"error": "Mechanic is not assigned to this ticket"}, 400
    
    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return service_schema.jsonify(ticket), 200

# Get all service tickets
@services_bp.route("/", methods=['GET'])
def get_services():
    query= select(Service)
    services = db.session.execute(query).scalars().all()
    return services_schema.jsonify(services), 200