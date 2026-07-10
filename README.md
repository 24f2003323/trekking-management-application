# Trekking Management Application

A web-based **Trekking Management System** developed as part of the **Modern Application Development I (MAD-I)** course at **IIT Madras**.

The application enables adventure organizations to efficiently manage trekking activities through dedicated interfaces for **Admin**, **Trek Staff**, and **Trekkers (Users)**.

---

# Features

- Role-Based Authentication using Flask-Login
- User and Staff Registration
- Admin Dashboard
- User Management
- Staff Management
- Trek Creation, Editing and Deletion
- Staff Assignment to Treks
- Trek Booking System
- Booking Cancellation
- Refund Eligibility System
- Trek Status Management
- Participant Management
- Payment Verification
- Booking History
- Search and Filtering
- User Profile Management
- RESTful JSON APIs
- Frontend and Backend Validation
- Duplicate Entry Prevention
- Overbooking Prevention

---

# Technology Stack

- Python
- Flask
- Flask-Login
- Flask-RESTful
- SQLAlchemy
- SQLite
- Jinja2
- HTML5
- CSS3

---

# User Roles

## Admin

- View dashboard statistics
- Add, edit and delete treks
- Approve, reject and manage staff
- Assign staff to treks
- Activate and deactivate users
- Activate and deactivate staff
- Search users, staff and treks
- View complete booking history

---

## Trek Staff

- Register and login after admin approval
- View assigned treks
- Modify trek description and available slots
- View registered participants
- Verify participant payments
- Remove unpaid participants
- Update trek status (Upcoming, Ongoing and Completed)

---

## Trekker (User)

- Register and login
- Browse available treks
- Search treks by location
- Filter treks by difficulty
- Book treks
- Cancel bookings
- View booking history
- View refund eligibility
- Update profile

---

# REST API Endpoints

## Trek APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/treks` | Get all treks |
| GET | `/api/treks/<trek_id>` | Get a specific trek |
| PUT | `/api/treks/<trek_id>` | Replace trek |
| PATCH | `/api/treks/<trek_id>` | Partially update trek |
| DELETE | `/api/treks/<trek_id>` | Soft delete trek |

---

## User APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get all users |
| POST | `/api/users` | Create user |
| GET | `/api/users/<user_id>` | Get a specific user |
| PUT | `/api/users/<user_id>` | Replace user |
| PATCH | `/api/users/<user_id>` | Partially update user |
| DELETE | `/api/users/<user_id>` | Deactivate user |

---

## Booking APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings` | Get all bookings |
| GET | `/api/bookings/<registration_id>` | Get booking details |

---

# Validation

## Frontend Validation

- Required fields
- Email validation
- Date validation
- Number validation
- Dropdown validation
- HTML5 input validation

## Backend Validation

- Duplicate username prevention
- Duplicate email prevention
- Staff approval validation
- Trek date validation
- Staff assignment conflict validation
- Slot validation
- Duplicate booking prevention
- Registration status validation
- Overbooking prevention
- Refund eligibility validation

---

# Project Structure

```text
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

# Installation

## Install Dependencies

```bash
pip install flask flask_sqlalchemy flask_login flask_restful
```

## Run the Application

```bash
python main.py
```

The application will run at:

```
http://127.0.0.1:5000
```

---

# Completed Functionalities

- ✅ User Registration and Login
- ✅ Staff Registration and Approval
- ✅ Admin Dashboard
- ✅ User Management
- ✅ Staff Management
- ✅ Trek Management
- ✅ Trek Booking System
- ✅ Booking Cancellation
- ✅ Refund Eligibility
- ✅ Payment Verification
- ✅ Participant Management
- ✅ Trek Status Tracking
- ✅ Booking History
- ✅ Search and Filtering
- ✅ Flask-Login Authentication and Authorization
- ✅ RESTful API Integration
- ✅ Frontend Validation
- ✅ Backend Validation
- ✅ Duplicate Entry Prevention
- ✅ Overbooking Prevention

---

Developed as part of the **Modern Application Development I (MAD-I)** course for the **IIT Madras BS Degree in Data Science and Applications**.