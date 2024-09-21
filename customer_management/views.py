from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, request
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views import generic
from .models import *
from .forms import *
from .mixin import *
import os
import random
from django.urls import reverse_lazy
from django.conf import settings



# CRUD: Create, Retrieve, Update, Delete.


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context


class LeadListView(OrganiserLoginRequiredMixin, generic.ListView):
    template_name = "lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of lead for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lead List"
        return context


class LeadDetailView(OrganiserLoginRequiredMixin, generic.DetailView):
    template_name = "lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of lead for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Details for {self.object}"
        return context


class LeadCreateView(OrganiserLoginRequiredMixin, generic.CreateView):
    template_name = "register_lead.html"
    form_class = LeadModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create a Lead"
        return context

    def form_valid(self, form):
        # Automatically assign the organisation (assuming the logged-in user is an organiser)
        form.instance.organisation = self.request.user.userprofile  # Ensure user has a UserProfile

        # Send email notification upon successful lead creation
        send_mail(
            subject="New Lead created",
            message=f"Lead created successfully for {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
            from_email=settings.EMAIL_HOST_USER,  # Fetch email from settings instead of os.environ
            recipient_list=[settings.EMAIL_HOST_USER], # Send email to the configured user
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("lead_list")  # Use reverse_lazy for URL resolution


class LeadUpdateView(OrganiserLoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of lead for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update for {self.object}"
        return context

    def get_success_url(self):
        return reverse("lead_list")


class LeadDeleteView(OrganiserLoginRequiredMixin, generic.DeleteView):
    template_name = "lead_delete.html"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of lead for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("lead_list")


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = UserRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign Up"
        return context

    def get_success_url(self):
        return reverse("login")


def logout_view(request):
    logout(request)
    return redirect("login")



# def lead_list(request):
#     leads = Lead.objects.all()
#     return render(request, "lead_list.html", {"": leads})


# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }
#     return render(request, "lead_detail.html", context)


# def register_lead(request):
#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Lead created successfully")
#             return redirect("home")
#     else:
#         form = LeadModelForm()
#     return render(
#         request, "register_lead.html", {"form": form, "title": "Register Lead"}
#     )


# def UpdateLead(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)
#     if request.method == "POST":
#         form = LeadModelForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Lead updated successfully")
#             return redirect("lead_list")
#     return render(
#         request,
#         "lead_update.html",
#         {"form": form, "lead": lead, "title": "Update Record"},
#     )


# def DeleteLead(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("home")
