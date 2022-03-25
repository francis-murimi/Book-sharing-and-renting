from django.contrib import admin
from.models import Genre, Author, Book, Kitabu, BookReview

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Kitabu)

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book','writer']
admin.site.register(BookReview,BookReviewAdmin)
