from django.db import models
from django.contrib.auth.models import User
from library.models import Book, BookReview

class Profile(models.Model):
    OCCUPATION_STATE = (
        (0,"STUDENT"),
        (1,"EMPLOYED"),
        (2,"RETIRED"),
        )
    AGE_SET = (
        (0,"UNDER 18"),
        (1,"18-35"),
        (2,"ABOVE 35")
    )
    CAREFUL_RATE = (
        (0,"GOOD"),
        (1,"AVERAGE"),
        (2,"POOR"),
    )
    LOCATION_CHOICE = (
        (0,"SET LATER"),
        (1,"KUTUS"),
        (2,"KERUGOYA"),
        (3,"KAGUMO"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    occupation = models.IntegerField(choices=OCCUPATION_STATE, default=0)
    age = models.IntegerField(choices=AGE_SET, default=1)
    location = models.IntegerField(choices=LOCATION_CHOICE,default=0)
    read_books = models.ManyToManyField(Book,blank=True)
    caretaker = models.IntegerField(choices=CAREFUL_RATE, default=1)
    def __str__(self):
        return self.user.username

class ReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookreview = models.ForeignKey(BookReview, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class BookComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username