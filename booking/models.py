import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from library.models import Book, Kitabu
from django.urls import reverse

class Booking(models.Model):
    BOOKING_CHOICE = (
        (0,"DAILY"),
        (1,"WEEKLY"),
        (2,"MONTHLY"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    book = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    kitabu = models.ForeignKey(Kitabu,on_delete=models.SET_NULL,null=True, blank=True)
    booking_type = models.IntegerField(choices=BOOKING_CHOICE, default=1)
    duration = models.IntegerField(blank=True,null=True)
    payed = models.BooleanField(default= False)
    delivered_state = models.BooleanField(default= False)
    returned_state = models.BooleanField(default= False)
    booking_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(auto_now_add=False, blank=True,null=True) 
    return_date = models.DateField(auto_now_add= False, blank=True,null=True)
    
    class Meta:
        ordering = ['-booking_date']
    def __str__(self):
        return self.user.username
    def get_booking_url(self):
        return reverse('booking:booking_detail',args=[self.id])
    def get_booking_detail(self):
        return reverse('booking:process_booking',args=[self.id])
    def clean(self):
        if self.returned_state == True and self.delivered_state == False:
            raise ValidationError(_('You cannot return a book that was not delivered.'))
        if self.return_date is not None and self.duration is None:
            raise ValidationError(_('Duration is required to calculate Return date.'))
        if self.payed == False and self.delivered_state == True: 
            raise ValidationError(_('Payment must be complete for delivery to proceed.'))
        if self.delivered_state == True and self.delivery_date is None:
            self.delivery_date = datetime.date.today()
        if self.delivered_state ==True and self.duration is None:
            raise ValidationError(_('A duration must be given for a delivery to be possible'))

