from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import Center, GovtAgency

class CenterRegistrationView(APIView):
    def post(self, request, format = None):
        data = request.data
        
        center = Center.objects.create(user = request.user)
        center.name = data["name"]
        center.address = data["address"]
        center.district = data["district"]
        center.state = data["state"]
        center.pin_code = data["pinCode"]
        center.govt_agency_id = (GovtAgency.objects.all().first()).pk
        
        center.save()
        
        center.generate_center_id()
        center.generate_static_key(GovtAgency.objects.all().first().master_key)
        
        center.save()
        
        res = {
            "centerID": center.center_id,
            "centerName": center.name,
            "address": center.address,
            "pinCode": center.pin_code,
            "staticKey": center.static_key,
        }
        
        return Response(res, status=status.HTTP_201_CREATED)
        
    # def get(self, request, format = None):
    #     center = Center.objects.get(user = request.user)
        
    #     res = {
    #         "centerID": center.center_id,
    #         "centerName": center.name,
    #         "address": center.address,
    #         "pinCode": center.pinCode,
    #         "staticKey": center.static_key,
    #     }
        
    #     return Response(res, status=status.HTTP_200_OK)

