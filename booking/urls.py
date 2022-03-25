from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [
    path('start/<slug>/',views.start_booking,name='start_booking'),
    path('my-bookings/',views.my_bookings,name='my_bookings'),
    path('booking/<int:id>/',views.booking_detail,name='booking_detail'),
    path('list/',views.bookings_list,name='bookings_list'),
    path('process/<int:id>/',views.process_booking,name='process_booking'),
    path('change/<int:id>/',views.booking_change,name='booking_change'),
]