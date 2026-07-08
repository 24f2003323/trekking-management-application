# Trekking Management Application

A web-based Trekking Management System developed as part of the **Modern Application Development I (MAD-I)** course.

The application enables adventure organizations to efficiently manage trekking activities through dedicated interfaces for **Admin**, **Trek Staff**, and **Trekkers (Users)**.

---

# Features

- User Registration and Login
- Role-Based Authentication using Flask-Login
- Trek Staff Management
- Trek Creation and Management
- Trek Booking System
- Booking History Tracking
- Trek Status Management
- Search and Filtering
- RESTful JSON APIs
- Frontend and Backend Validation
- Duplicate Entry Prevention
- Booking Validation
- Responsive Bootstrap UI

---

# Technology Stack

- Python
- Flask
- Flask-Login
- Flask-RESTful
- SQLite
- SQLAlchemy
- Jinja2
- HTML5
- CSS3
- Bootstrap

---

# User Roles

## Admin

- Manage users
- Manage trek staff
- Create, edit and delete treks
- Assign staff to treks
- View booking history
- Monitor trek statistics

---

## Trek Staff

- View assigned treks
- Update trek status
- Modify trek information
- Manage participants
- Verify payments

---

## Trekker (User)

- Register and login
- Browse available treks
- Book treks
- View booking history
- Update profile
- Cancel bookings

---

# REST API Endpoints

## Trek APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/treks` | Get all treks |
| GET | `/api/treks/<trek_id>` | Get a specific trek |
| PUT | `/api/treks/<trek_id>` | Update an entire trek |
| PATCH | `/api/treks/<trek_id>` | Partially update a trek |
| DELETE | `/api/treks/<trek_id>` | Soft delete a trek |

---

## User APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create a new user |
| GET | `/api/users/<user_id>` | Get a specific user |
| PUT | `/api/users/<user_id>` | Update user profile |
| PATCH | `/api/users/<user_id>` | Partially update user profile |
| DELETE | `/api/users/<user_id>` | Deactivate a user |

---

## Booking APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings` | Get all bookings |
| GET | `/api/bookings/<registration_id>` | Get a specific booking |

---

# Validation Features

## Frontend Validation

- HTML5 form validation
- Required field validation
- Email validation
- Number range validation
- Date validation
- Input length validation
- Dropdown validation

## Backend Validation

- Duplicate username prevention
- Duplicate email prevention
- Duplicate trek name prevention
- Trek date validation
- Trek slot validation
- Booking validation
- Registration status validation
- Trek status validation
- Difficulty validation
- User profile validation

---

# Admin Credentials

**Username**

```
aman_admin
```

**Password**

```
aman@9897
```

---

# Project Structure

```
Trekking-Management-Application
│
├── controllers/
│   ├── routes.py
│   └── api.py
│
├── Database/
│   ├── models.py
│   └── trekking.db
│
├── templates/
├── static/
├── main.py
├── test.py
└── README.md
```

---

# Running the Project

## Install dependencies

```bash
pip install flask flask_sqlalchemy flask_login flask_restful
```

## Run the application

```bash
python main.py
```

The application will be available at:

```
http://127.0.0.1:5000
```

---

# Current Milestones Completed

- ✅ User Registration and Login
- ✅ Admin Dashboard
- ✅ Trek Management
- ✅ Staff Management
- ✅ Trek Booking System
- ✅ Booking History and Trek Status Tracking
- ✅ Flask-Login Authentication and Authorization
- ✅ RESTful API Integration using Flask-RESTful
- ✅ Frontend Validation using HTML5
- ✅ Backend Validation in Flask Controllers
- ✅ Invalid Booking and Duplicate Entry Prevention

---

# Future Improvements

- Charts and Analytics Dashboard
- Responsive UI Enhancements


---

Developed as part of the **Modern Application Development I (MAD-I)** course.