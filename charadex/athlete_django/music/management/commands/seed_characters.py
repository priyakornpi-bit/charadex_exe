from django.core.management.base import BaseCommand

from music.models import Character


CHARACTERS = [
    ("Spider-Man", "Marvel", "Hero", "Male", "Peter Parker", "Spider-sense, web projection, agility", "His loved ones can be targeted", "Witty and responsible", "A young hero balancing city life with a promise to help others."),
    ("Wonder Woman", "DC", "Hero", "Female", "Diana Prince", "Super strength, flight, combat mastery", "Magic can pierce her defenses", "Compassionate and fearless", "An Amazon champion standing for truth and justice."),
    ("Mickey Mouse", "Disney", "Creature", "Male", "Mickey Mouse", "Optimism, cartoon resilience", "Mischief can distract him", "Cheerful and curious", "A classic icon whose optimism turns every problem into an adventure."),
    ("Sailor Moon", "Anime", "Hero", "Female", "Usagi Tsukino", "Moon magic, healing, cosmic power", "Doubt can weaken her focus", "Kind and determined", "A guardian who protects the world through friendship and courage."),
]


class Command(BaseCommand):
    help = "Seed CHARADEX with demo character records."

    def handle(self, *args, **options):
        for name, universe, character_type, gender, real_name, power, weakness, personality, description in CHARACTERS:
            Character.objects.update_or_create(name=name, defaults={"universe": universe, "character_type": character_type, "gender": gender, "real_name": real_name, "power": power, "weakness": weakness, "personality": personality, "description": description, "is_featured": True})
        self.stdout.write(self.style.SUCCESS(f"CHARADEX seeded with {len(CHARACTERS)} characters."))