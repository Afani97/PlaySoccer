from flask import Blueprint, g
from flask import jsonify

current_bp = Blueprint('current_bp', __name__)


@current_bp.route("/", methods=["GET"])
def current_user():
    if g.user:
        return jsonify({"msg": "Current session valid",
                        "user": g.user.to_json()}), 200
    else:
        return jsonify({"msg": "Not valid session"}), 400
