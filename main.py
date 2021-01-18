

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@192.168.1.100:5432/Raspberry Database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect = True)
User_settings = Base.classes.user_settings

@app.route('/')
def index():
    results = db.session.query(User_settings).all()
    for r in results:
        print(str(r.area_of_solarpanel)) 
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug = True)