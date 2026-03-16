# ai_engine/services/course_service.py

from django.utils import timezone
from ..models import GeneratedCourse, CourseModule, ModuleProgress, CapstoneProject


class CourseService:

    def generate_personalized_course(self, user, career, level, assessment_results, user_traits=None):
        """Generate a full course using RAGCourseGenerator for rich content."""
        try:
            from ..rag.course_generator import RAGCourseGenerator
            gen = RAGCourseGenerator()
            course_data = gen.generate_personalized_course(
                career=career,
                level=level,
                assessment_results=assessment_results,
                personality_strengths=user_traits,
            )
            print(f"✅ RAG course generated: {len(course_data.get('modules', []))} modules")
        except Exception as e:
            print(f"⚠️  RAG generator failed: {e} — using basic fallback")
            import traceback
            traceback.print_exc()
            course_data = self._basic_course_data(career, level)

        course = GeneratedCourse.objects.create(
            user               = user,
            career             = career,
            difficulty_level   = level.capitalize(),
            course_title       = course_data.get("title", f"{career} — {level.capitalize()} Track"),
            course_description = course_data.get("description", f"Personalised {level} course for {career}"),
            estimated_duration = f'{course_data.get("duration_weeks", 8)} weeks',
            skills_covered     = self._get_skills_for_career(career, level),
            total_modules      = len(course_data.get("modules", [])),
        )

        # Create modules — use RAG-provided objectives if available
        for mod_data in course_data.get("modules", []):
            # BUG FIX 2: _build_objectives() was ALWAYS overwriting RAG-generated
            # learning objectives with generic "Understand key concept X.Y" text.
            # Now we use the RAG objectives if present, fall back only when absent.
            rag_objectives = mod_data.get("learning_objectives") or mod_data.get("objectives") or []
            objectives = rag_objectives if rag_objectives else self._build_objectives(mod_data)

            # Normalise exercises — RAG may return key "exercises" or "practical_exercises"
            exercises = (
                mod_data.get("practical_exercises")
                or mod_data.get("exercises")
                or []
            )

            # Normalise resources — RAG may return key "reference_links" or "resources"
            resources = (
                mod_data.get("resources")
                or mod_data.get("reference_links")
                or []
            )

            # Normalise theory — RAG may return key "theory_content" or "theoretical_content"
            theory = (
                mod_data.get("theoretical_content")
                or mod_data.get("theory_content")
                or ""
            )

            CourseModule.objects.create(
                course              = course,
                module_number       = mod_data["module_number"],
                title               = mod_data["title"],
                description         = mod_data["description"],
                learning_objectives = objectives,
                theoretical_content = theory,
                practical_exercises = exercises,
                resources           = resources,
                estimated_time      = f'{mod_data.get("estimated_hours", 8)} hours',
                prerequisites       = (
                    f'Complete Module {mod_data["module_number"] - 1}'
                    if mod_data["module_number"] > 1 else 'None'
                ),
            )

        # BUG FIX 1: CapstoneProject model only has: title, description, requirements, created_at
        # Old code passed deliverables + evaluation_criteria → TypeError → silent failure.
        # Fix: store all extra fields inside requirements as formatted text.
        capstone_data = course_data.get("capstone", {})
        if capstone_data:
            # Build a rich requirements text from all available capstone data
            req_parts = []

            raw_req = capstone_data.get("requirements", [])
            if isinstance(raw_req, list):
                req_parts.append("REQUIREMENTS:\n" + "\n".join(f"• {r}" for r in raw_req))
            elif raw_req:
                req_parts.append(f"REQUIREMENTS:\n{raw_req}")

            deliverables = capstone_data.get("deliverables", [])
            if deliverables:
                req_parts.append("\nDELIVERABLES:\n" + "\n".join(f"• {d}" for d in deliverables))

            criteria = capstone_data.get("evaluation_criteria", [])
            if criteria:
                req_parts.append("\nEVALUATION CRITERIA:\n" + "\n".join(f"• {c}" for c in criteria))

            try:
                CapstoneProject.objects.create(
                    course       = course,
                    title        = capstone_data.get("title", f"{career} Capstone Project"),
                    description  = capstone_data.get("description", f"Apply all skills from this {level} {career} course."),
                    requirements = "\n".join(req_parts),
                )
            except Exception as e:
                print(f"⚠️  Capstone creation failed: {e}")

        return course

    def get_user_courses(self, user):
        courses      = GeneratedCourse.objects.filter(user=user, is_active=True)
        courses_data = []

        for course in courses:
            progress = self._calculate_course_completion(course, user)
            courses_data.append({
                "course":            course,
                "progress":          progress,
                "module_count":      course.total_modules,
                "completed_modules": self._get_completed_modules_count(course, user),
            })

        return courses_data

    def get_module_progress(self, user, module):
        progress, created = ModuleProgress.objects.get_or_create(
            user     = user,
            module   = module,
            defaults = {"started": True, "started_at": timezone.now()},
        )

        if created:
            progress.started    = True
            progress.started_at = timezone.now()
            progress.save()

        exercises       = module.practical_exercises or []
        total_tasks     = 1 + len(exercises)

        # BUG FIX 4: exercises_completed from JSONField can be None, a list, or
        # in rare DB driver cases a set. Always normalise to a plain list of ints.
        raw_completed = progress.exercises_completed or []
        exercises_completed = [int(x) for x in raw_completed] if raw_completed else []

        completed_tasks = (1 if progress.theory_read else 0) + len(exercises_completed)

        return {
            "progress":            progress,
            "completion":          int(completed_tasks / total_tasks * 100) if total_tasks else 0,
            "theory_completed":    progress.theory_read,
            "exercises_completed": exercises_completed,  # always a list of ints
        }

    def mark_theory_complete(self, user, module):
        progress, _ = ModuleProgress.objects.get_or_create(
            user     = user,
            module   = module,
            defaults = {"started": True, "started_at": timezone.now()},
        )
        progress.theory_read = True
        self._check_module_completion(progress, module)
        progress.save()

    def complete_exercise(self, user, module, exercise_index):
        progress, _ = ModuleProgress.objects.get_or_create(
            user     = user,
            module   = module,
            defaults = {"started": True, "started_at": timezone.now()},
        )

        if progress.exercises_completed is None:
            progress.exercises_completed = []

        idx = int(exercise_index)
        if idx not in progress.exercises_completed:
            progress.exercises_completed.append(idx)

        self._check_module_completion(progress, module)
        progress.save()

    def get_next_module(self, user, course):
        modules = CourseModule.objects.filter(course=course).order_by("module_number")
        for module in modules:
            progress = ModuleProgress.objects.filter(user=user, module=module).first()
            if not progress or not progress.completed:
                return module, False
        return None, False

    def get_capstone(self, course):
        return CapstoneProject.objects.filter(course=course).first()

    # ── Private helpers ───────────────────────────────────────

    def _build_objectives(self, mod_data):
        """
        Fallback only — used when RAG provides no learning_objectives.
        Generates objectives from the module title instead of the old
        generic "Understand key concept X.Y" placeholder text.
        """
        concept = mod_data.get("title", "")
        # Strip "Module N: " prefix if present
        if ": " in concept:
            concept = concept.split(": ", 1)[1]
        career = mod_data.get("career", "this field")
        return [
            f"Understand the core principles and theory of {concept}",
            f"Apply {concept} techniques in real-world {career} scenarios",
            f"Evaluate and critique {concept} implementations using best practices",
        ]

    def _calculate_course_completion(self, course, user):
        modules = CourseModule.objects.filter(course=course)
        if not modules.exists():
            return 0
        completed = ModuleProgress.objects.filter(
            user=user, module__course=course, completed=True
        ).count()
        return int((completed / modules.count()) * 100)

    def _get_completed_modules_count(self, course, user):
        return ModuleProgress.objects.filter(
            user=user, module__course=course, completed=True
        ).count()

    def _check_module_completion(self, progress, module):
        exercises       = module.practical_exercises or []
        total_tasks     = 1 + len(exercises)
        completed_tasks = (1 if progress.theory_read else 0) + len(progress.exercises_completed or [])
        if completed_tasks >= total_tasks and not progress.completed:
            progress.completed    = True
            progress.completed_at = timezone.now()

    def _get_skills_for_career(self, career, level):
        base = {
            "Software Engineer":         ["Programming", "Data Structures", "Algorithms", "System Design", "Testing"],
            "Data Analyst":              ["SQL", "Excel", "Data Visualisation", "Statistical Analysis", "Dashboards"],
            "Data Scientist":            ["Python", "Machine Learning", "Statistics", "Feature Engineering", "Model Deployment"],
            "Product Manager":           ["Product Strategy", "Roadmapping", "Stakeholder Management", "Agile", "Metrics"],
            "UX Designer":               ["User Research", "Wireframing", "Prototyping", "Design Systems", "Usability Testing"],
            "Marketing Manager":         ["Campaign Planning", "SEO", "Analytics", "Brand Strategy", "Digital Advertising"],
            "DevOps Engineer":           ["CI/CD", "Docker", "Kubernetes", "Linux", "Cloud Infrastructure"],
            "Cybersecurity Analyst":     ["Network Security", "Penetration Testing", "Incident Response", "SIEM", "Compliance"],
            "Machine Learning Engineer": ["Python", "ML Algorithms", "Model Deployment", "MLOps", "Deep Learning"],
            "Business Analyst":          ["Requirements", "Process Modelling", "Stakeholder Management", "Data Analysis", "Business Case"],
        }
        skills = list(base.get(career, ["Core Concepts", "Fundamentals", "Best Practices", "Industry Tools"]))
        if level.lower() == "intermediate":
            skills.append("Advanced Techniques")
        elif level.lower() == "advanced":
            skills.extend(["Advanced Techniques", "Leadership", "Strategy"])
        return skills

    def _basic_course_data(self, career, level):
        """
        Emergency fallback — only used when RAGCourseGenerator raises an exception.
        Produces real structured content instead of "key concept X.Y" placeholders.
        """
        module_count = {"beginner": 6, "intermediate": 8, "advanced": 10}.get(level.lower(), 6)
        topics = self._get_fallback_topics(career, level)

        modules = []
        for i in range(1, module_count + 1):
            topic = topics[i - 1] if i <= len(topics) else f"{career} Advanced Topic {i}"
            modules.append({
                "module_number": i,
                "title":         f"Module {i}: {topic}",
                "description":   f"Master {topic} to build your {career} skills at {level} level.",
                "learning_objectives": [
                    f"Understand the core principles of {topic}",
                    f"Apply {topic} in real {career} scenarios",
                    f"Follow industry best practices for {topic}",
                ],
                "theory_content": self._basic_theory(topic, career, level),
                "exercises": [
                    {
                        "title":       f"🔍 Research: {topic} in Practice",
                        "description": f"Find 2-3 real-world examples of {topic} in {career} roles. Write a 200-word summary of what you learned.",
                        "difficulty":  "Easy",
                        "type":        "research",
                    },
                    {
                        "title":       f"🛠 Apply: {topic} Scenario",
                        "description": f"Given a realistic {career} challenge, apply {topic} principles to propose a solution. Document your reasoning.",
                        "difficulty":  "Medium",
                        "type":        "scenario",
                    },
                    {
                        "title":       f"🚀 Build: {topic} Mini-Project",
                        "description": f"Create a small deliverable demonstrating {topic}. Include a brief write-up explaining your approach and decisions.",
                        "difficulty":  "Hard",
                        "type":        "project",
                    },
                ],
                "reference_links": [
                    {"title": f"{topic} — GeeksforGeeks",    "url": f"https://www.geeksforgeeks.org/{topic.lower().replace(' ', '-')}/", "type": "tutorial"},
                    {"title": f"{topic} — YouTube Tutorial", "url": f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+tutorial", "type": "video"},
                    {"title": "FreeCodeCamp — Learn for Free", "url": "https://www.freecodecamp.org/", "type": "tutorial"},
                ],
                "estimated_hours": 8,
            })

        return {
            "title":          f"{career} — {level.capitalize()} Track",
            "description":    f"A structured {level} learning path for aspiring {career} professionals.",
            "duration_weeks": module_count + 2,
            "modules":        modules,
            "capstone": {
                "title":       f"{career} Capstone Project",
                "description": f"Apply everything you have learned to build a real {career} portfolio piece.",
                "requirements":  ["Apply concepts from every module", "Follow professional best practices", "Write clear documentation"],
                "deliverables":  ["Final deliverable or project", "Technical documentation", "Reflection write-up"],
                "evaluation_criteria": ["Quality (40%)", "Completeness (30%)", "Documentation (30%)"],
            },
        }

    def _basic_theory(self, topic, career, level):
        return f"""<h1>{topic}</h1>

<section>
<h2>🎯 Learning Outcomes</h2>
<p>By the end of this module you will be able to:</p>
<ul>
<li>Explain the core concepts and purpose of <strong>{topic}</strong></li>
<li>Apply {topic} techniques in real-world {career} tasks</li>
<li>Follow industry best practices and avoid common mistakes</li>
</ul>
</section>

<section>
<h2>📚 What is {topic}?</h2>
<p><strong>{topic}</strong> is a fundamental area of expertise for {career} professionals. It enables you to work more effectively, make better decisions, and deliver higher-quality results in your day-to-day work.</p>
<p>At the <strong>{level}</strong> level, mastering {topic} means understanding not just the mechanics but also the reasoning behind best practices — so you can adapt them to new situations with confidence.</p>
</section>

<section>
<h2>💡 Why {topic} Matters for {career}</h2>
<ul>
<li>Improves speed and accuracy in core tasks</li>
<li>Enables confident decision-making under uncertainty</li>
<li>Makes you a more effective collaborator with colleagues and stakeholders</li>
<li>Provides a strong foundation for advancing to more senior roles</li>
</ul>
</section>

<section>
<h2>🛠 How to Apply {topic}</h2>
<ol>
<li><strong>Understand the goal:</strong> Clarify what you are trying to achieve before starting</li>
<li><strong>Gather context:</strong> Collect the information and tools you need</li>
<li><strong>Apply the technique:</strong> Work through the process step by step</li>
<li><strong>Validate your output:</strong> Check results against your original goal</li>
<li><strong>Reflect and document:</strong> Record what worked and what you would do differently</li>
</ol>
</section>

<section>
<h2>✅ Best Practices</h2>
<ul>
<li><strong>Start simple:</strong> Get a working solution first, then optimise</li>
<li><strong>Document as you go:</strong> Notes made in the moment are far more useful than those written later</li>
<li><strong>Seek feedback early:</strong> A second opinion before you invest too much time can save hours</li>
<li><strong>Iterate:</strong> Most professional work improves through multiple passes, not a single perfect attempt</li>
</ul>
</section>

<section>
<h2>⚠️ Common Mistakes</h2>
<ul>
<li><strong>Skipping the fundamentals:</strong> Rushing to advanced topics without a solid foundation leads to gaps</li>
<li><strong>Ignoring edge cases:</strong> Real-world data and situations are messier than tutorials suggest</li>
<li><strong>Not validating work:</strong> Always verify outputs before treating them as final</li>
</ul>
</section>

<section>
<h2>📝 Summary</h2>
<p>You have now covered the core concepts of <strong>{topic}</strong> and why they matter for {career} professionals. Complete the exercises below to turn this theory into hands-on experience.</p>
</section>"""

    def _get_fallback_topics(self, career, level):
        kb = {
            "Data Analyst": {
                "beginner":     ["Excel & Spreadsheets", "SQL Basics", "Data Visualisation", "Statistics Fundamentals", "Data Quality", "Business Metrics"],
                "intermediate": ["Advanced SQL", "Tableau / Power BI", "Python for Analysis", "Statistical Analysis", "Dashboard Design", "Data Storytelling"],
                "advanced":     ["Business Intelligence Strategy", "Predictive Analytics", "Data Governance", "Advanced Analytics", "ETL Design", "Data Strategy"],
            },
            "Data Scientist": {
                "beginner":     ["Python Programming", "Statistics", "Data Cleaning", "Pandas & NumPy", "Exploratory Analysis", "Basic ML"],
                "intermediate": ["Machine Learning", "Feature Engineering", "Model Evaluation", "SQL", "Scikit-learn", "Visualisation"],
                "advanced":     ["Deep Learning", "MLOps", "Model Deployment", "A/B Testing", "Big Data", "Advanced ML"],
            },
            "Software Engineer": {
                "beginner":     ["Programming Basics", "Variables & Data Types", "Control Flow", "Functions", "Debugging", "Version Control"],
                "intermediate": ["Object-Oriented Programming", "Data Structures", "Algorithms", "APIs", "Databases", "Testing"],
                "advanced":     ["System Design", "Scalability", "Microservices", "Security", "DevOps", "Performance"],
            },
            "Product Manager": {
                "beginner":     ["Product Fundamentals", "User Research", "Roadmapping", "User Stories", "Metrics & KPIs", "Agile Basics"],
                "intermediate": ["Product Strategy", "Stakeholder Management", "Prioritisation Frameworks", "Analytics", "Go-to-Market", "Product Discovery"],
                "advanced":     ["Product Vision & Strategy", "Platform Strategy", "Business Models", "Leadership", "Data-Driven PM", "Strategic Planning"],
            },
            "UX Designer": {
                "beginner":     ["Design Thinking", "User Research", "Wireframing", "Prototyping", "Usability Basics", "Design Tools"],
                "intermediate": ["Interaction Design", "Design Systems", "Accessibility", "User Testing", "Information Architecture", "Visual Design"],
                "advanced":     ["Service Design", "Design Strategy", "Design Leadership", "Advanced Research", "Design Ops", "Strategic UX"],
            },
        }
        return kb.get(career, {}).get(level.lower(), [
            f"{career} Fundamentals", "Core Concepts", "Best Practices",
            "Tools & Techniques", "Real-World Applications", "Advanced Topics",
        ])