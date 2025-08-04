from django.contrib import admin
from .models import User,Internship,Enrollment,Task,TaskAssignment,TaskSubmission,MockInterview,ActivityLog

# Register your models here.
admin.site.register(User)
admin.site.register(Internship)
admin.site.register(Enrollment)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskSubmission)
admin.site.register(MockInterview)
admin.site.register(ActivityLog)
