import io

from PIL import Image
from flask import Blueprint, g
from flask import request, jsonify, send_file
from flask_expects_json import expects_json
from sqlalchemy import asc

from app.models import User, Sport, Event
from config import NON_NULL_STRING

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route("/", methods=["GET"])
def get_profile_info():
    return jsonify({"msg": "Successfully get profile",
                    "profile": g.user.to_json()}), 200


@profile_bp.route("/", methods=["PUT"])
@expects_json({
    'type': 'object',
    'properties': {
        'first_name': NON_NULL_STRING,
        'last_name': {'type': 'string'},
        'current_job': {'type': 'string'},
        'current_zip': NON_NULL_STRING,
        'about_me': {'type': 'string'}
    },
    'required': ['first_name', 'current_zip']
})
def save_profile_info():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    user = g.user
    first_name = request.json.get('first_name', None)
    if first_name:
        user.first_name = first_name
    last_name = request.json.get('last_name', None)
    if last_name:
        user.last_name = last_name
    current_job = request.json.get('current_job', None)
    if current_job:
        user.current_job = current_job
    current_zip = request.json.get('current_zip', None)
    if current_zip:
        user.current_zip = current_zip
    about_me = request.json.get('about_me', None)
    if about_me:
        user.about_me = about_me
    user.save_to_db()
    return jsonify({"msg": "Successfully updated profile",
                    "profile": user.to_json()}), 200


@profile_bp.route("/profile_image", methods=["PUT"])
def update_profile_image():
    user = g.user
    if request.method == "PUT":
        image_data = request.files.get("file", None)
        if image_data is not None:
            file_type = image_data.content_type.split("/")[1]
            i = Image.open(image_data)
            i.thumbnail((100, 100))
            output = io.BytesIO()
            i.save(output, format=file_type)
            user.image = output.getvalue()
            user.save_to_db()
            return jsonify({"msg": "Successfully updated profile image"}), 200
        else:
            return jsonify({"msg": "Error updating profile image"}), 400


@profile_bp.route("/get_profile_image/<user_id>", methods=["GET"])
def get_profile_image(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "Bad email or password"}), 401
    if request.method == "GET":
        if user.image is not None:
            return send_file(io.BytesIO(user.image), attachment_filename="user_profile.jpeg", mimetype="image/jpg")
        else:
            return jsonify({"msg": "User has not image"}), 400


@profile_bp.route("/events", methods=["GET"])
def get_my_events():
    soccer = Sport.query.filter_by(title="soccer").first()
    events = Event.query.order_by(asc(Event.timestamp)).filter_by(sports_id=soccer.id).filter_by(created_by_user_id=g.user.id)
    return jsonify({"msg": "Successfully retrieved user's events",
                    "events": [i.to_json() for i in events]}), 200
