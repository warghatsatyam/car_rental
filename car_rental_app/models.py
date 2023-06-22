from django.db import models
# from car_rental_app.views import str_time
# Create your models here.
from icecream import ic
from django.db.models import Q
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
    
    def get_booking_detail(self,booking,return_date):
        car_id = booking.car_id
        avail_car = booking.car.available_cars
        booking_id=booking.id
        extend = False
        if avail_car>1:
            booking.return_date = return_date
            booking.save()
            extend=True
        else:
            bool_extend = Booking.objects.filter(Q(car_id=car_id)& ~Q(booking_status='Cancel') & ~Q(id=booking_id) & Q(issue_date__lt=return_date)& Q(return_date__gt=return_date)).exists()
            ic(bool_extend)
            if bool_extend:
                extend = True
            else:
                extend = False
        ic(extend)
        return extend


    