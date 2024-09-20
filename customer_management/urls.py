from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("lead_list/", LeadListView.as_view(), name="lead_list"),
    path("agent_list/", AgentListView.as_view(), name="agent_list"),
    path("<int:pk>/", LeadDetailView.as_view(), name="lead_detail"),
    path("<int:pk>/update/", LeadUpdateView.as_view(), name="lead_detail_update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="delete_lead"),
    path("register_lead/", LeadCreateView.as_view(), name="register_lead"),
    path("register_agent/", AgentCreateView.as_view(), name="register_agent"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
