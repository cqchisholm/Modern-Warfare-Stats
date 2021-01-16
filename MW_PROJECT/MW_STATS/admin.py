from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Friends)
admin.site.register(PrivateUsers)
admin.site.register(Score)