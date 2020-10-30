from django.contrib import admin
from .models import Student, Team, Challenge, Mentoring, Mentor, Judge

# Register your models here.
admin.site.register(Student)
admin.site.register(Team)
admin.site.register(Challenge)
admin.site.register(Mentoring)
admin.site.register(Mentor)
admin.site.register(Judge)