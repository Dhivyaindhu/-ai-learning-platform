# ai_engine/models.py
# Complete model set:
#   - All original models unchanged
#   - CapstonProject (typo) → CapstoneProject  (renamed + field update)
#   - ProjectSubmission     → CapstoneSubmission (renamed + field update)
#   Both renames match the imports in views.py

from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# ═══════════════════════════════════════════════════════════════
# PSYCHOLOGICAL ASSESSMENT
# ═══════════════════════════════════════════════════════════════

class PsychologyQuestion(models.Model):
    """Stores psychology assessment questions linked to a personality trait."""
    question_text = models.TextField()
    trait         = models.CharField(max_length=100)
    order         = models.IntegerField(default=0, help_text="Display order")
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering       = ['order', 'id']
        verbose_name   = "Psychology Question"
        verbose_name_plural = "Psychology Questions"

    def __str__(self):
        return f"{self.trait}: {self.question_text[:50]}"


# ═══════════════════════════════════════════════════════════════
# TEST SESSION
# ═══════════════════════════════════════════════════════════════

class UserTestSession(models.Model):
    """Tracks individual test sessions; allows multiple attempts per user."""
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_sessions')
    started_at              = models.DateTimeField(auto_now_add=True)
    completed_at            = models.DateTimeField(blank=True, null=True)
    is_completed            = models.BooleanField(default=False)
    current_question_index  = models.IntegerField(default=0)

    class Meta:
        ordering       = ['-started_at']
        verbose_name   = "Test Session"
        verbose_name_plural = "Test Sessions"

    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"{self.user.username} - Session {self.id} ({status})"

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def get_progress_percentage(self):
        total = PsychologyQuestion.objects.filter(is_active=True).count()
        if total == 0:
            return 0
        return int((self.responses.count() / total) * 100)


# ═══════════════════════════════════════════════════════════════
# USER RESPONSES
# ═══════════════════════════════════════════════════════════════

class UserResponse(models.Model):
    """Stores individual answers to psychology questions."""
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    session     = models.ForeignKey(UserTestSession, on_delete=models.CASCADE, related_name='responses')
    question    = models.ForeignKey(PsychologyQuestion, on_delete=models.CASCADE, related_name='responses')
    answer      = models.IntegerField(help_text="Numeric score (e.g. 1–5)")
    answer_text = models.TextField(blank=True, null=True, help_text="Text answer for conversational questions")
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering        = ['answered_at']
        verbose_name    = "User Response"
        verbose_name_plural = "User Responses"
        unique_together = ['session', 'question']

    def __str__(self):
        return f"{self.user.username} - {self.question.trait} - Score: {self.answer}"


# ═══════════════════════════════════════════════════════════════
# USER PROFILE
# ═══════════════════════════════════════════════════════════════

class UserProfile(models.Model):
    CAREER_LEVEL_CHOICES = [
        ('Beginner',     'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced',     'Advanced'),
    ]

    user                  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    personality_traits    = models.JSONField(blank=True, null=True)
    personality_summary   = models.TextField(blank=True, null=True)
    recommended_careers   = models.JSONField(blank=True, null=True)
    selected_career       = models.CharField(max_length=100, blank=True, null=True)
    career_level          = models.CharField(max_length=50, blank=True, null=True, choices=CAREER_LEVEL_CHOICES)
    last_assessment_date  = models.DateTimeField(blank=True, null=True)
    profile_updated_at    = models.DateTimeField(auto_now=True)
    created_at            = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def has_completed_assessment(self):
        return bool(self.personality_traits)

    def get_top_traits(self, limit=3):
        if not self.personality_traits:
            return []
        return sorted(self.personality_traits.items(), key=lambda x: x[1], reverse=True)[:limit]


# ═══════════════════════════════════════════════════════════════
# GENERATED COURSE
# ═══════════════════════════════════════════════════════════════

