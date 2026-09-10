from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="character-search"),
    path("character/<int:character_id>/", views.character_detail, name="character-detail"),
    path("character/<int:character_id>/image/", views.character_image, name="character-image"),
    path("character/<int:character_id>/favorite/", views.toggle_favorite, name="toggle-favorite"),
    path("character/create/", views.character_create, name="character-create"),
    path("character/<int:character_id>/edit/", views.character_edit, name="character-edit"),
    path("character/<int:character_id>/delete/", views.character_delete, name="character-delete"),
    path("favorites/", views.favorites, name="favorites"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
]
