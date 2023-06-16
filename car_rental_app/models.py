from django.db import models

# Create your models here.

class Car(models.Model):
    car_name = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    seat_capacity = models.PositiveSmallIntegerField()
    per_day_price = models.PositiveSmallIntegerField()
    no_of_cars = models.PositiveSmallIntegerField()
    available_cars = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'car'

    def __str__(self):
        return self.car_name
    
class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=50)
    email = models.EmailField()
    contact_no = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'userprofile'

    def __str__(self):
        return self.username

class Booking(models.Model):
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField()
    booking_status = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'booking'
    
    def get_booking_detail(self,return_date):
        print(return_date)
        return '1'


    