# ai_engine/views.py - YOUR ORIGINAL with ONLY quiz fix

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

from .psychology.engine import PsychologyEngine
from .services.career_assessment_service import CareerAssessmentService
from .services.course_service import CourseService
from .models import (
    UserProfile, GeneratedCourse, CourseModule, ModuleProgress,
    CapstoneProject, CapstoneSubmission,
)

def _get_assessment_session(request):
    return request.session.get("assessment_session")

def _save_assessment_session(request, session_data):
    request.session["assessment_session"] = session_data
    request.session.modified = True

def _get_psych_session(request):
    return request.session.get("psych_session")

def _save_psych_session(request, session_data):
    request.session["psych_session"] = session_data
    request.session.modified = True

def _get_course_progress(course, user):
    if not course:
        return 0
    try:
        modules = CourseModule.objects.filter(course=course)
        if not modules.exists():
            return 0
        total_tasks, completed_tasks = 0, 0
        for mod in modules:
            exercises = mod.practical_exercises or []
            mod_total = 1 + len(exercises)
            total_tasks += mod_total
            prog = ModuleProgress.objects.filter(user=user, module=mod).first()
            if prog:
                completed_tasks += ((1 if prog.theory_read else 0) + len(prog.exercises_completed or []))
        return int(completed_tasks / total_tasks * 100) if total_tasks else 0
    except:
        return 0


def _careers_from_traits(trait_names):
    """COMPREHENSIVE career mapping - 50+ unique careers"""
    
    trait_career_map = {
        "openness": [
            "UX Designer", "Product Designer", "Graphic Designer", "Creative Director",
            "Content Creator", "Digital Artist", "Video Editor", "Animator",
            "Data Scientist", "Research Scientist", "Bioinformatics Specialist", "Astrophysicist",
            "Innovation Consultant", "Design Thinking Facilitator", "Futurist", "Trend Analyst"
        ],
        "conscientiousness": [
            "Project Manager", "Program Manager", "Operations Manager", "Supply Chain Manager",
            "Financial Analyst", "Investment Banker", "Accountant", "Auditor",
            "Software Engineer", "DevOps Engineer", "Systems Architect", "Quality Assurance Engineer",
            "Business Analyst", "Management Consultant", "Strategic Planner"
        ],
        "extraversion": [
            "Product Manager", "Marketing Manager", "Sales Manager", "Business Development Manager",
            "Public Relations Manager", "Corporate Communications Manager", "Event Manager",
            "HR Manager", "Recruiter", "Training & Development Manager", "Career Coach",
            "Account Executive", "Customer Success Manager", "Sales Director"
        ],
        "agreeableness": [
            "Teacher", "Corporate Trainer", "Educational Technologist", "Curriculum Designer",
            "Healthcare Administrator", "Patient Care Coordinator", "Medical Social Worker",
            "HR Business Partner", "Employee Relations Specialist", "Diversity & Inclusion Manager",
            "Career Counselor", "Life Coach", "Organizational Psychologist", "Mediator"
        ],
        "neuroticism": [
            "Risk Analyst", "Compliance Officer", "Security Analyst", "Data Privacy Officer",
            "Market Research Analyst", "User Research Analyst", "Forensic Analyst",
            "Quality Control Specialist", "Test Engineer", "Validation Engineer"
        ],
        "analytical": [
            "Data Scientist", "Data Engineer", "Data Analyst", "Business Intelligence Analyst",
            "Machine Learning Engineer", "AI Research Scientist", "Quantitative Analyst",
            "Systems Analyst", "Network Analyst", "Cybersecurity Analyst", "Penetration Tester",
            "Operations Research Analyst", "Statistical Analyst", "Bioinformatics Analyst"
        ],
        "creative": [
            "UI/UX Designer", "Product Designer", "Interaction Designer", "Service Designer",
            "Brand Designer", "Motion Graphics Designer", "3D Artist",
            "Content Strategist", "Copywriter", "Video Producer", "Podcast Producer",
            "Social Media Manager", "Influencer Marketing Manager"
        ],
        "technical": [
            "Full Stack Developer", "Frontend Developer", "Backend Developer", "Mobile Developer",
            "Game Developer", "Embedded Systems Engineer", "Firmware Engineer",
            "Cloud Architect", "Site Reliability Engineer", "Platform Engineer", "Database Administrator",
            "Blockchain Developer", "IoT Engineer", "AR/VR Developer", "Robotics Engineer"
        ],
        "leadership": [
            "Chief Technology Officer", "Chief Product Officer", "VP of Engineering", "VP of Product",
            "Engineering Manager", "Product Manager", "Program Director", "Department Head",
            "Strategy Consultant", "Change Management Consultant", "Executive Coach"
        ],
        "empathy": [
            "UX Researcher", "Customer Experience Manager", "Service Designer", "Patient Advocate",
            "Customer Support Manager", "Community Manager", "Social Worker", "Counselor"
        ],
        "detail_oriented": [
            "Data Analyst", "Financial Analyst", "Tax Analyst", "Actuarial Analyst",
            "Quality Assurance Engineer", "Regulatory Affairs Specialist", "Compliance Manager",
            "Technical Writer", "Documentation Specialist", "System Administrator"
        ],
        "problem_solving": [
            "Solutions Architect", "Technical Consultant", "Systems Engineer", "Process Engineer",
            "Support Engineer", "Field Engineer", "Integration Engineer", "Performance Engineer"
        ],
        "communication": [
            "Technical Writer", "Content Manager", "Editor", "Journalist", "Blogger",
            "Corporate Trainer", "Instructional Designer", "Learning Experience Designer",
            "Marketing Communications Manager", "PR Specialist", "Brand Manager"
        ]
    }
    
    seen = set()
    careers = []
    career_scores = {}
    
    for trait in trait_names:
        trait_lower = trait.lower()
        if trait_lower in trait_career_map:
            for career in trait_career_map[trait_lower]:
                if career not in career_scores:
                    career_scores[career] = 0
                career_scores[career] += 1
    
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    
    for career, score in sorted_careers:
        if career not in seen:
            seen.add(career)
            careers.append(career)
        if len(careers) >= 9:
            break
    
    tech_defaults = [
        "Software Engineer", "Data Scientist", "Product Manager", "UX Designer",
        "Data Analyst", "DevOps Engineer", "Machine Learning Engineer",
        "Cybersecurity Analyst", "Cloud Architect", "Full Stack Developer",
        "Business Analyst", "Marketing Manager", "Project Manager"
    ]
    
    for career in tech_defaults:
        if career not in seen:
            careers.append(career)
            seen.add(career)
        if len(careers) >= 9:
            break
    
    return careers[:9]


