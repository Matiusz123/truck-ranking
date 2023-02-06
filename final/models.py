from django.db import models
from datetime import datetime, timedelta
# Create your models here.
from django.utils.timezone import now


class User(models.Model):
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=40, default="No Company name")


class Vehicle(models.Model):
    vin = models.CharField(max_length=20, unique=True)
    avgFuelConsumptionPer100Km = models.FloatField()
    distance_traveled = models.IntegerField()
    fuel_consumed = models.IntegerField()
    last_data_upload = models.DateTimeField()
    first_data_upload = models.DateTimeField()
    average_fuel_consumption_from_update = models.FloatField(default=0)
    days_from_update = models.IntegerField(default=0)


class Fleet(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    models.ManyToManyField(Vehicle, through='VehiclesInFleet')


class VehiclesInFleet(models.Model):
    Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    Fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)


class API(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
