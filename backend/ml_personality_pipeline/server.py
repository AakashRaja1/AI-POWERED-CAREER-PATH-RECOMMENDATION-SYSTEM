from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, request

from config import DEFAULT_CONFIG
from inference import PersonalityPredictor


app = Flask(__name__)
predictor = PersonalityPredictor(model_path=DEFAULT_CONFIG.model_path)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/predict/personality", methods=["POST", "OPTIONS"])
def predict_personality():
    if request.method == "OPTIONS":
        return ("", 204)

    uploaded = request.files.get("file")
    if uploaded is None:
        return jsonify({"error": "Missing file upload."}), 400

    temp_dir = Path(DEFAULT_CONFIG.model_dir) / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / uploaded.filename
    uploaded.save(temp_path)

    try:
        prediction = predictor.predict_enriched(temp_path)
        return jsonify(prediction)
    finally:
        if temp_path.exists():
            temp_path.unlink()


if __name__ == "__main__":
    host = os.environ.get("PERSONALITY_HOST", "127.0.0.1")
    port = int(os.environ.get("PERSONALITY_PORT", "8765"))
    app.run(host=host, port=port, debug=False)