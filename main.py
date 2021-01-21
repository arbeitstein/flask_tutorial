from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/SmartFlow'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect = True)
sf_user = Base.classes.sf_user

@app.route('/')
def base():
    return "Hello World 1"


@app.route('/get', methods=['GET'])
def index():
    if request.method == 'GET':
        results = db.session.query(sf_user).all()
        for r in results:
            print(str(r.firstname))
    return "Hello World 2 - GET"

if __name__ == "__main__":
    app.run(debug = True)