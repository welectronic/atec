from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Company
from .selectors import get_allowed_company_ids
from .permissions import require_company_access

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from .models import Company
from .permissions import CompanyScopeMixin
from .forms import CompanyForm

@login_required(login_url="/admin/login/")
def company_list(request):
    user = request.user
    if user.is_superuser:
        qs = Company.objects.all()
    else:
        allowed = get_allowed_company_ids(user)
        qs = Company.objects.filter(id__in=allowed)
    # salida simple
    content = "Companies:\n" + "\n".join(f"- {c.name} ({c.tax_id})" for c in qs[:50])
    return HttpResponse(content, content_type="text/plain")


@require_company_access(lambda request, pk: pk)
@login_required(login_url="/admin/login/")
def company_detail(request, pk: int):
    company = get_object_or_404(Company, pk=pk)
    content = f"Company: {company.name}\nNIT: {company.tax_id}\nMunicipio: {company.municipality}"
    return HttpResponse(content, content_type="text/plain")

class CompanyListView(LoginRequiredMixin, PermissionRequiredMixin, CompanyScopeMixin, ListView):
    permission_required = "core.view_company"
    model = Company
    template_name = "core/company_list.html"
    context_object_name = "companies"
    is_company_model = True  # para el mixin

class CompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, CompanyScopeMixin, DetailView):
    permission_required = "core.view_company"
    model = Company
    template_name = "core/company_detail.html"
    is_company_model = True

class CompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "core.add_company"
    model = Company
    form_class = CompanyForm
    template_name = "core/company_form.html"
    success_url = reverse_lazy("company_list")

    def form_valid(self, form):
        # advisor = usuario actual (no-admin UI)
        obj = form.save(commit=False)
        obj.advisor = self.request.user
        # si manejas Organization aquí puedes fijarla o mostrarla como hidden/selector
        # obj.organization = ...
        obj.save()
        return redirect(self.success_url)

class CompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, CompanyScopeMixin, UpdateView):
    permission_required = "core.change_company"
    model = Company
    form_class = CompanyForm
    template_name = "core/company_form.html"
    success_url = reverse_lazy("company_list")
    is_company_model = True  # para scoping del objeto
