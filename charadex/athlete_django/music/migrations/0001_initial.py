from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Character",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("universe", models.CharField(choices=[("Marvel", "Marvel"), ("DC", "DC"), ("Disney", "Disney"), ("Anime", "Anime"), ("Cartoon", "Cartoon"), ("Brainrot", "Brainrot"), ("Original", "Original")], max_length=30)),
                ("character_type", models.CharField(choices=[("Hero", "Hero"), ("Villain", "Villain"), ("Antihero", "Antihero"), ("Sidekick", "Sidekick"), ("Creature", "Creature"), ("Original", "Original")], max_length=30, verbose_name="character type")),
                ("gender", models.CharField(choices=[("Female", "Female"), ("Male", "Male"), ("Non-binary", "Non-binary"), ("Unknown", "Unknown")], default="Unknown", max_length=20)),
                ("real_name", models.CharField(blank=True, max_length=150)),
                ("power", models.TextField()),
                ("weakness", models.TextField()),
                ("personality", models.TextField()),
                ("description", models.TextField()),
                ("image_data", models.BinaryField(blank=True, null=True)),
                ("image_name", models.CharField(blank=True, max_length=255)),
                ("image_content_type", models.CharField(blank=True, max_length=100)),
                ("creator", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="created_characters", to=settings.AUTH_USER_MODEL)),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at", "name"]},
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="character_favorites", to=settings.AUTH_USER_MODEL)),
                ("character", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorited_by", to="music.character")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(fields=("user", "character"), name="unique_user_character_favorite"),
        ),
    ]
