# ai_engine/llm/prompts.py
# COMPLETE VERSION - ALL prompts for entire system

# ======================================================
# CAREER ASSESSMENT - OPTIMIZED FOR QWEN 0.5B
# ======================================================

# Strategy 1: With Example (BEST for 0.5B)
WITH_EXAMPLE_PROMPT = """Example:
Q: What is Python?
A) A programming language for data science
B) Only a web framework
C) A database system
D) A text editor

Now write {difficulty} question about {topic} for {career}:

Q:"""

# Strategy 2: Ultra-Simple
ULTRA_SIMPLE_PROMPT = """Topic: {topic}
Career: {career}

Q: [question?]
A) [answer]
B) [answer]
C) [answer]
D) [answer]

Write:

Q:"""

# Strategy 3: Forced Format
FORCED_FORMAT_PROMPT = """Write quiz for {career} about {topic}.

EXACT format:

Q: [question?]
A) [answer]
B) [answer]
C) [answer]
D) [answer]

Q:"""

# Default for career assessment
DEFAULT_CAREER_PROMPT = WITH_EXAMPLE_PROMPT


# ======================================================
# ADAPTIVE PSYCHOMETRIC QUESTION GENERATION
# ======================================================

ADAPTIVE_PSYCHOLOGY_QUESTION_PROMPT = """You are conducting a personality assessment.

Context: {previous_responses}
Avoid: {previous_questions}
Focus: {trait}

Ask ONE question (18-30 words) about a work or life situation.
Do NOT use psychology terms.

Question:"""


# ======================================================
# INDIVIDUAL ANSWER ANALYSIS (TRAIT SCORING)
# ======================================================

ANALYZE_ANSWER_PROMPT = """Analyze this response for {trait}.

Question: {question}
Answer: {answer}

Rate 1-5 based on clarity, confidence, initiative, examples.

Score:"""


# ======================================================
# FINAL PERSONALITY & CAREER ANALYSIS
# ======================================================

PERSONALITY_ANALYSIS_PROMPT = """Assessment complete: {total_questions} questions

Scores: {trait_scores}
Responses: {user_responses}

Write analysis:

PERSONALITY OVERVIEW:
[2-3 sentences]

CORE STRENGTHS:
- Strength 1
- Strength 2
- Strength 3

DEVELOPMENT AREAS:
- Area 1
- Area 2

SUGGESTED CAREER DOMAINS:
1. Career - reason
2. Career - reason
3. Career - reason
4. Career - reason
5. Career - reason

WORK STYLE PREFERENCE:
[Environment and collaboration]

CAREER GUIDANCE:
[Next steps]

Analysis:"""


# ======================================================
# CAREER-SPECIFIC EXPLORATION QUESTIONS
# ======================================================

CAREER_EXPLORATION_PROMPT = """Career: {career}
Personality: {personality_summary}
Avoid: {previous_questions}
Question #{question_number}

Ask ONE question about interest in {career}:

Question:"""


# ======================================================
# CAREER READINESS & FIT EVALUATION
# ======================================================

CAREER_FIT_ANALYSIS_PROMPT = """Evaluate fit for {career}

Responses: {all_responses}
Personality: {personality_summary}

Rate 0-100:

OVERALL READINESS: ___%

SCORES:
Interest: __/100
Experience: __/100
Skills: __/100
Understanding: __/100
Motivation: __/100

STRENGTHS:
- Point 1
- Point 2

GROWTH AREAS:
- Area 1
- Area 2

OBSERVATIONS:
[1-2 paragraphs]

RECOMMENDATION:
READY / PARTIALLY READY / NEEDS PREPARATION

ACTIONS:
1. Action
2. Action
3. Action

Evaluation:"""


# ======================================================
# RAG-BASED PERSONALIZED COURSE GENERATION
# ======================================================

PERSONALIZED_COURSE_PROMPT = """Design {career} course for {level} level.

Profile:
- Strengths: {strengths}
- Development: {development_areas}
- Readiness: {readiness_score}%

Create learning path:

TITLE:
[Professional title]

DURATION:
[Weeks + hours]

OBJECTIVE:
[What learner will do]

MODULE 1 – FOUNDATIONS
Topics:
- Topic 1
- Topic 2
Practice:
- Task

MODULE 2 – CORE SKILLS
Topics:
- Topic 1
- Topic 2
Practice:
- Task

MODULE 3 – ADVANCED
Topics:
- Topic 1
- Topic 2
Practice:
- Task

CAPSTONE:
[Project]

OUTCOMES:
- Skill 1
- Skill 2
- Portfolio ready

Course:"""


