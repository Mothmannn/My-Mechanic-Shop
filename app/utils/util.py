# app/utils/util.py
from datetime import datetime, timedelta, timezone
from flask import jsonify, request
from functools import wraps
import jwt

SECRET_KEY = "SECRET SECRET SECRET"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(tz=timezone.utc),
        'sub': str(customer_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:

            token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'missing token'}), 400
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                print(data)
                customer_id = int(data['sub'])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'token expired'}), 400
            except jwt.InvalidTokenError:
                return jsonify({'message': 'invalid token'}), 400
            
            return f(customer_id, *args, **kwargs)
        
        else:
            return jsonify({'message': 'You must be logged in to access this.'}), 400
        
    return decorated