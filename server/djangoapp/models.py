from itertools import product
from django.db import models
from django.utils.timezone import now


# Create your models here.

# Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=48)
    description = models.TextField()
    founded = models.DateField()
    headquarters = models.CharField(max_length=48)
    products = models.CharField(max_length=48)
    parent = models.CharField(max_length=48)

    def __str__(self):
        return f'#{self.id}: {self.name}'


# Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=48)
    dealer_id = models.IntegerField()
    TYPES = (
        ("SEDAN", "Sedan"),
        ("COUPE", "Coupe"),
        ("SPORTS", "Sports Car"),
        ("WAGON", "Station Wagon"),
        ("HATCHBACK", "Hatchback"),
        ("CONVERTIBLE", "Convertible"),
        ("SUV", "Sport-Utility Vehicle (SUV)"),
        ("MINIVAN", "Minivan"),
        ("PICKUP", "Pickup Truck")
    )
    type = models.CharField(blank=True, choices=TYPES, max_length=11)
    year = models.IntegerField()
    fuel_consumption = models.IntegerField()
    efficiency_class = models.CharField(max_length=24)

    def __str__(self):
        return f'#{self.id}: {self.name}, type: {self.type}'


# Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer state
        self.state = state
        # Dealer zip
        self.zip = zip
        
        def __str__(self):
            return f'Dealer name: {self.full_name}'

# <HINT> Create a plain Python class `DealerReview` to hold review data
