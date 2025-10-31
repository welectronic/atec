# apps/profiles/urls.py
from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    # vista principal tipo "manage"
    path("<str:company_id>/", views.assessment_manage, name="manage"),

    # tabs HTMX
    path("<str:company_id>/assessments/", views.assessment_list, name="assessment_list"),
    path("<str:company_id>/assessments/new/", views.assessment_create, name="assessment_create"),
    path("<str:company_id>/questions/", views.question_list, name="question_list"),
    path("<str:company_id>/responses/", views.response_list, name="response_list"),
    path("<str:company_id>/assessments/<uuid:assessment_id>/fill/", views.assessment_fill, name="assessment_fill"),
]
