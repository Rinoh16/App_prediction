from django.contrib import admin

# Register your models here.
from .models import Student,Person

admin.site.register(Student)
admin.site.register(Person)