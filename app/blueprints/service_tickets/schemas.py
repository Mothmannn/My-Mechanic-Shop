from app.extensions import ma
from app.models import Service
from marshmallow import fields
from marshmallow import validates_schema
from app.blueprints.mechanics.schemas import MechanicSchema
from app.models import Mechanic

class MechanicNameOnlySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("name",)
        load_instance = True

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Int(load_only=True)
    mechanics = fields.Nested(MechanicSchema, many=True)
    inventory = fields.Nested('app.blueprints.inventory.schemas.InventorySchema', many=True)
    #mechanics = fields.Nested(MechanicNameOnlySchema, many=True)
    class Meta:
        model = Service
        load_instance = True
        fields=("id", "VIN", "service_date", "service_desc", "customer_id", "mechanics", "inventory")
        include_fk=True

class EditMechanicsServiceSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int())
    remove_mechanic_ids = fields.List(fields.Int())

    @validates_schema
    def validate_mechanic_ids(self, data, **kwargs):
        add_mechanic_ids = data.get('add_mechanic_ids')
        remove_mechanic_ids = data.get('remove_mechanic_ids')
        if not add_mechanic_ids and not remove_mechanic_ids:
            raise ma.ValidationError('At least one of add_mechanic_ids or remove_mechanic_ids must be present.')

    class Meta:
        fields = ('add_mechanic_ids', 'remove_mechanic_ids')

class EditPartsServiceSchema(ma.Schema):
    add_parts_ids = fields.List(fields.Int())
    remove_parts_ids = fields.List(fields.Int())

    @validates_schema
    def validate_parts_ids(self, data, **kwargs):
        add_parts_ids = data.get('add_parts_ids')
        remove_parts_ids = data.get('remove_parts_ids')
        if not add_parts_ids and not remove_parts_ids:
            raise ma.ValidationError('At least one of add_parts_ids or remove_parts_ids must be present.')

    class Meta:
        fields = ('add_parts_ids', 'remove_parts_ids')


service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
edit_mechanics_service_schema = EditMechanicsServiceSchema()
edit_parts_service_schema = EditPartsServiceSchema()