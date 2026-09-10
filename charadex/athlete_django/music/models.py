from django.conf import settings
from django.db import models
class Character(models.Model):
    UNIVERSE_CHOICES = [(value, value) for value in ("Marvel", "DC", "Disney", "Anime", "Cartoon", "Brainrot", "Original")]
    TYPE_CHOICES = [(value, value) for value in ("Hero", "Villain", "Antihero", "Sidekick", "Creature", "Original")]
    GENDER_CHOICES = [(value, value) for value in ("Female", "Male", "Non-binary", "Unknown")]

    name = models.CharField(max_length=150)
    universe = models.CharField(max_length=30, choices=UNIVERSE_CHOICES)
    character_type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name="character type")
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="Unknown")
    real_name = models.CharField(max_length=150, blank=True)
    power = models.TextField()
    weakness = models.TextField()
    personality = models.TextField()
    description = models.TextField()
    image_data = models.BinaryField(blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True)
    image_content_type = models.CharField(max_length=100, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_characters", null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="character_favorites")
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "character"], name="unique_user_character_favorite")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.character.name}"
