from car_rental_app.models import Car,Booking,UserProfile
from rest_framework import serializers


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','car_name','car_model','seat_capacity','per_day_price','no_of_cars','available_cars']

class AvailableCarSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    car_name = serializers.CharField()
    car_model = serializers.CharField()
    seat_capacity = serializers.IntegerField()
    per_day_price = serializers.IntegerField()
    # no_of_cars = serializers.IntegerField()


class BookingSerialzers(serializers.ModelSerializer):
    # id = serializers.IntegerField(source='car')
    # user_id = serializers.IntegerField(source='user')
    class Meta:
        model = Booking
        fields = ['car','user','issue_date','return_date']
        
class ExtendBookingSerializers(serializers.Serializer):
    car = serializers.IntegerField()
    user = serializers.IntegerField()
    issue_date = serializers.DateField()
    return_date = serializers.DateField()
    
    
