from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask_marshmallow import Marshmallow
from collections import OrderedDict

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@192.168.1.100:5432/Raspberry Database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

ma = Marshmallow(app)
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect = True)
sf_user = Base.classes.sf_user
user_settings = Base.classes.user_settings

class UserSchema(ma.Schema): # Make sf_user JSON Serializable
    class Meta:
        # Fields to expose
        fields = ("id", "firstname", "email", "password", "settings_id", "shelly_id", "weather_id", "measurement_id")
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/')
def base():
    return "base"

@app.route('/settings', methods=['GET'])
def index_get():
    if request.method == 'GET':
        results = db.session.query(sf_user).all()
        data = users_schema.dump(results)
        for r in data:
            dict_users = {
                "data": {
                    "r":{
                    "id": r['id'],
                    "firstname": r['firstname'],
                    "email": r['email'],
                    "password": r['password'],
                    "settings_id": r['settings_id'],
                    "shelly_id": r['shelly_id'],
                    "weather_id": r['weather_id'],
                    "measurement_id": r['measurement_id']
                    }
                }
            }
            print(dict_users)
    return jsonify(dict_users)

@app.route('/settings/<first>', methods=['POST'])
def index_post(first):
    if request.method == 'POST':
        new_setting = user_settings(solarpanel=first)
        db.session.add(new_setting)
        db.session.commit()
    return 'posted'

if __name__ == "__main__":
    app.run(debug = True)