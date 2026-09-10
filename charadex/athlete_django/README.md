# CHARADEX

CHARADEX is a practical Django character database for discovering, filtering, favoriting, and creating characters across Marvel, DC, Disney, Anime, Cartoon, Brainrot, and Original universes.

## Features

- Search by character name, real name, or power
- Filter by universe, character type, and gender
- Character detail pages with database-stored image uploads
- Register, log in, log out, and manage a profile
- Create, edit, and delete characters you own
- Save and remove personal favorites
- Django admin with PostgreSQL support

## Run locally

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_characters
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Create an admin account with `python manage.py createsuperuser`, then visit `/admin/`.

## Main URLs

- `/` - explore the archive
- `/search/` - search and filter characters
- `/character/create/` - create a character
- `/favorites/` - saved characters
- `/profile/` - account and character collection
- `/login/`, `/register/`, `/logout/` - authentication
- `/admin/` - database administration
