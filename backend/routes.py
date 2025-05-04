from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture_by_id = [picture for picture in data if picture["id"] == id]
    if not picture_by_id or len(picture_by_id) == 0:
        # return 404 if picture not found
        return jsonify({"message": "Picture not found"}), 404
    return jsonify(picture_by_id[0]), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    picture_by_id = [picture for picture in data if picture["id"] == new_picture.get("id")]
    # if picture exists, return 302
    if len(picture_by_id) > 0:
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302
    data.append(new_picture)
    return jsonify(new_picture), 201
    

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()
    picture_by_id = [picture for picture in data if picture["id"] == id]
    # if picture not found, return 404
    if len(picture_by_id) == 0:
        return jsonify({"message": "Picture not found"}), 404
    # update the picture
    data.remove(picture_by_id[0])
    data.append(updated_picture)
    return jsonify(updated_picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture_by_id = [picture for picture in data if picture["id"] == id]
    # if picture not found, return 404
    if len(picture_by_id) == 0:
        return jsonify({"message": "picture not found"}), 404
    # delete the picture
    data.remove(picture_by_id[0])
    return jsonify({}), 204
