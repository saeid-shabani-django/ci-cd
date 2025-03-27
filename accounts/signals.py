from .models import CustomUser, Profile
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=CustomUser)
def save_profile_automatically(sender, **kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")
    if created:
        profile = Profile(user=instance)
        profile.save()
