from django.contrib import admin
from users.models import Center, GovtAgency

admin.site.register([Center, GovtAgency])
