from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@192.168.1.100:5432/Raspberry Database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    return "Hello, this is the Standard Website, you get prompted to when opening the link in the console."

@app.route('/user', methods=['GET'])
def index_get():
    if request.method == 'GET':
        results = db.session.query(sf_user).all()
        data = users_schema.dump(results)
    return jsonify(data)

@app.route('/post/<first>', methods=['POST'])
def index_post(first):
    if request.method == 'POST':
        new_setting = user_settings(solarpanel=first)
        db.session.add(new_setting)
        db.session.commit()
    return 'posted'

if __name__ == "__main__":
    app.run(debug = True)