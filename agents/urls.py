from django.urls import path
from .views import AgentListView

app_name = "agents"

urlpatterns = [
    path("agent_list/", AgentListView.as_view(), name="agent_list"),
]
