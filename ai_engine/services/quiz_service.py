# ai_engine/services/quiz_service.py - FIXED to use YOUR models

import random
from django.utils import timezone

# Import YOUR actual models (not Quiz, Question, etc. - those don't exist!)
from ..models import ModuleQuiz, QuizAttempt


class QuizService:
    """Quiz service using ModuleQuiz and QuizAttempt models"""
    
    def get_quiz_for_module(self, module):
        """Get or generate quiz for module"""
        
        print(f"\n{'='*60}")
        print(f"🎯 Generating Quiz: {module.title}")
        print(f"{'='*60}")
        
        # Check if quiz already exists
        try:
            quiz = ModuleQuiz.objects.get(module=module)
            if quiz.questions:  # Has questions
                print(f"✅ Found existing quiz with {len(quiz.questions)} questions")
                return quiz
        except ModuleQuiz.DoesNotExist:
            pass
        
        # Generate new quiz
        concept_name = module.title.replace(f"Module {module.module_number}: ", "")
        print(f"📌 Concept: '{concept_name}'")
        
        # Generate questions
        questions_data = self._generate_fallback_questions(module, 5)
        
        # Create quiz
        quiz, created = ModuleQuiz.objects.update_or_create(
            module=module,
            defaults={
                'title': f"{module.title} - Quiz",
                'questions': questions_data,  # Store as JSON
                'passing_score': 60,
            }
        )
        
        print(f"✅ Quiz created with {len(questions_data)} questions")
        return quiz
    
    def _generate_fallback_questions(self, module, num_questions):
        """Generate fallback questions"""
        
        concept = module.title.replace(f"Module {module.module_number}: ", "")
        career = module.course.career
        
        templates = [
            {
                "id": "q1",
                "question": f"What is the primary purpose of {concept} in {career}?",
                "options": {
                    "A": f"To understand core principles and applications",
                    "B": f"To memorize definitions without context",
                    "C": f"To avoid using industry tools",
                    "D": f"To work without documentation"
                },
                "correct": "A",
                "explanation": f"{concept} helps professionals understand core principles and apply them effectively."
            },
            {
                "id": "q2",
                "question": f"Which of the following is a best practice when working with {concept}?",
                "options": {
                    "A": f"Skip the fundamentals and jump to advanced topics",
                    "B": f"Follow industry standards and proven methodologies",
                    "C": f"Avoid seeking feedback from experienced colleagues",
                    "D": f"Never document your work or decisions"
                },
                "correct": "B",
                "explanation": f"Following industry standards and proven methodologies is essential when working with {concept}."
            },
            {
                "id": "q3",
                "question": f"What is a common mistake to avoid with {concept}?",
                "options": {
                    "A": f"Practicing hands-on with real examples",
                    "B": f"Following best practices and guidelines",
                    "C": f"Skipping fundamentals and not validating work",
                    "D": f"Collaborating with experienced professionals"
                },
                "correct": "C",
                "explanation": f"Skipping fundamentals and not validating your work are common mistakes that should be avoided."
            },
            {
                "id": "q4",
                "question": f"How does {concept} benefit {career} professionals?",
                "options": {
                    "A": f"It has no practical applications",
                    "B": f"It improves efficiency and decision-making",
                    "C": f"It makes work more complicated",
                    "D": f"It should only be used by experts"
                },
                "correct": "B",
                "explanation": f"{concept} improves efficiency and enables better decision-making for {career} professionals."
            },
            {
                "id": "q5",
                "question": f"What should you do when applying {concept} in practice?",
                "options": {
                    "A": f"Work in isolation without feedback",
                    "B": f"Skip documentation to save time",
                    "C": f"Apply best practices and validate results",
                    "D": f"Avoid testing edge cases"
                },
                "correct": "C",
                "explanation": f"Applying best practices and validating results ensures effective use of {concept}."
            }
        ]
        
        return templates[:num_questions]
    
    def submit_quiz(self, user, quiz, answers):
        """Submit and grade quiz"""
        
        # Create attempt
        attempt = QuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            answers={},  # Will fill this
            score=0,
            passed=False,
            attempted_at=timezone.now()
        )
        
        correct_count = 0
        total_questions = len(quiz.questions)
        results = []
        
        # Grade each question
        for i, question in enumerate(quiz.questions):
            question_id = question['id']
            user_answer = answers.get(f"q_{question_id}", "").strip().upper()
            correct_answer = question['correct'].upper()
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            # Store answer
            attempt.answers[question_id] = user_answer
            
            # Build results
            results.append({
                'question': question['question'],
                'options': question['options'],
                'user_answer': user_answer,
                'correct': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })
        
        # Calculate score
        score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
        passed = score >= quiz.passing_score
        
        # Update attempt
        attempt.score = score
        attempt.passed = passed
        attempt.save()
        
        return {
            'attempt': attempt,
            'score': score,
            'passed': passed,
            'correct': correct_count,
            'total': total_questions,
            'pct': score,
            'results': results
        }
    
    def get_previous_attempts(self, user, quiz):
        """Get previous quiz attempts"""
        return QuizAttempt.objects.filter(
            user=user,
            quiz=quiz
        ).order_by('-attempted_at')[:5]