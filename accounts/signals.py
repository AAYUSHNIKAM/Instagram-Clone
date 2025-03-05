from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from posts.models import Profile  # Profile is in the posts app

User = get_user_model()  # Ensure you're using the correct User model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
