from django.shortcuts import render, redirect, get_object_or_404
from .models import Poster, Author
from .forms import PosterForm

# Create your views here.


def index(request):
    '''
    Obtains all Poster and Author objects and renders the 'index.html'
    template with the instances.
    '''
    posters = Poster.objects.all()
    authors = Author.objects.all()
    return render(request, "index.html",
                  {"posters": posters, "authors": authors})


def add_poster(request):
    '''
    Checks if the request method is POST.

    If it is GET:
    Retrieves the PosterForm form, and renders the 'add_poster.html'
    template with the form fields.

    If it is POST:
    Checks the form fields have valid inputs, and if so saves the form
    data, and updates the databases. Then returns the 'index.html'
    template.
    '''
    if request.method == "POST":
        form = PosterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = PosterForm()
    return render(request, "add_poster.html", {"form": form})


def view_poster(request, poster_id):
    '''
    Retrieves a unique Poster instance with its ID, and renders the
    'view_poster.html' template with the instance data. 
    '''
    poster = get_object_or_404(Poster, id=poster_id)
    return render(request, "view_poster.html", context={"poster": poster})


def edit_poster(request, poster_id):
    '''
    Checks if the Poster instance with that ID exists. If it does,
    retrieve instance data. Else, return 404 error.
    
    Then, checks the request method is POST.

    If it is GET:
    Retrieves the PosterForm form and Poster instance data, and renders
    the 'edit_poster.html' template with the form fields pre-filled.

    If it is POST:
    Retrieves the PosterForm form and Poster instance data. Check the
    updated form fields have valid inputs, and if so saves the form
    data and updates the databases. Then returns the 'index.html'
    template.
    '''
    poster = get_object_or_404(Poster, id=poster_id)

    if request.method == "POST":
        form = PosterForm(request.POST, instance=poster)
        if form.is_valid():
            edited_poster = form.save()
            return redirect("view_poster", poster_id=edited_poster.id)
        else:
            print(form.errors)

    form = PosterForm(instance=poster)
    return render(request, "edit_poster.html",
                  context={"form": form,
                           "poster": poster})


def delete_poster(request, poster_id):
    '''
    Checks if the Poster instance with that ID exists. If it does,
    retrieve instance data. Else, return 404 error.

    Then, render the 'delete_poster.html' template with the poster
    instance data.
    '''
    poster = get_object_or_404(Poster, id=poster_id)
    return render(request, "delete_poster.html", context={"poster": poster})


def poster_deleted(request, poster_id):
    '''
    Checks if the Poster instance with that ID exists. If it does,
    retrieve instance data. Else, return 404 error.

    Then, checks the request method is POST.

    If it is GET:
    Renders the 'view_poster.html' template with the poster instance
    data.

    If it is POST:
    Deletes the poster instance from the database, and then redirects
    to the 'index.html' template.
    '''
    poster = get_object_or_404(Poster, id=poster_id)
    if request.method == "POST":
        poster.delete()
        return redirect("index")
    return render(request, "view_poster.html", context={"poster": poster})


def filter_author(request):
    '''
    Retrieves both the author ID and form submit data from the GET
    parameters in the request data.

    If request is 'filter':
    Checks if the author ID exists, and if it does it retrieves all
    poster objects from that author.
    If it doesn't, retrieve all poster objects and author objects,
    and render the 'index.html' template with all objects data..

    If request is 'delete':
    Checks if the author ID exists, then if it does retrieves the
    Author instance. It then renders the 'delete.html' template with
    the author ID.
    If the ID doesn't exist, it retrieves all poster and author
    objects, and renders the 'index.html' template with all the
    retrieved data.

    '''
    author_id = request.GET.get('author_id')
    action = request.GET.get('action')

    if action == 'filter':
        if author_id:
            posters = Poster.objects.filter(author_id=author_id)
        else:
            posters = Poster.objects.all()
        authors = Author.objects.all()
        return render(request, "index.html",
                      context={"posters": posters,
                               "authors": authors})

    elif action == 'delete':
        if author_id:
            author = get_object_or_404(Author, id=author_id)
            return render(request, "delete_author.html", context={"author": author})
        else:
            authors = Author.objects.all()
            posters = Poster.objects.all()
            return render(request, "index.html",
                          context={"posters": posters,
                                   "authors": authors})


def delete_author(request, author_id):
    '''
    Retrieves the author instance, and if it doesn't exist return a
    404 error. Then, deletes the author from the database.

    Redirect to the 'index.html' template.
    '''
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return redirect('index')

