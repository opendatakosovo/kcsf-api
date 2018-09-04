#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt, datetime, json
from os.path import join, dirname, realpath, os
from flask import Blueprint, request, Response, render_template
from bson import json_util
from app import mongo, bcrypt, secret_key, mail
from app.utils.auth import token_required
from app.utils.file_utils import allowedFiles, getFileName
from app.utils.mailer import sendResetPassword
from importer.data_importer_new import DataImporterNew
from importer.data_importer_old import DataImporterOld

from datetime import timedelta
from app.controllers.ResetPasswordController import resetPassword, preResetPassword


import time

# from mimetypes import MimeTypes
# import urllib

mod_api = Blueprint('kcsf', __name__)


UPLOAD_FOLDER = join(dirname(realpath(__file__)), "../../importer/data/")

@mod_api.route('/', methods=['GET'])
def index():
    ''' Renders the API index page.
    :return:
    '''
    return render_template('index.html')

@mod_api.route('/reset_password/<string:code>', methods=['GET', 'POST'])
def resetPass(code):
   return resetPassword(code)

@mod_api.route('/forgot_password', methods=['POST'])
def forgotPassword():
   return preResetPassword()

@mod_api.route('/register', methods=['POST'])
def register():
    data = json_util.loads(request.data)
    # Check if email is already used
    if mongo.db.user.find({'email': data['email']}).count() > 0:
        return Response(
        response=json_util.dumps({'success': False, 'msg': 'Email is already used'}),
        mimetype='application/json')

    # Check if password is matched with confirm password
    if data['password'] != data['confirmPassword']:
        return Response(
        response=json_util.dumps({'success': False, 'msg': 'Password and Confirm Password do not match!'}),
        mimetype='application/json')

    # Hashing password
    hash_pwd = bcrypt.generate_password_hash(data['password'])

    # Saving new user into db
    mongo.db.user.insert({
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'email': data['email'],
        'password': hash_pwd
    })

    return Response(
        response=json_util.dumps({'success': True, 'msg': 'User successfully saved!'}),
        mimetype='application/json')

@mod_api.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    data = json_util.loads(request.data)

    # Check if current password is not same
    if not bcrypt.check_password_hash(current_user['password'], data['currentPassword']):
        return Response(
            response=json_util.dumps({'success': False, 'msg': u'Fjalëkalimi aktual nuk është i saktë!'}),
            mimetype='application/json')
    
    # Check if new password is not longer than 6 chars
    if len(data['newPassword']) < 6 :
        return Response(
            response=json_util.dumps({'success': False, 'msg': u'Fjalëkalimi i ri duhet të jetë së paku 6 karaktere!'}),
            mimetype='application/json')

    # Check if new password is not same with confirm new password
    if data['newPassword'] != data['newPasswordConfirm']:
        return Response(
            response=json_util.dumps({'success': False, 'msg': u'Fjalëkalimi i ri nuk përputhet me konfirmimin e tij!'}),
            mimetype='application/json')

    # Hashing new password
    hash_new_pwd = bcrypt.generate_password_hash(data['newPassword'])

    mongo.db.user.update({'_id': current_user['_id']}, {'$set': { 'password': hash_new_pwd } })

    return Response(
        response=json_util.dumps({'success': True, 'msg': u'Fjalëkalimi u ndryshua me sukses!'}),
        mimetype='application/json')

