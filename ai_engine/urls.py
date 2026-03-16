from django.urls import path
from . import views

# app_name MUST stay — both ai_engine/views.py and users/views.py use "ai_engine:..." prefix
app_name = "ai_engine"

urlpatterns = [
    # ── Dashboard ─────────────────────────────────────────────
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # ── Psychometric Flow ─────────────────────────────────────
    path("start-test/", views.start_test, name="start_test"),
    path("assessment/question/", views.psychometric_question, name="psychometric_question"),
    path("assessment/result/", views.psychometric_result, name="psychometric_result"),

    # ── Career Selection & Recommendations ────────────────────
    path("select-career/", views.select_career, name="select_career"),
    path("career-recommendations/", views.career_recommendations, name="career_recommendations"),

    # ── Career Assessment Flow ────────────────────────────────
    path("career-assessment/questions/", views.assessment_questions, name="assessment_questions"),
    path("career-assessment/complete/", views.assessment_complete, name="assessment_complete"),

    # ── Courses ───────────────────────────────────────────────
    path("courses/", views.my_courses, name="my_courses"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),

    # ── Module Learning ───────────────────────────────────────
    path("module/<int:module_id>/", views.module_learn, name="module_learn"),
    path("module/<int:module_id>/theory-complete/", views.mark_theory_complete, name="mark_theory_complete"),
    path("module/<int:module_id>/exercise/<int:exercise_index>/complete/", views.complete_exercise, name="complete_exercise"),
    path("module/<int:module_id>/quiz/", views.module_quiz, name="module_quiz"),

    # ── Capstone Project ──────────────────────────────────────
    path("capstone/<int:course_id>/", views.capstone_project, name="capstone_project"),
    path("capstone/<int:capstone_id>/submit/", views.submit_capstone_project, name="submit_capstone_project"),
    path("capstone/<int:course_id>/status/", views.capstone_status, name="capstone_status"),
]