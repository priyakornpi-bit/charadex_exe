from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CharacterForm
from .models import Character, Favorite


def home(request):
    characters = Character.objects.all()
    query = (request.GET.get("q") or "").strip()
    universe = (request.GET.get("universe") or "").strip()
    if query:
        characters = characters.filter(
            Q(name__icontains=query) | Q(real_name__icontains=query) | Q(power__icontains=query)
        )
    if universe:
        characters = characters.filter(universe=universe)
    popular = Character.objects.filter(is_featured=True)[:6]
    latest = Character.objects.order_by("-created_at")[:6]
    universes = [choice[0] for choice in Character.UNIVERSE_CHOICES]
    return render(
        request,
        "music/home.html",
        {
            "characters": characters[:24],
            "popular": popular,
            "latest": latest,
            "universes": universes,
            "query": query,
            "universe": universe,
        },
    )


def search(request):
    query = (request.GET.get("q") or "").strip()
    universe = (request.GET.get("universe") or "").strip()
    character_type = (request.GET.get("type") or "").strip()
    gender = (request.GET.get("gender") or "").strip()
    results = Character.objects.all()
    if query:
        results = results.filter(Q(name__icontains=query) | Q(real_name__icontains=query) | Q(power__icontains=query))
    if universe: results = results.filter(universe=universe)
    if character_type: results = results.filter(character_type=character_type)
    if gender: results = results.filter(gender=gender)

    return render(
        request,
        "music/search.html",
        {"query": query, "results": results, "searched": bool(query or universe or character_type or gender), "count": results.count(), "universes": Character.UNIVERSE_CHOICES, "types": Character.TYPE_CHOICES, "genders": Character.GENDER_CHOICES},
    )


def character_detail(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    liked = request.user.is_authenticated and Favorite.objects.filter(user=request.user, character=character).exists()
    return render(request, "music/character_detail.html", {"character": character, "liked": liked})


def character_image(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    if not character.image_data:
        return HttpResponse(status=404)
    return HttpResponse(character.image_data, content_type=character.image_content_type or "image/jpeg")


@login_required
def toggle_favorite(request, character_id):
    if request.method != "POST":
        return redirect("character-detail", character_id=character_id)
    character = get_object_or_404(Character, pk=character_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, character=character)
    if created:
        messages.success(request, f"{character.name} was added to My Favorites.")
    else:
        favorite.delete()
        messages.info(request, f"{character.name} was removed from My Favorites.")
    return redirect("character-detail", character_id=character_id)


@login_required
def favorites(request):
    favorite_rows = Favorite.objects.filter(user=request.user).select_related("character")
    return render(request, "music/favorites.html", {"favorites": favorite_rows})


@login_required
def profile(request):
    return render(request, "music/profile.html", {"characters": Character.objects.filter(creator=request.user), "favorites": Favorite.objects.filter(user=request.user).select_related("character")})


@login_required
def character_create(request):
    form = CharacterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        character = form.save(commit=False)
        character.creator = request.user
        character.save()
        messages.success(request, "Character added to the archive.")
        return redirect("character-detail", character_id=character.id)
    return render(request, "music/character_form.html", {"form": form, "heading": "Create character"})


@login_required
def character_edit(request, character_id):
    character = get_object_or_404(Character, pk=character_id, creator=request.user)
    form = CharacterForm(request.POST or None, request.FILES or None, instance=character)
    if form.is_valid():
        form.save()
        messages.success(request, "Character record updated.")
        return redirect("character-detail", character_id=character.id)
    return render(request, "music/character_form.html", {"form": form, "heading": "Edit character", "character": character})


@login_required
def character_delete(request, character_id):
    character = get_object_or_404(Character, pk=character_id, creator=request.user)
    if request.method == "POST":
        character.delete()
        messages.success(request, "Character removed from the archive.")
        return redirect("home")
    return render(request, "music/character_confirm_delete.html", {"character": character})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back to CHARADEX.")
            return redirect(request.GET.get("next") or "home")
        messages.error(request, "Invalid username or password.")
    return render(request, "music/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        if not username or not password:
            messages.error(request, "Username and password are required.")
        elif password != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "That username is already taken.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Your CHARADEX account is ready.")
            return redirect("home")
    return render(request, "music/register.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")
