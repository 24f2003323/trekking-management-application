from flask import Flask
import os
from controllers.routes import application_routes
from sqlalchemy.orm import sessionmaker
from Database.models import create_db,Users
from sqlalchemy import create_engine
from datetime import date
engine = create_engine("sqlite:///Database/trekking.db")
Session = sessionmaker(bind=engine)
if not os.path.isfile("Database/trekking.db"):
    create_db()
    admin = Users(username = "aman_admin",email= "24f2003323@study.iitm.ac.in", password = "aman@9897",name="aman kumar", gender="m",dob=date(2006,3,27),type= "admin")
    s= Session()
    s.add(admin)
    s.commit()
    print("admin is added to db ")
app=Flask(__name__)
app.secret_key = "aman@9897"

application_routes(app)

if __name__ == "__main__":
    app.run(debug=True)



