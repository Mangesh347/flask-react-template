from flask import Blueprint, request, jsonify
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient

# MongoDB connection (adjust as needed)
client = MongoClient("mongodb://localhost:27017/")
db = client["flask_app"]
comments_collection = db["comments"]

comment_blueprint = Blueprint("comments", __name__, url_prefix="/comments")

@comment_blueprint.route("/", methods=["POST"])
def add_comment():
    data = request.json
    comment = {
        "task_id": data.get("task_id"),
        "content": data.get("content"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = comments_collection.insert_one(comment)
    comment["_id"] = str(result.inserted_id)
    return jsonify(comment), 201

@comment_blueprint.route("/<comment_id>", methods=["PUT"])
def update_comment(comment_id):
    data = request.json
    comments_collection.update_one(
        {"_id": ObjectId(comment_id)},
        {"$set": {"content": data.get("content"), "updated_at": datetime.utcnow()}}
    )
    return jsonify({"message": "Comment updated"}), 200

@comment_blueprint.route("/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comments_collection.delete_one({"_id": ObjectId(comment_id)})
    return jsonify({"message": "Comment deleted"}), 200

@comment_blueprint.route("/", methods=["GET"])
def get_comments():
    task_id = request.args.get("task_id")
    comments = list(comments_collection.find({"task_id": task_id}))
    for c in comments:
        c["_id"] = str(c["_id"])
    return jsonify(comments), 200
