from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='home'),  # ✅ Root URL shows login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_school, name='register_school'),  # ✅ Corrected name

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('parent/', views.parent_dashboard, name='parent_dashboard'),
    path('platform/', views.platform_dashboard, name='platform_dashboard'),
    path('school/<int:school_id>/', views.view_school, name='view_school'),
    path('delete_school/<int:school_id>/', views.delete_school, name='delete_school'),
    path('edit_school/<int:school_id>/', views.edit_school, name='edit_school'),
    path('settings/', views.settings_view, name='settings'),
    path('manage_users/', views.manage_users_view, name='manage_users'),
    path('announcements/', views.announcements_view, name='announcements'),

    # Students
    path('manage_students/', views.manage_students, name='manage_students'),
    path('add_student/', views.add_student, name='add_student'),
    path('student/<int:student_id>/', views.view_student, name='view_student'),
    path('student/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),


    # Teachers
    path('manage_teachers/', views.manage_teachers, name='manage_teachers'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('view_teacher/<int:teacher_id>/', views.view_teacher, name='view_teacher'),
    path('edit_teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),


    # Support Staff
    path('manage_staff/', views.manage_staff, name='manage_staff'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('view_staff/<int:staff_id>/', views.view_staff, name='view_staff'),
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),



    # Admin Actions
    path('add_student/', views.add_student, name='add_student'),
    path('record_fee/', views.record_fee, name='record_fee'),

    # Teacher Actions
    path('record_attendance/', views.record_attendance, name='record_attendance'),

    # Chatbot
      path("admin/dashboard/", views.dashboard, name="admin_dashboard"),
    path("admin/chatbot-reply/", views.chatbot_reply, name="chatbot_reply"),
]
