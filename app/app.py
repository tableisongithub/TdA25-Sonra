mport os
from flask import Flask
# from . import db
from flask import Flask, jsonify

app = Flask(__name__)

# app.config.from_mapping(
#     DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
# )
# ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass
# db.init_app(app)
@app.route('/')
def hello_world():  # put application's code here
def hello_world():  # Základní HTML stránka
    return "<html><head><title>Test</title></head><body>Hello TdA</body></html>"

@app.route("/api")
def return_api():
    return '{"organization": "Student Cyber Games"}'
    # Flask automaticky nastaví Content-Type na application/json při použití jsonify
    return jsonify({"organization": "Student Cyber Games"})

if __name__ == '__main__':
    app.run(debug=True)