@mod_api.route('/login', methods=['POST'])
def authenticate():
    data = json_util.loads(request.data)

    # Finding user by username or email
    user = mongo.db.user.find_one({'email': data['email']})

    # If user not found
    if not user:
        return Response(
        response=json_util.dumps({'success': False, 'msg': 'Perdoruesi nuk ekziston!'}),
        mimetype='application/json')

    # Checking password
    if bcrypt.check_password_hash(user['password'], data['password']):
        # If user is active give the token
        token = jwt.encode({'email': user['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, secret_key)

        return Response(response=json_util.dumps({'success': True, 
                                  'msg': 'Successfully login!', 
                                  'token': token.decode('UTF-8')
                                }),
        mimetype='application/json')

    # if password is wrong
    return Response(
        response=json_util.dumps({'success': False, 'msg': 'Fjalëkalimi nuk eshte i sakte!'}),
        mimetype='application/json')

@mod_api.route('/profile', methods=['GET'])
@token_required
def profile(current_user):

    user_data = {}
    user_data['firstName'] = current_user['firstName']
    user_data['lastName'] = current_user['lastName']
    user_data['email'] = current_user['email']

    return Response(
        response=json_util.dumps(user_data),
        mimetype='application/json'
    )

@mod_api.route('/import-data', methods=['POST'])
@token_required
def import_data(current_user):
    year = request.form['year']
    updated = False
    # Validation
    if year == '' or not bool(request.files):
        return Response(
            response=json_util.dumps({'success': False, 'msg': 'Fajlli i të dhënave dhe viti duhet te zgjedhen!'}),
            mimetype='application/json')
    
    # Getting the file
    data_file = request.files['data-file']
    answers_file = request.files['answers-file']
    questions_file = request.files['questions-file']
    
    # Get file mimetype 
    data_mime = data_file.mimetype
    question_mime = questions_file.mimetype
    answer_mime = questions_file.mimetype

    if (data_mime not in allowedFiles()) or (question_mime not in allowedFiles()) or (answer_mime not in allowedFiles()):
        return Response(
            response=json_util.dumps({'success': False, 'msg': 'Fajlli i të dhënave duhet te jete i tipit csv!'}),
            mimetype='application/json')

    # Year data directory
    data_dir = UPLOAD_FOLDER + '/' + year
    # Create year directory if not exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if data_file.filename != '':
        # Building new filename with extension from current filename of uploaded file        
        data_filename = 'cso-data' + '.' + data_file.filename.split('.')[len(data_file.filename.split('.')) - 1]

        # Saving uploaded file
        data_file.save(os.path.join(data_dir, data_filename))

    dataset = mongo.db.datasets.find_one({"year":year})
    if dataset:
        mongo.db.datasets.update({"year":year},{"$set":{"updatedAt":datetime.datetime.now()}})
        updated = True
    else:
        mongo.db.datasets.insert({"year":year,"createdAt":datetime.datetime.now(),"updatedAt":datetime.datetime.now()})
        
    getFileName(questions_file, "questions", data_dir)
    getFileName(answers_file, "answers", data_dir)
    splitedYearRange = year.split("-")
    if(int(splitedYearRange[0]) == 2015 and int(splitedYearRange[1]) == 2016):
        DataImporterOld().run(year)
    else:
        DataImporterNew().run(year)

    # Returning success response
    return Response(
        response=json_util.dumps({'success': True, 'msg': 'Fajlli i të dhënave u ngarkua me sukses!'}),
        mimetype='application/json'
    )

@mod_api.route('/comparison', methods=['POST'])
def comparison():
    json_string = request.data
    json_obj = json_util.loads(json_string)
    q1_id = json_obj['q1_id']
    q2_id = json_obj['q2_id']
    lang = json_obj['lang']
    year = str(json_obj['year'])

    aggregation = get_aggregation(q1_id, q2_id, lang, year)
    result = mongo.db.cso_survey.aggregate(aggregation)
    resp = Response(
        response=json_util.dumps(result['result']),
        mimetype='application/json')
    return resp

def get_aggregation(q1, q2, lang, year):
    if(year == "2015-2016"):
        array_questions = ["q7", "q22", "q77", "q109", "q128"]
    elif (year == "2017-2018"):
        array_questions = ["q7", "q22", "q32", "q69", "q94", "q113"]
    

    aggregation = build_aggregation_pipeline(q1, q2, lang, year)

    if q2 in array_questions:
        unwind = get_unwind(q2, lang)
        aggregation.insert(0, unwind)
    if q1 in array_questions:
        unwind = get_unwind(q1, lang)
        aggregation.insert(0, unwind)
    return aggregation

def get_unwind(question, lang):
    return {
        "$unwind": "$" + question + ".answer." + lang
    }

def build_aggregation_pipeline(q1, q2, lang, year):
    year = year
    q1_answer = str(q1) + ".answer." + lang
    q2_answer = str(q2) + ".answer." + lang
    match = {
        "$match": {
            q1_answer: {
                "$nin": ["", None]
            },
            "year": year

        }
    }
    group = {
        "$group": {
            "_id": {
                "type1": "$" + q1_answer
            },
            "count": {
                "$sum": 1
            }
        }
    }

    project = {
        "$project": {
            "_id": 0,
            "type1": "$_id.type1",
            "count": "$count"
        }
    }

    sort = {
        '$sort': {
            "type1": 1
        }
    }
    if q2 != "":
        match["$match"][q2_answer] = {}
        match["$match"][q2_answer]["$nin"] = ["", None]
        group['$group']['_id']["type2"] = "$" + q2_answer
        project["$project"]["type2"] = "$_id.type2"
        sort["$sort"] = {
            "type2": 1
        }
    aggregation = [match, group, project, sort]
    return aggregation
