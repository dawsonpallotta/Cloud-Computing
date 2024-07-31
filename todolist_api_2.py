from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set the database file path
db_path = os.path.join(os.path.dirname(__file__), "instance/todolist.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_to_do = db.Column(db.String(120))
    due_date = db.Column(db.String(10))
    status = db.Column(db.String(10))


@app.route("/api/items", methods=["GET"])
def get_items():
    entries = Entry.query.all()
    result = [
        {"what_to_do": entry.what_to_do, "due_date": entry.due_date, "status": entry.status}
        for entry in entries
    ]
    return jsonify(result)


@app.route("/api/items", methods=["POST"])
def add_item():
    if not request.json or "what_to_do" not in request.json or "due_date" not in request.json:
        abort(400)
    new_entry = Entry(what_to_do=request.json["what_to_do"], due_date=request.json["due_date"], status="open")
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"result": "success"}), 201


@app.route("/api/items/<item>", methods=["PUT"])
def mark_as_done(item):
    entry = Entry.query.filter_by(what_to_do=item).first()
    if entry is None:
        entry = Entry.query.filter_by(what_to_do=item.lower()).first()
    if entry is None:
        entry = Entry.query.filter_by(what_to_do=item.capitalize()).first()
    if entry is not None:
        entry.status = "done"
        db.session.commit()
        return jsonify({"status": "done"})
    return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<item>", methods=["DELETE"])
def delete_entry(item):
    entry = Entry.query.filter_by(what_to_do=item).first()
    if entry is None:
        entry = Entry.query.filter_by(what_to_do=item.lower()).first()
    if entry is None:
        entry = Entry.query.filter_by(what_to_do=item.capitalize()).first()
    if entry is not None:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run("0.0.0.0", port=5001)

# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
# db = SQLAlchemy(app)


# class Entry(db.Model):
#     what_to_do = db.Column(db.String(80), primary_key=True)
#     due_date = db.Column(db.String(10))
#     status = db.Column(db.String(10))

#     def to_dict(self):
#         return {"what_to_do": self.what_to_do, "due_date": self.due_date, "status": self.status}


# @app.route("/api/items", methods=["GET"])
# def get_items():
#     entries = Entry.query.all()
#     tdlist = [entry.to_dict() for entry in entries]
#     return jsonify(tdlist)


# @app.route("/api/items", methods=["POST"])
# def add_item():
#     item = request.get_json()
#     try:
#         entry = Entry(**item)
#         db.session.add(entry)
#         db.session.commit()
#         return jsonify({"success": True}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


# @app.route("/api/items/<item>", methods=["DELETE"])
# def delete_item(item):
#     entry = Entry.query.get(item)
#     if entry:
#         db.session.delete(entry)
#         db.session.commit()
#         return jsonify({"success": True}), 204
#     return jsonify({"error": "Item not found"}), 404


# @app.route("/api/items/<item>", methods=["PUT"])
# def mark_as_done(item):
#     entry = Entry.query.get(item)
#     if entry:
#         entry.status = "done"
#         db.session.commit()
#         return jsonify({"success": True}), 204
#     return jsonify({"error": "Item not found"}), 404


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run("0.0.0.0", port=5001)

