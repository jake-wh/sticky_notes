from django.urls import path
from . import views

urlpatterns = [

    # Index page displaying all posters
    path("", views.index, name="index"),

    # Page to create a poster
    path("add/", views.add_poster, name="add_poster"),

    # Page to view a specific poster by its ID
    path("poster/<int:poster_id>/", views.view_poster, name="view_poster"),

    # Page to edit a specific poster by its ID
    path("edit/<int:poster_id>/", views.edit_poster, name="edit_poster"),

    # Page to deletion of a specific poster by its ID
    path("confirm_delete/<int:poster_id>/", views.delete_poster, name="delete_poster"),

    # Page to delete a specific poster by its ID
    path("deleted/<int:poster_id>/", views.poster_deleted, name="poster_deleted"),

    # Filter posters by author
    path("author/", views.filter_author, name="filter_author"),

    # Delete specific author by their ID
    path("delete_author/<int:author_id>/", views.delete_author, name="delete_author"),
]
