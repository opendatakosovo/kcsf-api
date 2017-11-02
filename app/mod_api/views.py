from flask import Blueprint, request, Response, render_template
from bson import json_util
from app import mongo

mod_api = Blueprint('kcsf', __name__)


@mod_api.route('/', methods=['GET'])
def index():
    ''' Renders the API index page.
    :return:
    '''
    return render_template('index.html')


@mod_api.route('/comparison', methods=['POST'])
def comparison():
    json_string = request.data

    json_obj = json_util.loads(json_string)
    q1_id = json_obj['q1_id']
    q2_id = json_obj['q2_id']
    lang = json_obj['lang']

    aggregation = get_aggregation(q1_id, q2_id, lang)
    result = mongo.db.cso_survey.aggregate(aggregation)
    resp = Response(
        response=json_util.dumps(result['result']),
        mimetype='application/json')
    return resp


def get_aggregation(q1, q2, lang):
    array_questions = ["q7", "q22", "q77", "q109", "q128"]

    aggregation = build_aggregation_pipeline(q1, q2, lang)

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


def build_aggregation_pipeline(q1, q2, lang):
    q1_answer = str(q1) + ".answer." + lang
    q2_answer = str(q2) + ".answer." + lang
    match = {
        "$match": {
            q1_answer: {
                "$nin": ["", None]
            }
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
