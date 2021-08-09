from django.urls import path
from users.views import CenterRegistrationView

urlpatterns = [
    path('center', CenterRegistrationView.as_view(), name="center_registration"),
]
