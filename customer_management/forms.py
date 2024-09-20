from django import forms
from .models import Lead, Agent
from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
        ]
    

    field_classes ={'username': UsernameField}

class LeadModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=0)
    # agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    class Meta:
        model = Lead
        fields = ("first_name", "last_name", "age", "agent")
