from django.contrib import admin
from abcd.populatedb import *

from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Stakeholders)
