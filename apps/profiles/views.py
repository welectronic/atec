# apps/profiles/views.py
from typing import cast
from decimal import Decimal
from collections import defaultdict
from django.conf import settings
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction

from apps.core.selectors import get_allowed_company_ids
from apps.core.models import Company as CompanyType
from .models import Question, Assessment, Response

from .forms import AssessmentForm

# mismo patrón que inventory
COMPANY_MODEL = getattr(settings, "COMPANY_MODEL", "core.Company")
app_label, model_name = COMPANY_MODEL.rsplit(".", 1)
Company = django_apps.get_model(app_label, model_name)


@login_required
def assessment_manage(request, company_id):
    """
    Vista principal con los tabs (preguntas, assessments, respuestas)
    """
    allowed = get_allowed_company_ids(request.user)
    # si hay filtro de empresas y la que piden no está, 403
    if allowed and str(company_id) not in [str(x) for x in allowed]:
        return render(request, "403.html", status=403)

    company = get_object_or_404(Company, id=company_id)
    current_tab = request.GET.get("tab", "assessments")

    ctx = {
        "company": company,
        "current_tab": current_tab,
        "page_title": f"Perfiles / Diagnóstico — {cast(CompanyType, company).name}",
    }

    # si viene por HTMX, devolvemos solo el fragmento
    if request.headers.get("HX-Request") == "true":
        return render(request, f"profiles/tabs/_{current_tab}.html", ctx)

    return render(request, "profiles/manage.html", ctx)


@login_required
def assessment_list(request, company_id):
    """
    Lista de assessments de la empresa (tab)
    """
    allowed = get_allowed_company_ids(request.user)
    if allowed and str(company_id) not in [str(x) for x in allowed]:
        return render(request, "403.html", status=403)

    company = get_object_or_404(Company, id=company_id)
    assessments = Assessment.objects.filter(company=company).select_related("analyst").order_by("-assessment_date")

    ctx = {
        "company": company,
        "assessments": assessments,
    }
    return render(request, "profiles/tabs/_assessments.html", ctx)


@login_required
def assessment_create(request, company_id):
    allowed = get_allowed_company_ids(request.user)
    if allowed and str(company_id) not in [str(x) for x in allowed]:
        return render(request, "403.html", status=403)

    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.company = company
            assessment.analyst = request.user
            assessment.save()

            if request.headers.get("HX-Request") == "true":
                assessments = Assessment.objects.filter(company=company).order_by("-assessment_date")
                return render(
                    request,
                    "profiles/tabs/_assessments.html",
                    {"company": company, "assessments": assessments},
                )
            return redirect("profiles:manage", company_id=company_id)
    else:
        form = AssessmentForm()

    return render(
        request,
        "profiles/tabs/_assessment_form.html",
        {
            "company": company,
            "form": form,
        },
    )

@login_required
def question_list(request, company_id):
    """
    Tab de preguntas (catálogo)
    """
    allowed = get_allowed_company_ids(request.user)
    if allowed and str(company_id) not in [str(x) for x in allowed]:
        return render(request, "403.html", status=403)

    company = get_object_or_404(Company, id=company_id)
    questions = Question.objects.filter(is_active=True).order_by("instrument_code", "code")
    return render(
        request,
        "profiles/tabs/_questions.html",
        {
            "company": company,
            "questions": questions,
        },
    )


@login_required
def response_list(request, company_id):
    """
    Tab de respuestas: mostramos las respuestas de los últimos assessments
    """
    allowed = get_allowed_company_ids(request.user)
    if allowed and str(company_id) not in [str(x) for x in allowed]:
        return render(request, "403.html", status=403)

    company = get_object_or_404(Company, id=company_id)
    # traemos los últimos 5 assessments con sus respuestas
    assessments = (
        Assessment.objects.filter(company=company)
        .order_by("-assessment_date")
        .prefetch_related("responses__question")[:5]
    )

    return render(
        request,
        "profiles/tabs/_responses.html",
        {
            "company": company,
            "assessments": assessments,
        },
    )

@login_required
def assessment_fill(request, company_id, assessment_id):
    allowed = get_allowed_company_ids(request.user)
    if allowed and str(company_id) not in [str(x) for x in allowed]:
        return render(request, "403.html", status=403)

    company = get_object_or_404(Company, id=company_id)
    assessment = get_object_or_404(Assessment, id=assessment_id, company=company)

    # normalizamos porque a veces se guarda "INNOVATION_PROFILE v1" o "INNOVATION_PROFILE 1"
    raw_code = (assessment.instrument_code or "").strip()
    instrument_code = (
        raw_code.replace(" v1", "")
        .replace(" V1", "")
        .replace(" 1", "")
        .strip()
    )

    questions_qs = Question.objects.filter(
        instrument_code=instrument_code,
        instrument_version=assessment.instrument_version,
        is_active=True,
    ).order_by("dimension", "sub_dimension", "code")

    # respuestas ya guardadas
    existing_responses = {
        r.question.id: r for r in Response.objects.filter(assessment=assessment)
    }

    # ----------------- POST: guardar -----------------
    if request.method == "POST":
        with transaction.atomic():
            for q in questions_qs:
                prefix = f"q_{q.id}"
                answer_value = request.POST.get(f"{prefix}_answer_value")
                observations = request.POST.get(f"{prefix}_observations", "")

                if not answer_value:
                    continue

                answer_value = int(answer_value)
                score = Decimal(str(answer_value))  # 1→1, 2→2, ...

                if q.id in existing_responses:
                    resp = existing_responses[q.id]
                    resp.answer_value = answer_value
                    resp.score = score
                    resp.observations = observations
                    resp.save()
                else:
                    Response.objects.create(
                        assessment=assessment,
                        question=q,
                        answer_value=answer_value,
                        score=score,
                        observations=observations,
                    )

        # volvemos a la lista
        assessments = (
            Assessment.objects.filter(company=company)
            .order_by("-assessment_date")
            .select_related("analyst")
        )
        return render(
            request,
            "profiles/tabs/_assessments.html",
            {"company": company, "assessments": assessments},
        )

    # ----------------- GET: agrupamos -----------------
    grouped = defaultdict(lambda: defaultdict(list))

    for q in questions_qs:
        dim = q.dimension or "Sin dimensión"
        sub = q.sub_dimension or ""
        grouped[dim][sub].append(q)

    # 👇 convertir a dict “normal” para que el template sí pueda iterar
    grouped_clean = {}
    for dim, subs in grouped.items():
        grouped_clean[dim] = dict(subs)

    ctx = {
        "company": company,
        "assessment": assessment,
        "grouped_questions": grouped_clean,  # ← este es el que usamos en el template
        "existing_responses": existing_responses,
    }
    return render(request, "profiles/tabs/_assessment_fill.html", ctx)