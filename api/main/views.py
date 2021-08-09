from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from users.models import Center, GovtAgency
from main.models import Citizen, Vaccination

class CitizenRegistrationView(APIView):
    def post(self, request, format = None):
        data = request.data 
        
        citizen = Citizen.objects.create()
        citizen.generate_pseudo_uuid(data["uuid"])
        citizen.district = data["district"]
        citizen.state = data["state"]
        citizen.pin_code = data["pinCode"]
        citizen.govt_agency_id = GovtAgency.objects.get(user = request.user).pk
        citizen.gender = data["gender"]
        
        citizen.save()
        citizen.generate_static_key(GovtAgency.objects.get(user = request.user).master_key)
        citizen.generate_secret_code()
        citizen.calculate_age(data["dob"])
        
        citizen.save()
        
        res = {
            "citizenPseudoUUID": citizen.pseudo_uuid,
            "doses": citizen.doses,
            "gender": citizen.gender,
            "age": citizen.age,
            "staticKey": citizen.static_key,
            "secretCode": citizen.secret_code
        }
        
        return Response(res, status=status.HTTP_201_CREATED)
    
class VaccinationView(APIView):
    def post(self, request, format = None):
        data = request.data 
        
        citizen = Citizen.objects.get(pseudo_uuid = data["pseudoUUID"])
        center = Center.objects.get(user = request.user)
        
        vaccination = Vaccination.objects.create()
        vaccination.pseudo_uuid = citizen.pseudo_uuid
        vaccination.center_id = center.center_id
        vaccination.health_conditions = data["healthConditions"]
        vaccination.vaccinator = data["vaccinator"]
        vaccination.vaccine_name = data["vaccineName"]
        vaccination.dose_number = citizen.doses + 1
        
        vaccination.save()
        vaccination.generate_vaccination_id()
        vaccination.save()
        
        citizen.doses = vaccination.dose_number
        citizen.save()
        
        res = {
            "pseudoUUID": vaccination.pseudo_uuid,
            "centerID": vaccination.center_id,
            "vaccineName": vaccination.vaccine_name,
            "vaccinator": vaccination.vaccinator,
            "doseNumber": vaccination.dose_number,
            "healthConditions": vaccination.health_conditions,
        }
        
        return Response(res, status = status.HTTP_201_CREATED)
    