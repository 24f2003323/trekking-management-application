from flask import render_template,request,session,redirect
from sqlalchemy.orm import sessionmaker
from Database.models import Users,deleted_items
from sqlalchemy import create_engine
from datetime import datetime
engine = create_engine("sqlite:///Database/trekking.db")
Session = sessionmaker(bind=engine)
def application_routes(app):
    @app.route("/",methods = ["POST","GET"])
    def homepage():
        return render_template("Home.html")
    @app.route("/logout",methods=["GET"])
    def logout():
        session.clear()
        return redirect("/")
    @app.route("/login",methods = ["POST","GET"])
    def login_page():
        if request.method =="GET":
            return render_template("login.html",valid_username_or_password =True)
        elif request.method =="POST":
            username = request.form["username"]
            password = request.form["password"]
            s= Session()
            
            u = s.query(Users).filter(Users.username ==username).first()
            if u  is None: 
                return render_template("login.html",valid_username = False)
            else :
                if u.password !=password:
                    return render_template("login.html", valid_username_or_password = False)
                else :
                    if u.type =="admin":
                        session["admin_login"]= True
                        return redirect("/admin_dashboard")
                    elif u.type == "user":
                        session["user_login"]= True
                        return render_template("user_dashboard.html")
                    elif u.type == "staff":
                        session["user_login"]= True
                        return render_template("staff.dashboard.html")
    @app.route('/user_list',methods=["POST","GET"])
    @app.route('/staff_list',methods=["POST","GET"])
    @app.route('/admin_dashboard',methods = ["POST","GET"])
    def admin_dashboard():
        s = Session()
        d= s.query(deleted_items).filter(deleted_items.from_table=="users").all()
        u = s.query(Users).all()
        if request.path =="/admin_dashboard":
            if request.method  == "GET":
                if "admin_login" in session:
                    return render_template("admin_dashboard.html", request = "ok" )    
                else :
                    return redirect("/login")
            
        elif request.path =="/staff_list":
            if request.method  == "GET":
                if "admin_login" in session:
                    return render_template("admin_dashboard.html", request ="staff_list" ,users = u,deleted_user = d)    
                else :
                    return redirect("/login")
            elif request.method=="POST":
                if "admin_login" in session:
                    user_id = request.form.get("user_id")
                    status = request.form.get("status")
                    u = s.query(Users).filter(Users.id ==user_id).first()
                    if status=="approved":
                        u.type = "staff"
                    elif status =="rejected":
                        u.type="rejected"
                    elif status =="delete":
                        u.type ="removed"
                    s.commit()
                    return redirect('/staff_list')
                else :
                    return redirect('/login')
        elif request.path =="/user_list":
            if request.method  == "GET":
                if "admin_login" in session:
                    return render_template("admin_dashboard.html", request ="user_list" ,users = u,deleted_user = d )    
                else :
                    return redirect("/login")
        
    @app.route('/add_staff',methods = ["POST","GET"])
    def add_staff():
        if "admin_login" in session:
            if request.method == "GET":
                return render_template("add_staff.html",added = False,exists_uname = False,used_mail = False)
            elif request.method =="POST":
                name = request.form['name']
                email  = request.form['email']
                u_name = request.form['username']
                password  = request.form['password']
                gender = request.form['gender']
                age  = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
                type= "staff"
                Session = sessionmaker(bind=engine)
                s = Session()
                u = s.query(Users).filter((Users.username==u_name) | (Users.email==email)).first()
                if u is None :
                    user  = Users(name = name,username= u_name, password= password, email = email, gender = gender, dob = age , type= type)
                    s.add(user)
                    s.commit()
                    return render_template('add_staff.html',staff_name = name,added = True,exists_uname = False,used_mail = False)
                elif u.username == u_name:
                    return render_template("add_staff.html",added = False,exists_uname = True,used_mail = False)
                elif u.email== email :
                    return render_template("add_staff.html",added = False,exists_uname = False, used_mail = True)
            

    @app.route('/user_dashboard',methods = ["POST","GET"])
    def user_dashboard():
        if "user_login" in session:
            return render_template("user_dashboard.html")    
        else :
            return redirect("/login")


    @app.route('/staff_dashboard',methods = ["POST","GET"])
    def staff_dashboard():
        if "staff_login" in session:
            return render_template("staff_dashboard.html")    
        else :
            return redirect("/login")
    @app.route('/staff_apply',methods = ["GET","POST"])
    @app.route('/signup', methods = ["GET","POST"])
    def signup():
        if request.path =="/signup":
            if request.method=="GET":
                return render_template("signup.html",signup_done = False,exists_uname = False,used_mail = False,type = "signup")
            elif request.method == "POST":
                name = request.form['name']
                email  = request.form['email']
                u_name = request.form['username']
                password  = request.form['password']
                gender = request.form['gender']
                age  = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
                type= "user"
                Session = sessionmaker(bind=engine)
                s = Session()
                u = s.query(Users).filter((Users.username==u_name) | (Users.email==email)).first()
                if u is None :
                    user  = Users(name = name,username= u_name, password= password, email = email, gender = gender, dob = age , type= type)
                    s.add(user)
                    s.commit()
                    return render_template("signup.html",signup_done = True,exists_uname = False,used_mail = False)
                elif u.username == u_name:
                    return render_template("signup.html",exists_uname = True,used_mail = False)
                elif u.email== email :
                    return render_template("signup.html",exists_uname = False, used_mail = True)
        elif request.path =="/staff_apply" :
            if request.method=="GET":
                return render_template("signup.html",signup_done = False,exists_uname = False,used_mail = False,type = "staff_request")
            elif request.method == "POST":
                name = request.form['name']
                email  = request.form['email']
                u_name = request.form['username']
                password  = request.form['password']
                gender = request.form['gender']
                age  = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
                type= "staff_request"
                Session = sessionmaker(bind=engine)
                s = Session()
                u = s.query(Users).filter((Users.username==u_name) | (Users.email==email)).first()
                if u is None :
                    user  = Users(name = name,username= u_name, password= password, email = email, gender = gender, dob = age , type= type)
                    s.add(user)
                    s.commit()
                    return render_template("signup.html",signup_done = True,exists_uname = False,used_mail = False)
                elif u.username == u_name:
                    return render_template("signup.html",exists_uname = True,used_mail = False)
                elif u.email== email :
                    return render_template("signup.html",exists_uname = False, used_mail = True)
