from flask import render_template,request,session,redirect
from sqlalchemy.orm import sessionmaker
from Database.models import *
from sqlalchemy import create_engine
from datetime import datetime
engine = create_engine("sqlite:///Database/trekking.db")
Session = sessionmaker(bind=engine)
def application_routes(app):
    @app.route("/",methods = ["GET"])
    def homepage():
        return render_template("home.html")
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
                s.close()
                return render_template("login.html",valid_username = False)
            else :
                if u.password !=password:
                    s.close()
                    return render_template("login.html", valid_username_or_password = False)
                else :
                    if u.type =="admin":
                        s.close()
                        session["admin_login"]= True
                        return redirect("/admin_dashboard")
                    elif u.type == "user":
                        s.close()
                        session["user_login"]= True
                        return redirect("/user_dashboard")
                    elif u.type == "staff":
                        s.close()
                        session["staff_login"]= True
                        return redirect("/staff_dashboard")
    
    @app.route('/staff_apply',methods = ["GET","POST"])
    @app.route('/signup', methods = ["GET","POST"])
    def signup_or_staff_apply():
        if request.method=="GET":
            if request.path =="/signup":
                type = "user"
            else:
                type = "staff_request"
            return render_template("signup.html",signup_done = False,exists_uname = False,used_mail = False,type = type)
        elif request.method == "POST":
            name = request.form['name']
            email  = request.form['email']
            u_name = request.form['username']
            password  = request.form['password']
            gender = request.form['gender']
            age  = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
            Session = sessionmaker(bind=engine)
            s = Session()
            u = s.query(Users).filter((Users.username==u_name) | (Users.email==email)).first()
            if u is None :
                if request.path =="/signup":
                    type = "user"
                else:
                    type = "staff_request"
                user  = Users(name = name,username= u_name, password= password, email = email, gender = gender, dob = age , type= type)
                s.add(user)
                s.commit()
                s.close()
                return render_template("signup.html",exists_uname = False,used_mail = False,type = "detailed_filled")
            elif u.username == u_name:
                s.close()
                return render_template("signup.html",exists_uname = True,used_mail = False)
            elif u.email== email :
                s.close()
                return render_template("signup.html",exists_uname = False, used_mail = True)
            
    
    @app.route('/admin_dashboard',methods = ["POST","GET"])
    def admin_dashboard():
        if "admin_login" in session:
            s = Session()
            active_staff = s.query(Users).filter(Users.type=="staff").count() 
            deactivated_staff = s.query(Users).filter(Users.type=="deactivated_staff").count() 
            pending_staff = s.query(Users).filter(Users.type=="staff_request").count() 
            active_user= s.query(Users).filter(Users.type =="user").count() 
            deactivated_users = s.query(Users).filter(Users.type =="deactivated_user").count()
            upcoming_trek = s.query(Trek).filter(Trek.trek_status =="upcoming").count()
            completed_trek = s.query(Trek).filter(Trek.trek_status=="completed").count()
            ongoing_trek = s.query(Trek).filter(Trek.trek_status =="ongoing").count()
            deleted_trek = s.query(Trek).filter(Trek.trek_status=="deleted").count()
            payment_pending = s.query(User_terk).filter(User_terk.payment_status=="pending").count()
            payment_done = s.query(User_terk).filter(User_terk.payment_status=="done").count()
            if request.method  == "GET":              
                s.close()
                return render_template("admin_dashboard.html", 
                                       request = "ok" ,active_staff=active_staff,
                                       deactivated_staff=deactivated_staff,
                                       pending_staff=pending_staff,active_user=active_user,
                                       deactivated_user=deactivated_users,upcoming_trek=upcoming_trek,
                                       completed_trek=completed_trek,ongoing_trek=ongoing_trek,
                                       deleted_trek=deleted_trek,payment_done=payment_done,
                                       payment_pending=payment_pending)   
            
        else :
            return redirect("/login")
    @app.route('/admin_dashboard/user_list',methods=["POST","GET"])
    def admin_user_list():
        if "admin_login" in session:
            s=Session()
            u = s.query(Users).filter((Users.type == "user") | (Users.type=="deactivated_user")).all()
            print(u)
            if request.method=="GET":
                s.close()
                return render_template("admin_manage_user.html",users = u)
            if request.method=="POST":
                query = s.query(Users).filter((Users.type == "user") | (Users.type == "deactivated_user"))
                search = request.form.get("search")
                user_type = request.form.get("type")
                if search:
                    query = query.filter((Users.username.ilike(f"%{search}%")) & ((Users.type =="user" )|(Users.type =="deactivated_user") ))
                if user_type not in ("None", "All"):
                    query = query.filter(Users.type == user_type)
                
                users = query.all()
                s.close()
                return render_template("admin_manage_user.html", users=users) 
        else :
            return redirect("/login")
    @app.route('/admin_dashboard/user_access',methods = ["GET"])
    def admin_user_access():
        if "admin_login" in session:
            if request.method=="GET":
                action = request.args.get("view_user_id")
                deactivate_user_id = request.args.get("deactivate_user_id")
                activate_user_id = request.args.get("activate_user_id")
                s=Session()
                if action :
                    user_info = s.query(Users).filter(Users.id ==action).first()
                    s.close()
                    return render_template("admin_user_access.html",user=user_info)
                elif deactivate_user_id:
                    user = s.query(Users).filter(Users.id ==deactivate_user_id).first()
                    user.type = "deactivated_user"
                    s.commit()
                    s.close()
                    return redirect("/admin_dashboard/user_list")
                elif activate_user_id:
                    user = s.query(Users).filter(Users.id ==activate_user_id).first()
                    user.type = "user"
                    s.commit()
                    s.close()
                    return redirect("/admin_dashboard/user_list")

        else:
            return redirect('/login')

    @app.route('/admin_dashboard/add_staff',methods = ["POST","GET"])
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
                    s.close()
                    return render_template('add_staff.html',staff_name = name,added = True,exists_uname = False,used_mail = False)
                elif u.username == u_name:
                    s.close()
                    return render_template("add_staff.html",added = False,exists_uname = True,used_mail = False)
                elif u.email== email :
                    s.close()
                    return render_template("add_staff.html",added = False,exists_uname = False, used_mail = True)
    
    @app.route('/admin_dashboard/staff_list',methods=["POST","GET"])
    def admin_staff_list():
        if "admin_login" not in session:
            return redirect("/login")
        s=Session()
        if request.method=="GET":
            staffs=s.query(Users).filter((Users.type=="staff")|(Users.type=="deactivated_staff")|(Users.type=="staff_request")|(Users.type=="rejected")|(Users.type=="removed_staff")).all()
            s.close()
            return render_template("staff_list.html",staffs=staffs)
        elif request.method=="POST":
            status=request.form.get("status")
            user_id=request.form.get("user_id")
            if status:
                u=s.query(Users).filter(Users.id==user_id).first()
                if status=="approved":
                    u.type="staff"
                elif status=="rejected":
                    u.type="rejected"
                elif status=="deactivated":
                    u.type="deactivated_staff"
                elif status=="removed":
                    u.type="removed_staff"
                s.commit()
                s.close()
                return redirect("/admin_dashboard/staff_list")
            query=s.query(Users).filter((Users.type=="staff")|(Users.type=="deactivated_staff")|(Users.type=="staff_request")|(Users.type=="rejected")|(Users.type=="removed_staff"))
            search=request.form.get("search")
            staff_type=request.form.get("type")
            if search:
                query=query.filter(Users.username.ilike(f"%{search}%"))
            if staff_type not in ("None","All"):
                query=query.filter(Users.type==staff_type)
            staffs=query.all()
            s.close()
            return render_template("staff_list.html",staffs=staffs)
    @app.route('/admin_dashboard/add_trek',methods = ["POST","GET"])
    def admin_add_trek():
        if not  "admin_login" in session:
            return redirect("/login")
        if request.method=="GET":
            s= Session()
            staff = s.query(Users).filter(Users.type =="staff").all()
            return render_template("add_trek.html",added = False,staff=staff)
        elif request.method =="POST":
            name = request.form.get("name")
            age =request.form.get("age")
            slots = request.form.get("slots")
            difficulty =request.form.get("difficulty")
            start_date = datetime.strptime(request.form['start_date'],"%Y-%m-%d").date()
            end_date = datetime.strptime(request.form['end_date'],"%Y-%m-%d").date()
            start_location = request.form.get("starting_location")
            end_location = request.form.get("ending_location")
            staff_id = request.form.get("staff")
            t = Trek(name = name,for_age_group = age , no_of_slots = slots, difficulty= difficulty, trek_status = "upcoming", start_date= start_date, end_date= end_date, starting_location = start_location, ending_location = end_location,no_of_registration=0)
            s_t = Staff_trek(trek_id = t.id , staff_id = staff_id)
            s= Session()
            s.add(t)
            s.commit()
            trek = s.query(Trek).filter(Trek.name ==name).first()
            s_t = Staff_trek(trek_id = trek.id , staff_id = staff_id)
            s.add(s_t)
            s.commit()
            s.close()
            return render_template("add_trek.html", added = True,trek_name = name,start_location = start_location,end_location = end_location )
    @app.route('/admin_dashboard/manage_trek',methods=["POST","GET"])
    def admin_manage_trek():
        if "admin_login" not in session:
            return redirect("/login")
        s= Session()
        t = s.query(Trek).all()
        if request.method=="GET":
            return render_template("trek_list.html",treks = t)
        elif request.method =="POST":
            query = s.query(Trek)
            search = request.form.get("search")
            trek_type = request.form.get("type")
            difficulty = request.form.get("difficulty")
            print(difficulty)
            if search:
                query = query.filter(Trek.name.ilike(f"%{search}%"))
            if trek_type not in ("None", "All"):
                query = query.filter(Trek.trek_status == trek_type)
            if difficulty not in ("None", "All"):
                query = query.filter(Trek.difficulty == difficulty)
            treks = query.all()
            s.close()
            return render_template("trek_list.html", treks=treks)       
    @app.route('/admin_dashboard/edit_trek',methods =["POST","GET"])
    def admin_edit_trek():
        if "admin_login" not in session:
            return redirect("/login")
        if request.method =="GET":
            trek_id = request.args.get("trek_id")
            s= Session()
            trek = s.query(Trek).filter(Trek.id ==trek_id).first()
            staff_id = s.query(Staff_trek).filter(Staff_trek.trek_id==trek_id).first()
            staff = s.query(Users).filter(Users.type=="staff").all()
            s.close()
            return render_template("edit_trek.html",trek = trek ,edited = False, staff_id = staff_id.staff_id,staff= staff,trek_id = trek_id)
        if request.method == "POST":
            trek_id = request.form.get("trek_id")
            s = Session()       
            trek = s.query(Trek).filter(Trek.id == trek_id).first()
            trek.name = request.form.get("name")
            trek.for_age_group = request.form.get("age")
            trek.no_of_slots = request.form.get("slots")
            trek.difficulty = request.form.get("difficulty")
            trek.start_date = datetime.strptime(
                request.form.get("start_date"),
                "%Y-%m-%d"
            ).date()
            trek.end_date = datetime.strptime(
                request.form.get("end_date"),
                "%Y-%m-%d"
            ).date()
            trek.starting_location = request.form.get("starting_location")
            trek.ending_location = request.form.get("ending_location")
            new_staff_id = request.form.get("staff")
            staff_trek = s.query(Staff_trek).filter(
                Staff_trek.trek_id == trek_id
            ).first()
            if staff_trek:
                staff_trek.staff_id = new_staff_id
            s.commit()
            
            s.close()
            return render_template(
                "edit_trek.html",
                trek=trek,
                edited=True,
                
            )

    @app.route("/admin_dashboard/delete_trek", methods = ["POST","GET"])
    def admin_delete_trek():
        if "admin_login" in session:
            if request.method =="POST":
                trek_id = request.form.get("trek_id")
                s= Session()
                trek = s.query(Trek).filter(Trek.id == trek_id).first()
                trek.trek_status= "deleted"
                s.commit()
                s.close()
                return redirect('/admin_dashboard/manage_trek')
        else :
            return redirect("/login")   
    @app.route('/admin_dashboard/booking_history',methods=["POST","GET"])
    def admin_booking_history():
        if "admin_login" not in session:
            return redirect("/login")
        s=Session()
        if request.method=="GET":
            bookings=[]
            records=s.query(User_terk).all()
            for i in records:
                user=s.query(Users).filter(Users.id==i.user_id).first()
                trek=s.query(Trek).filter(Trek.id==i.trek_id).first()
                bookings.append({
                    "registration_id":i.registartion_id,
                    "username":user.username,
                    "trek_name":trek.name,
                    "payment_status":i.payment_status,
                    "completion":i.completion
                })
            s.close()
            return render_template("admin_booking_history.html",bookings=bookings)
        elif request.method=="POST":
            query=s.query(User_terk)
            search=request.form.get("search")
            payment_status=request.form.get("payment_status")
            if search:
                query=query.join(Users,Users.id==User_terk.user_id).filter(Users.username.ilike(f"%{search}%"))
            if payment_status not in ("None","All"):
                query=query.filter(User_terk.payment_status==payment_status)
            records=query.all()
            bookings=[]
            for i in records:
                user=s.query(Users).filter(Users.id==i.user_id).first()
                trek=s.query(Trek).filter(Trek.id==i.trek_id).first()
                bookings.append({
                    "registration_id":i.registartion_id,
                    "username":user.username,
                    "trek_name":trek.name,
                    "payment_status":i.payment_status,
                    "completion":i.completion
                })
            s.close()
            return render_template("admin_booking_history.html",bookings=bookings)
                  
    @app.route('/user_dashboard',methods =["POST","GET"])
    def user_dashboard():
        if "user_login" in session:
            if request.method =="GET":
                render_template("user_dashboard.html",login_first  = True)
        else:
            return redirect("/login")
    @app.route('/staff_dashboard',methods =["POST","GET"])
    def staff_dashboard():
        if "staff_login" in session:
            if request.method =="GET":
                return render_template("staff_dashboard.html")
        else:
            return redirect("/login",login_first  = True)
    
    
    @app.route("/logout",methods=["GET"])
    def logout():
        session.clear()
        return redirect("/")
    