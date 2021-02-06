from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine, Table, Integer, Column, String, Numeric, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only


app = Flask(__name__)
engine = create_engine('postgresql://postgres:Xxxx44Rd@localhost:5432/postgres')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Xxxx44Rd@localhost:5432/postgres' # Change IP of Database and Name!!!
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

@app.route('/user/sign_in', methods=['GET'])
def user_sign_in():
    if request.method == 'GET':
        sent_email = request.args['email']
        sent_password = request.args['password']
        res = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).first()
        print(res)
        if res:
            return jsonify({"data": res})
        else:
            abort(404)

@app.route('/user/register', methods=['POST'])
def user_register():
    if request.method == 'POST':
        sent_firstname = request.args['firstname']
        sent_lastname = request.args['lastname']
        sent_email = request.args['email']
        sent_password = request.args['password']
        sent_area = request.args['area']
        sent_light = request.args['light']
        
        existing_records = session.query(sf_user).filter(and_(sf_users.email.like(sent_email), sf_users.password.like(sent_password))).first()
        if not existing_records:
            new_user = sf_users(firstname = sent_firstname, lastname = sent_lastname, email = sent_email, password = sent_password,
                                area_of_solar = sent_area, light_sensor = sent_light) 
            session.add(new_user)
            session.commit()
            return "User has been registered"
        else:
            abort(404)
        
if __name__ == "__main__":
    app.run(debug = True)