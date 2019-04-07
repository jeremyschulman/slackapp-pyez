from flask import jsonify
from blueprint import blueprint


@blueprint.route("/health", methods=["GET"])
def api_health():
    return jsonify({'ok': True}), 200
