from django.contrib import admin
from .models import Applicant, Bid, CompleteTask, TestTask, Rating

admin.site.register(Applicant)
admin.site.register(Bid)
admin.site.register(CompleteTask)
admin.site.register(TestTask)
admin.site.register(Rating)