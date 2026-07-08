from flask import render_template,request,session,redirect
from sqlalchemy.orm import sessionmaker
from Database.models import *
from sqlalchemy import create_engine
from datetime import datetime,date
from flask_login import login_user,logout_user,login_required,current_user

engine = create_engine("sqlite:///Database/trekking.db")
Session = sessionmaker(bind=engine)
def get_Age(dob):
    today = date.today()
    age= today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age-= 1
    return age
def application_routes(app,login_manager):
    @login_manager.user_loader
    def load_user(user_id):
        s = Session()
        user = s.query(Users).filter(Users.id == int(user_id)).first()
        s.close()
        return user
    @app.route("/",methods = ["GET"])
    def homepAge():
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
                    login_user(u)
                    user_type = u.type 
                    s.close()
                    if user_type =="admin":                       
                        return redirect("/admin_dashboard")
                    elif user_type== "user":
                        return redirect("/user_dashboard")
                    elif user_type== "staff":
                        return redirect("/staff_dashboard")
    
    @app.route('/staff_apply',methods = ["GET","POST"])
    @app.route('/signup', methods = ["GET","POST"])
    def signup_or_staff_apply():
        type = None
        user_type = None
        if request.path =="/signup":
            type = "signup"
            user_type = "user"
        else:
            type = "staff_apply"
            user_type= "staff"
        if request.method=="GET":
            return render_template("signup.html",signup_done = False,exists_uname = False,used_mail = False,type = type)
        elif request.method == "POST":
            name = request.form['name']
            email  = request.form['email']
            u_name = request.form['username']
            password  = request.form['password']
            gender = request.form['gender']
            dob  = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
            age= get_Age(dob)
            s = Session()
            u = s.query(Users).filter((Users.username==u_name) | (Users.email==email)).first()
            if u is None :
                user  = Users(name = name,username= u_name, password= password, email = email, gender = gender, dob = dob ,age=age, type= user_type)
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
    @login_required
    def admin_dashboard():
        if current_user.type != "admin":
            return redirect('/login')
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
        
    @app.route('/admin_dashboard/user_list',methods=["POST","GET"])
    @login_required
    def admin_user_list():
        if current_user.type != "admin":
            return redirect('/login')
        s=Session()
        u = s.query(Users).filter((Users.type == "user") | (Users.type=="deactivated_user")).all()
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
            return render_template("admin_manage_user.html",users = users ) 
    @app.route('/staff_user_view')
    @app.route('/admin_dashboard/user_access',methods = ["GET"])
    @login_required
    def admin_user_access():
        if current_user.type not in  ("admin","staff"):
            return redirect('/login')
        if request.method=="GET":
            action = request.args.get("view_user_id")
            deactivate_user_id = request.args.get("deactivate_user_id")
            activate_user_id = request.args.get("activate_user_id")
            s=Session()
            if action :
                user_info = s.query(Users).filter(Users.id ==action).first()
                bookings=s.query(User_terk,Trek).join(Trek,User_terk.trek_id==Trek.id).filter(User_terk.user_id==action).all()
                s.close()
                if request.path =='/admin_dashboard/user_access':
                    return render_template("admin_user_access.html",user=user_info,bookings = bookings,admin = True)
                else :
                    return render_template("admin_user_access.html",user=user_info,bookings = bookings,admin = False )
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

    @app.route('/admin_dashboard/add_staff',methods = ["POST","GET"])
    @login_required
    def add_staff():
        if current_user.type != "admin":
            return redirect('/login')
        if request.method == "GET":
            return render_template("add_staff.html",added = False,exists_uname = False,used_mail = False)
        elif request.method =="POST":
            name = request.form['name']
            email  = request.form['email']
            u_name = request.form['username']
            password  = request.form['password']
            gender = request.form['gender']
            dob = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()            
            age = get_Age(dob)
            type= "staff"
            s = Session()
            u = s.query(Users).filter((Users.username==u_name) | (Users.email==email)).first()
            if u is None :
                user  = Users(name = name,username= u_name, password= password, email = email, gender = gender, dob = dob, type= type,age= age )
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
    @login_required
    def admin_staff_list():
        if current_user.type != "admin":
            return redirect('/login')
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
    @app.route('/admin_dashboard/add_trek',methods=["POST","GET"])
    @login_required
    def admin_add_trek():
        if current_user.type != "admin":
            return redirect('/login')
        s=Session()
        if request.method=="GET":
            staff=s.query(Users).filter(Users.type=="staff").all()
            s.close()
            return render_template("add_trek.html",added=False,staff=staff,error=None)
        elif request.method=="POST":
            name=request.form.get("name")
            age=request.form.get("age")
            slots=request.form.get("slots")
            difficulty=request.form.get("difficulty")
            start_date=datetime.strptime(request.form["start_date"],"%Y-%m-%d").date()
            end_date=datetime.strptime(request.form["end_date"],"%Y-%m-%d").date()
            start_location=request.form.get("starting_location")
            end_location=request.form.get("ending_location")
            staff_id=request.form.get("staff")
            if end_date<start_date:
                staff=s.query(Users).filter(Users.type=="staff").all()
                s.close()
                return render_template("add_trek.html",added=False,staff=staff,error="End date cannot be before start date.",admin = True )
            assigned_trek=s.query(Trek).join(Staff_trek,Trek.id==Staff_trek.trek_id).filter(Staff_trek.staff_id==staff_id,Trek.end_date>=start_date,Trek.start_date<=end_date).first()
            if assigned_trek:
                staff=s.query(Users).filter(Users.type=="staff").all()
                error="This staff is already assigned to '"+assigned_trek.name+"' from "+str(assigned_trek.start_date)+" to "+str(assigned_trek.end_date)+"."
                s.close()
                return render_template("add_trek.html",added=False,staff=staff,error=error,admin = True)
            t=Trek(name=name,for_age_group=age,no_of_slots=slots,difficulty=difficulty,trek_status="upcoming",start_date=start_date,end_date=end_date,starting_location=start_location,ending_location=end_location,no_of_registration=0,registration_status="open")
            s.add(t)
            s.commit()
            s_t=Staff_trek(trek_id=t.id,staff_id=staff_id)
            s.add(s_t)
            s.commit()
            s.close()
            return render_template("add_trek.html",added=True,trek_name=name,start_location=start_location,end_location=end_location,admin = True )
    @app.route('/admin_dashboard/manage_trek',methods=["POST","GET"])
    @login_required
    def admin_manage_trek():
        if current_user.type != "admin":
            return redirect('/login')
        s= Session()
        t = s.query(Trek).all()
        if request.method=="GET":
            return render_template("trek_list.html",treks = t)
        elif request.method =="POST":
            query = s.query(Trek)
            search = request.form.get("search")
            trek_type = request.form.get("type")
            difficulty = request.form.get("difficulty")

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
    @login_required
    def admin_edit_trek():
        if current_user.type != "admin":
            return redirect('/login')
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
            trek.description = request.form.get("description")
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
            staff_trek.staff_id = new_staff_id
            s.commit()
            trek = s.query(Trek).filter(Trek.id == trek_id).first()
            staff_id = s.query(Staff_trek).filter(Staff_trek.trek_id==trek_id).first()
            staff = s.query(Users).filter(Users.type=="staff").all()
            s.close()
            return render_template("edit_trek.html",trek=trek,edited=True,staff_id = staff_id.staff_id,staff= staff,trek_id = trek_id)

    @app.route("/admin_dashboard/delete_trek", methods = ["POST"])
    @login_required
    def admin_delete_trek():
        if current_user.type != "admin":
            return redirect('/login')
        if request.method =="POST":
            trek_id = request.form.get("trek_id")
            s= Session()
            trek = s.query(Trek).filter(Trek.id == trek_id).first()
            trek.trek_status= "deleted"
            s.commit()
            s.close()
            return redirect('/admin_dashboard/manage_trek')
              
    @app.route('/admin_dashboard/booking_history',methods=["POST","GET"])
    @login_required
    def admin_booking_history():
        if current_user.type != "admin":
            return redirect('/login')
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
                  
    @app.route('/staff_dashboard',methods=["GET","POST"])
    @login_required
    def staff_dashboard():
        if current_user.type != "staff":
            return redirect('/login')

        s=Session()
        staff=s.query(Users).filter(Users.id==current_user.id).first()

        if request.method=="GET":
            treks=s.query(Trek).join(Staff_trek,Trek.id==Staff_trek.trek_id).filter(Staff_trek.staff_id==current_user.id).all()
            s.close()
            return render_template("staff_dashboard.html",staff=staff,treks=treks,update_wrong=False)

        trek=s.query(Trek).filter(Trek.id==request.form.get("trek_id")).first()

        if trek.start_date<=date.today():

            if trek.trek_status=="upcoming":
                trek.trek_status="ongoing"
                s.query(User_terk).filter(User_terk.trek_id==trek.id).update({"completion":"ongoing"},synchronize_session=False)

            elif trek.trek_status=="ongoing":
                if trek.end_date<=date.today():
                    trek.trek_status="completed"
                    s.query(User_terk).filter(User_terk.trek_id==trek.id).update({"completion":"completed"},synchronize_session=False)
                else:
                    treks=s.query(Trek).join(Staff_trek,Trek.id==Staff_trek.trek_id).filter(Staff_trek.staff_id==current_user.id).all()
                    s.close()
                    return render_template("staff_dashboard.html",staff=staff,treks=treks,update_wrong=True)

            s.commit()
            treks=s.query(Trek).join(Staff_trek,Trek.id==Staff_trek.trek_id).filter(Staff_trek.staff_id==current_user.id).all()
            staff=s.query(Users).filter(Users.id==current_user.id).first()
            s.close()
            return render_template("staff_dashboard.html",staff=staff,treks=treks,update_wrong=False)

        else:
            treks=s.query(Trek).join(Staff_trek,Trek.id==Staff_trek.trek_id).filter(Staff_trek.staff_id==current_user.id).all()
            s.close()
            return render_template("staff_dashboard.html",staff=staff,treks=treks,update_wrong=True)
    @app.route('/staff_profile',methods=["GET","POST"])
    @login_required
    def staff_profile():
        if current_user.type != "staff":
            return redirect('/login')
        s=Session()
        if request.method=="GET":
            s.close()
            return render_template("profile.html",user = current_user,updated = False)
        elif request.method =="POST":
            name = request.form.get("name")
            dob = datetime.strptime(request.form.get("dob"),"%Y-%m-%d").date()
            staff = s.query(Users).filter(Users.id==current_user.id).first()
            staff.name = name
            staff.dob = dob
            staff.age= get_Age(dob)
            s.commit()
            s.close()
            s  = Session()
            staff = s.query(Users).filter(Users.id==current_user.id).first()
            s.close()
            return render_template("profile.html",user = staff,updated = True)
    
    @app.route("/staff_trek",methods = ["GET","POST"])
    @login_required
    def staff_terk():
        if current_user.type != "staff":
            return redirect('/login')
        if request.method =="GET":
            s= Session()
            staff = s.query(Users).filter(Users.id == current_user.id).first()
            treks = (s.query(Trek).join(Staff_trek, Trek.id == Staff_trek.trek_id).filter(Staff_trek.staff_id ==staff.id).all())
            s.close()
            return render_template("staff_trek_list.html",treks=treks)
        elif request.method =="POST":
            s=Session()
            query = (s.query(Trek).join(Staff_trek, Trek.id == Staff_trek.trek_id).filter(Staff_trek.staff_id == current_user.id)   )
            search = request.form.get("search")
            trek_type = request.form.get("type")
            difficulty = request.form.get("difficulty")
            if search:
                query = query.filter(Trek.name.ilike(f"%{search}%"))
            if trek_type not in ("None", "All"):
                query = query.filter(Trek.trek_status == trek_type)
            if difficulty not in ("None", "All"):
                query = query.filter(Trek.difficulty == difficulty)
            treks = query.all()
            s.close()
            return render_template("staff_trek_list.html", treks=treks)
    @app.route("/staff_trek_participants",methods=["GET","POST"])
    @login_required
    def staff_trek_participants():
        if current_user.type != "staff":
            return redirect('/login')
        s=Session()
        if request.method=="GET":
            trek_id=request.args.get("trek_id")
            trek=s.query(Trek).filter(Trek.id==trek_id).first()
            participants=s.query(Users,User_terk).join(User_terk,Users.id==User_terk.user_id).filter(User_terk.trek_id==trek_id).all()
            s.close()
            return render_template("staff_trek_participants.html",users=participants,trek=trek)
        else:
            trek_id=request.form.get("trek_id")
            remove_user_id=request.form.get("remove_user_id")
            u_p_user_id=request.form.get("u_p_user_id")
            trek=s.query(Trek).filter(Trek.id==trek_id).first()
            if remove_user_id:
                registration=s.query(User_terk).filter(User_terk.user_id==remove_user_id,User_terk.trek_id==trek_id).first()
                if registration:
                    if registration.payment_status=="done":
                        if trek.no_of_registration>0:
                            trek.no_of_registration-=1
                    registration.payment_status="pending"
                    registration.completion="cancelled"
                    s.commit()
            elif u_p_user_id:
                registration=s.query(User_terk).filter(User_terk.user_id==u_p_user_id,User_terk.trek_id==trek_id).first()
                if registration:
                    if registration.payment_status=="pending":
                        registration.payment_status="done"
                        trek.no_of_registration+=1
                        s.commit()
            s.close()
            return redirect(f"/staff_trek_participants?trek_id={trek_id}")
    @app.route("/staff_modify_trek",methods = ["GET","POST"])
    @login_required
    def staff_modify_trekk():
        if current_user.type != "staff":
            return redirect('/login')
        if request.method=="GET":
            s= Session()
            treks = s.query(Trek).filter(Trek.id == request.args.get("trek_id")).first()
            s.close()
            return render_template("staff_modify_trek.html", trek = treks , edited = False,less_value = False)
        elif request.method=="POST":
            s=Session()
            treks=s.query(Trek).filter(Trek.id==int(request.form.get("trek_id"))).first()
            slots=int(request.form.get("slots"))
            description=request.form.get("description")
            if slots<treks.no_of_registration:
                return render_template("staff_modify_trek.html",trek=treks,edited=False,less_value=True)
            treks.no_of_slots=slots
            treks.description=description
            if treks.no_of_registration==treks.no_of_slots:
                treks.registration_status="closed"
            else:
                treks.registration_status="open"
            s.commit()
            treks=s.query(Trek).filter(Trek.id==int(request.form.get("trek_id"))).first()
            s.close()
            return render_template("staff_modify_trek.html",trek=treks,edited=True,less_value=False)
    @app.route('/user_dashboard',methods =["POST","GET"])
    @login_required
    def user_dashboard():
        if current_user.type != "user":
            return redirect('/login')
        s= Session()
        user = s.query(Users).filter(Users.id == current_user.id).first()
        if request.method =="GET":
            trek = s.query(Trek).filter((Trek.registration_status=="open") & (Trek.trek_status == "upcoming")).all()
            s.close()
            return render_template("user_dashboard.html",user = user,treks =trek  )
        elif request.method =="POST":
            s= Session()
            query = s.query(Trek)
            search = request.form.get("search")
            difficulty = request.form.get("difficulty")
            applied = False
            if search:
                applied= True
                query = query.filter((Trek.starting_location.ilike(f"%{search}%")) & (Trek.registration_status=="open") & (Trek.trek_status == "upcoming") )
            if difficulty not in ("None", "All"):
                applied= True
                query = query.filter((Trek.difficulty == difficulty) &(Trek.registration_status=="open") & (Trek.trek_status == "upcoming"))
            if not applied:
                query = query.filter((Trek.registration_status=="open") & (Trek.trek_status == "upcoming"))
            treks = query.all()
            s.close()
            return render_template("user_dashboard.html", treks=treks, user = user)    
    
    @app.route('/user_profile',methods=["GET","POST"])
    @login_required
    def user_profile():
        if current_user.type != "user":
            return redirect('/login')
        s=Session()
        if request.method=="GET":
            user = s.query(Users).filter(Users.id==current_user.id).first()
            s.close()
            return render_template("profile.html",user = user,updated = False)
        elif request.method =="POST":
            name = request.form.get("name")
            dob = datetime.strptime(request.form.get("dob"),"%Y-%m-%d").date()
            user = s.query(Users).filter(Users.id==current_user.id).first()
            user.name = name
            user.dob = dob
            user.age= get_Age(dob)
            s.commit()
            s.close()
            s  = Session()
            user = s.query(Users).filter(Users.id==current_user.id).first()
            s.close()
            return render_template("profile.html",user = user,updated = True)
    @app.route('/user_trek_view',methods= ["GET"])
    @login_required
    def user_trek_view():
        if current_user.type != "user":
            return redirect('/login')
        s=Session()
        trek =  s.query(Trek).filter(Trek.id == request.args.get("trek_id")).first()
        s.close()
        return render_template("user_trek_view.html", trek = trek)   
    
    @app.route('/user_book_trek',methods=["GET","POST"])
    @login_required
    def user_book_trek():
        if current_user.type != "user":
            return redirect('/login')
        s=Session()
        if request.method=="GET":
            trek_id=request.args.get("trek_id")
            trek=s.query(Trek).filter(Trek.id==trek_id).first()
            s.close()
            return render_template("user_book_trek.html",trek=trek)
        else:
            trek_id=request.form.get("trek_id")
            already_booked=s.query(User_terk).filter(User_terk.user_id==current_user.id,User_terk.trek_id==trek_id).first()
        if already_booked:
            if already_booked.completion=="cancelled":
                already_booked.completion="upcoming"
                already_booked.payment_status="pending"
                s.commit()
                trek=s.query(Trek).filter(Trek.id==trek_id).first()
                s.close()
                return render_template("user_book_trek.html",booked=True)
            trek=s.query(Trek).filter(Trek.id==trek_id).first()
            s.close()
            return render_template("user_book_trek.html",trek=trek,already_booked=True)
        trek=s.query(Trek).filter(Trek.id==trek_id).first()
        s.close()
        return render_template("user_book_trek.html",trek=trek,already_booked=False)

    @app.route('/user_trek_list',methods=["GET","POST"])
    @login_required
    def user_trek_list():
        if current_user.type != "user":
            return redirect('/login')
        s=Session()
        if request.method=="GET":
            booked_trek=s.query(User_terk,Trek,Users).join(Trek,User_terk.trek_id==Trek.id).join(Staff_trek,Trek.id==Staff_trek.trek_id).join(Users,Staff_trek.staff_id==Users.id).filter(User_terk.user_id==current_user.id).all()
            user=s.query(Users).filter(Users.id==current_user.id).first()
            s.close()
            return render_template("user_trek_list.html",booked_trek=booked_trek,user=user,today=date.today(),refund=None)
        registration_id=request.form.get("registration_id")
        refund=None
        if registration_id:
            booking=s.query(User_terk).filter(User_terk.registartion_id==registration_id).first()
            if booking:
                trek=s.query(Trek).filter(Trek.id==booking.trek_id).first()
                if trek.trek_status=="upcoming":
                    refund="yes"
                    if booking.payment_status=="done":
                        if (trek.start_date-date.today()).days<=1:
                            refund="no"
                        if trek.no_of_registration>0:
                            trek.no_of_registration-=1
                    booking.completion="cancelled"
                    if booking.payment_status=="done":
                        if (trek.start_date-date.today()).days<=1:
                            refund="no"
                        else:
                            refund="yes"
                        if trek.no_of_registration>0:
                            trek.no_of_registration-=1
                    s.commit()
        booked_trek=s.query(User_terk,Trek,Users).join(Trek,User_terk.trek_id==Trek.id).join(Staff_trek,Trek.id==Staff_trek.trek_id).join(Users,Staff_trek.staff_id==Users.id).filter(User_terk.user_id==current_user.id).all()
        user=s.query(Users).filter(Users.id==current_user.id).first()
        s.close()
        return render_template("user_trek_list.html",booked_trek=booked_trek,user=user,today=date.today(),refund=refund)
    @app.route("/logout",methods=["GET"])
    @login_required
    def logout():
        logout_user()
        return redirect("/")
    