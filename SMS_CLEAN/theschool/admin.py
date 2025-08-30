from django.contrib import admin
from .models import (
    School, User, Stream, Student, ParentDetails, GuardianDetails,
    Attendance, FeeRecord, LessonPlan, PlatformConfig,
    Teacher, SupportStaff, ClassRoom
)

admin.site.register(School)
admin.site.register(User)
admin.site.register(Stream)
admin.site.register(Student)
admin.site.register(ParentDetails)
admin.site.register(GuardianDetails)
admin.site.register(Attendance)
admin.site.register(FeeRecord)
admin.site.register(LessonPlan)
admin.site.register(PlatformConfig)
admin.site.register(Teacher)
admin.site.register(SupportStaff)
admin.site.register(ClassRoom)