class GeneratedCourse(models.Model):
    DIFFICULTY_CHOICES = [
        ('Beginner',     'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced',     'Advanced'),
    ]

    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    career              = models.CharField(max_length=100)
    difficulty_level    = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Beginner')
    course_title        = models.CharField(max_length=200)
    course_description  = models.TextField(blank=True)
    estimated_duration  = models.CharField(max_length=50, blank=True)
    skills_covered      = models.JSONField(default=list)
    total_modules       = models.IntegerField(default=0)
    is_active           = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        ordering        = ['-created_at']
        verbose_name    = "Generated Course"
        verbose_name_plural = "Generated Courses"

    def __str__(self):
        return f"{self.user.username} - {self.course_title}"

    def get_module_count(self):
        return self.modules.count()

    @property
    def completion_percentage(self):
        if self.total_modules == 0:
            return 0
        completed = self.modules.filter(
            module_progress__user=self.user,
            module_progress__completed=True
        ).count()
        return int((completed / self.total_modules) * 100)


# ═══════════════════════════════════════════════════════════════
# COURSE MODULE
# ═══════════════════════════════════════════════════════════════

class CourseModule(models.Model):
    """Individual module within a course — theory + exercises + resources."""
    course               = models.ForeignKey(GeneratedCourse, on_delete=models.CASCADE, related_name='modules')
    module_number        = models.IntegerField()
    title                = models.CharField(max_length=255)
    description          = models.TextField()
    learning_objectives  = models.JSONField(default=list)
    theoretical_content  = models.TextField()
    practical_exercises  = models.JSONField(default=list)
    resources            = models.JSONField(default=list)
    estimated_time       = models.CharField(max_length=50)
    prerequisites        = models.TextField(blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)

    # Convenience aliases used in some views
    @property
    def module_title(self):
        return self.title

    @property
    def difficulty_level(self):
        return self.course.difficulty_level.lower()

    class Meta:
        ordering        = ['module_number']
        unique_together = ['course', 'module_number']
        verbose_name    = "Course Module"
        verbose_name_plural = "Course Modules"

    def __str__(self):
        return f"Module {self.module_number}: {self.title}"


# ═══════════════════════════════════════════════════════════════
# MODULE PROGRESS
# ═══════════════════════════════════════════════════════════════

class ModuleProgress(models.Model):
    """Per-user progress through a single module."""
    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_progress')
    module              = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='module_progress')
    started             = models.BooleanField(default=False)
    completed           = models.BooleanField(default=False)
    theory_read         = models.BooleanField(default=False)
    exercises_completed = models.JSONField(default=list)
    started_at          = models.DateTimeField(null=True, blank=True)
    completed_at        = models.DateTimeField(null=True, blank=True)
    user_notes          = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'module']
        ordering        = ['module__module_number']
        verbose_name    = "Module Progress"
        verbose_name_plural = "Module Progress Records"

    def __str__(self):
        status = "Completed" if self.completed else "In Progress" if self.started else "Not Started"
        return f"{self.user.username} - {self.module.title} ({status})"

    @property
    def completion_percentage(self):
        total     = 1 + len(self.module.practical_exercises)
        done      = (1 if self.theory_read else 0) + len(self.exercises_completed)
        return int((done / total) * 100) if total else 0


# ═══════════════════════════════════════════════════════════════
# MODULE QUIZ
# ═══════════════════════════════════════════════════════════════

class ModuleQuiz(models.Model):
    """Stored quiz for a module (optional; views can also generate on-the-fly)."""
    module        = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='quizzes')
    title         = models.CharField(max_length=255)
    questions     = models.JSONField(default=list, help_text="Questions with options and answers")
    passing_score = models.IntegerField(default=70)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Module Quiz"
        verbose_name_plural = "Module Quizzes"

    def __str__(self):
        return f"Quiz: {self.title}"


class QuizAttempt(models.Model):
    """Record of a user's quiz attempt."""
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz         = models.ForeignKey(ModuleQuiz, on_delete=models.CASCADE, related_name='attempts')
    answers      = models.JSONField(default=dict)
    score        = models.IntegerField(default=0)
    passed       = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering        = ['-attempted_at']
        verbose_name    = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"


# ═══════════════════════════════════════════════════════════════
# CAPSTONE PROJECT  (replaces the old misspelled CapstonProject)
# ═══════════════════════════════════════════════════════════════

