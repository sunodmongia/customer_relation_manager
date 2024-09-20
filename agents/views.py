from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views import generic
from customer_management.views import Agent
from django.shortcuts import reverse


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agent_list.html"
    queryset = Agent.objects.all()
    context_object_name = "agents"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Agent List"
        return context

    def get_success_url(self):
        return reverse("home")

    