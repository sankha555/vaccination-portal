from django.db import models
from django.contrib.auth.models import User

from math import ceil, log2
import random
import os
from hashlib import sha256

def hex_equ(string):
    ans = ""
    for c in string:
        ans += str(hex(ord(c)))
    return int(ans.replace("0x", ""), 16)

class Center(models.Model):
    """
    Model to encapsulate Vaccination Center's details.
    """
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    center_id = models.CharField(verbose_name="Center ID", max_length=50, blank=True, null=True)
    name = models.CharField(verbose_name="Center Name", max_length=50, blank=True, null=True)
    address = models.TextField(verbose_name="Address", max_length=500, blank=True, null=True)
    district = models.CharField(verbose_name="Serving District", max_length=50, blank=True, null=True)
    state = models.CharField(verbose_name="Serving State", max_length=50, blank=True, null=True)
    pin_code = models.CharField(verbose_name="Serving PINCode", max_length=50, blank=True, null=True)
    govt_agency_id = models.CharField(verbose_name="Govt. Agency ID", max_length=50, blank=True, null=True)
    static_key = models.CharField(verbose_name="Static Key", max_length=50, blank=True, null=True)
    
    def generate_center_id(self):
        self.center_id = self.state + self.pin_code + str(self.pk)
    
    def generate_static_key(self, master_key):
        random.seed()
        r = int(random.random())
        
        id_hex = hex_equ(self.center_id)
        master_key_hex = hex_equ(master_key)
        random_hex = int(r)
        
        xor = (hex(id_hex ^ master_key_hex ^ random_hex)).encode('utf-8')
        
        self.static_key = sha256(xor.rstrip()).hexdigest()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        
class GovtAgency(models.Model):
    """
    Model to encapsulate Government Agency's details.
    """
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    district = models.CharField(verbose_name="Serving District", max_length=50, blank=True, null=True)
    state = models.CharField(verbose_name="Serving State", max_length=50, blank=True, null=True)
    pin_code = models.CharField(verbose_name="Serving PINCode", max_length=50, blank=True, null=True)
    serving_centers = models.ManyToManyField(Center)
    master_key = models.CharField(verbose_name="Master Key", max_length=50, blank=True, null=True)
    
    def generate_master_key(self):
        pass
        #self.master_key = os.urandom(16)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_master_key()
        