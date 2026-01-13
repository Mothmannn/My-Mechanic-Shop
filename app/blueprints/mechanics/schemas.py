
from app.extensions import ma
from app.models import Mechanic

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        #load_instance=True
        exclude = ("service_tickets",)

    assignments = ma.auto_field(dump_only=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)