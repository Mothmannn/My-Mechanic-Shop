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
    mechanics = fields.Nested(MechanicNameOnlySchema, many=True)
    class Meta:
        model = Service
        load_instance=True
        exclude = ("service_date",)
        include_fk=True

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)