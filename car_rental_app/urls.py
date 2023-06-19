from django.urls import path
from car_rental_app import views

urlpatterns = [
    path('car/',views.add_car,name='car'),
    path('available-car/',views.getavailablecar,name='available-car'),
    path('car/<int:pk>/',views.get_particular_car,name='get-car'),
    path('userbooking/<int:pk>/',views.userbookingdetail,name='userbookingdetail'),
   # path('userbooking/<int:pk>/<int:pk1>',views.extend_user_booking,name='userbookingdetail'),
    path('userbooking/cancel/<int:pk>/',views.cancelbooking,name='userbookingdetail'),
    path('filter-available-car/',views.filter_available_car,name='filter-car'),
    path('userbooking/extend/<int:pk>',views.extend_user_booking,name='extend_user_booking'),
]
