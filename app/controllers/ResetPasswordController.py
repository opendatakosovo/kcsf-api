# coding=utf-8

from bson import json_util
import json
from app import mongo, bcrypt, mail
from flask import request, Response
import datetime

from datetime import timedelta
import random
import string
from app.utils.mailer import sendResetPassword

def resetPassword(code):
    print request.method

    if request.method == 'POST':

        print "post"
        
        data       = json_util.loads(request.data)
        reset_data = mongo.db.reset_passwords.find_one({'code': code})

    	if reset_data == None:
            return Response(
                response=json_util.dumps({'success': True, 'msg': u'Kodi është jo valid!'}),
                mimetype='application/json')

        if reset_data['user_id']:

            code_expired =  datetime.datetime.now().strftime('%b %d %Y %I:%M%p')  > reset_data['expires_after'].strftime('%b %d %Y %I:%M%p')

            if code_expired:
                return Response(
                response=json_util.dumps({'success': False, 'msg': 'Kodi ka skaduar!'}),
                mimetype='application/json')

            # Hashing new password
            hash_new_pwd = bcrypt.generate_password_hash(data['newPassword'])

            # Update password and "used" field in reset_password
            mongo.db.user.update({'_id': reset_data['user_id']}, {'$set': { 'password': hash_new_pwd } })
            mongo.db.reset_passwords.remove({'_id': reset_data['_id']})

            return Response(
                response=json_util.dumps({'success': True, 'msg': u'Fjalëkalimi u ndryshua me sukses!'}),
                mimetype='application/json')

        return Response(
                response=json_util.dumps({'success': True, 'msg': u'Gabim në server!'}),
                mimetype='application/json')

    elif request.method == 'GET':

        print "GET"
       
        reset_data = mongo.db.reset_passwords.find_one({'code': code})
        if reset_data :
            date_now = datetime.datetime.now()
            my_date = reset_data.get("expires_after")
            my_date = my_date.replace(tzinfo=None)
            if my_date <= date_now:
                return Response(
                    response=json_util.dumps({'success': False, 'msg': 'Ka skaduar tokeni'}),
                    mimetype='application/json')
            elif my_date > date_now:
                return Response(
                    response=json_util.dumps({'success': True, 'msg': 'Duke ndërruar fjalëkalimin!'}),
                    mimetype='application/json')
        else:
                return Response(
                    response=json_util.dumps({'success': False, 'msg': 'Tokeni jo valid'}),
                    mimetype='application/json')

    return 'true'


# Email user with reset password link 
def preResetPassword():

    rand  = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
    data  = json_util.loads(request.data)
    email = data['email']

    if email == '':
    	return Response(
            response=json_util.dumps({'success': True, 'msg': 'Fusha për email është obligative!'}),
            mimetype='application/json')

    try:
        user    = mongo.db.user.find_one({'email': email})
        code    = rand + '_' + str(user['_id'])
        expires = datetime.datetime.now() + timedelta(days=1)

        # return 'True'
        mongo.db.reset_passwords.insert({
            'user_id': user['_id'],
            'user_email': user['email'],
            'code': code,
            'created_at': datetime.datetime.now(),
            'expires_after': expires,
            })

        msg = sendResetPassword(user, request, code)
        mail.send(msg)
        return Response(
            response=json_util.dumps({'success': True, 'msg': u'Kërkesa u dergua me sukses!'}),
            mimetype='application/json')
    except Exception as e:
        return Response(
            response=json_util.dumps({'success': False, 'msg': e.message}),
            mimetype='application/json')