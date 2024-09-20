from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views import generic
from .models import *
from .forms import *
import os

# CRUD: Create, Retrieve, Update, Delete.


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lead List"
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Details for {self.object}"
        return context


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "register_lead.html"
    form_class = LeadModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Lead"
        return context

    def form_valid(self, form):
        send_mail(
            subject="New Lead created",
            message=(
                f"Respected sir, "
                f"Lead created successfully for {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
            ),
            from_email=os.environ.get("WIRE_APP_EMAIL_USER"),
            recipient_list=[os.environ.get("WIRE_APP_EMAIL_USER")],
        )
        return super(LeadCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("home")


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update for {self.object}"
        return context

    def get_success_url(self):
        return reverse("lead_list")


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()

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


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agent_list.html"
    queryset = Agent.objects.all()
    context_object_name = "agents"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Agent List"
        return context


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "register_agent.html"
    form_class = AgentModelForm

    def form_valid(self, form):
        send_mail(
            subject="New Agent",
            message=f"Agent created successfully for {form.cleaned_data['user']} {form.cleaned_data['organisation']}",
            from_email=os.environ.get("WIRE_APP_EMAIL_USER"),
            recipient_list=[os.environ.get("WIRE_APP_EMAIL_USER")],
        )
        return super(LeadCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("agent_list")

    def form_valid(self, form):
        agent = form.save()
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Agent Create"
        return context


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "agent_detail.html"
    Agent.objects.all()

    def get_queryset(self):
        return Agent.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Details for {self.object}"
        return context


class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agent_update.html"
    queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update for {self.object}"
        return context

    def get_success_url(self):
        return reverse("agent_detail", kwargs={"pk": self.object.pk})


class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "agent_delete.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("agent_list")


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
