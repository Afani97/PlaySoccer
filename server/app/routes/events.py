import time
from datetime import datetime

from flask import Blueprint, g
from flask import request, jsonify
from flask_expects_json import expects_json
from sqlalchemy import asc

from app.models import Event, Sport
from config import NON_NULL_STRING

events_bp = Blueprint('events_bp', __name__)


@events_bp.route("/list", methods=["GET"])
def get_events():
    # TODO: Remove this, get from user model
    soccer = Sport.query.filter_by(title="soccer").first()
    current_page = request.args.get("page", 1)
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    events = Event.query.filter(Event.timestamp >= todays_datetime) \
        .order_by(asc(Event.timestamp)) \
        .filter_by(sports_id=soccer.id) \
        .paginate(int(current_page), 5, False).items
    return jsonify({"msg": "Successfully retrieved events",
                    "events": [i.to_json() for i in events]}), 200


@events_bp.route("/new_event", methods=["POST"])
@expects_json({
    'type': 'object',
    'properties': {
        'title': NON_NULL_STRING,
        'where': NON_NULL_STRING,
        'when': {
            'type': 'number',
            'minimum': int(time.time()) - (60 * 60 * 1000)
        },
        'max_players': {'type': 'string'},
        'additional_info': {'type': 'string'}
    },
    'required': ['title', 'where', 'when']
})
def create_new_event():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    title = request.json.get("title", None)
    where = request.json.get("where", None)
    when = request.json.get("when", None)
    if not title or not where or not when:
        return jsonify({"msg": "When and where cannot be empty"}), 401
    # TODO: Remove this, get from user model
    soccer = Sport.query.filter_by(title="soccer").first()
    new_event = Event(title, where, datetime.utcfromtimestamp(when), g.user.id, soccer.id)
    if request.json.get("max_players", None):
        new_event.member_limit_count = request.json.get("max_players")
    if request.json.get("additional_info", None):
        new_event.description = request.json.get("additional_info")
    new_event.save_to_db()
    return jsonify({"msg": "Successfully saved new event",
                    "event": new_event.to_json()}), 200


@events_bp.route("/<event_id>", methods=["GET"])
def get_event_details(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify({"msg": "Error retrieving event details"}), 400
    return jsonify({"msg": "Successfully retrieved event",
                    "event": event.to_json()}), 200


@events_bp.route("/<string:event_id>/edit", methods=["PUT"])
@expects_json({
    'type': 'object',
    'properties': {
        'title': NON_NULL_STRING,
        'where': NON_NULL_STRING,
        'when': {
            'type': 'number',
            'minimum': int(time.time()) - (60 * 60 * 1000)
        },
        'max_players': {'type': 'string'},
        'additional_info': {'type': 'string'}
    },
    'required': ['title', 'where', 'when']
})
def edit_event(event_id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return jsonify({"msg": "Cannot find event"}), 401
    title = request.json.get("title", None)
    where = request.json.get("where", None)
    when = request.json.get("when", None)
    if not title or not where or not when:
        return jsonify({"msg": "When and where cannot be empty"}), 401
    event.title = title
    event.location = where
    event.timestamp = datetime.utcfromtimestamp(when)
    if request.json.get("max_players", None):
        event.member_limit_count = request.json.get("max_players")
    if request.json.get("additional_info", None):
        event.description = request.json.get("additional_info")
    event.save_to_db()
    return jsonify({"msg": "Successfully updated event",
                    "event": event.to_json()}), 200


@events_bp.route("/<string:event_id>/delete", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return jsonify({"msg": "Cannot find event"}), 401
    event.delete_from_db()
    return jsonify({"msg": "Successfully removed event"}), 200


@events_bp.route("/join_event", methods=["PUT"])
@expects_json({
    'type': 'object',
    'properties': {
        'event_id': NON_NULL_STRING
    },
    'required': ['event_id']
})
def join_event():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    event_id = request.json.get("event_id", None)
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return jsonify({"msg": "Missing event"}), 400
    event.users.append(g.user)
    event.save_to_db()
    return jsonify({"msg": "Successfully added to event"})
