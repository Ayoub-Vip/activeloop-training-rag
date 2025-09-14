from flask import Blueprint, render_template, jsonify, request
from services import llama_service

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def home():
    return "Hello World!"

@api_bp.route("/ping")
def ping():
    return jsonify({"status": "ok"})

@api_bp.route("/echo", methods=["POST"])
def echo():
    data = request.json
    return jsonify({"you_sent": data})

@api_bp.route("/upload_doc", methods=["POST"])
def handle_doc():
    
    #something
    return llama_service.parse_doc()