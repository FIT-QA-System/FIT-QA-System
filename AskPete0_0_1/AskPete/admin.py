from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import * #this line added
admin.site.register(Question)#this line added
admin.site.register(Answer)
admin.site.register(CourseInfo)
