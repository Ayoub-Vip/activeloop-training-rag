from flask import Blueprint, render_template, jsonify, request

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/ping")
def ping():
    return jsonify({"status": "ok"})

@main_bp.route("/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"you_sent": data})
