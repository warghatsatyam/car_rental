from django.db import models
# from car_rental_app.views import str_time
# Create your models here.
from icecream import ic
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
    
    def get_booking_detail(self,request,booking,return_date):
        car_id = booking.car_id
        avail_car = booking.car.available_cars
        all_x_car_booking = Booking.objects.filter(car_id=car_id).order_by('issue_date')
        ic(all_x_car_booking)
        ic(avail_car)
        extend = False
        if avail_car>1:
            booking.return_date = return_date
            booking.save()
            extend=True
        else:
            for x in all_x_car_booking:
                ic(type(return_date),type(x.issue_date),type(x.return_date))
                if return_date >= x.issue_date and return_date <= x.return_date :
                    extend = False
                else:
                    booking.return_date = return_date
                    booking.save()
                    extend = True
        return extend


    