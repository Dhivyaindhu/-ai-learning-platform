# ai_engine/services/assessment_service.py
# ENHANCED VERSION - Truly Dynamic, Non-Repeating Questions

from ..llm.llm_engine import LLMEngine
from ..psychology.traits import PERSONALITY_TRAITS
from ..psychology.scoring import calculate_trait_scores
import random


class AssessmentService:
    """
    Handles conversational personality assessment with TRULY ADAPTIVE questions
    - Questions never repeat
    - Each question builds on previous answers
    - Deep extraction of personality and interests
    """

    def __init__(self):
        try:
            self.llm_engine = LLMEngine()
            print("✅ LLM Engine initialized successfully")
        except Exception as e:
            print(f"⚠️ LLM Engine initialization failed: {e}")
            self.llm_engine = None

        self.max_questions = 10

    def start_assessment(self):
        """Initialize a new assessment session"""
        return {
            'question_count': 0,
            'max_questions': self.max_questions,
            'answers': [],
            'trait_sequence': self._generate_trait_sequence(),
            'asked_questions': [],  # Track all questions asked to prevent repeats
            'user_insights': {}  # Store insights extracted from answers
        }

    def _generate_trait_sequence(self):
        """Generate balanced sequence of traits to assess"""
        traits = list(PERSONALITY_TRAITS.keys())
        sequence = []
        sequence.extend(traits)

        while len(sequence) < self.max_questions:
            sequence.append(random.choice(traits))

        random.shuffle(sequence)
        return sequence[:self.max_questions]

    def get_next_question(self, session_data):
        """
        Generate TRULY ADAPTIVE question that:
        1. Never repeats previous questions
        2. Builds on insights from previous answers
        3. Extracts deeper personality information
        """
        current_index = session_data['question_count']
        trait = session_data['trait_sequence'][current_index]
        trait_info = PERSONALITY_TRAITS[trait]

        # Build deep context from all previous answers
        deep_context = self._build_deep_context(session_data)

        # Generate unique question
        max_attempts = 3
        question_text = None

        for attempt in range(max_attempts):
            try:
                if self.llm_engine:
                    question_text = self._generate_unique_adaptive_question(
                        trait,
                        trait_info,
                        deep_context,
                        session_data['asked_questions'],
                        current_index
                    )

                    # Check if question is truly unique
                    if self._is_question_unique(question_text, session_data['asked_questions']):
                        print(f"✅ Generated UNIQUE adaptive question for {trait}")
                        print(f"   Q{current_index + 1}: {question_text[:70]}...")
                        break
                    else:
                        print(f"⚠️ Question too similar, regenerating... (attempt {attempt + 1})")
                        question_text = None
                else:
                    raise ValueError("LLM engine not available")

            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                question_text = None

        # If LLM failed, use intelligent fallback
        if not question_text:
            print(f"📝 Using intelligent fallback for {trait}")
            question_text = self._get_intelligent_fallback_question(
                trait,
                trait_info,
                session_data,
                current_index
            )

        # Store the question to prevent repeats
        session_data['asked_questions'].append(question_text.lower())

        return {
            'id': f'q_{current_index + 1}',
            'trait': trait,
            'question': question_text,
            'trait_name': trait_info['name']
        }

    def _build_deep_context(self, session_data):
        """
        Build rich context from previous answers including:
        - What user values
        - How they behave
        - Their interests and preferences
        """
        if not session_data['answers']:
            return "This is the first question. The user has not provided any information yet."

        context_parts = []
        context_parts.append("INSIGHTS FROM PREVIOUS ANSWERS:")
        context_parts.append("")

        # Get recent answers with insights
        recent_answers = session_data['answers'][-3:]

        for i, ans in enumerate(recent_answers, 1):
            trait_name = PERSONALITY_TRAITS[ans['trait']]['name']
            answer_preview = ans['answer'][:150]

            context_parts.append(f"{i}. {trait_name}:")
            context_parts.append(f"   User said: \"{answer_preview}...\"")
            context_parts.append(f"   Score: {ans.get('score', 'N/A')}/10")
            context_parts.append("")

        # Add extracted insights if available
        if session_data.get('user_insights'):
            context_parts.append("KEY INSIGHTS ABOUT USER:")
            for key, value in session_data['user_insights'].items():
                context_parts.append(f"- {key}: {value}")

        return "\n".join(context_parts)

    def _generate_unique_adaptive_question(self, trait, trait_info, context, asked_questions, question_num):
        """
        Generate truly unique adaptive question using LLM
        """
        # Build list of previous questions to avoid
        previous_questions = "\n".join([f"- {q}" for q in asked_questions[-5:]])

        prompt = f"""You are conducting a deep personality assessment. Generate question #{question_num + 1} to assess {trait_info['name']}.

{context}

IMPORTANT RULES:
1. DO NOT ask any question similar to these previous questions:
{previous_questions}

2. Build on what you learned from their previous answers
3. Ask about SPECIFIC situations, behaviors, or real-life examples
4. Make the question conversational and natural
5. The question should reveal deeper aspects of their {trait}
6. Avoid generic questions - be specific and personal
7. Keep it under 30 words
8. The question must be completely different from any previous question

Generate ONLY the question text, nothing else."""

        try:
            question = self.llm_engine.generate_text(prompt, max_tokens=150)
            return question.strip()
        except Exception as e:
            raise ValueError(f"LLM generation failed: {e}")

    def _is_question_unique(self, new_question, asked_questions):
        """
        Check if question is sufficiently different from previous questions
        """
        if not new_question or not asked_questions:
            return True

        new_q_lower = new_question.lower()

        # Check for exact duplicates
        if new_q_lower in asked_questions:
            return False

        # Check for very similar questions (word overlap)
        new_words = set(new_q_lower.split())

        for asked in asked_questions:
            asked_words = set(asked.split())

            # Calculate overlap
            overlap = len(new_words & asked_words)
            overlap_ratio = overlap / len(new_words) if len(new_words) > 0 else 0

            # If more than 50% word overlap, too similar
            if overlap_ratio > 0.5:
                return False

        return True

    def _get_intelligent_fallback_question(self, trait, trait_info, session_data, question_num):
        """
        Intelligent fallback questions that still adapt to context
        """
        # Different question templates based on what we already know
        templates = {
            'openness': [
                "Tell me about the most unconventional decision you've made in the past year.",
                "Describe a situation where you had to learn something completely outside your expertise.",
                "What's something you're curious about that most people wouldn't understand?",
                "How do you react when your established routine gets disrupted?",
                "Tell me about a time you challenged conventional wisdom or traditional approaches."
            ],
            'conscientiousness': [
                "Walk me through how you planned and executed your last major project.",
                "Describe a goal you set for yourself. How did you track your progress?",
                "Tell me about a time you had competing priorities. How did you handle it?",
                "What systems or methods do you use to stay organized in your daily life?",
                "Describe a situation where attention to detail was crucial."
            ],
            'extraversion': [
                "Describe your energy levels before, during, and after a large social event.",
                "Tell me about a situation where you had to work alone for an extended period.",
                "How do you prefer to celebrate personal achievements?",
                "Describe a typical weekend for you - who's involved and what do you do?",
                "Tell me about a time you had to present ideas to a group."
            ],
            'agreeableness': [
                "Describe a recent disagreement you had. How did you handle it?",
                "Tell me about a time someone asked you for help at an inconvenient time.",
                "How do you respond when someone criticizes your work or ideas?",
                "Describe a situation where you had to choose between being liked and being right.",
                "Tell me about a time you worked with someone whose values differed from yours."
            ],
            'neuroticism': [
                "Describe how you handled the most stressful week you've had recently.",
                "Tell me about a time something didn't go as planned. What went through your mind?",
                "How do you typically respond when you're worried about something?",
                "Describe your thought process when facing an uncertain outcome.",
                "Tell me about techniques you use when feeling overwhelmed."
            ]
        }

        # Get available questions for this trait
        available = templates.get(trait, [
            f"Tell me about a specific experience related to {trait_info['name'].lower()}."
        ])

        # Filter out any that are too similar to asked questions
        unique_options = []
        for q in available:
            if self._is_question_unique(q, session_data['asked_questions']):
                unique_options.append(q)

        if unique_options:
            return random.choice(unique_options)
        else:
            # Last resort - create a completely custom question
            number = random.randint(1, 1000)
            return f"Thinking about your {trait_info['name'].lower()}, describe a specific recent situation that best illustrates how you approach life (example #{number})."

    def submit_answer(self, session_data, trait, question, answer):
        """
        Record answer, extract insights, and score
        """
        # Analyze answer deeply
        score = self._analyze_answer_deeply(trait, answer, session_data)

        # Extract insights from answer
        insights = self._extract_insights(answer, trait)

        # Store insights for future questions
        if insights:
            session_data['user_insights'].update(insights)

        # Store answer with all metadata
        session_data['answers'].append({
            'trait': trait,
            'question': question,
            'answer': answer,
            'word_count': len(answer.split()),
            'score': score,
            'question_number': session_data['question_count'] + 1,
            'insights': insights
        })

        session_data['question_count'] += 1

        return score

    def _analyze_answer_deeply(self, trait, answer, session_data):
        """
        Deep analysis of answer using LLM with full context
        """
        try:
            if not self.llm_engine:
                raise ValueError("LLM not available")

            # Build context of previous answers
            context = ""
            if len(session_data['answers']) > 0:
                context = f"\nPrevious answers suggest certain patterns. Consider the overall personality emerging from all responses."

            prompt = f"""Analyze this personality assessment answer for {trait}.{context}

Answer: "{answer}"

On a scale of 1-10, rate how strongly this answer demonstrates the trait of {trait}:
- 1-2: Very low (opposite traits strongly evident)
- 3-4: Low (some opposite traits)
- 5-6: Moderate/balanced
- 7-8: High (trait clearly evident)
- 9-10: Very high (trait dominant)

Consider:
- Specific behaviors described
- Underlying values revealed
- Emotional responses shown
- Decision-making patterns

Respond with ONLY a number 1-10."""

            score_text = self.llm_engine.generate_text(prompt, max_tokens=10)
            score = int(''.join(filter(str.isdigit, score_text)))

            if 1 <= score <= 10:
                print(f"✅ Deep analysis: {score}/10 for {trait}")
                return score
            else:
                raise ValueError("Score out of range")

        except Exception as e:
            print(f"⚠️ Deep analysis failed: {e}")
            score = self._keyword_analysis(trait, answer)
            print(f"📝 Keyword analysis: {score}/10")
            return score

    def _extract_insights(self, answer, trait):
        """
        Extract key insights about user from their answer
        """
        insights = {}
        answer_lower = answer.lower()

        # Extract interests mentioned
        interest_keywords = ['love', 'enjoy', 'passion', 'interested', 'hobby', 'like']
        for keyword in interest_keywords:
            if keyword in answer_lower:
                # User expressed an interest
                insights[f'interest_{trait}'] = f"Shows interest patterns related to {trait}"
                break

        # Extract behavioral patterns
        behavior_keywords = ['always', 'usually', 'typically', 'tend to', 'often']
        for keyword in behavior_keywords:
            if keyword in answer_lower:
                insights[f'behavior_{trait}'] = f"Consistent behavior pattern for {trait}"
                break

        # Extract values
        value_keywords = ['important', 'value', 'believe', 'principle', 'matter']
        for keyword in value_keywords:
            if keyword in answer_lower:
                insights[f'values_{trait}'] = f"Strong values related to {trait}"
                break

        return insights

    def _keyword_analysis(self, trait, answer):
        """Enhanced keyword-based scoring with context awareness"""
        word_count = len(answer.split())
        base_score = min(7, 4 + (word_count // 20))

        keywords = {
            'openness': ['new', 'creative', 'imagine', 'explore', 'curious', 'different', 'unique', 'unusual',
                         'innovative'],
            'conscientiousness': ['organized', 'plan', 'schedule', 'goal', 'complete', 'responsible', 'detail',
                                  'systematic'],
            'extraversion': ['people', 'social', 'party', 'friends', 'energy', 'outgoing', 'talk', 'group',
                             'interaction'],
            'agreeableness': ['help', 'cooperate', 'kind', 'empathy', 'team', 'compromise', 'care', 'understanding'],
            'neuroticism': ['worry', 'stress', 'anxious', 'nervous', 'overwhelm', 'fear', 'concern', 'pressure']
        }

        answer_lower = answer.lower()
        for word in keywords.get(trait, []):
            if word in answer_lower:
                base_score += 0.5

        return int(max(1, min(10, base_score)))

    def is_complete(self, session_data):
        """Check if assessment is complete"""
        return session_data['question_count'] >= session_data['max_questions']

    def generate_profile(self, session_data):
        """Generate deep personality profile with insights"""
        trait_scores = calculate_trait_scores(session_data['answers'])

        sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
        level = self._determine_level(trait_scores)

        try:
            characterization = self._generate_deep_profile(sorted_traits, session_data)
            print("✅ Generated deep personality profile")
        except Exception as e:
            print(f"⚠️ Deep profile failed: {e}")
            characterization = self._get_template_characterization(sorted_traits)

        careers = self._recommend_careers(sorted_traits)

        return {
            'traits': [(trait, score) for trait, score in sorted_traits],
            'level': level,
            'characterism': characterization,
            'career_recommendations': careers,
            'insights': session_data.get('user_insights', {})
        }

    def _generate_deep_profile(self, sorted_traits, session_data):
        """Generate deep characterization using actual answers and insights"""
        if not self.llm_engine:
            raise ValueError("LLM not available")

        top_traits = sorted_traits[:3]

        # Get sample quotes
        sample_quotes = []
        for ans in session_data['answers'][-5:]:
            sample_quotes.append(f"'{ans['answer'][:100]}...'")

        prompt = f"""Based on this personality assessment, write a personal characterization:

Top Traits: {', '.join([f"{PERSONALITY_TRAITS[t]['name']} ({s}/10)" for t, s in top_traits])}

Sample Responses:
{chr(10).join(sample_quotes)}

Write 3-4 sentences that:
- Feel personal and specific to this individual
- Highlight their unique strengths
- Reference their actual behaviors/values shown
- Are encouraging and insightful
- Use "you" language

Keep it authentic and under 120 words."""

        summary = self.llm_engine.generate_text(prompt, max_tokens=250)
        return {'llm_summary': summary.strip(), 'summary': summary.strip()}

    def _get_template_characterization(self, sorted_traits):
        """Fallback characterization"""
        top_trait = sorted_traits[0][0]
        templates = {
            'openness': "You have a creative and curious mind that thrives on new experiences.",
            'conscientiousness': "You are organized and reliable with strong attention to detail.",
            'extraversion': "You draw energy from social connections and enjoy engaging with others.",
            'agreeableness': "You have a compassionate approach and value harmonious relationships.",
            'neuroticism': "You are emotionally aware and thoughtful in your responses."
        }
        summary = templates.get(top_trait, "You have a unique personality profile.")
        return {'llm_summary': summary, 'summary': summary}

    def _determine_level(self, trait_scores):
        """Determine difficulty level"""
        avg_score = sum(trait_scores.values()) / len(trait_scores)
        if avg_score >= 7:
            return 'advanced'
        elif avg_score >= 5:
            return 'intermediate'
        else:
            return 'beginner'

    def _recommend_careers(self, sorted_traits):
        """Recommend careers based on trait profile"""
        career_map = {
            'openness': ['UI/UX Designer', 'Content Creator', 'Research Scientist', 'Innovation Consultant'],
            'conscientiousness': ['Project Manager', 'Data Analyst', 'Software Engineer', 'Operations Manager'],
            'extraversion': ['Sales Manager', 'Marketing Specialist', 'Event Coordinator', 'Business Development'],
            'agreeableness': ['Human Resources', 'Counselor', 'Teacher', 'Healthcare Provider'],
            'neuroticism': ['Psychologist', 'Writer', 'Quality Analyst', 'Editor']
        }

        recommended = []
        for trait, score in sorted_traits[:3]:
            recommended.extend(career_map.get(trait, [])[:3])

        seen = set()
        unique = [c for c in recommended if not (c in seen or seen.add(c))]
        return unique[:10]