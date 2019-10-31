import flask
from flask import request
from flask import jsonify
import os
import json
import dotenv
dotenv.load_dotenv()
app = flask.Flask(__name__)
app.config["DEBUG"] = True
# class Controller:
#     @staticmethod
#     def take_headers(request):
#         headers={"Authorization":request.headers.get('Authorization'),
#         "Content-Type":request.headers.get("Content-Type")}
#         return headers
#     def process_endpoint(self):
#         headers=take_headers(request)
#         if headers==valid_headers:
#             number_of_page = int(request.args.get('page'))
        
        
# class Cadence(Controller):

# class Step(Controller):

# class User(Controller):

# class People(Controller):

# class CadenceMembership(Controller):

# class Actions(Controller):

# class Emails(Controller):

SALESLOFT_TOKEN = "Bearer " + os.getenv("SALESLOFT_API_KEY")
valid_headers={"Authorization": SALESLOFT_TOKEN,"Content-Type": "application/json"}
def take_headers(request):
    headers={"Authorization":request.headers.get('Authorization'),
    "Content-Type":request.headers.get("Content-Type")}
    return headers
@app.route('/cadences.json', methods=['GET'])
def cadence():
    headers=take_headers(request)
    if headers==valid_headers:
        number_of_page = int(request.args.get('page'))
        return jsonify(my_dict['/cadences.json'][number_of_page])
@app.route('/steps.json', methods=['GET'])
def step():
    headers=take_headers(request)
    if headers==valid_headers:
        number_of_page = int(request.args.get('page'))
        return jsonify(my_dict['/steps.json'][number_of_page])

@app.route('/users.json', methods=['GET'])
def user():
    headers=take_headers(request)
    if headers==valid_headers:
        number_of_page = int(request.args.get('page'))
        return jsonify(my_dict['/users.json'])


@app.route('/people.json', methods=['GET'])
def people():
    headers=take_headers(request)
    if headers==valid_headers:
        number_of_page = int(request.args.get('page'))
        return jsonify(my_dict['/people.json'][number_of_page])


@app.route('/cadence_memberships.json', methods=['GET'])
def membership():
    headers=take_headers(request)
    if headers==valid_headers:
        number_of_page = int(request.args.get('page'))
        return jsonify(my_dict['/cadence_memberships.json'][number_of_page])
@app.route('/actions.json', methods=['GET'])
def actions():
    headers=take_headers(request)
    if headers==valid_headers:
        number_of_page = int(request.args.get('page'))
        return jsonify(my_dict['/actions.json'][number_of_page])

@app.route('/activities/emails.json', methods=['GET'])
def emails():
    headers=take_headers(request)
    if headers==valid_headers:
        number_of_page = int(request.args.get('page'))
        return jsonify(my_dict['/activities/emails.json'][number_of_page])

my_dict={}
with open('responses.json','r') as f:
    my_dict=json.load(f)

if __name__=="__main__":
    app.run()