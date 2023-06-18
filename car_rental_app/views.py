from django.shortcuts import render
from django.db.models import F,Q
from car_rental_app.models import Car,Booking
from car_rental_app.serializers import CarSerializers,AvailableCarSerializers,BookingSerializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from icecream import ic
from datetime import datetime
from django.http import Http404

@api_view(['GET','POST'])
def add_car(request):
    if request.method == 'GET':
        return Response("Add Car",status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serialze = CarSerializers(data=request.data)
        serialze.is_valid(raise_exception=True)
        serialze.save()
        return Response(serialze.data,status=status.HTTP_201_CREATED)
    
    
@api_view(['GET','POST'])
def getavailablecar(request):
    if request.method == 'GET':
        car = Car.objects.filter(available_cars__gt=0)
        serialize = AvailableCarSerializers(car,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        car = Car.objects.get(pk=request.data['car'])
        if car.available_cars>0:
            serialize = BookingSerializers(data=request.data)
            serialize.is_valid(raise_exception=True)
            serialize.save()
            car.available_cars = car.available_cars -1
            car.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        else:
            return Response("Car is not available",status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@api_view()
def get_particular_car(request,pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist as e:
        raise Http404("The car is not available") from e
    if car.available_cars>0:
        serialize = AvailableCarSerializers(car)
    else:
        booking = Booking.objects.filter(car=car.id)
        serialize = BookingSerializers(booking,many=True)
    return Response(serialize.data,status=status.HTTP_200_OK)
    
@api_view(['GET','POST'])
def userbookingdetail(request,pk):
    if request.method == 'GET':
        userbooking = Booking.objects.filter(user_id=pk)
        ic(userbooking)
        serialize = BookingSerializers(userbooking,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        booking = Booking.objects.filter(pk=pk)
        ic(booking)
        return Response(booking)
        
@api_view()
def cancelbooking(request,pk):
    booking = Booking.objects.get(pk=pk)
    booking.booking_status = 'Cancel'
    car_id = booking.car.id
    car = Car.objects.get(pk=car_id)
    car.available_cars = car.available_cars + 1
    car.save()
    booking.save()
    return Response('Booking Cancel',status=status.HTTP_200_OK)

def str_time(date):  # sourcery skip: avoid-builtin-shadow
    format = '%Y-%m-%d'
    return datetime.strptime(date,format).date()

@api_view(['GET'])
def filter_available_car(request):
    if request.method == 'GET':
        issue_date = str_time(request.GET.get('issue_date'))
        return_date = str_time(request.GET.get('return_date'))
        car_name = request.GET.get('car_name')
        car_model = request.GET.get('car_model')
        seat_capacity = request.GET.get('seat_capacity')
        per_day_price = request.GET.get('per_day_price')
        available_cars = []
        queryset = Car.objects.filter(Q(available_cars__gt=0)|Q(car_name=car_name)|Q(car_model=car_model)|Q(seat_capacity=seat_capacity)|Q(per_day_price=per_day_price))
        available_cars.extend(queryset)
        car2 = Car.objects.filter(available_cars=0)
        for x in car2:
            bookings = Booking.objects.filter(car_id=x.id).order_by('issue_date')
            ic(bookings)
            for booking in bookings:
                if (issue_date<booking.issue_date and return_date < booking.issue_date) or (issue_date>booking.return_date and return_date>booking.return_date):
                    car_available=True
                else:
                    car_available = False
                if car_available and (x not in available_cars):
                        available_cars.append(x) 
        serialize = AvailableCarSerializers(available_cars,many=True)
        return Response(serialize.data)


@api_view(['GET','POST'])
def extend_user_booking(request,pk):
    if request.method == 'GET':
        userbooking = Booking.objects.filter(pk=pk)
        ic(userbooking)
        serialize = BookingSerializers(userbooking,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        booking_id = request.data['id']
        booking = Booking.objects.get(pk=booking_id)
        return_date = str_time(request.data['return_date'])
        response = booking.get_booking_detail(request,booking,return_date)
        booking = Booking.objects.get(pk=booking_id)
        booking_serializer = BookingSerializers(booking)
        if response:
            return Response(booking_serializer.data,status=status.HTTP_200_OK)
        return Response("Cannot Extend",status=status.HTTP_405_METHOD_NOT_ALLOWED)


