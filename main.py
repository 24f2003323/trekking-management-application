import os
from sqlalchemy.orm import sessionmaker
from Database.models import create_db,Users
from sqlalchemy import create_engine
from datetime import date
engine = create_engine("sqlite:///instance/trekking.db")
Session = sessionmaker(bind=engine)
if not os.path.isfile("Database/trekking.db"):
    create_db()
    admin = Users(username = "aman_admin",email= "24f2003323@study.iitm.ac.in", password = "aman@9897",name="aman kumar", gender="m",dob=date(2006,3,27),type= "admin")
    s= Session()
    s.add(admin)
    s.commit()
    print("admin is added to db ")



