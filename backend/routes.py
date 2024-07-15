from flask import Blueprint, request, jsonify
from .models import User, House, Room, Occupant
from . import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='User registered successfully'), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401

@auth.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@auth.route('/houses', methods=['GET'])
@jwt_required()
def get_houses():
    houses = House.query.all()
    houses_list = [{'id': house.id, 'name': house.name} for house in houses]
    return jsonify(houses=houses_list)

@auth.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    rooms = Room.query.all()
    rooms_list = [{'id': room.id, 'number': room.number, 'house_id': room.house_id} for room in rooms]
    return jsonify(rooms=rooms_list)

@auth.route('/occupants', methods=['GET'])
@jwt_required()
def get_occupants():
    occupants = Occupant.query.all()
    occupants_list = [{'id': occupant.id, 'name': occupant.name, 'room_id': occupant.room_id} for occupant in occupants]
    return jsonify(occupants=occupants_list)

@auth.route('/houses', methods=['POST'])
@jwt_required()
def add_house():
    data = request.get_json()
    new_house = House(name=data['name'])
    db.session.add(new_house)
    db.session.commit()
    return jsonify(message='House added successfully'), 201

@auth.route('/rooms', methods=['POST'])
@jwt_required()
def add_room():
    data = request.get_json()
    new_room = Room(number=data['number'], house_id=data['house_id'])
    db.session.add(new_room)
    db.session.commit()
    return jsonify(message='Room added successfully'), 201

@auth.route('/occupants', methods=['POST'])
@jwt_required()
def add_occupant():
    data = request.get_json()
    new_occupant = Occupant(name=data['name'], room_id=data['room_id'])
    db.session.add(new_occupant)
    db.session.commit()
    return jsonify(message='Occupant added successfully'), 201
