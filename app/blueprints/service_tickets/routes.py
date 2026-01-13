from app.extensions import limiter, cache
from app.utils.util import token_required
from .schemas import service_schema, services_schema, edit_service_schema
from marshmallow import ValidationError
from flask import request, jsonify
from sqlalchemy import select
from . import services_bp
from app.models import Mechanic, Service, Customer, db

# Create a new service ticket
@services_bp.route("/", methods=['POST'])
#@limiter.limit("1 per 3 minutes")
@token_required
def create_service(customer_id):
    try:
        service = service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.get(Customer, customer_id)
    if not customer:
        return {"error": "Customer not found."}, 404

    existing = db.session.execute(
        select(Service).where(
            Service.VIN == service.VIN,
            Service.service_date == service.service_date,
            Service.customer_id == customer_id
        )
    ).scalar_one_or_none()

    if existing:
        return {"error": "Service ticket already exists."}, 400
    
    customer.service_tickets.append(service)

    db.session.commit()

    return service_schema.jsonify(service), 201

# Assign a mechanic to a service ticket
# @services_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
# @token_required
# def assign_mechanic(customer_id, ticket_id, mechanic_id):
#     ticket = db.session.get(Service, ticket_id)
#     if not ticket:
#         return {"error": "Service ticket not found"}, 404
    
#     if ticket.customer_id != customer_id:
#         return {"error": "Unauthorized access to this service ticket"}, 403
    
#     mechanic = db.session.get(Mechanic, mechanic_id)
#     if not mechanic:
#         return {"error": "Mechanic not found"}, 404
    
#     if mechanic in ticket.mechanics:
#         return {"error": "Mechanic already assigned to this ticket"}, 400
    
#     ticket.mechanics.append(mechanic)
#     db.session.commit()

#     return service_schema.jsonify(ticket), 200

# Remove a mechanic from a service ticket
# @services_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
# @token_required
# def remove_mechanic(customer_id, ticket_id, mechanic_id):
#     ticket = db.session.get(Service, ticket_id)
#     if not ticket:
#         return {"error": "Service ticket not found"}, 404
    
#     if ticket.customer_id != customer_id:
#         return {"error": "Unauthorized access to this service ticket"}, 403
    
#     mechanic = db.session.get(Mechanic, mechanic_id)
#     if not mechanic:
#         return {"error": "Mechanic not found"}, 404
    
#     if mechanic not in ticket.mechanics:
#         return {"error": "Mechanic is not assigned to this ticket"}, 400
    
#     ticket.mechanics.remove(mechanic)
#     db.session.commit()

#     return service_schema.jsonify(ticket), 200

# Get all service tickets
@services_bp.route("/", methods=['GET'])
#@cache.cached(timeout=60)
def get_services():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page', 10))
        query= select(Service)
        services = db.paginate(query, page=page, per_page=per_page)
        return services_schema.jsonify(services.items), 200
    except:
        query= select(Service)
        services = db.session.execute(query).scalars().all()
        return services_schema.jsonify(services), 200

@services_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_my_service_tickets(customer_id):
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page', 10))
        query = select(Service).where(Service.customer_id == customer_id)
        my_tickets = db.paginate(query, page=page, per_page=per_page)
        return services_schema.jsonify(my_tickets), 200
    except:
        query = select(Service).where(Service.customer_id == customer_id)
        my_tickets = db.session.execute(query).scalars().all()

        if not my_tickets:
            return jsonify({
                'message': 'No service tickets found for this customer.'
            }), 404

        return services_schema.jsonify(my_tickets), 200
    

@services_bp.route("/<int:service_id>/edit", methods=['PUT'])
@token_required
def edit_service_ticket(customer_id, service_id):
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    try:
        service_edits = edit_service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    service_ticket = db.session.get(Service, service_id)
    if not service_ticket:
        return {"error": "Service ticket not found"}, 404

    # 🔒 ownership check
    if service_ticket.customer_id != customer_id:
        return {"error": "Unauthorized"}, 403

    # Current mechanic IDs
    current_ids = {m.id for m in service_ticket.mechanics}

    # Desired mechanic IDs
    desired_ids = (
        current_ids
        | set(service_edits["add_mechanic_ids"])
    ) - set(service_edits["remove_mechanic_ids"])

    # Fetch mechanics fresh
    mechanics = (
        db.session.execute(
            select(Mechanic).where(Mechanic.id.in_(desired_ids))
        )
        .scalars()
        .all()
    )

    # 🔑 Replace the relationship entirely
    service_ticket.mechanics = mechanics

    db.session.commit()
    db.session.refresh(service_ticket)

    return service_schema.jsonify(service_ticket), 200


@services_bp.route("/search", methods=['GET'])
def search_service_tickets():
    vin_query = request.args.get('VIN', None)
    query = select(Service).where(Service.VIN.like(f'%{vin_query}%'))
    services = db.session.execute(query).scalars().all()
    return services_schema.jsonify(services), 200