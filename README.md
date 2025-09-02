# EduTrack 📚  
**Enhancing educational productivity through technology**

EduTrack is a school digitization platform designed to streamline administrative workflows, improve data visibility, and support scalable education infrastructure across Kenyan institutions. Built with Django and SQLite, it currently supports multi-role access for super admins, school admins, and teachers.

---

## 📚 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#️-project-structure)
- [Setup Instructions](#-setup-instructions)
- [User Roles & Access](#-user-roles--access)
- [Implemented Features](#-implemented-features)
- [Screenshots](#-screenshots)
- [AI Integration](#-ai-integration)
- [Known Limitations](#️-known-limitations)
- [Future Roadmap](#-future-roadmap)
- [Subscription Model](#-subscription-model)
- [Data Flow Overview](#-data-flow-overview)
- [Deployment Status](#-deployment-status)
- [Licensing](#-licensing)
- [Contributors](#-contributors)
- [Contact & Support](#-contact--support)

---

## 🧰 Tech Stack

- **Backend**: Python 3.x, Django  
- **Frontend**: HTML5, CSS3, JavaScript  
- **Database**: SQLite (default for local setup)  
- **Static Assets**: `/static/css/`, `/media/`  
- **Templating**: Django Templates (`/templates/`)

---

## 🗂️ Project Structure

```plaintext
README.md

SMS_CLEAN/
├── db.sqlite3
├── manage.py
│
├── media/
│   ├── staff_photos/
│   ├── student_photos/
│   └── teacher_photos/
│
├── SMS_CLEAN/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
│   └── __pycache__/
│
├── static/
│   ├── css/
│   ├── js/
│   └── media/
│
├── templates/
│   ├── *.html
│   └── school_admin/
│       ├── add_student.html
│       ├── add_teacher.html
│       └── ...
│
└── theschool/
    ├── *.py
    ├── migrations/
    ├── templatetags/
    └── __pycache__/
```

---

## 🚀 Setup Instructions

### Clone the project
```bash
git clone <repo-url>
cd SMS_CLEAN
```

### Install Django
```bash
pip install django
```

### Run migrations
```bash
python manage.py migrate
```

### Create superuser
```bash
python manage.py createsuperuser
```

### Start the server
```bash
python manage.py runserver
```

### Access the app
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🔐 User Roles & Access

### 👑 Super Admin
- Registers schools  
- Manages platform settings and users  
- Views global metrics and fee compliance  

**Dummy Credentials**  
- Username: `PRIMUS`  
- Password: `optimusprime`

### 🏫 School Admin
- Manages students, teachers, and support staff  
- Records fees and monitors attendance  
- Accesses school-level dashboards  

**Dummy Credentials**  
- Username: `admin`  
- Password: `admin1`

### 👨‍🏫 Teacher
- Logs in once account is created  
- Views dashboard, submits lesson plans, records attendance  
> _Note: Teacher-side logic is partially implemented. Login flow pending._

---

## ✅ Implemented Features

- Student registration and management  
- Teacher registration and management  
- Support staff registration and management  
- Auto-ID generation for students, teachers, and staff  
- Attendance recording and weekly summaries  
- Fee recording and SMS notifications  
- Role-based dashboards for each user type  

---

## 🖼️ Screenshots

### 🔐 Login Screen
![Login page](<Screenshot (2399).png>)

### 🧭 Platform Admin Dashboard
![Super Admin Dashboard](<Screenshot (2400).png>)

### 🏫 School Admin Dashboard
![School Admin Dashboard](<Screenshot (2401).png>)

---

## 🤖 AI Integration

The system includes a placeholder AI module designed to support future analytics and automation. While currently inactive due to lack of training data, it is structured to accommodate:

- Insights on student attendance 
- Summaries provided based on present school records
- Various enquiries

**To be added:**  
- Timetable scheduling
- Fee tracking
- Linkage to submitted in-system attendance records  
- Database access under logical restrictions

---

## ⚠️ Known Limitations

- No student or parent login flows  
- No payment gateway integration (e.g., M-Pesa, Stripe)  
- No bulk upload or export features  
- No mobile responsiveness or PWA setup  
- No audit logs or in-app notifications  
- AI module present but inactive due to lack of attendance data  

---

## 📈 Future Roadmap

- Implement teacher-stream-subject assignment logic  
- Build out fee ledger and receipt generation  
- Integrate payment gateways for fees and subscriptions  
- Enforce subscription tiers with feature gating  
- Expand teacher dashboard with attendance history and messaging  
- Launch student and parent dashboards once core logic is stable  
- Activate AI module once attendance data is available  

---

## 💳 Subscription Model

| Tier     | Features                                                                 |
|----------|--------------------------------------------------------------------------|
| Free     | Basic student/teacher CRUD, attendance, dashboard                        |
| Standard | Fee tracking, lesson plans, parent messaging                             |
| Premium  | Reports, exports, analytics, mobile payment integration (M-Pesa, banks)  |

---

## 🔄 Data Flow Overview

```plaintext
Class Teacher → Attendance Records → AI Module → Attendance Insights
```

- Teachers submit attendance via dashboard  
- AI module (once active) analyzes patterns  
- Insights delivered to admins for intervention or reporting  

---

## 🧪 Deployment Status

- Currently runs on `localhost` only  
- No production deployment or cloud hosting configured  
- No `.env` or environment variable setup required  

---

## 📜 Licensing

- No license currently applied  
- Not intended for third-party use or redistribution  

---

## 👥 Contributors

- **Chrysanthus Jumaa** – GIS Developer & System Architect  
- **Calvin Wanderi** – AI Developer & Automation Lead 

---

## 📬 Contact & Support

For questions, integration help, or roadmap discussions, reach out to:

**Chrysanthus Jumaa**  
📧 _[chrysanthusjumaa@gmail.com]_

**Calvin Wanderi**  
📧 _[calvinwanderi10260@gmail.com]_
