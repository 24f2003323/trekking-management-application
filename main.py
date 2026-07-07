from flask import Flask
import os
from controllers.routes import application_routes
from controllers.api import api_routes
from sqlalchemy.orm import sessionmaker
from Database.models import create_db,Users
from sqlalchemy import create_engine
from datetime import date
from flask_login import LoginManager
from flask_restful import Api

engine = create_engine("sqlite:///Database/trekking.db")
Session = sessionmaker(bind=engine)
if not os.path.isfile("Database/trekking.db"):
    create_db()
    admin = Users(username = "aman_admin",email= "24f2003323@study.iitm.ac.in", password = "aman@9897",name="aman kumar", gender="m",dob=date(2006,3,27),type= "admin",age = 20)
    s= Session()
    s.add(admin)
    s.commit()
    s.close()
    print("admin is added to db ")
app=Flask(__name__)
app.secret_key = "aman@9897"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ="login_page"
api = Api(app)

application_routes(app, login_manager)
api_routes(api)

if __name__ == "__main__":
    app.run(debug=True)



