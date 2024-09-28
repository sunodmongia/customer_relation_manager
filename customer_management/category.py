from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import *
from .forms import *

class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "lead_detail.html"
    form_class = LeadCategoryModelForm

    # def get_queryset(self):
    #     user = self.request.user
    
    #     if user.is_organiser:
    #         queryset = Category.objects.filter(organisation=user.userprofile)
    #     else:
    #         queryset = Category.objects.filter(organisation=user.agent.organisation)
    #         queryset = queryset.filter(agent__user=user)
    #     return queryset

    def get_success_url(self):
        return reverse("lead_list")


# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }
#     return render(request, "lead_detail.html", context)
