from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine, Table, Integer, Column, String, Numeric, and_ , update, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only


app = Flask(__name__)
engine = create_engine('postgresql://postgres:Xxxx44Rd@localhost:5432/sf')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Xxxx44Rd@localhost:5432/sf' # Change IP of Database and Name!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData()
session = Session(engine)

sf_user = Table('sf_user',metadata, Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)

Base = automap_base(metadata=metadata)
Base.prepare(engine, reflect=True)

sf_users = Base.classes.sf_user

@app.route('/')
def base():
    return "SmartFlow WebServer"

@app.route('/users', methods=['GET'])
def user_list():
    if request.method == 'GET':
        all_users = session.query(sf_user).all() 
        if all_users:
            return jsonify({"data": all_users})
        else:
            abort(404)

@app.route('/user/sign_in/<string:sent_email>/<string:sent_password>', methods=['GET'])
def user_sign_in(sent_email, sent_password):
    if request.method == 'GET':
        # sent_email = request.args['email']
        # sent_password = request.args['password']
        user = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).first()
        if user:
            return jsonify({"data": user})
        else:
            abort(404)

@app.route('/user/register/<string:sent_firstname>/<string:sent_lastname>/<string:sent_email>/<string:sent_password>/<float:sent_area>/<float:sent_light>',
             methods=['POST'])
def user_register(sent_firstname, sent_lastname, sent_email, sent_password, sent_area, sent_light):
    if request.method == 'POST':
        existing_records = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).first()
        if not existing_records:
            new_user = sf_users(firstname = sent_firstname, lastname = sent_lastname, email = sent_email, password = sent_password,
                                area_of_solar = sent_area, light_sensor = sent_light) 
            session.add(new_user)
            session.commit()
            return "User has been registered"
        else:
            abort(404)

@app.route('/user/update/<int:user_id>/<string:sent_firstname>/<string:sent_lastname>/<string:sent_email>/<string:sent_password>/<float:sent_area>/<float:sent_light>', methods = ['POST'])
def update_user(user_id, sent_firstname, sent_lastname, sent_email, sent_password, sent_area, sent_light):
    if request.method == 'POST':
        change_user = session.query(sf_users).filter(sf_users.id == user_id).first()
        if change_user:
            change_user.firstname = sent_firstname
            session.commit()
            change_user.lastname = sent_lastname
            session.commit()
            change_user.email = sent_email
            session.commit()
            change_user.password = sent_password
            session.commit()
            change_user.area = sent_area
            session.commit()
            change_user.light = sent_light
            session.commit()
            return "User has been updated"  
        else:
            abort(404)


if __name__ == "__main__":
    app.run(debug = True)