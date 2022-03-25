from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Genre, Author,Book,BookReview
from profiles.models import ReviewComment, BookComment
from profiles.forms import ReviewCommentForm,BookCommentForm


def review_list(request, genre_name=None):
    # get the list of all book reviews.
    template = loader.get_template('library/list.html')
    genre = None
    genres = Genre.objects.all()
    reviews = BookReview.objects.all()
    if genre_name:
        genre = get_object_or_404(Genre,name=genre_name)
        reviews = BookReview.objects.filter(book__genre= genre)
    
    context = {'genre':genre,
                'genres':genres,
                'reviews':reviews,}
    return HttpResponse(template.render(context,request))

def review_detail(request, id, slug):
    # show the detail of an individual review.
    template = loader.get_template('library/detail.html')
    review = get_object_or_404(BookReview,id=id,slug=slug)
    
    comments = ReviewComment.objects.filter(bookreview= review )
    new_comment = None
    # Comment posted
    if request.method == 'POST': 
        comment_form = ReviewCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.bookreview = review
            new_comment.user = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = ReviewCommentForm()
    
    context = {'review':review, 'comments':comments, 'comment_form':comment_form}
    
    return HttpResponse(template.render(context,request))

def book_detail(request, slug):
    # show the detail of a book
    template = loader.get_template('library/book.html')
    book = get_object_or_404(Book,slug=slug)
    
    comments = BookComment.objects.filter(book= book )
    new_comment = None
    # Comment posted
    if request.method == 'POST': 
        comment_form = BookCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.book = book
            new_comment.user = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = BookCommentForm()
    
    context = {'book':book, 'comments':comments, 'comment_form':comment_form}
    
    return HttpResponse(template.render(context,request))

def book_list(request,genre_name=None):
    # get the list of all book reviews.
    template = loader.get_template('library/book_list.html')
    genre = None
    genres = Genre.objects.all()
    books = Book.objects.all()
    if genre_name:
        genre = get_object_or_404(Genre,name=genre_name)
        books = Book.objects.filter(genre= genre)
    
    context = {'genre':genre,
                'genres':genres,
                'books':books,}
    return HttpResponse(template.render(context,request))
    

def author_detail(request, id):
    # show the detail of an author
    template = loader.get_template('library/author.html')
    author = get_object_or_404(Author,id=id)
    books = Book.objects.filter(author=author)
    context = {'author':author, 'books':books}
    
    return HttpResponse(template.render(context,request))