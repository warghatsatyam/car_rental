from django.urls import path
from car_rental_app import views
urlpatterns = [
    path('car/',views.car,name='car'),
    path('available-car/',views.available_car,name='available_car'),
    path('available-car/<int:pk>/',views.particular_car,name='particular-car'),
    path('filtered-car/',views.filtered_car,name='filtered-car'),
    path('booking/<int:pk>',views.particular_user_booking,name='particular_user_booking'), 
    path('booking/cancel/<int:pk>',views.cancel_booking,name='cancel-booking'),
    path('booking/extend-booking/<int:pk>',views.extend_booking,name='extend-booking')
]
