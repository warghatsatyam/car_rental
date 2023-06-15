from django.shortcuts import render
from django.db.models import F,Q
from car_rental_app.models import Car,UserProfile,Booking
from car_rental_app.serializers import CarSerializers,AvailableCarSerializers,BookingSerializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from icecream import ic
from datetime import datetime

# # Create your views here.
# @api_view(['GET','POST'])
# def car(request):
#     if request.method == 'GET':
#         queryset = Car.objects.all()
#         serializers = CarSerializers(queryset,many=True)
#         return Response(serializers.data,status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializers = CarSerializers(data=request.data)
#         print(serializers)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data,status=status.HTTP_201_CREATED)
    

# @api_view(['GET','POST'])
# def available_car(request):
#     if request.method == 'GET':
#         queryset = Car.objects.filter(available_cars__gt=0)
#         serializers = AvailableCarSerializers(queryset,many=True)
#         return Response(serializers.data,status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         available_cars = Car.objects.get(pk=request.data['car']).available_cars
#         if available_cars>0:    
#             serializers = BookingSerialzers(data=request.data)
#             serializers.is_valid(raise_exception=True)
#             serializers.save()
#             car_id = request.data['car']
#             car = Car.objects.get(pk=car_id)
#             car.available_cars = car.available_cars -1
#             car.save()
#             return Response(serializers.data,status=status.HTTP_201_CREATED)
#         else:
#             car_id = request.data['car']
#             ic(request.data)
#             car  = Car.objects.get(pk=car_id)
#             ic(car.booking_queue)
#             car.booking_queue.append(request.data)
#             car.save()
#             return Response(request.data)
# @api_view()
# def particular_car(request,pk):
#     """
#     Here the pk which is passed is of 
#     """
#     car = Car.objects.get(pk=pk)
#     # sourcery skip: remove-pass-elif
#     if request.method == 'GET':
#         no_of_car = car.available_cars
#         if no_of_car > 0:
#             car_queryset = Car.objects.get(pk=pk)
#             serializer = CarSerializers(car_queryset)
#         else:
#             booking_queryset = Booking.objects.filter(Q(car_id=car.id) & ~Q(booking_status='CANCEL'))
#             serializer = BookingSerialzers(booking_queryset,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    

# @api_view(['GET','POST'])
# def filtered_car(request):
#     if request.method=='GET':
#         car_name = request.GET.get('car_name')
#         car_model = request.GET.get('car_model')
#         available_cars = request.GET.get('available_cars')
#         per_day_price = request.GET.get('per_day_price')
#         seat_capacity = request.GET.get('seat_capacity')
#         queryset = Car.objects.filter(Q(car_name=car_name)|Q(car_model=car_model)|Q(available_cars=available_cars)|Q(per_day_price=per_day_price)|Q(seat_capacity=seat_capacity))
#         serialize = CarSerializers(queryset,many=True)
#         return Response(serialize.data,status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializers = BookingSerialzers(data=request.data)
#         ic(request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         car_id = request.data['car']
#         car = Car.objects.get(pk=car_id)
#         car.available_cars = car.available_cars -1
#         car.save()
#         return Response(serializers.data,status=status.HTTP_201_CREATED)
 
# def str_to_date(str_date):
#     format_date = "%y-%m-%d"
#     return datetime.strptime(str_date,format_date)


# @api_view(['GET','PATCH'])
# def particular_user_booking(requset,pk):
#     if requset.method == 'GET':
#         user_booking_detail = Booking.objects.filter(Q(user_id=pk)& ~Q(booking_status='CANCEL'))
#         serializer = BookingSerialzers(user_booking_detail,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     elif requset.method == 'PATCH':
#         car = Car.objects.get(pk=requset.data['car'])
#         available_cars = car.available_cars
#         if available_cars > 0:
#             booking = BookingSerialzers(data=requset.data)
#             booking.is_valid(raise_exception=True)
#             booking.save()
#             car.available_cars = car.available_cars - 1
#             car.save()
#             return Response(booking.data,status=status.HTTP_201_CREATED)
#         else:
#             ic(requset.data)
#             issue_date = requset.data['issue_date']
#             return_date = requset.data['return_date']
#             car_id = requset.data['car']
#             user_id = requset.data['user']
#             ic(issue_date,return_date,car_id,user_id)
#             return Response('Car is not available let me write that logic to handle this part.')
        
# @api_view()
# def cancel_booking(request,pk):
#     """_summary_
#     Here we are passing the booking id.
#     Args:
#         request (_type_): _description_
#         pk (_type_): _description_
#     """
#     if request.method =='GET':
#         ic(pk)
#         booked_car = Booking.objects.get(pk=pk)
#         ic(booked_car)
#         Booking.objects.filter(pk=pk).update(booking_status='CANCEL')
#         car_id = booked_car.car.id
#         # booked_car.booking_status = 'CANCEL'
#         # booked_car.save()
#         car = Car.objects.get(pk=car_id)
#         if booked_car.booking_status!='CANCEL' and len(car.booking_queue)>0:
#             booked_car.booking_status = 'CANCEL'
#             ic(car.available_cars)
#             car.available_cars = car.available_cars + 1
#             booked_car.save()
#             car_booking = car.booking_queue.pop(0)
#             serialize = BookingSerialzers(data=car_booking)
#             serialize.is_valid(raise_exception=True)
#             serialize.save()
#             car.available_cars = car.available_cars -1
#             car.save()
#             ic(car.available_cars)
#             return Response('Cancel The Normal booking and the element from booking queue is added to booking record',status=status.HTTP_200_OK)
#         elif booked_car.booking_status!='CANCEL':
#             booked_car.booking_status = 'CANCEL'
#             car.available_cars = car.available_cars + 1
#             booked_car.save()
#             car.save()
#             return Response("This is Normal Cancel when there is no advance booking",status=status.HTTP_200_OK)
#         else:
#             return Response("No Such Booking Entry Present",status=status.HTTP_200_OK)

# @api_view(['GET','POST'])
# def extend_booking(request,pk):
#     if request.method == 'GET':
#         user_booking = Booking.objects.filter(user=pk)
#         serialize = BookingSerialzers(user_booking,many=True) 
#         return Response(serialize.data,status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         return Response(request.data,status=status.HTTP_200_OK)
    

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
    car = Car.objects.get(pk=pk)
    if car.available_cars>0:
        serialize = AvailableCarSerializers(car)
        return Response(serialize.data,status=status.HTTP_200_OK)
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
        booking = Booking.objects.filter(pk=pk1)
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

def str_time(date):
    format = '%Y-%m-%d'
    return datetime.strptime(date,format)

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
        # car1 = Car.objects.filter(available_cars__gt=0)
        available_cars.extend(queryset)
        car2 = Car.objects.filter(available_cars=0)
        for x in car2:
            bookings = Booking.objects.filter(car_id=x.id)
            for booking in bookings:
                if (issue_date<booking.issue_date and return_date < booking.issue_date) or (issue_date>booking.return_date and return_date>booking.return_date):
                    car_available=True
                else:
                    car_available = False
                if car_available:
                    if x not in available_cars:
                        available_cars.append(x) 
        serialize = AvailableCarSerializers(available_cars,many=True)
        return Response(serialize.data)


@api_view(['GET','POST'])
def extend_user_booking(request,pk,pk1):
    if request.method == 'GET':
        userbooking = Booking.objects.filter(pk=pk1)
        ic(userbooking)
        serialize = BookingSerializers(userbooking,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        issue_date = str_time(request.data['issue_date'])
        return_date = str_time(request.data['return_date'])
        ic(issue_date,return_date)
        return Response('OK')

