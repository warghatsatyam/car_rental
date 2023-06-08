from car_rental_app.models import Car,Booking,UserProfile
from rest_framework import serializers


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','car_name','car_model','seat_capacity','per_day_price','no_of_cars','available_cars']


class BookingSerialzers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='car')
    user_id = serializers.IntegerField(source='user')
    class Meta:
        model = Booking
        fields = ['id','user_id','issue_date','return_date']
        
class ExtendBookingSerializers(serializers.Serializer):
    car = serializers.IntegerField()
    user = serializers.IntegerField()
    issue_date = serializers.DateField()
    return_date = serializers.DateField()
    
    