@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.filter(user=request.user).first()
        has_personality = profile and profile.personality_traits
        has_career = profile and profile.selected_career
        svc = CourseService()
        courses_data = svc.get_user_courses(request.user)
        show_assessment_popup = not has_personality
        show_career_popup = has_personality and not has_career
        recommended_careers = []
        if has_personality:
            if profile.recommended_careers:
                recommended_careers = profile.recommended_careers
            else:
                trait_names = list(profile.personality_traits.keys())[:5]
                recommended_careers = _careers_from_traits(trait_names)
                profile.recommended_careers = recommended_careers
                profile.save()
        in_progress = [c for c in courses_data if 0 < c["progress"] < 100]
        completed = [c for c in courses_data if c["progress"] == 100]
        not_started = [c for c in courses_data if c["progress"] == 0]
        return render(request, "ai_engine/dashboard.html", {
            "profile": profile, "courses_data": courses_data, "in_progress": in_progress,
            "completed": completed, "not_started": not_started, "total_courses": len(courses_data),
            "show_assessment_popup": show_assessment_popup, "show_career_popup": show_career_popup,
            "recommended_careers": recommended_careers, "has_personality": has_personality, "has_career": has_career,
        })
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render(request, "ai_engine/dashboard.html", {"show_assessment_popup": True, "courses_data": []})

