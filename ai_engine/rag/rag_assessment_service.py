# ai_engine/services/rag_assessment_service.py
# RAG-BASED Career Assessment with Vector Retrieval

from ..llm.llm_engine import get_llm_engine
from ..rag.embeddings import get_embedding
from ..rag.vectorstore import VectorStore
import random
import re
import json
import numpy as np
from pathlib import Path


class RAGAssessmentService:
    """
    RAG-Enhanced Career Assessment Service
    
    Uses Retrieval-Augmented Generation:
    1. Load high-quality question examples into vector DB
    2. For each question, retrieve similar examples
    3. Use examples to guide LLM generation
    4. Validate and score generated questions
    """

    def __init__(self):
        self.llm = get_llm_engine()
        self.vector_store = None
        self._load_knowledge_base()
        print("🚀 RAG Assessment Service initialized")

    def _load_knowledge_base(self):
        """Load assessment questions into vector database"""
        try:
            # Load question bank
            kb_path = Path(__file__).parent.parent / 'rag' / 'data' / 'assessment_questions.json'
            
            if not kb_path.exists():
                print(f"⚠️ Knowledge base not found at {kb_path}")
                self.vector_store = None
                return
            
            with open(kb_path, 'r') as f:
                self.knowledge_base = json.load(f)
            
            # Initialize vector store
            self.vector_store = VectorStore(collection_name="assessment_questions")
            
            # Index all questions
            documents = []
            metadatas = []
            
            for career, difficulties in self.knowledge_base.items():
                for difficulty, questions in difficulties.items():
                    for q in questions:
                        # Create searchable text
                        text = f"{q['topic']} {difficulty} {career} {q['question']} {' '.join(q['keywords'])}"
                        
                        documents.append(text)
                        metadatas.append({
                            'id': q['id'],
                            'career': career,
                            'difficulty': difficulty,
                            'topic': q['topic'],
                            'question': q['question'],
                            'options': json.dumps(q['options']),
                            'explanation': q['explanation'],
                        })
            
            # Add to vector store
            self.vector_store.add_documents(documents, metadatas)
            print(f"✅ Loaded {len(documents)} questions into vector DB")
            
        except Exception as e:
            print(f"⚠️ Failed to load knowledge base: {e}")
            self.vector_store = None

    def start_career_assessment(self, career, total_questions=15):
        random.seed()
        difficulty_plan = ["beginner"] * 5 + ["intermediate"] * 5 + ["advanced"] * 5
        random.shuffle(difficulty_plan)
        return {
            "career": career,
            "max_questions": total_questions,
            "question_count": 0,
            "used_topics": [],
            "used_question_ids": [],
            "answers": [],
            "difficulty_plan": difficulty_plan,
            "performance_tracking": {
                "beginner": {"correct": 0, "total": 0},
                "intermediate": {"correct": 0, "total": 0},
                "advanced": {"correct": 0, "total": 0},
            },
            "completed": False,
            "llm_attempts": 0,
            "llm_success": 0,
            "rag_retrievals": 0,
        }

    def is_complete(self, sd):
        return sd["question_count"] >= sd["max_questions"]

    def get_next_question(self, sd):
        if self.is_complete(sd):
            return None
        
        idx = sd["question_count"]
        if "current_question" in sd:
            return sd["current_question"]
        
        diff = sd["difficulty_plan"][idx]
        career = sd["career"]
        topic = self._get_topic(career, diff, sd["used_topics"])
        sd["used_topics"].append(topic)
        
        print(f"\n{'='*70}\n🎯 Q{idx+1}/15: {career} | {topic} | {diff.upper()}\n{'='*70}")
        
        # RAG-ENHANCED GENERATION
        question = self._generate_with_rag(career, topic, diff, idx + 1, sd)
        
        if question:
            sd["llm_success"] += 1
            print(f"   ✅ RAG-enhanced generation successful")
        else:
            print(f"   ⚠️ RAG generation failed, using emergency template")
            question = self._emergency_template(career, topic, diff, idx + 1)
        
        # Randomize correct answer
        shuffled, correct = self._shuffle(question["options"])
        question["options"] = shuffled
        question["correct_answer"] = correct
        sd["current_question"] = question
        
        print(f"\n   Q: {question['question'][:70]}...")
        print(f"   🔀 Correct: {correct}")
        return question

    def _generate_with_rag(self, career, topic, diff, qn, sd):
        """
        RAG-ENHANCED GENERATION PIPELINE:
        1. Retrieve similar questions from vector DB
        2. Use them as few-shot examples for LLM
        3. Generate new question with better context
        4. Validate quality
        """
        
        # Step 1: Retrieve similar examples
        examples = self._retrieve_similar_questions(career, topic, diff)
        sd["rag_retrievals"] += len(examples)
        
        print(f"   📚 Retrieved {len(examples)} similar examples from RAG")
        
        # Step 2: Try multiple strategies with RAG
        for attempt in range(1, 4):
            sd["llm_attempts"] += 1
            print(f"\n   🔄 RAG Strategy {attempt}/3...")
            
            if attempt == 1:
                question = self._rag_strategy_fewshot(career, topic, diff, qn, examples)
            elif attempt == 2:
                question = self._rag_strategy_template(career, topic, diff, qn, examples)
            else:
                question = self._rag_strategy_hybrid(career, topic, diff, qn, examples)
            
            if question:
                print(f"   ✅ RAG strategy {attempt} succeeded")
                return question
        
        return None

    def _retrieve_similar_questions(self, career, topic, difficulty):
        """Retrieve similar questions from vector database"""
        if not self.vector_store:
            return []
        
        try:
            # Create query text
            query = f"{topic} {difficulty} {career}"
            
            # Search vector DB
            results = self.vector_store.similarity_search(query, k=3)
            
            examples = []
            for result in results:
                meta = result['metadata']
                examples.append({
                    'question': meta['question'],
                    'options': json.loads(meta['options']),
                    'topic': meta['topic'],
                    'difficulty': meta['difficulty'],
                })
            
            return examples
            
        except Exception as e:
            print(f"   ⚠️ RAG retrieval error: {e}")
            return []

    def _rag_strategy_fewshot(self, career, topic, diff, qn, examples):
        """Strategy 1: Few-shot learning with retrieved examples"""
        
        if not examples:
            return None
        
        # Build prompt with examples
        prompt = "Here are examples of good quiz questions:\n\n"
        
        for i, ex in enumerate(examples[:2], 1):
            prompt += f"Example {i}:\n"
            prompt += f"Q: {ex['question']}\n"
            for letter, text in ex['options'].items():
                prompt += f"{letter}) {text}\n"
            prompt += "\n"
        
        prompt += f"Now create a {diff} question about {topic} for {career}:\n\nQ:"
        
        return self._try_generate_and_parse(prompt, topic, career, diff, qn, "rag_fewshot")

    def _rag_strategy_template(self, career, topic, diff, qn, examples):
        """Strategy 2: Use example as template"""
        
        if not examples:
            return None
        
        template = examples[0]
        
        prompt = f"""Based on this example structure:

Q: {template['question']}
A) {template['options']['A']}
B) {template['options']['B']}
C) {template['options']['C']}
D) {template['options']['D']}

Create a similar {diff} question about {topic} for {career}:

Q:"""
        
        return self._try_generate_and_parse(prompt, topic, career, diff, qn, "rag_template")

    def _rag_strategy_hybrid(self, career, topic, diff, qn, examples):
        """Strategy 3: Hybrid - examples + explicit instructions"""
        
        prompt = f"""Create a {diff} quiz question about {topic} for {career}.

Format:
Q: [Clear question about {topic}?]
A) [Correct answer - detailed and accurate]
B) [Plausible but incomplete answer]
C) [Common misconception]
D) [Clearly incorrect option]

Q:"""
        
        return self._try_generate_and_parse(prompt, topic, career, diff, qn, "rag_hybrid")

    def _try_generate_and_parse(self, prompt, topic, career, diff, qn, strategy_name):
        """Generate and parse with validation"""
        try:
            response = self.llm.generate(prompt, max_length=350)
            
            if len(response) < 30:
                print(f"      ⚠️ {strategy_name}: Too short ({len(response)} chars)")
                return None
            
            print(f"      📝 {strategy_name}: Generated {len(response)} chars")
            
            return self._parse(response, topic, career, diff, qn, strategy_name)
            
        except Exception as e:
            print(f"      ❌ {strategy_name}: Error - {e}")
            return None

    def _parse(self, text, topic, career, diff, qn, source):
        """Parse with strict validation"""
        
        # Extract question
        q = self._extract_question(text, topic, career, diff)
        if not q:
            return None
        
        # Extract options
        opts = self._extract_options(text)
        if len(opts) != 4:
            print(f"      ✗ Only {len(opts)} options found")
            return None
        
        # Validate options
        if not self._validate_options(opts, q, topic):
            return None
        
        # Calculate quality score
        score = self._score_question(q, opts, topic, career)
        print(f"      📊 Quality score: {score}/100")
        
        if score < 60:
            print(f"      ✗ Quality too low ({score})")
            return None
        
        print(f"      ✅ High-quality question (score: {score})")
        
        return {
            "id": f"q_{qn}",
            "question": q,
            "options": opts,
            "correct_answer": "A",
            "explanation": f"{topic} is important for {career}.",
            "topic": topic,
            "difficulty": diff,
            "career": career,
            "source": f"rag_{source}",
            "quality_score": score,
        }

    def _score_question(self, question, options, topic, career):
        """Score question quality (0-100)"""
        score = 100
        
        # Check question quality
        if len(question) < 20:
            score -= 20
        if len(question) > 200:
            score -= 10
        if '?' not in question:
            score -= 15
        
        # Check options quality
        option_lengths = [len(opt) for opt in options.values()]
        avg_length = sum(option_lengths) / 4
        
        if avg_length < 15:
            score -= 20
        if avg_length > 150:
            score -= 10
        
        # Check for variation in option lengths
        length_variance = np.var(option_lengths)
        if length_variance < 10:  # Too similar
            score -= 15
        
        # Check topic relevance
        topic_words = topic.lower().split()
        question_lower = question.lower()
        
        topic_mentions = sum(1 for word in topic_words if word in question_lower)
        if topic_mentions == 0:
            score -= 25
        
        return max(0, score)

    def _extract_question(self, text, topic, career, diff):
        """Extract question text"""
        m = re.search(r'Q:\s*(.+?\?)', text, re.I|re.DOTALL)
        if m:
            q = ' '.join(m.group(1).split())
            if 15 < len(q) < 250:
                return q
        
        for line in text.split('\n'):
            line = line.strip()
            if line.endswith('?') and 20 < len(line) < 200:
                if not re.match(r'^[A-D][):]', line):
                    return line
        
        return f"What is the purpose of {topic} in {career}?"

    def _extract_options(self, text):
        """Extract options"""
        opts = {}
        
        for letter in ['A', 'B', 'C', 'D']:
            patterns = [
                rf'{letter}\)\s*([^\n]+)',
                rf'{letter}\.\s*([^\n]+)',
                rf'{letter}:\s*([^\n]+)',
            ]
            
            for pat in patterns:
                m = re.search(pat, text)
                if m and letter not in opts:
                    opt = self._clean_option(m.group(1))
                    if 8 < len(opt) < 250:
                        opts[letter] = opt
                        break
        
        return opts

    def _clean_option(self, text):
        """Clean option text"""
        text = ' '.join(text.split())
        for p in [r'^Correct:\s*', r'^Wrong:\s*', r'^\[.*?\]\s*', r'^Answer:\s*']:
            text = re.sub(p, '', text, flags=re.I)
        text = re.sub(r'^[A-D][):.\s]+', '', text, flags=re.I)
        return text.strip('.,;:-').strip()

    def _validate_options(self, options, question, topic):
        """Strict validation"""
        if len(options) != 4:
            return False
        
        for letter, text in options.items():
            text_lower = text.lower()
            
            # Check for placeholders
            placeholders = ['answer choice', '[0]', '[1]', '[2]', '[3]', '(answer', 'option here']
            if any(p in text_lower for p in placeholders):
                print(f"      ✗ {letter}: Placeholder: {text[:40]}")
                return False
            
            # Check length
            if len(text) < 10 or len(text) > 200:
                print(f"      ✗ {letter}: Length ({len(text)})")
                return False
            
            # Check if repeats question
            if question and len(text) > 20:
                q_words = set(question.lower().split()[:5])
                t_words = set(text_lower.split()[:5])
                if len(q_words & t_words) >= 3:
                    print(f"      ✗ {letter}: Repeats question")
                    return False
        
        # Check for duplicates
        texts = [t.lower().strip() for t in options.values()]
        if len(set(texts)) != 4:
            print(f"      ✗ Duplicate options")
            return False
        
        return True

    def _emergency_template(self, career, topic, diff, qn):
        """Emergency fallback"""
        templates = {
            "beginner": (
                f"What is {topic} used for in {career}?",
                {
                    "A": f"To develop {career} skills and understand fundamentals",
                    "B": f"To document work without practical application",
                    "C": f"To evaluate only at the end of projects",
                    "D": f"To replace all human decision-making",
                }
            ),
            "intermediate": (
                f"How should a {career} apply {topic} effectively?",
                {
                    "A": f"By understanding context and applying best practices",
                    "B": f"By using the same approach every time",
                    "C": f"By prioritizing speed over quality always",
                    "D": f"By waiting for approval before any action",
                }
            ),
            "advanced": (
                f"Why is {topic} critical for {career} professionals?",
                {
                    "A": f"Because complex scenarios require nuanced expertise",
                    "B": f"Because regulations mandate certification",
                    "C": f"Because one solution works for all cases",
                    "D": f"Because it is only for presentations",
                }
            ),
        }
        
        q, opts = templates.get(diff, templates["intermediate"])
        return {"id": f"q_{qn}", "question": q, "options": opts, "correct_answer": "A",
                "explanation": f"{topic} is important.", "topic": topic, "difficulty": diff,
                "career": career, "source": "emergency"}

    def _get_topic(self, career, diff, used):
        topics = {
            "Data Scientist": {
                "beginner": ["Python Basics", "Pandas", "NumPy", "Machine Learning", "Statistics"],
                "intermediate": ["Feature Engineering", "Model Validation", "SQL", "Data Visualization"],
                "advanced": ["Deep Learning", "MLOps", "Model Deployment", "A/B Testing"],
            },
        }
        default = {"beginner": ["Basics"], "intermediate": ["Methods"], "advanced": ["Strategy"]}
        lvl = topics.get(career, {}).get(diff, default[diff])
        avail = [t for t in lvl if t not in used]
        return random.choice(avail if avail else lvl)

    def _shuffle(self, opts):
        items = list(opts.items())
        random.shuffle(items)
        shuf, corr = {}, None
        for i, (orig, txt) in enumerate(items):
            new = chr(65+i)
            shuf[new] = txt
            if orig == "A":
                corr = new
        return shuf, corr

    def submit_answer(self, sd, qid, ua, ca, diff):
        correct = str(ua).upper() == str(ca).upper()
        weights = {"beginner":1, "intermediate":2, "advanced":3}
        sd["answers"].append({"question_id":qid, "difficulty":diff, "is_correct":correct, "weighted_score":weights[diff] if correct else 0})
        sd["performance_tracking"][diff]["total"] += 1
        if correct:
            sd["performance_tracking"][diff]["correct"] += 1
        sd["question_count"] += 1
        if "current_question" in sd:
            del sd["current_question"]
        return correct

    def calculate_level(self, sd):
        perf = sd["performance_tracking"]
        rate = lambda p: p["correct"]/p["total"] if p["total"]>0 else 0
        beg, inter, adv = rate(perf["beginner"]), rate(perf["intermediate"]), rate(perf["advanced"])
        total = sum(a["weighted_score"] for a in sd["answers"])
        max_s = sum({"beginner":1,"intermediate":2,"advanced":3}[a["difficulty"]] for a in sd["answers"])
        pct = (total/max_s*100) if max_s>0 else 0
        level = "advanced" if inter>=0.70 and adv>=0.60 and pct>=70 else "intermediate" if beg>=0.70 and inter>=0.50 and pct>=50 else "beginner"
        llm = sd.get("llm_success",0)
        attempts = sd.get("llm_attempts",0)
        retrievals = sd.get("rag_retrievals",0)
        rate_pct = (llm/attempts*100) if attempts>0 else 0
        print(f"\n{'='*70}\n📊 {sd['career'].upper()} RAG ASSESSMENT COMPLETE\n{'='*70}")
        print(f"Level: {level.upper()} | Score: {pct:.1f}%")
        print(f"LLM: {llm}/{attempts} ({rate_pct:.0f}%) | RAG Retrievals: {retrievals}")
        print(f"{'='*70}\n")
        return {"career":sd["career"], "level":level, "overall_score":round(pct,1), "llm_generated":llm, "rag_retrievals":retrievals}