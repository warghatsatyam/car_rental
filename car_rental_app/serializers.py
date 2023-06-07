from car_rental_app.models import Car,Booking,UserProfile
from rest_framework import serializers


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','car_name','car_model','seat_capacity','per_day_price','no_of_cars']


class BookingSerialzers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['car','user','issue_date','return_date']
