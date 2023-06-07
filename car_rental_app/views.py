from django.shortcuts import render
from django.db.models import F,Q
from car_rental_app.models import Car,UserProfile,Booking
from car_rental_app.serializers import CarSerializers,BookingSerialzers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['GET','POST'])
def car(request):
    if request.method == 'GET':
        queryset = Car.objects.all()
        serializers = CarSerializers(queryset,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializers = CarSerializers(data=request.data)
        print(serializers)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    

@api_view(['GET','POST'])
def available_car(request):
    car_name = request.GET.get('car_name')
    print(request.GET)
    if request.method == 'GET':
        queryset = Car.objects.filter(no_of_cars__gt=0)
        serializers = CarSerializers(queryset,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializers = BookingSerialzers(data=request.data)
        print(request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        car_id = request.data['car']
        car = Car.objects.get(pk=car_id)
        car.no_of_cars = car.no_of_cars -1
        car.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    
@api_view()
def particular_car(request,pk):
    """
    Here the pk which is passed is of 
    """
    car = Car.objects.get(pk=pk)
    # sourcery skip: remove-pass-elif
    if request.method == 'GET':
        no_of_car = car.no_of_cars
        if no_of_car > 0:
            car_queryset = Car.objects.get(pk=pk)
            serializer = CarSerializers(car_queryset)
        else:
            booking_queryset = Booking.objects.filter(car_id=car.id)
            serializer = BookingSerialzers(booking_queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

@api_view(['GET','POST'])
def filtered_car(request):
    if request.method=='GET':
        car_name = request.GET.get('car_name')
        car_model = request.GET.get('car_model')
        no_of_cars = request.GET.get('no_of_cars')
        per_day_price = request.GET.get('per_day_price')
        seat_capacity = request.GET.get('seat_capacity')
        queryset = Car.objects.filter(Q(car_name=car_name)|Q(car_model=car_model)|Q(no_of_cars=no_of_cars)|Q(per_day_price=per_day_price)|Q(seat_capacity=seat_capacity))
        serialize = CarSerializers(queryset,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializers = BookingSerialzers(data=request.data)
        print(request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        car_id = request.data['car']
        car = Car.objects.get(pk=car_id)
        car.no_of_cars = car.no_of_cars -1
        car.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    


@api_view(['GET','POST'])
def particular_user_booking(requset,pk):
    if requset.method == 'GET':
        user_booking_detail = Booking.objects.filter(user=pk)
        serializer = BookingSerialzers(user_booking_detail,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif requset.method == 'POST':
        pass

@api_view()
def cancel_booking(request,pk):
    """_summary_
    Here we are passing the booking id.
    Args:
        request (_type_): _description_
        pk (_type_): _description_
    """
    if request.method =='GET':
        booked_car = Booking.objects.filter(pk=pk)[0]
        Booking.objects.filter(pk=pk).update(booking_status='CANCEL')
        car_id = booked_car.car.id
        booked_car.booking_status = 'CANCEL'
        booked_car.save()
        car = Car.objects.get(pk=car_id)
        car.no_of_cars = F("no_of_cars") + 1
        car.save()
        return Response('OK',status=status.HTTP_200_OK)
    