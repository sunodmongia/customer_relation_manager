from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *
from . import views
from .category import *


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home/", HomeView.as_view(), name="home"),
    # urls for leads
    path("lead/lead_list/", LeadListView.as_view(), name="lead_list"),
    path("lead/<int:pk>/", LeadDetailView.as_view(), name="lead_detail"),
    path("lead/<int:pk>/update/", LeadUpdateView.as_view(), name="lead_detail_update"),
    path("lead/<int:pk>/assign_agent/", AssignAgentView.as_view(), name="assign_agent"),
    path("lead/<int:pk>/delete/", LeadDeleteView.as_view(), name="delete_lead"),
    path("lead/register_lead/", LeadCreateView.as_view(), name="register_lead"),
    # urls for agents
    path("agent/agent_list/", AgentListView.as_view(), name="agent_list"),
    path("agent/<int:pk>/", AgentDetailView.as_view(), name="agent_detail"),
    path("<int:pk>/update/", AgentUpdateView.as_view(), name="agent_detail_update"),
    path("<int:pk>/delete/", AgentDeleteView.as_view(), name="agent_delete"),
    path("register_agent/", AgentCreateView.as_view(), name="register_agent"),
    # Category of leads and agents
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path(
        "category/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category_detail_update",
    ),
    # urls for login, logout and sign up
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