class CapstoneProject(models.Model):
    """
    One capstone brief per course.
    Auto-generated the first time a user visits the capstone page.

    NOTE: replaces the old `CapstonProject` model (typo fixed).
    After replacing models.py run:
        python manage.py makemigrations
        python manage.py migrate
    """
    course        = models.OneToOneField(
        GeneratedCourse,
        on_delete    = models.CASCADE,
        related_name = "capstone",
    )
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    requirements  = models.TextField(
        blank     = True,
        help_text = "Plain-text list of deliverables / tasks",
    )
    created_at    = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name        = "Capstone Project"
        verbose_name_plural = "Capstone Projects"

    def __str__(self):
        return f"Capstone: {self.title}"


# ═══════════════════════════════════════════════════════════════
# CAPSTONE SUBMISSION  (replaces the old ProjectSubmission)
# ═══════════════════════════════════════════════════════════════

class CapstoneSubmission(models.Model):
    """
    One submission per user per capstone.
    Updated in-place on resubmission (update_or_create in views).

    NOTE: replaces the old `ProjectSubmission` model.
    """
    STATUS_CHOICES = [
        ("pending",   "Pending"),
        ("submitted", "Submitted"),
        ("approved",  "Approved"),
        ("rejected",  "Needs Revision"),
    ]

    capstone         = models.ForeignKey(
        CapstoneProject,
        on_delete    = models.CASCADE,
        related_name = "submissions",
    )
    user             = models.ForeignKey(
        User,
        on_delete    = models.CASCADE,
        related_name = "capstone_submissions",
    )
    submission_text  = models.TextField(blank=True)
    project_url      = models.URLField(blank=True)
    notes            = models.TextField(blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    feedback         = models.TextField(blank=True, help_text="Reviewer feedback")
    submitted_at     = models.DateTimeField(default=timezone.now)
    reviewed_at      = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together     = ("capstone", "user")
        verbose_name        = "Capstone Submission"
        verbose_name_plural = "Capstone Submissions"

    def __str__(self):
        return f"{self.user.username} — {self.capstone.title} [{self.status}]"


# ═══════════════════════════════════════════════════════════════
# USER RESULT
# ═══════════════════════════════════════════════════════════════

class UserResult(models.Model):
    """Final analysis and results from a completed assessment session."""
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    session               = models.OneToOneField(UserTestSession, on_delete=models.CASCADE, related_name='result')
    personality_summary   = models.JSONField()
    recommended_careers   = models.JSONField()
    strengths             = models.JSONField(blank=True, null=True)
    areas_for_development = models.JSONField(blank=True, null=True)
    ai_insights           = models.TextField(blank=True, null=True)
    created_at            = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering        = ['-created_at']
        verbose_name    = "User Result"
        verbose_name_plural = "User Results"

    def __str__(self):
        return f"{self.user.username} - Result for Session {self.session.id}"

    def get_top_career_matches(self, limit=5):
        if not self.recommended_careers:
            return []
        if isinstance(self.recommended_careers, list):
            return self.recommended_careers[:limit]
        return []


# ═══════════════════════════════════════════════════════════════
# DEPRECATED: UserProgress  (kept for backward compatibility)
# ═══════════════════════════════════════════════════════════════

class UserProgress(models.Model):
    """DEPRECATED — use ModuleProgress instead. Kept to avoid migration conflicts."""
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='old_progress')
    course                = models.ForeignKey(GeneratedCourse, on_delete=models.CASCADE, related_name='old_progress')
    current_module        = models.IntegerField(default=0)
    completed_modules     = models.JSONField(default=list)
    completion_percentage = models.IntegerField(default=0)
    started_at            = models.DateTimeField(auto_now_add=True)
    last_accessed         = models.DateTimeField(auto_now=True)
    completed_at          = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering        = ['-last_accessed']
        verbose_name    = "User Progress (Deprecated)"
        verbose_name_plural = "User Progress Records (Deprecated)"
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.career} ({self.completion_percentage}%)"

    def mark_module_complete(self, module_index):
        if module_index not in self.completed_modules:
            self.completed_modules.append(module_index)
            self.update_completion_percentage()
            self.save()

    def update_completion_percentage(self):
        total = self.course.get_module_count()
        if total > 0:
            self.completion_percentage = int((len(self.completed_modules) / total) * 100)
            if self.completion_percentage >= 100:
                self.completed_at = timezone.now()
                self.save()