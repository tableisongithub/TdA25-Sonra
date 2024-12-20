import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():  # Základní HTML stránka
    return "<html><head><title>Test</title></head><body>Hello TdA</body></html>"

@app.route("/api")
def return_api():
    # Flask automaticky nastaví Content-Type na application/json při použití jsonify
    return jsonify({"organization": "Student Cyber Games"})

if __name__ == '__main__':
    app.run(debug=True)
