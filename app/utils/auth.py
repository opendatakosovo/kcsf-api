import jwt
from flask import request, Response
from bson import json_util
from functools import wraps
from app import mongo, secret_key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        print secret_key

        if not token:
            return Response(
                        response=json_util.dumps({'success': False, 'msg': 'Token is missing!'}),
                        mimetype='application/json')

        try:
            data = jwt.decode(token, secret_key)
            current_user = mongo.db.user.find_one({'email': data['email']})
        except:
            return Response(
                        response=json_util.dumps({'success': False, 'msg': 'Token is invalid!!'}),
                        mimetype='application/json')

        return f(current_user, *args, **kwargs)

    return decorated