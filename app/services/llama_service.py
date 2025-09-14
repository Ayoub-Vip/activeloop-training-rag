import os

from ...vector_stores import *
from ...agents import *
from flask import request, jsonify

from ...config import DATA_DIR

VectorStore = None
Index = None
QueryEngine = None

def ingest_data():
    pass

def build_vector_store():
    global VectorStore
    pass

def initialize_index():
    global Index
    pass

def initialize_query_engine():
    global QueryEngine
    pass

def parse_doc():
    """
    Upload a single file or multiple files.
    """
    if "files" not in request.files:
        return jsonify({"error": "No files part in request"}), 400

    files = request.files.getlist("files")  # works for single or multiple

    saved_files = []
    for file in files:
        if file.filename == "":
            continue  # skip empty filenames

        file_path = os.path.join(DATA_DIR, file.filename)
        file.save(file_path)
        saved_files.append(file.filename)

    if not saved_files:
        return jsonify({"error": "No valid files uploaded"}), 400

    return jsonify({"uploaded_files": saved_files}), 201