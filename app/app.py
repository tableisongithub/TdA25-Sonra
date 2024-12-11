import os

from flask import Flask
from . import db

app = Flask(__name__)

# app.config.from_mapping(
#     DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
# )

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# db.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return "<html><head><title>Test</title></head><body>Hello TdA</body></html>"

@app.route("/api")
def return_api():
    return '{"organization": "Student Cyber Games"}'

if __name__ == '__main__':
    app.run(debug=True)
