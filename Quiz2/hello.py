from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response

app = Flask(__name__)

users=[]

@app.route('/', methods=['GET'])
def hello():
    return "Hello!"

@app.route('/users', methods=['POST'])
def new_users():
    name = request.form['name']
    user = {
        'id': len(users)+1,
        'name': name
    }
    users.append(user)
    return jsonify(user), 201

@app.route('/users/<int:ID>', methods=['GET'])
def get_users(ID):
    user = [user for user in users if user['id'] == ID]
    if len(user) == 0:
        abort(404)
    return jsonify(user), 200

@app.route('/users/<int:ID>', methods=['DELETE'])
def deleteUser(ID):
    user = [user for user in users if user['id'] == ID]
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True}), 204

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)