from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Database.models import *
from datetime import datetime
from flask import request
from controllers.routes import get_Age

engine = create_engine("sqlite:///Database/trekking.db")
Session = sessionmaker(bind=engine)

class TreksAPI(Resource):
    def get(self):
        s = Session()
        treks = s.query(Trek).all()
        l = []
        for trek in treks:
            l.append({
                "id": trek.id,
                "name": trek.name,
                "max_age_for": trek.for_age_group,
                "number_of_slots": trek.no_of_slots,
                "number_of_registrations": trek.no_of_registration,
                "status": trek.trek_status,
                "difficulty": trek.difficulty,
                "start_date": str(trek.start_date),
                "end_date": str(trek.end_date),
                "description": trek.description,
                "starting_location": trek.starting_location,
                "ending_location": trek.ending_location,
                "registration_status": trek.registration_status
            })
        s.close()
        return l, 200
class TrekAPI(Resource):
    def get(self, trek_id):
        s = Session()
        trek = s.query(Trek).filter(Trek.id == trek_id).first()
        if trek is None:
            s.close()
            return {"message": "Trek not found"}, 404
        data = {
            "id": trek.id,
            "name": trek.name,
            "for_age_group": trek.for_age_group,
            "no_of_slots": trek.no_of_slots,
            "no_of_registration": trek.no_of_registration,
            "trek_status": trek.trek_status,
            "difficulty": trek.difficulty,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "description": trek.description,
            "starting_location": trek.starting_location,
            "ending_location": trek.ending_location,
            "registration_status": trek.registration_status
        }
        s.close()
        return data, 200

    def put(self, trek_id):
        s = Session()
        trek = s.query(Trek).filter(Trek.id == trek_id).first()
        if trek is None:
            s.close()
            return {"message": "Trek not found"}, 404
        data = request.get_json()
        if not data:
            s.close()
            return {"message": "No JSON data received"}, 400
        existing = s.query(Trek).filter(
            Trek.name == data["name"],
            Trek.id != trek_id
        ).first()
        if existing:
            s.close()
            return {"message": "Trek name already exists"}, 400
        start_date = datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        ).date()
        end_date = datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        ).date()
        if end_date < start_date:
            s.close()
            return {"message": "End date cannot be before start date"}, 400
        if data["no_of_slots"] < trek.no_of_registration:
            s.close()
            return {
                "message":
                "Number of slots cannot be less than current registrations"
            }, 400
        if data["difficulty"] not in ("Easy", "Moderate", "Hard"):
            s.close()
            return {"message": "Invalid difficulty"}, 400
        if data["trek_status"] not in (
            "upcoming",
            "ongoing",
            "completed",
            "deleted"
        ):
            s.close()
            return {"message": "Invalid trek status"}, 400
        if data["registration_status"] not in ("open", "closed"):
            s.close()
            return {"message": "Invalid registration status"}, 400
        trek.name = data["name"]
        trek.for_age_group = data["for_age_group"]
        trek.no_of_slots = data["no_of_slots"]
        trek.difficulty = data["difficulty"]
        trek.start_date = start_date
        trek.end_date = end_date
        trek.description = data["description"]
        trek.starting_location = data["starting_location"]
        trek.ending_location = data["ending_location"]
        trek.registration_status = data["registration_status"]
        trek.trek_status = data["trek_status"]
        s.commit()
        s.close()
        return {"message": "Trek updated successfully"}, 200
    def patch(self, trek_id):
        s = Session()
        trek = s.query(Trek).filter(Trek.id == trek_id).first()
        if trek is None:
            s.close()
            return {"message": "Trek not found"}, 404
        data = request.get_json()
        if not data:
            s.close()
            return {"message": "No JSON data received"}, 400
        if "name" in data:
            existing = s.query(Trek).filter(
                Trek.name == data["name"],
                Trek.id != trek_id
            ).first()
            if existing:
                s.close()
                return {"message": "Trek name already exists"}, 400
            trek.name = data["name"]
        if "for_age_group" in data:
            trek.for_age_group = data["for_age_group"]
        if "no_of_slots" in data:
            if data["no_of_slots"] < trek.no_of_registration:
                s.close()
                return {
                    "message":
                    "Number of slots cannot be less than current registrations"
                }, 400
            trek.no_of_slots = data["no_of_slots"]
        if "difficulty" in data:
            if data["difficulty"] not in ("Easy", "Moderate", "Hard"):
                s.close()
                return {"message": "Invalid difficulty"}, 400
            trek.difficulty = data["difficulty"]
        if "start_date" in data:
            start_date = datetime.strptime(
                data["start_date"],
                "%Y-%m-%d"
            ).date()
            if start_date > trek.end_date:
                s.close()
                return {
                    "message":
                    "Start date cannot be after end date"
                }, 400
            trek.start_date = start_date
        if "end_date" in data:
            end_date = datetime.strptime(
                data["end_date"],
                "%Y-%m-%d"
            ).date()
            if end_date < trek.start_date:
                s.close()
                return {
                    "message":
                    "End date cannot be before start date"
                }, 400
            trek.end_date = end_date
        if "description" in data:
            trek.description = data["description"]
        if "starting_location" in data:
            trek.starting_location = data["starting_location"]
        if "ending_location" in data:
            trek.ending_location = data["ending_location"]
        if "registration_status" in data:
            if data["registration_status"] not in ("open", "closed"):
                s.close()
                return {"message": "Invalid registration status"}, 400
            trek.registration_status = data["registration_status"]
        if "trek_status" in data:
            if data["trek_status"] not in (
                "upcoming",
                "ongoing",
                "completed",
                "deleted"
            ):
                s.close()
                return {"message": "Invalid trek status"}, 400
            trek.trek_status = data["trek_status"]
        s.commit()
        s.close()
        return {"message": "Trek updated successfully"}, 200
    def delete(self, trek_id):
        s = Session()
        trek = s.query(Trek).filter(Trek.id == trek_id).first()
        if trek is None:
            s.close()
            return {"message": "Trek not found"}, 404
        trek.trek_status = "deleted"
        s.commit()
        s.close()
        return {"message": "Trek deleted successfully"}, 200
