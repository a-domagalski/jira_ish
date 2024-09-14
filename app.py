from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')  # Load config from config.py

db = SQLAlchemy(app)

# Import routes after initializing app and db
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
