from django.urls import path
from main.views import CitizenRegistrationView, VaccinationView

urlpatterns = [
    path('citizen', CitizenRegistrationView.as_view(), name="citizen_registration"),
    
    path('vaccination', VaccinationView.as_view(), name="vaccination"),
]
