from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.shortcuts import reverse


# Custom User model with organiser and agent roles
class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


# A UserProfile model linked to the User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Lead model representing the lead details, with organisation reference
class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    # Organisation references UserProfile, must be set during creation
    organisation = models.ForeignKey(
        UserProfile, null=False, blank=False, on_delete=models.CASCADE
    )
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(
        "category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
    )

    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Agent model, linking agents to a specific organisation
class Agent(models.Model):
    description = models.TextField()
    # User references UserProfile, must be set during creation
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=20)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


# Signal to create a UserProfile whenever a User is created
@receiver(post_save, sender=User)
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance
        )  # Use get_or_create to avoid duplicates
