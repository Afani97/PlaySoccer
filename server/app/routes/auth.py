from flask import Blueprint, session, g
from flask import request, jsonify
from config import NON_NULL_STRING
from app.models import User
from flask_expects_json import expects_json

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route("/register", methods=["POST"])
@expects_json({
    'type': 'object',
    'properties': {
        'email': NON_NULL_STRING,
        'password': NON_NULL_STRING,
        'name': NON_NULL_STRING,
        'zip': NON_NULL_STRING
    },
    'required': ['email', 'password', 'name', 'zip']
})
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    name = request.json.get('name', None)
    zip = request.json.get('zip', None)
    if not email or not password or not name or not zip:
        return jsonify({"msg": "Missing name, zip, email and password parameter"}), 400

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify({"msg": "Account already created"}), 401
    else:
        user = User(email, password, name, "", zip)
        user.save_to_db()

    session["email"] = email
    return jsonify({"msg": "Register successful",
                    "user": user.to_json()}), 200


@auth_bp.route("/login", methods=["POST"])
@expects_json({
    'type': 'object',
    'properties': {
        'email': NON_NULL_STRING,
        'password': NON_NULL_STRING
    },
    'required': ['email', 'password']
})
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or user.password != password:
        return jsonify({"msg": "Bad email or password"}), 401

    session["email"] = email
    return jsonify({"msg": "Login successful",
                    "user": user.to_json()}), 200


@auth_bp.route("/update_email", methods=["PUT"])
@expects_json({
    'type': 'object',
    'properties': {
        'email': NON_NULL_STRING,
    },
    'required': ['email']
})
def update_email():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get("email", None)
    if email is None:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "Email already used"}), 400
    user = g.user
    user.email = email
    user.save_to_db()
    return jsonify({"msg": "Email update successful"}), 200


@auth_bp.route("/update_password", methods=["PUT"])
@expects_json({
    'type': 'object',
    'properties': {
        'current_password': NON_NULL_STRING,
        'new_password': NON_NULL_STRING,
    },
    'required': ['current_password', 'new_password']
})
def update_password():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    user = g.user
    current_password = request.json.get("current_password", None)
    if current_password is None or user.password != current_password:
        return jsonify({"msg": "Error updating password"}), 400
    new_password = request.json.get("new_password", None)
    if new_password is None or user.password == new_password:
        return jsonify({"msg": "Error updating password"}), 400
    user.password = new_password
    user.save_to_db()
    return jsonify({"msg": "Password update successful"}), 200


@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.pop("email", None)
    return jsonify({"msg": "Successfully logged out"}), 200