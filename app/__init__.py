from flask import Flask

app = Flask(__name__)

from app import routes

app.run(host='0.0.0.0', port=5000, debug=True)
