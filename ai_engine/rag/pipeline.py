# ai_engine/rag/pipeline.py

import json
import os
from pathlib import Path
from .loader import load_documents
from .chunker import chunk_text
from .embeddings import embed
from .vectorstore import VectorStore
from .retriever import retrieve
from ..llm.client import LocalLLM
from ..llm.prompts import (
    COURSE_GENERATION_PROMPT,
    CAREER_ASSESSMENT_PROMPT,
    PROJECT_RECOMMENDATION_PROMPT
)


class RAGPipeline:
    """
    Enhanced RAG Pipeline for course content generation and retrieval.
    Supports document loading, embedding, and intelligent retrieval.
    """

    def __init__(self):
        """Initialize RAG pipeline with course knowledge base"""
        try:
            # Load documents from data folder
            docs = load_documents()
            print(f"✅ Loaded {len(docs)} documents")

            # Chunk documents for better retrieval
            self.chunks = []
            for doc in docs:
                try:
                    doc_chunks = chunk_text(doc)
                    self.chunks.extend(doc_chunks)
                except Exception as e:
                    print(f"⚠️ Error chunking document: {e}")
                    # Add document as-is if chunking fails
                    self.chunks.append(doc)

            print(f"✅ Created {len(self.chunks)} chunks from documents")

            # Create embeddings and vector store
            if self.chunks:
                try:
                    embeddings = embed(self.chunks)
                    self.store = VectorStore(embeddings)
                    print(f"✅ Vector store created with {len(embeddings)} embeddings")
                except Exception as e:
                    print(f"⚠️ Error creating embeddings: {e}")
                    self.store = VectorStore([])
            else:
                print("⚠️ No documents loaded. Creating empty vector store.")
                self.store = VectorStore([])

            # Initialize LLM
            self.llm = LocalLLM()
            print(f"✅ RAG Pipeline initialized successfully")

        except Exception as e:
            print(f"❌ Error initializing RAG Pipeline: {e}")
            import traceback
            traceback.print_exc()

            # Create minimal fallback
            self.chunks = []
            self.store = VectorStore([])
            self.llm = LocalLLM()

    def run(self, query):
        """
        Basic retrieval function (backward compatible)

        Args:
            query: Search query string

        Returns:
            List of relevant document chunks
        """
        return retrieve(query, self.chunks, self.store)

    # ==========================================
    # COURSE GENERATION METHODS
    # ==========================================

    def generate_course_structure(self, career, level, user_traits=None):
        """
        Generate complete course structure using RAG + LLM

        Args:
            career: Target career field (e.g., "Data Science")
            level: Skill level (Beginner/Intermediate/Advanced)
            user_traits: Optional user personality traits for personalization

        Returns:
            Dict with course structure including modules
        """
        # Retrieve relevant course content from knowledge base
        query = f"course modules for {career} at {level} level"
        relevant_docs = self.run(query)

        # Build context from retrieved documents
        context = self._build_context(relevant_docs, max_chunks=5)

        # Generate course using LLM
        course_plan = self._generate_with_llm(
            career=career,
            level=level,
            context=context,
            user_traits=user_traits
        )

        return self._parse_course_structure(course_plan, career, level)

    def generate_module_content(self, module_title, career, level, module_number):
        """
        Generate detailed content for a specific module

        Args:
            module_title: Title of the module
            career: Career field
            level: Skill level
            module_number: Module sequence number

        Returns:
            Dict with theory, exercises, resources, etc.
        """
        # Retrieve relevant content for this module
        query = f"{module_title} {career} {level} tutorial guide"
        relevant_docs = self.run(query)

        context = self._build_context(relevant_docs, max_chunks=3)

        # Generate detailed module content
        prompt = self._create_module_prompt(
            module_title, career, level, module_number, context
        )

        try:
            content = self.llm.generate(prompt)
            return self._parse_module_content(content)
        except Exception as e:
            print(f"Error generating module content: {e}")
            return self._generate_fallback_module(module_title, level)

    def generate_quiz_questions(self, module_title, career, level, num_questions=5):
        """
        Generate quiz questions for a module

        Args:
            module_title: Module title
            career: Career field
            level: Difficulty level
            num_questions: Number of questions to generate

        Returns:
            List of quiz questions with options and answers
        """
        # Retrieve relevant content
        query = f"{module_title} {career} quiz assessment questions"
        relevant_docs = self.run(query)

        context = self._build_context(relevant_docs, max_chunks=3)

        prompt = f"""Generate {num_questions} multiple choice quiz questions for:

Module: {module_title}
Career: {career}
Level: {level}

Context from knowledge base:
{context}

For each question, provide in this EXACT format:

Q1: [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
ANSWER: [Letter]
EXPLANATION: [Brief explanation]

---

Make questions practical and test real understanding, not just memorization.
"""

        try:
            quiz_content = self.llm.generate(prompt)
            return self._parse_quiz_questions(quiz_content)
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return []

    def generate_project_ideas(self, career, level, num_projects=2):
        """
        Generate capstone project ideas

        Args:
            career: Career field
            level: Skill level
            num_projects: Number of project ideas

        Returns:
            List of project descriptions
        """
        # FIXED: Added num_projects parameter
        prompt = PROJECT_RECOMMENDATION_PROMPT.format(
            career=career,
            level=level,
            num_projects=num_projects
        )

        try:
            projects = self.llm.generate(prompt)
            return self._parse_project_ideas(projects)
        except Exception as e:
            print(f"Error generating projects: {e}")
            return self._generate_fallback_projects(career, level)

    # ==========================================
    # HELPER METHODS
    # ==========================================

    def _build_context(self, retrieved_docs, max_chunks=5):
        """Build context string from retrieved documents"""
        if not retrieved_docs:
            return "No specific context available."

        context_parts = []
        for i, doc in enumerate(retrieved_docs[:max_chunks], 1):
            # Extract text content from document
            if isinstance(doc, dict):
                text = doc.get('content', doc.get('text', str(doc)))
            else:
                text = str(doc)

            context_parts.append(f"[{i}] {text[:500]}...")  # Limit each chunk

        return "\n\n".join(context_parts)

    def _generate_with_llm(self, career, level, context, user_traits=None):
        """Generate course plan using LLM"""
        traits_text = ""
        if user_traits:
            top_traits = [t[0] for t in user_traits[:3]]
            traits_text = f"\nUser personality traits: {', '.join(top_traits)}"

        prompt = f"""You are an expert curriculum designer.

Create a structured learning path for:
Career: {career}
Level: {level}{traits_text}

Reference content from knowledge base:
{context}

Generate 6-8 modules in this EXACT format:

MODULE_1: [Clear, descriptive title]
Description: [One line description]
Duration: [e.g., "4-5 hours"]
Skills: [skill1, skill2, skill3]

MODULE_2: [Clear, descriptive title]
Description: [One line description]
Duration: [e.g., "4-5 hours"]
Skills: [skill1, skill2, skill3]

[Continue for all modules...]

COURSE_DURATION: [Total time, e.g., "6 weeks"]
FINAL_PROJECT: [Project title and brief description]

Make the course practical, hands-on, and progressive in difficulty.
"""

        try:
            return self.llm.generate(prompt)
        except Exception as e:
            print(f"Error generating with LLM: {e}")
            return ""

    def _create_module_prompt(self, module_title, career, level, module_number, context):
        """Create prompt for detailed module content generation"""
        return f"""Generate comprehensive content for this course module:

Module Number: {module_number}
Module Title: {module_title}
Career: {career}
Level: {level}

Reference content:
{context}

Generate content in this EXACT format:

LEARNING_OBJECTIVES:
- [Specific, measurable objective 1]
- [Specific, measurable objective 2]
- [Specific, measurable objective 3]

THEORY:
[2-4 paragraphs of clear, practical explanation covering:
- Core concepts and definitions
- Why this matters in {career}
- Key principles to understand
- Common applications]

PRACTICAL_EXERCISES:
1. [Exercise Title]
   Description: [What to do, step by step]
   Expected Outcome: [What they'll learn/build]

2. [Exercise Title]
   Description: [What to do, step by step]
   Expected Outcome: [What they'll learn/build]

RESOURCES:
- [Resource name] | Type: [article/video/tool] | URL: [if available]
- [Resource name] | Type: [article/video/tool] | URL: [if available]
- [Resource name] | Type: [article/video/tool] | URL: [if available]

PREREQUISITES:
[What learners should know before starting this module]

ESTIMATED_TIME:
[e.g., "3-4 hours"]

Make it practical, clear, and actionable for {level} learners.
"""

    def _parse_course_structure(self, course_plan, career, level):
        """Parse LLM output into structured course data"""
        modules = []
        lines = course_plan.split('\n')

        current_module = None
        duration = "6 weeks"
        project_desc = f"Build a complete {career} project showcasing your skills"

        for line in lines:
            line = line.strip()

            if line.startswith('MODULE_'):
                # Save previous module
                if current_module:
                    modules.append(current_module)

                # Extract module title
                title = line.split(':', 1)[1].strip() if ':' in line else line
                current_module = {
                    'module_number': len(modules) + 1,
                    'title': title,
                    'description': '',
                    'duration': '3-4 hours',
                    'skills': []
                }

            elif current_module:
                if line.startswith('Description:'):
                    current_module['description'] = line.split(':', 1)[1].strip()
                elif line.startswith('Duration:'):
                    current_module['duration'] = line.split(':', 1)[1].strip()
                elif line.startswith('Skills:'):
                    skills_text = line.split(':', 1)[1].strip()
                    current_module['skills'] = [s.strip() for s in skills_text.split(',')]

            # Extract course-level info
            if line.startswith('COURSE_DURATION:'):
                duration = line.split(':', 1)[1].strip()
            elif line.startswith('FINAL_PROJECT:'):
                project_desc = line.split(':', 1)[1].strip()

        # Add last module
        if current_module:
            modules.append(current_module)

        # If no modules parsed, use fallback
        if not modules:
            modules = self._get_default_modules(career, level)

        return {
            'title': f"{career} Learning Path - {level}",
            'career': career,
            'level': level,
            'modules': modules,
            'duration': duration,
            'project': project_desc,
            'total_modules': len(modules)
        }

    def _parse_module_content(self, content):
        """Parse module content from LLM output"""
        parsed = {
            'learning_objectives': [],
            'theoretical_content': '',
            'practical_exercises': [],
            'resources': [],
            'prerequisites': '',
            'estimated_time': '3-4 hours'
        }

        sections = {
            'LEARNING_OBJECTIVES': [],
            'THEORY': [],
            'PRACTICAL_EXERCISES': [],
            'RESOURCES': [],
            'PREREQUISITES': [],
            'ESTIMATED_TIME': []
        }

        current_section = None
        lines = content.split('\n')

        for line in lines:
            line_strip = line.strip()

            # Detect section headers
            if 'LEARNING_OBJECTIVES:' in line_strip:
                current_section = 'LEARNING_OBJECTIVES'
            elif 'THEORY:' in line_strip:
                current_section = 'THEORY'
            elif 'PRACTICAL_EXERCISES:' in line_strip:
                current_section = 'PRACTICAL_EXERCISES'
            elif 'RESOURCES:' in line_strip:
                current_section = 'RESOURCES'
            elif 'PREREQUISITES:' in line_strip:
                current_section = 'PREREQUISITES'
            elif 'ESTIMATED_TIME:' in line_strip:
                current_section = 'ESTIMATED_TIME'
            elif current_section and line_strip:
                sections[current_section].append(line_strip)

        # Process sections
        parsed['learning_objectives'] = [
            obj.lstrip('- ').strip()
            for obj in sections['LEARNING_OBJECTIVES']
            if obj.lstrip('- ').strip()
        ]

        parsed['theoretical_content'] = '\n\n'.join(sections['THEORY'])
        parsed['prerequisites'] = ' '.join(sections['PREREQUISITES'])

        if sections['ESTIMATED_TIME']:
            parsed['estimated_time'] = sections['ESTIMATED_TIME'][0]

        # Parse exercises
        exercises = []
        current_ex = None

        for line in sections['PRACTICAL_EXERCISES']:
            if line and line[0].isdigit() and '.' in line:
                if current_ex:
                    exercises.append(current_ex)
                title = line.split('.', 1)[1].strip() if '.' in line else line
                current_ex = {
                    'title': title,
                    'description': '',
                    'outcome': ''
                }
            elif current_ex:
                if 'Description:' in line:
                    current_ex['description'] = line.split('Description:', 1)[1].strip()
                elif 'Expected Outcome:' in line or 'Outcome:' in line:
                    outcome_text = line.split('Outcome:', 1)[1].strip() if 'Outcome:' in line else line
                    current_ex['outcome'] = outcome_text

        if current_ex:
            exercises.append(current_ex)
        parsed['practical_exercises'] = exercises

        # Parse resources
        for line in sections['RESOURCES']:
            if '|' in line:
                parts = [p.strip() for p in line.lstrip('- ').split('|')]
                if len(parts) >= 2:
                    resource = {
                        'name': parts[0],
                        'type': parts[1].replace('Type:', '').strip()
                    }
                    if len(parts) > 2:
                        resource['url'] = parts[2].replace('URL:', '').strip()
                    else:
                        resource['url'] = ''
                    parsed['resources'].append(resource)

        return parsed

    def _parse_quiz_questions(self, quiz_content):
        """Parse quiz questions from LLM output"""
        questions = []
        lines = quiz_content.split('\n')

        current_q = None
        for line in lines:
            line = line.strip()

            if line.startswith('Q') and ':' in line:
                if current_q and current_q.get('question'):
                    questions.append(current_q)
                current_q = {
                    'question': line.split(':', 1)[1].strip(),
                    'options': {},
                    'correct_answer': '',
                    'explanation': ''
                }
            elif current_q:
                if line.startswith(('A)', 'B)', 'C)', 'D)')):
                    letter = line[0]
                    text = line[2:].strip()
                    current_q['options'][letter] = text
                elif line.startswith('ANSWER:'):
                    current_q['correct_answer'] = line.split(':', 1)[1].strip().upper()[0]
                elif line.startswith('EXPLANATION:'):
                    current_q['explanation'] = line.split(':', 1)[1].strip()

        if current_q and current_q.get('question'):
            questions.append(current_q)

        return questions

    def _parse_project_ideas(self, projects_text):
        """Parse project ideas from LLM output"""
        projects = []
        lines = projects_text.split('\n')

        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering/bullets
                project = line.lstrip('0123456789.-) ').strip()
                if project:
                    projects.append(project)

        return projects[:2]  # Limit to 2 projects

    # ==========================================
    # FALLBACK METHODS
    # ==========================================

    def _generate_fallback_module(self, module_title, level):
        """Generate basic module content as fallback"""
        return {
            'learning_objectives': [
                f"Understand the fundamentals of {module_title}",
                f"Apply {module_title} concepts in practice",
                f"Build confidence with {module_title} techniques"
            ],
            'theoretical_content': f"This module covers {module_title}. You will learn the core concepts and practical applications that are essential for mastery at the {level} level.",
            'practical_exercises': [
                {
                    'title': f'Hands-on Practice: {module_title}',
                    'description': 'Complete a practical exercise applying the concepts learned.',
                    'outcome': 'Gain practical experience and deeper understanding'
                }
            ],
            'resources': [
                {'name': 'Additional Reading Materials', 'type': 'article', 'url': ''},
                {'name': 'Video Tutorial', 'type': 'video', 'url': ''}
            ],
            'prerequisites': 'Basic understanding of the field' if level != 'Beginner' else 'None',
            'estimated_time': '3-4 hours'
        }

    def _generate_fallback_projects(self, career, level):
        """Generate fallback project ideas"""
        return [
            f"Build a complete {career} application showcasing core skills",
            f"Create a portfolio project demonstrating {level} level proficiency"
        ]

    def _get_default_modules(self, career, level):
        """Default module templates as fallback"""
        return [
            {
                'module_number': 1,
                'title': f'Introduction to {career}',
                'description': 'Get started with the fundamentals',
                'duration': '2-3 hours',
                'skills': ['basics', 'fundamentals']
            },
            {
                'module_number': 2,
                'title': 'Core Concepts and Principles',
                'description': 'Deep dive into essential concepts',
                'duration': '4-5 hours',
                'skills': ['core concepts', 'principles']
            },
            {
                'module_number': 3,
                'title': 'Practical Applications',
                'description': 'Apply what you learned in real scenarios',
                'duration': '5-6 hours',
                'skills': ['application', 'practice']
            },
            {
                'module_number': 4,
                'title': 'Advanced Techniques',
                'description': 'Master advanced methods and best practices',
                'duration': '6-7 hours',
                'skills': ['advanced', 'optimization']
            },
            {
                'module_number': 5,
                'title': 'Real-World Projects',
                'description': 'Build portfolio-worthy projects',
                'duration': '8-10 hours',
                'skills': ['project building', 'integration']
            },
            {
                'module_number': 6,
                'title': 'Industry Best Practices',
                'description': 'Learn professional standards and workflows',
                'duration': '3-4 hours',
                'skills': ['best practices', 'professional standards']
            }
        ]


# ==========================================
# CONVENIENCE FUNCTION (backward compatible)
# ==========================================
def create_rag_pipeline():
    """Factory function to create RAG pipeline instance"""
    return RAGPipeline()