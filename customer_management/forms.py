from django import forms
from .models import Lead, Agent
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()

# User registration form using the built-in UserCreationForm
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )
        field_classes = {
            "username": UsernameField,
        }


# Lead form that dynamically pulls the available agents
class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "age",
            "agent",
        )


# Agent form to create or update agent profiles
class AgentModelForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = (
            "user",
            "organisation",
        )
