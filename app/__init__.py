from flask import Flask, redirect, url_for
from .extensions import ma, limiter
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import services_bp
from .blueprints.inventory import inventory_bp
from .extensions import cache
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My Mechanic Shop API"
    }
)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #Initialize Extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #Root route - redirect to Swagger UI
    @app.route('/')
    def index():
        return redirect('/api/docs')

    #Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers' )
    app.register_blueprint(mechanics_bp, url_prefix = '/mechanics')
    app.register_blueprint(services_bp, url_prefix = '/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix = '/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprintw

    return app