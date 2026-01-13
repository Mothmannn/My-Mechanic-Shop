from app.extensions import ma
from app.models import Service
from marshmallow import fields
from app.blueprints.mechanics.schemas import MechanicSchema
from app.models import Mechanic

class MechanicNameOnlySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("name",)
        load_instance = True

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Int(required=True)
    mechanics = fields.Nested(MechanicSchema, many=True)
    #mechanics = fields.Nested(MechanicNameOnlySchema, many=True)
    class Meta:
        model = Service
        load_instance = True
        fields=("id", "VIN", "service_date", "service_desc", "customer_id", "mechanics")
        exclude = ("service_date",)
        include_fk=True

class EditServiceSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")


service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
edit_service_schema = EditServiceSchema()