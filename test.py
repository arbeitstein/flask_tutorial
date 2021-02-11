from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine, Table, Integer, Column, String, Numeric, and_ , update, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only


app = Flask(__name__)
engine = create_engine('postgresql://postgres:Xxxx44Rd@localhost:5432/postgres')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Xxxx44Rd@localhost:5432/postgres' # Change IP of Database and Name!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData()
session = Session(engine)

sf_user = Table('sf_user',metadata, Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)
shelly = Table('shelly', metadata , Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)

Base = automap_base(metadata=metadata)
Base.prepare(engine, reflect=True)

sf_users = Base.classes.sf_user
shellies = Base.classes.shelly

@app.route('/')
def base():
    return "SmartFlow WebServer"

@app.route('/users', methods=['GET'])
def list_users():
    if request.method == 'GET':
        all_users = session.query(sf_user).all() 
        if not all_users:
            return "No Users have been registered yet"
        if all_users:
            return jsonify({"data": all_users})
        else:
            abort(404)

@app.route('/user/sign_in/<string:sent_email>/<string:sent_password>', methods=['GET'])
def sign_in_user(sent_email, sent_password):
    if request.method == 'GET':

        user = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).first()
        if user:
            return jsonify({"data": user})
        else:
            abort(404)

@app.route('/user/register/<string:sent_firstname>/<string:sent_lastname>/<string:sent_email>/<string:sent_password>/<float:sent_area>/<float:sent_light>',
             methods=['POST'])
def register_user(sent_firstname, sent_lastname, sent_email, sent_password, sent_area, sent_light):
    if request.method == 'POST':
        existing_user = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).first()
        if not existing_user:
            new_user = sf_users(firstname = sent_firstname, lastname = sent_lastname, email = sent_email, password = sent_password,
                                area_of_solar = sent_area, light_sensor = sent_light) 
            session.add(new_user)
            session.commit()
            return "User has been registered"
        elif existing_user:
            return "User with the same Email already existing"
        else:
            abort(404)

@app.route('/user/update/<int:user_id>/<string:sent_firstname>/<string:sent_lastname>/<string:sent_email>/<string:sent_password>/<float:sent_area>/<float:sent_light>', methods = ['POST'])
def update_user(user_id, sent_firstname, sent_lastname, sent_email, sent_password, sent_area, sent_light):
    if request.method == 'POST':
        change_user = session.query(sf_users).filter(sf_users.id == user_id).first()
        if change_user:
            change_user.firstname = sent_firstname
            change_user.lastname = sent_lastname
            change_user.email = sent_email
            change_user.password = sent_password
            change_user.area = sent_area
            change_user.light = sent_light
            session.add(change_user)
            session.commit()
            return "User has been updated"  
        else:
            abort(404)



@app.route('/shellies', methods = ['GET'])
def list_shellies():
    if request.method == 'GET':
        shelly_list = session.query(shelly).all()
        if not shelly_list:
            return "No Shellies registered yet"
        if shelly_list:
            return jsonify(shelly_list)
        else:
            abort(404)


@app.route('/shelly/add/<string:sent_name>/<string:sent_address>', methods = ['POST'])
def add_shelly(sent_name, sent_address):
    if request.method == 'POST':
        existing_shelly = session.query(shelly).filter(shellies.ip == sent_address).first()
        if not existing_shelly:
            new_shelly = shellies(name = sent_name, ip = sent_address)
            session.add(new_shelly)
            session.commit()
            return "Shelly has been added"
        else:
            return "Shelly with the same IP address already exists"

@app.route('/shelly/delete/<int:shelly_id>', methods = ['POST'])
def delete_shelly(shelly_id):
    if request.method == 'POST':
        deleting_shelly = session.query(shellies).filter(shellies.id == shelly_id).delete()
        session.commit()
        return "Shelly has been deleted"
    
@app.route('/shelly/update/<int:shelly_id>/<string:sent_name>/<string:sent_ip>', methods=['POST'])
def update_shelly(shelly_id, sent_name, sent_ip):
    if request.method == 'POST':
        updating_shelly = session.query(shellies).filter(shellies.id == shelly_id).first()
        if updating_shelly:
            updating_shelly.name = sent_name
            updating_shelly.ip = sent_ip
            session.add(updating_shelly)
            session.commit()
            return "Shelly has been updated"
        else:
            abort(404)

if __name__ == "__main__":
    app.run(debug = True)