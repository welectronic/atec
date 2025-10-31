from django.urls import path
from .views import (
    CompanyListView, CompanyDetailView,
    CompanyCreateView, CompanyUpdateView,
)

app_name = "core"

urlpatterns = [
    path("", CompanyListView.as_view(), name="company_list"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company_detail"),
    path("companies/new/", CompanyCreateView.as_view(), name="company_create"),
    path("companies/<int:pk>/edit/", CompanyUpdateView.as_view(), name="company_update"),
]
