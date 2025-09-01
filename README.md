# ElimuDigital 📚  
**Enhancing Educational Productivity Technology**

ElimuDigital is a school digitization platform designed to streamline administrative workflows, improve data visibility, and support scalable education infrastructure across Kenyan institutions. Built with Django and SQLite, it currently supports multi-role access for super admins, school admins, and teachers.

---

## 🧰 Tech Stack

- **Backend**: Python 3.x, Django
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (default for local setup)
- **Static Assets**: Organized under `/static/css` and `/media/`
- **Templating**: Django Templates (`/templates/`)

---

## 🗂️ Project Structure

SMS_CLEAN/ ├── SMS_CLEAN/ # Core Django project │ └── settings.py, urls.py, wsgi.py, etc. ├── theschool/ # Main app with models, views, utils │ └── models.py, views.py, urls.py, utils.py ├── templates/ # HTML templates (admin, teacher, parent) ├── static/ # CSS and media assets ├── media/ # Uploaded profile photos └── manage.py

---

## 🚀 Setup Instructions

1. **Clone the project**  
   ```bash
   git clone <repo-url>
   cd SMS_CLEAN

2. Install Django
pip install django

3. Run the server
python manage.py runserver

4. Access the app
Visit http://127.0.0.1:8000 in your browser.

🔐 User Roles & Access
👑 Super Admin
Registers schools

Manages platform settings and users

Views global metrics and fee compliance

Dummy Credentials

Username: PRIMUS

Password: optimusprime

🏫 School Admin
Manages students, teachers, and support staff

Records fees and monitors attendance

Accesses school-level dashboards

Dummy Credentials

Username: admin

Password: admin1

👨‍🏫 Teacher
Can log in (once user account is created)

Views dashboard, submits lesson plans, records attendance 
Note: Teacher-side logic is partially implemented. No login flow yet.

✅ Implemented Features
Admin Modules
Student registration and management

Teacher registration and management

Support staff registration and management

Auto-ID generation for students, teachers, and staff

Attendance recording and weekly summaries

Fee recording and SMS notifications

Role-based dashboards for each user type

🟡 Partially Implemented / In Progress
Teacher dashboard (lesson plans, attendance form)

Parent dashboard (fee and attendance summary)

Fee compliance metrics (no payment gateway yet)

Subscription model (Free, Standard, Premium tiers)

Class teacher assignment and role hierarchy

Messaging and announcements

🤖 AI Integration Placeholder
This system is designed to accommodate future AI logic for:

Timetable creation and optimization

Teacher-stream-subject scheduling

Conflict resolution and availability tracking

Note to AI Developer: Models like TeachingAssignment and Stream are flexible and can be extended. No hard constraints have been enforced to allow seamless integration.

⚠️ Known Limitations
No student or parent login flows

No payment gateway integration (M-Pesa, Stripe, etc.)

No bulk upload or export features

No mobile responsiveness or PWA setup

No audit logs or in-app notifications

📈 Future Roadmap
Implement teacher-stream-subject assignment logic

Build out fee ledger and receipt generation

Integrate payment gateways for fees and subscriptions

Enforce subscription tiers with feature gating

Expand teacher dashboard with attendance history and messaging

Launch student and parent dashboards once core logic is stable

👥 Contributors
Chrysanthus Jumaa – GIS Developer & System Architect

Calvin Wanderi – AI Developer & Automation Lead (to be filled in)

📬 Contact & Support
For questions, integration help, or roadmap discussions, reach out to Chrysanthus directly.
