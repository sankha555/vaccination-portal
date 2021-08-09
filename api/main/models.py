from django.db import models
from django.utils import timezone

from math import ceil, log2
from hashlib import sha256
import random

def hex_equ(string):
    ans = ""
    for c in string:
        ans += str(hex(ord(c)))
    return int(ans.replace("0x", ""), 16)

class Citizen(models.Model):
    """
    Model to encapsulate Citizen's details.
    """
    pseudo_uuid = models.CharField(verbose_name="Pseudo UUID", max_length=50, blank=True, null=True)
    district = models.CharField(verbose_name="Serving District", max_length=50, blank=True, null=True)
    state = models.CharField(verbose_name="Serving State", max_length=50, blank=True, null=True)
    pin_code = models.CharField(verbose_name="Serving PINCode", max_length=50, blank=True, null=True)
    govt_agency_id = models.CharField(verbose_name="Govt. Agency ID", max_length=50, blank=True, null=True)
    gender = models.CharField(verbose_name="Gender", max_length=50, blank=True, null=True)
    age = models.IntegerField(verbose_name="Age", default = 18)
    doses = models.IntegerField(verbose_name="Doses", default = 0)
    secret_code = models.CharField(verbose_name="Secret Code", max_length=50, blank=True, null=True)
    static_key = models.CharField(verbose_name="Static Key", max_length=50, blank=True, null=True)
    
    def calculate_age(self, dob):
        birth_year = int(dob.split('-')[2])
        self.age = 2021 - birth_year
        
    def generate_pseudo_uuid(self, uuid):
        pass1 = sha256(uuid.rstrip().encode('utf-8')).hexdigest().encode('utf-8')
        self.pseudo_uuid = sha256(pass1.rstrip()).hexdigest()
    
    def generate_secret_code(self):
        base_key = sha256((self.pseudo_uuid + self.pin_code).rstrip().encode('utf-8')).hexdigest()
        val_int = int(base_key, 16)
        
        secret_code = ceil(log2(val_int))*5
        self.secret_code = secret_code
    
    def generate_static_key(self, master_key):
        random.seed()
        r = int(random.random())
        
        uuid_hex = hex_equ(self.pseudo_uuid)
        master_key_hex = hex_equ(master_key)
        random_hex = int(r)
        
        xor = hex(uuid_hex ^ master_key_hex ^ random_hex).encode('utf-8')
        
        self.static_key = sha256(xor.rstrip()).hexdigest()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        

class Vaccination(models.Model):
    """
    Model to encapsulate Vaccination details.
    """
    vaccination_id = models.CharField(verbose_name="Vaccination ID", max_length=50, blank=True, null=True)
    pseudo_uuid = models.CharField(verbose_name="Pseudo UUID", max_length=50, blank=True, null=True)
    center_id = models.CharField(verbose_name="Center ID", max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name="Vaccination Timestamp", default=timezone.now)
    health_conditions = models.TextField(verbose_name="Health Conditions", max_length=1000, blank=True, null=True)
    vaccinator = models.CharField(verbose_name="Vaccinator Name", max_length=50, blank=True, null=True)
    vaccine_name = models.CharField(verbose_name="Vaccine Name", max_length=50, blank=True, null=True)
    dose_number = models.IntegerField(verbose_name="Dose Number", default = 0)
    
    def generate_vaccination_id(self):
        self.vaccination_id = self.pseudo_uuid + str(self.dose_number) + self.center_id
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)