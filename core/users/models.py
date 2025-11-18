# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    class Roles(models.TextChoices):
        SUPER_REVIEWER = ('super_reviewer', 'Program Super User')
        AUDITOR = ('auditor', 'Auditor')
        VIEWER = ('viewer', 'Viewer')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=32, choices=Roles.choices, default=Roles.VIEWER)
    # Add other user metadata fields as needed (avatar, bio, etc.)

    def __str__(self):
        return self.display_name or self.user.username

    @property
    def is_program_super_user(self):
        return self.role == self.Roles.SUPER_REVIEWER

    @property
    def is_auditor(self):
        return self.role == self.Roles.AUDITOR

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Exception:
            pass