# ======================================================
# FOLLOW-UP REFLECTION QUESTION
# ======================================================

FOLLOWUP_QUESTION_PROMPT = """User said: "{previous_answer}"

Original: "{original_question}"
Focus: {trait}
Avoid: {previous_questions}

Ask ONE follow-up:

Question:"""


# ======================================================
# CAREER SKILL ASSESSMENT (LEGACY)
# ======================================================

CAREER_ASSESSMENT_QUESTION_PROMPT = """Create assessment for {career}.

Difficulty: {difficulty}
Skill: {skill_focus}
Context: {context}

FORMAT (JSON):
{{
  "question": "Question text",
  "options": {{
    "A": "Best answer",
    "B": "Plausible wrong",
    "C": "Common mistake",
    "D": "Incorrect"
  }},
  "correct_answer": "A",
  "explanation": "Why A is best",
  "topic": "Skill name"
}}

Question:"""


# ======================================================
# COURSE GENERATION (REQUIRED BY RAG PIPELINE)
# ======================================================

COURSE_GENERATION_PROMPT = """Design a comprehensive {career} course for {level} level.

Profile:
- Strengths: {strengths}
- Development needs: {development_areas}
- Readiness: {readiness_score}%

Create industry-aligned learning path:

TITLE:
[Professional course title]

DURATION:
[Total weeks + weekly hours]

OBJECTIVE:
[What learner will be able to do professionally]

MODULE 1 – FOUNDATIONS
Topics:
- Topic 1
- Topic 2
Practice:
- Hands-on task

MODULE 2 – CORE SKILLS
Topics:
- Topic 1
- Topic 2
Practice:
- Applied task

MODULE 3 – ADVANCED
Topics:
- Topic 1
- Topic 2
Practice:
- Real-world task

CAPSTONE:
[Industry-style project]

OUTCOMES:
- Skill 1
- Skill 2
- Portfolio ready

Course:"""


# ======================================================
# MODULE GENERATION (REQUIRED BY RAG PIPELINE)
# ======================================================

MODULE_GENERATION_PROMPT = """Create detailed module content for {career} course.

Module: {module_title}
Level: {difficulty}
Context: {context}

Create comprehensive module:

MODULE TITLE:
[Clear, professional title]

LEARNING OBJECTIVES:
- Objective 1
- Objective 2
- Objective 3

THEORY CONTENT:
[Detailed explanation of concepts]

PRACTICAL EXERCISES:
1. Exercise 1 - [description]
2. Exercise 2 - [description]
3. Exercise 3 - [description]

KEY TAKEAWAYS:
- Takeaway 1
- Takeaway 2

Module:"""


# ======================================================
# CAREER ASSESSMENT PROMPT (REQUIRED BY RAG PIPELINE)
# ======================================================

CAREER_ASSESSMENT_PROMPT = """Create a {difficulty} assessment question for {career}.

Topic: {topic}
Context: {context}

Generate ONE multiple-choice question:

Q: [Question about {topic}?]
A) [Correct answer]
B) [Plausible wrong answer]
C) [Common misconception]
D) [Obviously wrong answer]

Q:"""


# ======================================================
# PROJECT RECOMMENDATION (REQUIRED BY RAG PIPELINE)
# ======================================================

PROJECT_RECOMMENDATION_PROMPT = """Generate {num_projects} capstone project ideas for {career} at {level} level.

Requirements:
- Projects should be practical and portfolio-worthy
- Appropriate for {level} skill level
- Demonstrate real-world application
- Can be completed in 2-4 weeks

Format:
1. [Project Title]
   Description: [2-3 sentences about the project]
   Skills Demonstrated: [list key skills]

2. [Project Title]
   Description: [2-3 sentences about the project]
   Skills Demonstrated: [list key skills]

Projects:"""


# ======================================================
# RETRIEVAL AUGMENTED GENERATION (RAG) PROMPTS
# ======================================================

RAG_CONTEXT_PROMPT = """Based on the following reference material:

{context}

{instruction}

Response:"""


RAG_QUESTION_GENERATION_PROMPT = """Using this reference material:

{context}

Create a {difficulty} quiz question about {topic} for {career}.

Q:"""