from django.db import models
from login_app.models import Users

# Create your models here.
class Countries(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class States(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Countries, related_name="states", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
class Cities(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(States, related_name="cities", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Consignees(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
class Vessels(models.Model):
    name = models.CharField(max_length=100)
    MMSI = models.CharField(max_length=15)
    longitude = models.FloatField()
    latitude = models.FloatField()
    IMO = models.CharField(max_length=7)
    callsign = models.CharField(max_length=10)
    destination = models.CharField(max_length=255)
    eta = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    

class Shipments(models.Model):
    number = models.CharField(max_length=20)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="shipments")
    vessel = models.ForeignKey(Vessels, related_name="shipments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
