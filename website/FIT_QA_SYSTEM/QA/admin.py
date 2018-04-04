from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Building)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Word_Standard)
admin.site.register(QuestionAnswerPair)
admin.site.register(PastQuestion)