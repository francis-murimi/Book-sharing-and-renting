from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from profiles.models import Profile
from library.models import Book, Kitabu
from . models import Booking
from .forms import BookingProcessForm, DateForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime,timedelta,date
import pytz

@login_required(login_url='/api/v1/rest-auth/login/')
def start_booking(request,slug):
    # show the detail of a book
    book = get_object_or_404(Book,slug=slug)
    profile = get_object_or_404(Profile, user=request.user)
    p = Profile.objects.filter(user=request.user).count()
    if p ==1 and profile.location ==1:
        vitabu = Kitabu.objects.filter(book=book,available=True)
        v_number = vitabu.count()
        if v_number >=1:
            booking = Booking(
                user = request.user,
                book = book,
                kitabu = vitabu[0],
            )
            booking.save()
            kitabu = vitabu[0]
            kitabu.available = False
            kitabu.save() 
        else:
            return HttpResponse('Try again later. The book is not available.')
            #return redirect('library:book_list')
        context = {'book':book,'kitabu':kitabu,'booking':booking,}
        template = loader.get_template('booking/booking.html')
        return HttpResponse(template.render(context,request))
    else:
        return HttpResponse('Update your profile.')

@login_required(login_url='/api/v1/rest-auth/login/')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    template = loader.get_template('booking/bookings.html')
    context = {'bookings':bookings,}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/api/v1/rest-auth/login/')
def booking_detail(request,id):
    booking = get_object_or_404(Booking,id=id)
    context = {'booking':booking,}
    template = loader.get_template('booking/booking_detail.html')
    return HttpResponse(template.render(context,request))

@staff_member_required()
def bookings_list(request):
    bookings = Booking.objects.filter(returned_state=False)
    context = {'bookings':bookings,}
    template = loader.get_template('booking/bookings_list.html')
    return HttpResponse(template.render(context,request))

@staff_member_required()
def process_booking(request,id):
    booking = get_object_or_404(Booking,id=id)
    if request.method == 'POST':
        form = BookingProcessForm(request.POST,request.FILES,instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking:booking_change',id=booking.id)
        #return redirect('blog:blog_detail',id=aa,slug=ss)
    else:
        form = BookingProcessForm(instance=booking)
        #date_form = DateForm()
    template = loader.get_template('booking/process_booking.html')
    context = {'form':form,'booking':booking}
    return HttpResponse(template.render(context,request)) 

def booking_change(request,id):
    booking = get_object_or_404(Booking,id=id)
    r_status = booking.returned_state
    kitabu = booking.kitabu
    reader = booking.user
    if r_status == True:
        kitabu.available = True
        kitabu.readers.add(reader)
        kitabu.save()

    d_state = booking.delivered_state
    if d_state == True and r_status== False:  
        kitabu.current_reader = reader
        kitabu.save()
    else:
        kitabu.current_reader = None
        kitabu.save()

    tarehe = booking.delivery_date 
    if tarehe == None:
        return redirect('booking:bookings_list')
    else:
        duration = booking.duration 
        b_type = booking.booking_type
        kitabu = booking.kitabu
        if b_type == 0:
            r_date = tarehe + timedelta(days=duration)
            booking.return_date = r_date
            kitabu.return_date = r_date
            kitabu.save()
            booking.save()
            
        elif b_type == 1:
            r_date = tarehe + timedelta(weeks=duration)
            booking.return_date = r_date
            kitabu.return_date = r_date
            kitabu.save()
            booking.save()
        elif b_type == 2:
            r_date = tarehe + timedelta(weeks=duration * 4)
            booking.return_date = r_date
            kitabu.return_date = r_date
            kitabu.save()
            booking.save()
        return redirect('booking:bookings_list')
