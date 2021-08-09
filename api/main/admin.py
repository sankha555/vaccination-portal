from django.contrib import admin
from main.models import Citizen, Vaccination

admin.site.register([Citizen, Vaccination])
