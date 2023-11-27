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
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic["id"] == id:
            return pic
    return {"Message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.json

    if not new_pic:
        return {"message": "Invalid input parameter"}, 422

    for pic in data:
        if pic['id'] == new_pic['id']:
            return {"Message": f"picture with id {pic['id']} already present"}, 302

    try:
        data.append(new_pic)
    except NameError:
        return {"Message": "data not defined"}, 500

    return {"id": new_pic['id']}, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic_data = request.json
    if not pic_data:
        return {"message": "Invalid input parameter"}, 422
    
    for pic in data:
        if pic['id'] == pic_data['id']:
            pic.update(pic_data)
            return {"id": pic['id']}
    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return {"id": id}, 204

    return {"message": "picture not found"}, 404