@login_required
def start_test(request):
    has_profile = UserProfile.objects.filter(user=request.user, personality_traits__isnull=False).exists()
    if request.method == "POST":
        engine = PsychologyEngine()
        psych_session = engine.start_assessment()
        _save_psych_session(request, psych_session)
        return redirect("ai_engine:psychometric_question")
    return render(request, "ai_engine/start_test.html", {"has_profile": has_profile})

@login_required
def psychometric_question(request):
    psych_session = _get_psych_session(request)
    if not psych_session:
        messages.warning(request, "No active assessment. Please start again.")
        return redirect("ai_engine:start_test")
    engine = PsychologyEngine()
    if request.method == "POST":
        answer = request.POST.get("answer", "").strip()
        if len(answer) < 10:
            messages.error(request, "Please give a more detailed answer (at least 10 characters).")
            return redirect("ai_engine:psychometric_question")
        try:
            engine.submit_answer(psych_session, answer)
            _save_psych_session(request, psych_session)
        except:
            messages.error(request, "Error saving your answer. Please try again.")
            return redirect("ai_engine:psychometric_question")
        if engine.should_stop(psych_session):
            return redirect("ai_engine:psychometric_result")
        return redirect("ai_engine:psychometric_question")
    if engine.should_stop(psych_session):
        return redirect("ai_engine:psychometric_result")
    question = engine.get_next_question(psych_session)
    _save_psych_session(request, psych_session)
    if not question:
        return redirect("ai_engine:psychometric_result")
    return render(request, "ai_engine/question.html", {
        "question": question, "question_number": psych_session["current_question"] + 1,
        "max_questions": psych_session["max_questions"],
        "progress_pct": int(psych_session["current_question"] / psych_session["max_questions"] * 100),
    })

@login_required
def psychometric_result(request):
    psych_session = _get_psych_session(request)
    if not psych_session:
        messages.warning(request, "No assessment data found. Please start again.")
        return redirect("ai_engine:start_test")
    try:
        scores = psych_session.get("scores", {})
        top_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
        trait_names = [t[0] for t in top_traits]
        recommended_careers = _careers_from_traits(trait_names)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.personality_traits = scores
        profile.recommended_careers = recommended_careers
        profile.last_assessment_date = timezone.now()
        profile.save()
        request.session.pop("psych_session", None)
        messages.success(request, "Assessment complete! Choose your career path.")
        return redirect("ai_engine:career_recommendations")
    except Exception as e:
        print(f"Result processing error: {e}")
        messages.error(request, "Error processing your results. Please try again.")
        return redirect("ai_engine:start_test")

@login_required
def career_recommendations(request):
    try:
        profile = UserProfile.objects.filter(user=request.user).first()
    except:
        profile = None
    if profile and profile.recommended_careers:
        recommended = profile.recommended_careers
    elif profile and profile.personality_traits:
        trait_names = list(profile.personality_traits.keys())[:5]
        recommended = _careers_from_traits(trait_names)
        profile.recommended_careers = recommended
        profile.save()
    else:
        recommended = [
            "Software Engineer", "Data Scientist", "Product Manager", "UX Designer",
            "Data Analyst", "DevOps Engineer", "Marketing Manager", "Business Analyst", "Project Manager"
        ]
    existing_courses = {c.career: c for c in GeneratedCourse.objects.filter(user=request.user)}
    careers_with_status = []
    for career in recommended:
        course = existing_courses.get(career)
        careers_with_status.append({
            "name": career, "course": course, "course_id": course.id if course else None,
            "has_course": course is not None, "progress": _get_course_progress(course, request.user) if course else 0,
        })
    return render(request, "ai_engine/select_career.html", {
        "profile": profile, "careers": careers_with_status,
        "selected_career": profile.selected_career if profile else None,
        "has_personality": bool(profile and profile.personality_traits),
    })

