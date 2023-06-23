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
    try:
        if request.method == 'GET':
            return Response("Add Car",status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serialze = CarSerializers(data=request.data)
            serialze.is_valid(raise_exception=True)
            serialze.save()
            return Response(serialze.data,status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def getavailablecar(request):
    if request.method == 'GET':
        car = Car.objects.filter(available_cars__gt=0)
        serialize = AvailableCarSerializers(car,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        try:
            car = Car.objects.get(pk=request.data['car'])
            if car.available_cars>0:
                serialize = BookingSerializers(data=request.data)
                serialize.is_valid(raise_exception=True)
                serialize.save()
                car.available_cars = car.available_cars -1
                car.save()
                return Response(serialize.data,status=status.HTTP_201_CREATED)
            else:
                return Response("Car is not available",status=status.HTTP_404_NOT_FOUND)
        except Car.DoesNotExist:
            return Response("Car is not available",status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
            # else:
            # return Response("Car is not available",status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view()
def get_particular_car(request,pk):
    try:
        car = Car.objects.get(pk=pk)
        if car.available_cars>0:
            serialize = AvailableCarSerializers(car)
        else:
            booking = Booking.objects.filter(car=car.id)
            serialize = BookingSerializers(booking,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)
    except Car.DoesNotExist:
        return Response("Car Not Found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    

@api_view()
def userbookingdetail(request,pk):
    if request.method == 'GET':
        try:    
            userbookings = Booking.objects.filter(user_id=pk)
            if not userbookings:
                return Response("User Does Not Exist",status=status.HTTP_404_NOT_FOUND)
            serializer = BookingSerializers(userbookings,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def cancelBooking(request,pk):
    if request.method == 'GET':
        try:
            target_booking = Booking.objects.get(pk=pk)
            if target_booking.booking_status == 'Cancel':
                return Response("No Such Booking",status=status.HTTP_204_NO_CONTENT)
            else:
                target_booking.booking_status = 'Cancel'
                target_booking.save()
                car_id = target_booking.car.id
                booked_car = Car.objects.get(pk=car_id)
                booked_car.available_cars +=1
                booked_car.save()
                return Response("Booking Cancelled",status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response("No such Booking Found",status=status.HTTP_204_NO_CONTENT)

def str_time(date):  # sourcery skip: avoid-builtin-shadow
    format = '%Y-%m-%d'
    return datetime.strptime(date,format).date()

@api_view(['GET','POST'])
def filter_available_car(request):
    if request.method == 'GET':
        ic(request.query_params)
        if 'issue_date' in request.query_params:
            issue_date = request.query_params['issue_date']
        else:
            issue_date = False
        if 'return_date' in request.query_params:
            return_date = request.query_params['return_date']
        else:
            return_date = False
        car_name = request.GET.get('car_name')
        car_model = request.GET.get('car_model')
        seat_capacity = request.GET.get('seat_capacity')
        per_day_price = request.GET.get('per_day_price')
        available_cars = []
        queryset = Car.objects.filter(Q(available_cars__gt=0)|Q(car_name=car_name)|Q(car_model=car_model)|Q(seat_capacity=seat_capacity)|Q(per_day_price=per_day_price))
        available_cars.extend(queryset)
        car2 = Car.objects.filter(available_cars=0)
        ic(car2)
        # if issue_date and return_date:
        #     for x in car2:
        #         bookings = Booking.objects.filter(car_id=x.id).order_by('issue_date')
        #         for booking in bookings:
        #             car_available = (
        #                 issue_date < booking.issue_date
        #                 and return_date < booking.issue_date
        #             ) or (
        #                 issue_date > booking.return_date
        #                 and return_date > booking.return_date
        #             )
        #             if car_available and (x not in available_cars):
        #                 available_cars.append(x)
        if issue_date and return_date:
            for x in car2:
                user_date_greater_than_all_booking = Booking.objects.filter(Q(car_id = x.id),Q(return_date__lt=issue_date),Q(return_date__lt=return_date))
                user_date_lesser_than_all_booking = Booking.objects.filter(Q(car_id=x.id),Q(issue_date__gt=issue_date),Q(issue_date__gt=return_date))
                ic(user_date_greater_than_all_booking,user_date_lesser_than_all_booking)
        serialize = AvailableCarSerializers(available_cars,many=True)
        return Response(serialize.data)

    if request.method == 'POST':
        car_id = request.data['car']
        car = Car.objects.get(pk=car_id)
        serializer = BookingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        car_availablity = car.available_cars
        if car_availablity>0:
            car.available_cars = car.available_cars -1
            car.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['GET','PUT'])
def extend_user_booking(request,pk):
    if request.method == 'GET':
        try:
            userbooking = Booking.objects.filter(pk=pk)
            serialize = BookingSerializers(userbooking,many=True)
            return Response(serialize.data,status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response('Booking Does not Exists',status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e),status= status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'PUT':
        try:    
            booking_id = request.data['id']
            booking = Booking.objects.get(pk=booking_id)
            return_date = str_time(request.data['return_date'])
            response = booking.get_booking_detail(booking,return_date)
            booking = Booking.objects.get(pk=booking_id)
            booking_serializer = BookingSerializers(booking)
            if response:
                return Response(booking_serializer.data,status=status.HTTP_200_OK)
            return Response("Cannot Extend",status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Booking.DoesNotExist:
            return Response("Booking Does not exists",status=status.HTTP_404_NOT_FOUND)
        
        


