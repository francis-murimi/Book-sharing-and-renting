from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=400)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('library:review_list_by_genre',args=[self.name])
    def get_genre_books(self):
        return reverse('library:book_list_by_genre',args=[self.name])

class Author(models.Model):
    name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    def get_author_url(self):
        return reverse('library:author_detail',args=[self.id])

class Book(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150,db_index=True,unique=True)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    pages = models.IntegerField()
    chapters = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)
    def __str__(self):
        return self.title
    def get_book_url(self):
        return reverse('library:book_detail',args=[self.slug])
    def book_booking_url(self):
        return reverse('booking:start_booking',args=[self.slug])
class Kitabu(models.Model):
    # one single book
    CONDITION_STATE = (
        (0,"NEW"),
        (1,"AVERAGE"),
        (2,"OLD"),
        )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bcode = models.CharField(max_length=30, unique=True)
    current_reader = models.ForeignKey(User, on_delete= models.SET_NULL, blank=True, null=True)
    return_date = models.DateField(auto_now_add=False, blank=True, null=True)
    readers = models.ManyToManyField(User, related_name='relatives', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=False)
    condition_state = models.IntegerField(choices=CONDITION_STATE, default=0)
    
    class Meta:
        verbose_name = 'kitabu'
        verbose_name_plural = 'Vitabu'
    def __str__(self):
        return self.bcode

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200,db_index=True,unique=True)
    writer = models.CharField(max_length=30, blank=True)
    content = models.TextField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BookReview, self).save(*args, **kwargs)
    def __str__(self):
        return self.writer
    def get_review_url(self):
        return reverse('library:review_detail',args=[self.id,self.slug])