class UserListAPI(Resource):
    def get(self):
        s = Session()
        users = s.query(Users).all()
        data = []
        for user in users:
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "gender": user.gender,
                "dob": str(user.dob),
                "age": user.age,
                "type": user.type
            })
        s.close()
        return data, 200
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No JSON data received"}, 400
        required = [
            "username",
            "email",
            "password",
            "name",
            "gender",
            "dob"
        ]
        for field in required:
            if field not in data:
                return {"message": f"{field} is required"}, 400
        s = Session()
        user = s.query(Users).filter(
            (Users.username == data["username"]) |
            (Users.email == data["email"])
        ).first()
        if user:
            s.close()
            return {"message": "Username or Email already exists"}, 400
        dob = datetime.strptime(
            data["dob"],
            "%Y-%m-%d"
        ).date()
        new_user = Users(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            name=data["name"],
            gender=data["gender"],
            dob=dob,
            age=get_Age(dob),
            type="user"
        )
        s.add(new_user)
        s.commit()
        response = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "name": new_user.name,
            "gender": new_user.gender,
            "dob": str(new_user.dob),
            "age": new_user.age,
            "type": new_user.type
        }
        s.close()
        return response, 201
class UserAPI(Resource):
    def get(self, user_id):
        s = Session()
        user = s.query(Users).filter(
            Users.id == user_id
        ).first()
        if user is None:
            s.close()
            return {"message": "User not found"}, 404
        response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "gender": user.gender,
            "dob": str(user.dob),
            "age": user.age,
            "type": user.type
        }
        s.close()
        return response, 200
    def put(self, user_id):
        s = Session()
        user = s.query(Users).filter(
            Users.id == user_id
        ).first()
        if user is None:
            s.close()
            return {"message": "User not found"}, 404
        data = request.get_json()
        if not data:
            s.close()
            return {"message":"No JSON data received"},400
        if "name" in data:
            if len(data["name"].strip()) == 0:
                s.close()
                return {"message": "Invalid name"}, 400
            user.name = data["name"]
        if "dob" in data:
            try:
                dob = datetime.strptime(
                    data["dob"],
                    "%Y-%m-%d"
                ).date()
            except:
                s.close()
                return {"message": "Invalid DOB format"}, 400
            user.dob = dob
            user.age = get_Age(dob)
        s.commit()
        response = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "gender": user.gender,
            "dob": str(user.dob),
            "age": user.age,
            "type": user.type
        }
        s.close()
        return response, 200
    def patch(self, user_id):
        return self.put(user_id)
    def delete(self, user_id):
        s = Session()
        user = s.query(Users).filter(
            Users.id == user_id
        ).first()
        if user is None:
            s.close()
            return {"message": "User not found"}, 404
        if user.type not in ("user", "deactivated_user"):
            s.close()
            return {"message": "Only normal users can be deactivated"}, 403
        user.type = "deactivated_user"
        s.commit()
        s.close()
        return {
            "message": "User deactivated successfully"
        }, 200

class BookingAPI(Resource):
    def get(self, registration_id):
        s = Session()
        booking = (
            s.query(User_terk)
            .filter(User_terk.registartion_id == registration_id)
            .first()
        )
        if booking is None:
            s.close()
            return {"message": "Booking not found"}, 404
        user = s.query(Users).filter(
            Users.id == booking.user_id
        ).first()
        trek = s.query(Trek).filter(
            Trek.id == booking.trek_id
        ).first()
        data = {
            "registration_id": booking.registartion_id,
            "user_id": booking.user_id,
            "username": user.username,
            "trek_id": booking.trek_id,
            "trek_name": trek.name,
            "payment_status": booking.payment_status,
            "completion": booking.completion
        }
        s.close()
        return data, 200

class BookingListAPI(Resource):
    def get(self):
        s = Session()
        bookings = s.query(User_terk).all()
        data = []
        for booking in bookings:
            user = s.query(Users).filter(
                Users.id == booking.user_id
            ).first()
            trek = s.query(Trek).filter(
                Trek.id == booking.trek_id
            ).first()
            data.append({
                "registration_id": booking.registartion_id,
                "user_id": booking.user_id,
                "username": user.username,
                "trek_id": booking.trek_id,
                "trek_name": trek.name,
                "payment_status": booking.payment_status,
                "completion": booking.completion
            })
        s.close()
        return data, 200
def api_routes(api):
    api.add_resource(TreksAPI, "/api/treks")
    api.add_resource(TrekAPI, "/api/treks/<int:trek_id>")
    api.add_resource(UserListAPI, "/api/users")
    api.add_resource(UserAPI, "/api/users/<int:user_id>")
    api.add_resource(BookingListAPI, "/api/bookings")
    api.add_resource(BookingAPI, "/api/bookings/<int:registration_id>")