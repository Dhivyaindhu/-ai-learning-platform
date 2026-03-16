# ai_engine/services/career_assessment_service.py
"""
UPDATED: Balanced answer lengths, plausible distractors, no obvious giveaways
"""

from ..llm.llm_engine import get_llm_engine
from ..rag.enhanced_knowledge import EnhancedKnowledgeBase
import random
import re


class CareerAssessmentService:

    def __init__(self):
        print("\n" + "="*70)
        print("🚀 INITIALIZING CAREER ASSESSMENT SERVICE")
        print("="*70)

        try:
            self.llm = get_llm_engine()
            print("✅ LLM Engine: Ready")
        except Exception as e:
            print(f"❌ LLM Engine failed: {e}")
            raise

        try:
            self.kb = EnhancedKnowledgeBase()
            self.kb_available = True
            print(f"✅ Knowledge Base: {len(self.kb.supported_careers)} careers")
        except Exception as e:
            print(f"⚠️ Knowledge Base unavailable: {e}")
            self.kb = None
            self.kb_available = False

        print("="*70 + "\n")

    # ─────────────────────────────────────────────────────────
    #  SESSION
    # ─────────────────────────────────────────────────────────

    def start_career_assessment(self, career, total_questions=15):
        random.seed()
        difficulty_plan = ["beginner"] * 5 + ["intermediate"] * 5 + ["advanced"] * 5
        random.shuffle(difficulty_plan)
        return {
            "career":          career,
            "max_questions":   total_questions,
            "question_count":  0,
            "used_topics":     [],
            "answers":         [],
            "difficulty_plan": difficulty_plan,
            "performance_tracking": {
                "beginner":     {"correct": 0, "total": 0},
                "intermediate": {"correct": 0, "total": 0},
                "advanced":     {"correct": 0, "total": 0},
            },
            "completed":      False,
            "llm_success":    0,
            "template_used":  0,
        }

    def is_complete(self, sd):
        return sd["question_count"] >= sd["max_questions"]

    # ─────────────────────────────────────────────────────────
    #  MAIN QUESTION GENERATOR
    # ─────────────────────────────────────────────────────────

    def get_next_question(self, sd):
        if self.is_complete(sd):
            return None
        if "current_question" in sd:
            return sd["current_question"]

        idx    = sd["question_count"]
        diff   = sd["difficulty_plan"][idx]
        career = sd["career"]

        print(f"\n{'='*60}")
        print(f"🎯 Q{idx+1}/{sd['max_questions']}: {career} | {diff.upper()}")
        print(f"{'='*60}")

        topic = self._get_topic(career, diff, sd["used_topics"])
        sd["used_topics"].append(topic)
        print(f"📌 Topic: '{topic}'")

        q = None
        if self.kb_available:
            ctx = self._get_context(career, diff, topic)
            if ctx and len(ctx.get("description", "")) > 30:
                q = self._llm_generate(career, topic, diff, ctx, idx + 1)
                if q:
                    sd["llm_success"] += 1
                    print(f"✅ LLM generated ({sd['llm_success']}/{idx+1})")
                else:
                    print(f"⚠️  LLM failed → using KB direct")
                    q = self._kb_direct(career, topic, diff, ctx, idx + 1)

        if not q:
            sd["template_used"] += 1
            q = self._template(career, topic, diff, idx + 1)
            print(f"📚 Template used ({sd['template_used']} total)")

        shuf, cor = self._shuffle(q["options"])
        q["options"]        = shuf
        q["correct_answer"] = cor
        sd["current_question"] = q

        print(f"📝 {q['question'][:70]}...")
        print(f"   ✔ Correct: {cor}")
        return q

    # ─────────────────────────────────────────────────────────
    #  KB DIRECT — Uses KB content as-is (no LLM needed)
    # ─────────────────────────────────────────────────────────

    def _kb_direct(self, career, topic, diff, ctx, qn):
        """
        Builds question directly from KB without LLM.
        Guarantees balanced option lengths since all come from KB.
        """
        description   = ctx.get("description", "").strip()
        why_important = ctx.get("why_important", "").strip()
        wrong_concepts = ctx.get("wrong_concepts", [])

        if not description or len(wrong_concepts) < 3:
            return None

        # Build question from topic + difficulty
        question_map = {
            "beginner":     f"Which statement best describes {topic} in the context of {career}?",
            "intermediate": f"Which statement correctly explains how {topic} is applied in {career}?",
            "advanced":     f"Which statement best explains why {topic} is critical for a senior {career}?",
        }
        question = question_map.get(diff, f"Which statement about {topic} is correct for {career}?")

        # Use KB description/why_important as correct answer
        source = description if diff == "beginner" else why_important or description
        correct = self._trim_to_length(source, 120)

        # Trim wrong concepts to same length as correct answer
        target_len = len(correct)
        distractors = [
            self._trim_to_length(wc, target_len + 20)
            for wc in wrong_concepts[:3]
        ]

        q = {
            "id":             f"kb_{qn}",
            "question":       question,
            "options": {
                "A": correct,
                "B": distractors[0],
                "C": distractors[1],
                "D": distractors[2],
            },
            "correct_answer": "A",
            "explanation":    f"{topic} is a key concept for {career} professionals.",
            "topic":          topic,
            "difficulty":     diff,
            "career":         career,
            "source":         "kb_direct",
        }

        return q if self._validate(q) else None

    # ─────────────────────────────────────────────────────────
    #  LLM GENERATION
    # ─────────────────────────────────────────────────────────

    def _llm_generate(self, career, topic, diff, ctx, qn):
        """
        Generates question via LLM, uses KB for all options.
        Options are length-balanced to prevent guessing by length.
        """
        description    = ctx.get("description", "").strip()
        why_important  = ctx.get("why_important", "").strip()
        wrong_concepts = ctx.get("wrong_concepts", [])

        if not description or len(wrong_concepts) < 3:
            return None

        # Generate question only (LLM)
        print(f"   🤖 [1/1] Generating question...")
        question = self._gen_question(career, topic, diff, description)
        if not question or len(question) < 15:
            print(f"   ❌ Question generation failed")
            return None
        print(f"   ✅ Q: {question[:60]}...")

        # Correct answer — from KB (no LLM needed, more reliable)
        source  = description if diff == "beginner" else why_important or description
        correct = self._trim_to_length(source, 120)

        # Wrong options — from KB, trimmed to same length as correct
        target_len  = len(correct)
        distractors = [
            self._trim_to_length(wc, target_len + 20)
            for wc in wrong_concepts[:3]
        ]

        q = {
            "id":             f"llm_{qn}",
            "question":       question,
            "options": {
                "A": correct,
                "B": distractors[0],
                "C": distractors[1],
                "D": distractors[2],
            },
            "correct_answer": "A",
            "explanation":    f"Tests {topic} knowledge for {career}.",
            "topic":          topic,
            "difficulty":     diff,
            "career":         career,
            "source":         "llm",
        }

        return q if self._validate(q) else None

    def _gen_question(self, career, topic, diff, description):
        """Generate just the question text using LLM."""
        starters = {
            "beginner":     f"What is {topic}",
            "intermediate": f"How is {topic} applied",
            "advanced":     f"Why is {topic} critical",
        }
        starter = starters.get(diff, f"What is {topic}")

        prompt = (
            f"Career: {career}\n"
            f"Topic: {topic}\n"
            f"Context: {description[:80]}\n"
            f"Write one multiple choice question starting with '{starter}'.\n"
            f"Question only, no options:\n"
        )

        try:
            raw = self.llm.generate(prompt, max_tokens=60)
            return self._clean_question(raw)
        except Exception as e:
            print(f"      Error: {e}")
            return None

    # ─────────────────────────────────────────────────────────
    #  HELPERS
    # ─────────────────────────────────────────────────────────

    def _trim_to_length(self, text, max_len):
        """Trim text to max_len at sentence boundary."""
        text = text.strip()
        if not text.endswith('.'):
            text = text + "."
        if len(text) <= max_len:
            return text
        # Try to cut at sentence boundary
        end = text[:max_len].rfind('.')
        if end > max_len * 0.5:
            return text[:end + 1]
        return text[:max_len - 3] + "..."

    def _get_topic(self, career, diff, used):
        if self.kb_available:
            try:
                concepts = self.kb.get_all_concepts(career, diff)
                if concepts:
                    avail = [c for c in concepts if c not in used]
                    return random.choice(avail if avail else concepts)
            except Exception:
                pass
        fallback = {
            "beginner":     ["Fundamentals", "Core Concepts", "Basic Tools"],
            "intermediate": ["Methods", "Best Practices", "Techniques"],
            "advanced":     ["Strategy", "Optimization", "Leadership"],
        }
        return random.choice(fallback.get(diff, ["Concepts"]))

    def _get_context(self, career, diff, topic):
        if not self.kb_available:
            return {}
        try:
            return self.kb.get_concept_data(career, diff, topic)
        except Exception:
            return {}

    def _clean_question(self, text):
        if not text:
            return ""
        text = text.strip()
        for prefix in ["question:", "q:", "sure", "here", "okay", "write", "multiple choice"]:
            if text.lower().startswith(prefix):
                text = text[len(prefix):].lstrip(":, \n")
        if '?' in text:
            text = text[:text.find('?') + 1].strip()
        elif len(text) > 10:
            text = text.split('\n')[0].strip()
            if not text.endswith('?'):
                text += '?'
        return text

    def _validate(self, q):
        if len(q["options"]) != 4:
            return False
        for txt in q["options"].values():
            if not txt or len(txt) < 15 or len(txt) > 300:
                return False
        texts = [t.lower().strip() for t in q["options"].values()]
        if len(set(texts)) != 4:
            return False
        # Check options are roughly similar length (prevent giveaway)
        lengths = [len(t) for t in q["options"].values()]
        max_len = max(lengths)
        min_len = min(lengths)
        if max_len > min_len * 3:   # one option 3x longer is a giveaway
            return False
        return True

    def _template(self, career, topic, diff, qn):
        temps = {
            "beginner": {
                "q": f"Which statement correctly describes {topic} in {career}?",
                "a": f"It is a core concept that {career} professionals apply to solve common problems.",
                "w": [
                    f"It is an advanced technique reserved for specialist roles in large organisations.",
                    f"It is an outdated approach that has been replaced by more modern methodologies.",
                    f"It applies only to theoretical contexts and rarely appears in practical work.",
                ],
            },
            "intermediate": {
                "q": f"How should a {career} professional correctly apply {topic}?",
                "a": f"By understanding the context and selecting the approach that best fits the situation.",
                "w": [
                    f"By applying the same standardised process consistently regardless of context or constraints.",
                    f"By delegating the task to specialists and focusing on higher-level strategic concerns.",
                    f"By following the most recently published guidelines without adapting to specific circumstances.",
                ],
            },
            "advanced": {
                "q": f"Why is deep expertise in {topic} important for a senior {career} professional?",
                "a": f"It enables informed judgment and sound decision-making when facing complex trade-offs.",
                "w": [
                    f"It satisfies regulatory requirements that mandate certification in this specific area.",
                    f"It allows professionals to apply a single proven approach across all possible scenarios.",
                    f"It is primarily valued in academic research rather than in day-to-day professional practice.",
                ],
            },
        }
        t = temps.get(diff, temps["intermediate"])
        return {
            "id":             f"template_{qn}",
            "question":       t["q"],
            "options":        {"A": t["a"], "B": t["w"][0], "C": t["w"][1], "D": t["w"][2]},
            "correct_answer": "A",
            "explanation":    f"{topic} is essential for {career} professionals.",
            "topic":          topic,
            "difficulty":     diff,
            "career":         career,
            "source":         "template",
        }

    def _shuffle(self, opts):
        items = list(opts.items())
        random.shuffle(items)
        shuf, cor = {}, None
        for i, (orig, txt) in enumerate(items):
            new = chr(65 + i)
            shuf[new] = txt
            if orig == "A":
                cor = new
        return shuf, cor

    # ─────────────────────────────────────────────────────────
    #  ANSWER SUBMISSION & SCORING
    # ─────────────────────────────────────────────────────────

    def submit_answer(self, sd, qid, ua, ca, diff):
        correct = str(ua).upper() == str(ca).upper()
        weights = {"beginner": 1, "intermediate": 2, "advanced": 3}
        sd["answers"].append({
            "question_id":    qid,
            "difficulty":     diff,
            "is_correct":     correct,
            "weighted_score": weights[diff] if correct else 0,
        })
        sd["performance_tracking"][diff]["total"] += 1
        if correct:
            sd["performance_tracking"][diff]["correct"] += 1
        sd["question_count"] += 1
        sd.pop("current_question", None)
        return correct

    def calculate_level(self, sd):
        perf  = sd["performance_tracking"]
        rate  = lambda p: p["correct"] / p["total"] if p["total"] > 0 else 0
        beg   = rate(perf["beginner"])
        inter = rate(perf["intermediate"])
        adv   = rate(perf["advanced"])

        total = sum(a["weighted_score"] for a in sd["answers"])
        max_s = sum(
            {"beginner": 1, "intermediate": 2, "advanced": 3}[a["difficulty"]]
            for a in sd["answers"]
        )
        pct = (total / max_s * 100) if max_s > 0 else 0

        level = (
            "advanced"     if inter >= 0.7 and adv   >= 0.6 and pct >= 70 else
            "intermediate" if beg   >= 0.7 and inter >= 0.5 and pct >= 50 else
            "beginner"
        )

        llm      = sd.get("llm_success", 0)
        template = sd.get("template_used", 0)

        print(f"\n{'='*60}")
        print(f"📊 {sd['career'].upper()} — COMPLETE")
        print(f"Level : {level.upper()}  |  Score : {pct:.1f}%")
        print(f"Beg:{beg*100:.0f}%  Int:{inter*100:.0f}%  Adv:{adv*100:.0f}%")
        print(f"LLM:{llm}/15  |  Template:{template}/15")
        print(f"{'='*60}\n")

        return {
            "career":               sd["career"],
            "level":                level,
            "overall_score":        round(pct, 1),
            "determined_level":     level,
            "scores_by_difficulty": {
                "beginner":     round(beg   * 100, 1),
                "intermediate": round(inter * 100, 1),
                "advanced":     round(adv   * 100, 1),
            },
            "rag_generated":        llm,
            "questions_answered":   sd["question_count"],
        }