from functools import wraps
from flask import request, jsonify 
from coding_acme import app
from coding_acme.models import User
import jwt

def token_required(flask_function):
    @wraps(flask_function)
    def decorater(*args, **kwargs):
        token = none

        try:
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token'].split(' ')[1]
        except:
            if not token:
                return jsonify({'message':'yo Token missing!'}), 401

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            current_user_token = User.query.filter_by(id = data['public_id']).first()
        except:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            return jsonify({'message': 'Token invalid'}), 401
        return flask_function(current_user_token, *args, **kwargs)
    return decorater