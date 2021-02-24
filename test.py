from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine, Table, Integer, Column, String, Numeric, and_ , update, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
import json

app = Flask(__name__) # Name of Flask App Running
# engine = create_engine('postgresql://postgres:postgres@10.68.252.234:5432/Raspberry Database') # Raspberry Database
engine = create_engine('postgresql://postgres:Xxxx44Rd@localhost:5432/postgres') # At home Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disabling the Flask-SQLAlchemy Event System Tracking
app.config['JSON_SORT_KEYS'] = False # Turning off sorting when printing out JSON to WebSite

metadata = MetaData() # Object to read Datbase Tables when passed as argument ... see below
session = Session(engine) # Does the conversation between app and database

sf_user = Table('sf_user',metadata, Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine) # Loads Database Table with all it's columns
shelly = Table('shelly', metadata , Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)
city = Table('city', metadata , Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)


Base = automap_base(metadata=metadata)
Base.prepare(engine, reflect=True)


sf_users = Base.classes.sf_user # Generating Mapped Classes associated to the Tables in the Database
shellies = Base.classes.shelly
cities = Base.classes.city

@app.route('/') # Annotation to tell the Server that the Basic URL is having the following output
def base():
    return "SmartFlow WebServer"

@app.route('/users', methods=['GET']) # Adds another path to the URL to see all users with GET HTTP Method
def list_users():
    if request.method == 'GET': # Checking for the right HTTP Request Type
        all_users = session.query(sf_user).all() # Get all Users
        users_json = [] # Empty Dictionary, where all users will be stored in later on
        if not all_users: # Checking if there are any users
            return "No Users have been registered yet"
        elif all_users: # Checking if there are any users
            counter = 0
            while counter < len(all_users): # Adding all users to the above dict in appropriate JSON Format
                users_json.append({
                    "id": all_users[counter][0],
                    "firstname": all_users[counter][1],
                    "lastname": all_users[counter][2],
                    "email": all_users[counter][3],
                    "password": all_users[counter][4],
                    "area_of_solar": all_users[counter][5],
                    "light_sensor": all_users[counter][6],
                    "raspberry_ip": all_users[counter][7]
                })
                counter += 1
            return jsonify({"data": users_json})
        else: # If none of the above cases is valid give 404 Error
            abort(404)

@app.route('/user/sign_in/<string:sent_email>/<string:sent_password>', methods=['GET']) # Sign in Route with Parameters in <> Signs
def sign_in_user(sent_email, sent_password):
    if request.method == 'GET':
        user = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).all()
        signedInUser_json = []
        print(user)
        if user:
            counter = 0
            while counter < len(user): # Adding all users to the above dict in appropriate JSON Format
                signedInUser_json.append({
                    "id": user[counter][0],
                    "firstname": user[counter][1],
                    "lastname": user[counter][2],
                    "email": user[counter][3],
                    "password": user[counter][4],
                    "area_of_solar": user[counter][5],
                    "light_sensor": user[counter][6],
                    "raspberry_ip": all_users[counter][7]
                })
                counter += 1
            return jsonify({"data": signedInUser_json})
        else:
            abort(404)

@app.route('/user/register/<string:sent_firstname>/<string:sent_lastname>/<string:sent_email>/<string:sent_password>/<float:sent_area>/<float:sent_light>/<string:sent_raspberry_ip>',
             methods=['POST'])
def register_user(sent_firstname, sent_lastname, sent_email, sent_password, sent_area, sent_light, sent_raspberry_ip):
    if request.method == 'POST':
        existing_user = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).first()
        if not existing_user:
            new_user = sf_users(firstname = sent_firstname, lastname = sent_lastname, email = sent_email, password = sent_password,
                                area_of_solar = sent_area, light_sensor = sent_light, raspberry_ip = sent_raspberry_ip) 
            session.add(new_user)
            session.commit()
            return "User has been registered"
        elif existing_user:
            return "User with the same Email already existing"
        else:
            abort(404)

@app.route('/user/update/<int:user_id>/<string:sent_firstname>/<string:sent_lastname>/<string:sent_email>/<string:sent_password>/<float:sent_area>/<float:sent_light>/<string:sent_raspberry_ip>',
             methods = ['POST'])
def update_user(user_id, sent_firstname, sent_lastname, sent_email, sent_password, sent_area, sent_light, sent_raspberry_ip):
    if request.method == 'POST':
        change_user = session.query(sf_users).filter(sf_users.id == user_id).update({sf_users.firstname: sent_firstname,
        sf_users.lastname: sent_lastname, sf_users.email: sent_email, sf_users.password: sent_password, sf_users.sent_area: sent_area,
        sf_users.sent_light: sent_light, sf_users.raspberry_ip: sent_raspberry_ip})
        session.commit()
        return "User has been updated"
    else:
        abort(404)



@app.route('/shellies', methods = ['GET'])
def list_shellies():
    if request.method == 'GET':
        shelly_json = []
        shelly_list = session.query(shelly).all()
        if not shelly_list:
            return "No Shellies registered yet"
        if shelly_list:
            counter = 0
            while counter < len(shelly_list):
                shelly_json.append({
                    "id": shelly_list[counter][0],
                    "name": shelly_list[counter][1],
                    "ip": shelly_list[counter][2]
                })
                counter += 1
            return jsonify({"shellies":shelly_json})
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
        updating_shelly = session.query(shellies).filter(shellies.id == shelly_id).update({shellies.name: sent_name, shellies.ip: sent_ip})
        session.commit()
        return "Shelly has been updated"
    else:
        abort(404)



@app.route('/cities', methods = ['GET'])
def cities_list():
    if request.method == 'GET':
        cities_json = []
        all_cities = session.query(city).all()
        if not all_cities:
            return "No cities have been added yet"
        if all_cities:
            counter = 0
            while counter < len(all_cities):
                cities_json.append({
                    "id": all_cities[counter][0],
                    "name": all_cities[counter][1],
                    "user_id": all_cities[counter][2]
                })
                counter += 1
            return jsonify({"cities":cities_json})

@app.route('/city/add/<string:sent_name>/<int:sent_user_id>', methods = ['POST'])
def add_city(sent_name, sent_user_id):
    if request.method == 'POST':
        adding_city = cities(name = sent_name, user_id = sent_user_id)
        if adding_city:
            session.add(adding_city)
            session.commit()
            return "City with user has been added"
        else:
            abort(404)

@app.route('/city/update/<int:city_id>/<string:sent_name>/<string:sent_user_id>', methods=['POST'])
def update_city(city_id, sent_name, sent_user_id):
    if request.method == 'POST':
        updating_city = session.query(cities).filter(cities.id == city_id).update({cities.name: sent_name, cities.user_id: sent_user_id})
        session.commit()
        return "User has been updated"
    else:
        abort(404)


if __name__ == "__main__":
    app.run(debug = True)
    # app.run(host='10.68.252.234', port=5000) # Runs the BASE URL on the Raspberry PI with the following address
