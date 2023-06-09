from django.shortcuts import render
from django.db.models import F,Q
from car_rental_app.models import Car,UserProfile,Booking
from car_rental_app.serializers import CarSerializers,AvailableCarSerializers,BookingSerialzers,ExtendBookingSerializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from icecream import ic
from datetime import datetime

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
    if request.method == 'GET':
        queryset = Car.objects.filter(available_cars__gt=0)
        serializers = AvailableCarSerializers(queryset,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        available_cars = Car.objects.get(pk=request.data['car']).available_cars
        if available_cars>0:    
            serializers = BookingSerialzers(data=request.data)
            serializers.is_valid(raise_exception=True)
            ic(request.data)
            serializers.save()
            car_id = request.data['car']
            car = Car.objects.get(pk=car_id)
            car.available_cars = car.available_cars -1
            car.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        else:
            car_id = request.data['car']
            ic(request.data)
            car  = Car.objects.get(pk=car_id)
            ic(car.booking_queue)
            
            car.booking_queue.append(request.data)
            car.save()
            return Response(request.data)
@api_view()
def particular_car(request,pk):
    """
    Here the pk which is passed is of 
    """
    car = Car.objects.get(pk=pk)
    # sourcery skip: remove-pass-elif
    if request.method == 'GET':
        no_of_car = car.available_cars
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
        available_cars = request.GET.get('available_cars')
        per_day_price = request.GET.get('per_day_price')
        seat_capacity = request.GET.get('seat_capacity')
        queryset = Car.objects.filter(Q(car_name=car_name)|Q(car_model=car_model)|Q(available_cars=available_cars)|Q(per_day_price=per_day_price)|Q(seat_capacity=seat_capacity))
        serialize = CarSerializers(queryset,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializers = BookingSerialzers(data=request.data)
        ic(request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        car_id = request.data['car']
        car = Car.objects.get(pk=car_id)
        car.available_cars = car.available_cars -1
        car.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
 
def str_to_date(str_date):
    format_date = "%y-%m-%d"
    return datetime.strptime(str_date,format_date)


@api_view(['GET','PATCH'])
def particular_user_booking(requset,pk):
    if requset.method == 'GET':
        user_booking_detail = Booking.objects.filter(Q(user_id=pk)& ~Q(booking_status='CANCEL'))
        serializer = BookingSerialzers(user_booking_detail,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif requset.method == 'PATCH':
        car = Car.objects.get(pk=requset.data['car'])
        available_cars = car.available_cars
        if available_cars > 0:
            booking = BookingSerialzers(data=requset.data)
            booking.is_valid(raise_exception=True)
            booking.save()
            car.available_cars = car.available_cars - 1
            car.save()
            return Response(booking.data,status=status.HTTP_201_CREATED)
        else:
            ic(requset.data)
            issue_date = requset.data['issue_date']
            return_date = requset.data['return_date']
            car_id = requset.data['car']
            user_id = requset.data['user']
            ic(issue_date,return_date,car_id,user_id)
            return Response('Car is not available let me write that logic to handle this part.')
        
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
        car.available_cars = F("available_cars") + 1
        car.save()
        
        return Response('OK',status=status.HTTP_200_OK)
