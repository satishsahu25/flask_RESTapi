from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:newdata@localhost:5432/alma'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'asdfghj456'

db = SQLAlchemy(app)


with app.app_context():
    db.create_all()

from posts.controller import *
from weather.controller import *


if __name__ == "__main__":
    app.run(debug=True)