@login_required
def select_career(request):
    if request.method == "POST":
        career = request.POST.get("career", "").strip()
        if not career:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"error": "Please select a career"}, status=400)
            messages.error(request, "Please select a career.")
            return redirect("ai_engine:career_recommendations")
        try:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.selected_career = career
            profile.save()
            svc = CareerAssessmentService()
            session = svc.start_career_assessment(career, total_questions=15)
            _save_assessment_session(request, session)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "redirect": "/ai/career-assessment/questions/"})
            return redirect("ai_engine:assessment_questions")
        except Exception as e:
            print(f"Career selection error: {e}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"error": "Failed to start assessment"}, status=500)
            messages.error(request, "Failed to start assessment. Please try again.")
            return redirect("ai_engine:career_recommendations")
    return redirect("ai_engine:career_recommendations")

@login_required
def assessment_questions(request):
    session_data = _get_assessment_session(request)
    if not session_data:
        messages.warning(request, "No active assessment. Please select a career first.")
        return redirect("ai_engine:career_recommendations")
    svc = CareerAssessmentService()
    if request.method == "POST":
        user_answer = request.POST.get("answer", "").strip().upper()
        correct_answer = request.POST.get("correct_answer", "").strip().upper()
        question_id = request.POST.get("question_id", "")
        difficulty = request.POST.get("difficulty", "beginner")
        if not user_answer:
            messages.error(request, "Please select an answer before continuing.")
            return redirect("ai_engine:assessment_questions")
        try:
            svc.submit_answer(session_data, question_id, user_answer, correct_answer, difficulty)
            _save_assessment_session(request, session_data)
        except Exception as e:
            print(f"Submit answer error: {e}")
            messages.error(request, "Error submitting answer. Please try again.")
            return redirect("ai_engine:assessment_questions")
        if svc.is_complete(session_data):
            return redirect("ai_engine:assessment_complete")
        return redirect("ai_engine:assessment_questions")
    if svc.is_complete(session_data):
        return redirect("ai_engine:assessment_complete")
    question = svc.get_next_question(session_data)
    _save_assessment_session(request, session_data)
    if not question:
        return redirect("ai_engine:assessment_complete")
    options_list = [{"letter": letter, "text": text} for letter, text in sorted(question["options"].items())]
    return render(request, "ai_engine/career_assessment_question.html", {
        "career": session_data["career"], "question": question, "options_list": options_list,
        "question_number": session_data["question_count"] + 1, "total_questions": session_data["max_questions"],
        "difficulty": question["difficulty"], "topic": question.get("topic", ""),
        "progress_pct": int(session_data["question_count"] / session_data["max_questions"] * 100),
    })

@login_required
def assessment_complete(request):
    session_data = _get_assessment_session(request)
    if not session_data:
        messages.warning(request, "No active assessment found.")
        return redirect("ai_engine:career_recommendations")
    try:
        svc = CareerAssessmentService()
        result = svc.calculate_level(session_data)
        career, level = result["career"], result["level"]
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.selected_career, profile.career_level = career, level.capitalize()
        profile.save()
        try:
            course_svc = CourseService()
            course = course_svc.generate_personalized_course(
                user=request.user, career=career, level=level, assessment_results=result,
                user_traits=request.session.get("personality_strengths", []),
            )
        except Exception as e:
            print(f"Course generation error: {e}")
            course = GeneratedCourse.objects.create(
                user=request.user, career=career, difficulty_level=level.capitalize(),
                course_title=f"{career} Learning Path - {level.capitalize()}", total_modules=6,
                estimated_duration="8 weeks", created_at=timezone.now()
            )
            messages.warning(request, "Course created with default structure.")
    except Exception as e:
        print(f"Assessment complete error: {e}")
        messages.error(request, "Something went wrong. Please try again.")
        return redirect("ai_engine:career_recommendations")
    request.session.pop("assessment_session", None)
    request.session.modified = True
    return render(request, "ai_engine/career_assesment_complete.html", {
        "result": result, "career": career, "level": level, "course": course,
        "scores": result.get("scores_by_difficulty", {}),
    })

@login_required
def my_courses(request):
    try:
        svc = CourseService()
        courses_data = svc.get_user_courses(request.user)
    except Exception as e:
        print(f"Load courses error: {e}")
        messages.error(request, "Unable to load your courses.")
        courses_data = []
    return render(request, "ai_engine/my_courses.html", {"courses_data": courses_data})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(GeneratedCourse, id=course_id, user=request.user)
    modules = CourseModule.objects.filter(course=course).order_by("module_number")
    module_list = []
    for mod in modules:
        prog = ModuleProgress.objects.filter(user=request.user, module=mod).first()
        total_tasks = 1 + len(mod.practical_exercises or [])
        completed_tasks = 0
        if prog:
            completed_tasks = ((1 if prog.theory_read else 0) + len(prog.exercises_completed or []))
        pct = int(completed_tasks / total_tasks * 100) if total_tasks else 0
        module_list.append({"module": mod, "completion": pct, "progress": prog})
    svc = CourseService()
    overall_progress = svc._calculate_course_completion(course, request.user)
    capstone = CapstoneProject.objects.filter(course=course).first()
    return render(request, "ai_engine/course_detail.html", {
        "course": course, "module_list": module_list, "overall_progress": overall_progress, "capstone": capstone,
    })

@login_required
def module_learn(request, module_id):
    module = get_object_or_404(CourseModule, id=module_id, course__user=request.user)
    svc = CourseService()
    prog_data = svc.get_module_progress(request.user, module)
    next_mod, _ = svc.get_next_module(request.user, module.course)
    if next_mod and next_mod.id == module.id:
        next_mod = None
    return render(request, "ai_engine/module_learn.html", {
        "module": module, "completion": prog_data["completion"], "theory_completed": prog_data["theory_completed"],
        "exercises_completed": prog_data["exercises_completed"], "next_module": next_mod,
    })

@login_required
def mark_theory_complete(request, module_id):
    if request.method == "POST":
        module = get_object_or_404(CourseModule, id=module_id, course__user=request.user)
        svc = CourseService()
        svc.mark_theory_complete(request.user, module)
        messages.success(request, "Theory marked as complete!")
    return redirect("ai_engine:module_learn", module_id=module_id)

@login_required
def complete_exercise(request, module_id, exercise_index):
    if request.method == "POST":
        module = get_object_or_404(CourseModule, id=module_id, course__user=request.user)
        svc = CourseService()
        svc.complete_exercise(request.user, module, exercise_index)
        messages.success(request, "Exercise completed!")
    return redirect("ai_engine:module_learn", module_id=module_id)


# ═══════════════════════════════════════════════════════════════
# QUIZ SYSTEM - FIXED VERSION
# ═══════════════════════════════════════════════════════════════
@login_required
def module_quiz(request, module_id):
    """Module quiz - FIXED to use ModuleQuiz model"""
    
    module = get_object_or_404(CourseModule, id=module_id, course__user=request.user)
    
    # Import quiz service
    from .services.quiz_service import QuizService
    quiz_service = QuizService()
    
    # Get or generate quiz
    try:
        quiz = quiz_service.get_quiz_for_module(module)
        
        if not quiz or not quiz.questions:
            messages.error(request, "Quiz could not be generated. Please try again.")
            return redirect("ai_engine:module_learn", module_id=module_id)
    
    except Exception as e:
        print(f"❌ Quiz generation error: {e}")
        import traceback
        traceback.print_exc()
        messages.error(request, "Unable to generate quiz. Please try again.")
        return redirect("ai_engine:module_learn", module_id=module_id)
    
    # Handle quiz submission
    if request.method == "POST":
        try:
            # Submit and grade quiz
            result = quiz_service.submit_quiz(
                user=request.user,
                quiz=quiz,
                answers=request.POST
            )
            
            # Mark module as complete if passed
            if result['passed']:
                svc = CourseService()
                svc.mark_theory_complete(request.user, module)
                messages.success(request, f"Quiz passed with {result['pct']}%! Module marked complete.")
            else:
                messages.warning(request, f"Quiz score: {result['pct']}%. Review and try again.")
            
            # Return results page
            return render(request, "ai_engine/module_quiz_result.html", {
                "module": module,
                "quiz": quiz,
                "results": result['results'],
                "score": result['correct'],
                "total": result['total'],
                "pct": result['pct'],
                "passed": result['passed']
            })
            
        except Exception as e:
            print(f"❌ Quiz submission error: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, "Error submitting quiz. Please try again.")
            return redirect("ai_engine:module_quiz", module_id=module_id)
    
    # GET request - show quiz
    try:
        previous_attempts = quiz_service.get_previous_attempts(request.user, quiz)
    except:
        previous_attempts = []
    
    return render(request, "ai_engine/module_quiz.html", {
        "module": module,
        "quiz": quiz,
        "questions": quiz.questions,  # Pass questions from JSON field
        "previous_attempts": previous_attempts
    })

# ═══════════════════════════════════════════════════════════════
# CAPSTONE PROJECT
# ═══════════════════════════════════════════════════════════════

@login_required
def capstone_project(request, course_id):
    course = get_object_or_404(GeneratedCourse, id=course_id, user=request.user)
    capstone = CapstoneProject.objects.filter(course=course).first()
    if not capstone:
        career, level = course.career, course.difficulty_level.lower()
        try:
            capstone = CapstoneProject.objects.create(course=course, title=f"{career} Capstone Project", description=f"Demonstrate your {level}-level {career} skills.", requirements=_generate_capstone_requirements(career, level), created_at=timezone.now())
        except Exception as e:
            print(f"Capstone creation error: {e}")
            messages.error(request, "Unable to load capstone project.")
            return redirect("ai_engine:course_detail", course_id=course_id)
    submission = CapstoneSubmission.objects.filter(capstone=capstone, user=request.user).first()
    return render(request, "ai_engine/capstone_project.html", {"course": course, "capstone": capstone, "submission": submission, "can_submit": submission is None or submission.status == "rejected"})

@login_required
def submit_capstone_project(request, capstone_id):
    capstone = get_object_or_404(CapstoneProject, id=capstone_id, course__user=request.user)
    if request.method != "POST":
        return redirect("ai_engine:capstone_project", course_id=capstone.course.id)
    submission_text, project_url, notes = request.POST.get("submission_text", "").strip(), request.POST.get("project_url", "").strip(), request.POST.get("notes", "").strip()
    if not submission_text and not project_url:
        messages.error(request, "Please provide your project work or a link to it.")
        return redirect("ai_engine:capstone_project", course_id=capstone.course.id)
    try:
        submission, created = CapstoneSubmission.objects.update_or_create(capstone=capstone, user=request.user, defaults={"submission_text": submission_text, "project_url": project_url, "notes": notes, "status": "submitted", "submitted_at": timezone.now()})
    except Exception as e:
        print(f"Capstone submission error: {e}")
        messages.error(request, "Failed to submit your project.")
        return redirect("ai_engine:capstone_project", course_id=capstone.course.id)
    action = "submitted" if created else "resubmitted"
    messages.success(request, f"Capstone project {action} successfully!")
    return redirect("ai_engine:capstone_status", course_id=capstone.course.id)

@login_required
def capstone_status(request, course_id):
    course = get_object_or_404(GeneratedCourse, id=course_id, user=request.user)
    capstone = get_object_or_404(CapstoneProject, course=course)
    submission = CapstoneSubmission.objects.filter(capstone=capstone, user=request.user).first()
    if not submission:
        messages.info(request, "You haven't submitted your capstone project yet.")
        return redirect("ai_engine:capstone_project", course_id=course_id)
    return render(request, "ai_engine/capstone_status.html", {"course": course, "capstone": capstone, "submission": submission, "status_label": {"submitted": "Under Review", "approved": "Approved ✅", "rejected": "Needs Revision ❌", "pending": "Pending"}.get(submission.status, submission.status.title())})

def _generate_capstone_requirements(career, level):
    return {
        "beginner": f"1. Research three core concepts.\n2. Real-world examples.\n3. 300-word reflection.\n4. Summary chart.",
        "intermediate": f"1. Design a small {career} project.\n2. Document decisions.\n3. Identify challenges.\n4. Evaluate best practices.",
        "advanced": f"1. Comprehensive solution.\n2. Advanced techniques.\n3. 800+ word write-up.\n4. Testing evidence.\n5. Critical analysis.\n6. Improvement roadmap.",
    }.get(level, f"Complete a {career} project demonstrating your skills.")