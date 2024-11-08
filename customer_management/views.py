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
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=True
            )
            context.update({"unassigned_leads": queryset})
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
        form.instance.organisation = (
            self.request.user.userprofile
        )  # Ensure user has a UserProfile

        # Send email notification upon successful lead creation
        send_mail(
            subject="New Lead created",
            message=f"Lead created successfully for {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}",
            from_email=settings.EMAIL_HOST_USER,  # Fetch email from settings instead of os.environ
            recipient_list=[
                settings.EMAIL_HOST_USER
            ],  # Send email to the configured user
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
        return reverse("lead_detail", kwargs={"pk": self.object.pk})


class UpdateLeadStatusView(LoginRequiredMixin, generic.UpdateView):
    template_name = "lead_status_update.html"
    form_class = UpdatestatusForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of lead for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("lead_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update for {self.object}"
        return context


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


class AgentListView(OrganiserLoginRequiredMixin, generic.ListView):
    template_name = "agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Agent List"
        return context


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "register_agent.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agent_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f"{random.randint(1000000, 1000000000)}")
        user.save()
        Agent.objects.create(user=user, organisation=self.request.user.userprofile)
        send_mail(
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            subject="You are invited as an agent",
            message="You were added as an agent in CRM by wire. Change your password and Please login to confirm that it's you",
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create a Agent"
        return context


class AgentDetailView(OrganiserLoginRequiredMixin, generic.DetailView):
    template_name = "agent_detail.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Details for {self.object}"
        return context


class AgentUpdateView(OrganiserLoginRequiredMixin, generic.UpdateView):
    template_name = "agent_update.html"
    form_class = AgentModelForm

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Agent.objects.filter(organisation=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update for {self.object}"
        return context

    def get_success_url(self):
        return reverse("agent_detail", kwargs={"pk": self.object.pk})


class AgentDeleteView(OrganiserLoginRequiredMixin, generic.DeleteView):
    template_name = "agent_delete.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse("agent_list")


class UpdateAgentStatusView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agent_status_update.html"
    form_class = UpdateAgentStatusForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of lead for the entire organisation
        return Agent.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("agent_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Update for {self.object}"
        return context


class AssignAgentView(OrganiserLoginRequiredMixin, generic.FormView):
    template_name = "assign_agent.html"
    form_class = AgentAssignForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return reverse("lead_list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(OrganiserLoginRequiredMixin, generic.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of lead for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)

        context.update(
            {
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
                "assigned_lead_count": queryset.filter(category__isnull=False).count(),
            }
        )
        context["title"] = "Category List"
        return context


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "category_detail.html"
    context_object_name = "category_detail"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of lead for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()
        context.update({"leads": leads})
        context["title"] = "Category Details"
        return context


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "category_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("lead_list")


"""
There is function based created views
"""

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
