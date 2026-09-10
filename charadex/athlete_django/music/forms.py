from django import forms

from .models import Character


class CharacterForm(forms.ModelForm):
    image = forms.FileField(required=False, label="Character image")

    class Meta:
        model = Character
        fields = [
            "name", "universe", "character_type", "gender", "real_name",
            "power", "weakness", "personality", "description",
        ]
        widgets = {
            "power": forms.Textarea(attrs={"rows": 3}),
            "weakness": forms.Textarea(attrs={"rows": 3}),
            "personality": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image must be 5 MB or smaller.")
        return image

    def save(self, commit=True):
        character = super().save(commit=False)
        image = self.cleaned_data.get("image")
        if image:
            character.image_data = image.read()
            character.image_name = image.name
            character.image_content_type = image.content_type or "application/octet-stream"
        if commit:
            character.save()
            self.save_m2m()
        return character