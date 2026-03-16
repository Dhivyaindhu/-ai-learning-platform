# ai_engine/psychology/engine.py
# Key fix: _run_generation now tries 3 progressively simpler prompts before
# ever touching the static fallback — so the LLM does the work on the vast
# majority of questions.

import hashlib
import random
import re
from ..llm.llm_engine import get_llm_engine
from .traits import PERSONALITY_TRAITS as PSYCHOLOGICAL_TRAITS


# ── System prompts — one per retry level ──────────────────────────────────────
# Level 0: full instruction set
_SYS_FULL = (
    "You are a skilled interviewer in a one-on-one conversation. "
    "Write ONE open-ended question to help you understand the person. "
    "Rules:\n"
    "- Use 'you' or 'your' — never 'this person', 'they', or 'their'\n"
    "- One sentence ending with a question mark\n"
    "- Natural and conversational — no jargon, no test terminology\n"
    "- Do NOT assume anything not already stated\n"
    "- Do NOT apologise or add any preamble — output the question only."
)

# Level 1: shorter, stricter
_SYS_SHORT = (
    "Write ONE interview question using 'you' or 'your'. "
    "One sentence, ends with ?. No preamble, no apology. Question only."
)

# Level 2: minimal — last chance before fallback
_SYS_MINIMAL = (
    "Ask the user one short open-ended question. Use 'you'. End with ?."
)


class PsychologyEngine:

    MIN_QUESTIONS = 10
    MAX_QUESTIONS = 20
    MAX_DEPTH     = 2

    def __init__(self):
        self.llm    = get_llm_engine()
        self.traits = list(PSYCHOLOGICAL_TRAITS.keys())

    # ── Session ───────────────────────────────────────────────────────────────

    def start_assessment(self):
        return {
            "scores":           {trait: 50 for trait in self.traits},
            "responses":        [],
            "questions_asked":  [],
            "current_question": 0,
            "max_questions":    random.randint(self.MIN_QUESTIONS, self.MAX_QUESTIONS),
            "asked_hashes":     [],
            "completed":        False,
            "current_trait":    None,
            "depth_on_trait":   0,
        }

    # ── Core: get next question ───────────────────────────────────────────────

    def get_next_question(self, session):
        if self.should_stop(session):
            session["completed"] = True
            return None

        q_no  = session["current_question"] + 1
        trait = self._pick_trait(session)

        last_response = session["responses"][-1] if session["responses"] else None
        same_trait    = (trait == session.get("current_trait"))

        if last_response and same_trait and session.get("depth_on_trait", 0) < self.MAX_DEPTH:
            question = self._generate_with_retries(
                trait, q_no, session, mode="followup", last=last_response
            )
            session["depth_on_trait"] = session.get("depth_on_trait", 0) + 1
        else:
            question = self._generate_with_retries(
                trait, q_no, session, mode="opening", last=None
            )
            session["depth_on_trait"] = 0

        session["current_trait"] = trait
        session.setdefault("questions_asked", []).append(question)
        return question

    # ── Multi-strategy generation: 3 attempts before static fallback ──────────

    def _generate_with_retries(self, trait, q_no, session, mode, last):
        """
        Try 3 progressively simpler prompts before falling back to static pool.
        Strategy 0 — full context prompt  (best quality)
        Strategy 1 — concise prompt       (fewer tokens = less drift)
        Strategy 2 — minimal 1-line ask   (almost impossible to confuse the model)
        """
        strategies = [
            (self._build_prompt(trait, session, mode, last, level=0), _SYS_FULL,    80),
            (self._build_prompt(trait, session, mode, last, level=1), _SYS_SHORT,   60),
            (self._build_prompt(trait, session, mode, last, level=2), _SYS_MINIMAL, 40),
        ]

        for attempt, (prompt, sys_prompt, max_tok) in enumerate(strategies):
            try:
                raw      = self.llm.generate(prompt, max_tokens=max_tok, system_prompt=sys_prompt)
                question = self._clean_and_fix(raw)
                self._validate(question, session)

                session["asked_hashes"].append(self._hash(question))
                print(f"   ✅ [{mode}/s{attempt}] Q{q_no} ({trait}): {question[:70]}...")
                return _make_q(q_no, trait, question)

            except Exception as e:
                print(f"   ↩  [{mode}/s{attempt}] Q{q_no}: {str(e)[:60]} — trying next strategy")
                continue

        # All 3 LLM strategies failed → static fallback
        print(f"   📋 [fallback] Q{q_no} ({trait}): all LLM strategies failed")
        return self._static_fallback(trait, q_no, session)

    # ── Prompt builders — three detail levels ─────────────────────────────────

    def _build_prompt(self, trait, session, mode, last, level):
        theme = _TRAIT_THEMES[trait]

        # ── Level 2: bare minimum ─────────────────────────────────────────────
        if level == 2:
            if mode == "followup" and last:
                snippet = last["answer"][:80]
                return f'The person said: "{snippet}". Ask them one short follow-up question.'
            return f"Ask one question to explore {theme}."

        # ── Level 1: concise ──────────────────────────────────────────────────
        if level == 1:
            if mode == "followup" and last:
                snippet = last["answer"][:120]
                return (
                    f'You asked: "{last["question"]}"\n'
                    f'They said: "{snippet}"\n'
                    f"Ask one follow-up question about what they just shared."
                )
            recent = session["responses"][-1]["answer"][:100] if session["responses"] else ""
            context = f'Last answer: "{recent}"\n\n' if recent else ""
            return f"{context}Ask one open-ended question about {theme}."

        # ── Level 0: full context ─────────────────────────────────────────────
        if mode == "followup" and last:
            answer_snippet = last["answer"][:200]
            return (
                f'You asked: "{last["question"]}"\n'
                f'The person answered: "{answer_snippet}"\n\n'
                f"Write ONE follow-up question that digs into something specific they mentioned. "
                f"Use 'you' or 'your'. Do not repeat the previous question. "
                f"Do not add any preamble or apology."
            )

        # opening — level 0
        if session["responses"]:
            recent = session["responses"][-1]["answer"][:150]
            context_line = f'The person recently shared: "{recent}"\n\n'
        else:
            context_line = ""

        return (
            f"{context_line}"
            f"Write ONE open-ended question to explore {theme}. "
            f"Invite the person to share a specific experience or story. "
            f"Use 'you' or 'your'. Do not add any preamble or apology."
        )

    # ── Validation ────────────────────────────────────────────────────────────

    def _validate(self, question, session):
        """Raise ValueError if question fails any quality check."""

        if not question or len(question) < 15:
            raise ValueError(f"Too short: '{question}'")

        if not question.endswith("?"):
            raise ValueError(f"Missing '?': '{question[:60]}'")

        # Apology / filler detection — the most common 0.5B failure mode
        bad_starts = (
            "i'm sorry", "i am sorry", "i apologize", "i apologise",
            "apologies", "sorry for", "my apologies",
            "here's one", "here is one", "sure!", "great!",
            "of course", "certainly", "no problem", "absolutely",
            "i'd be happy", "i would be happy",
        )
        q_lower = question.lower()
        for b in bad_starts:
            if q_lower.startswith(b):
                raise ValueError(f"Bad opener '{b}': '{question[:50]}'")

        # Third-person leakage
        third_person = [
            "this person", "the person", "the individual",
            "the respondent", "he said", "she said",
        ]
        for tp in third_person:
            if tp in q_lower:
                raise ValueError(f"Third-person: '{question[:60]}'")

        # Must address the user
        if "you" not in q_lower and "your" not in q_lower:
            raise ValueError(f"No second-person pronoun: '{question[:60]}'")

        # Deduplicate
        q_hash = self._hash(question)
        if q_hash in session.get("asked_hashes", []):
            raise ValueError("Duplicate question")

    # ── Clean + second-person correction ─────────────────────────────────────

    def _clean_and_fix(self, text):
        if not text:
            return ""

        t = text.strip()

        # ── 1. Strip surrounding quotes the model sometimes adds ──────────────
        # e.g.  "What does you's approach involve?"  →  What does you's approach involve?
        if (t.startswith('"') and t.endswith('"')) or \
           (t.startswith("'") and t.endswith("'")):
            t = t[1:-1].strip()

        # ── 2. Strip preamble prefixes ────────────────────────────────────────
        prefixes = (
            "question:", "q:", "follow-up:", "here's a question:",
            "sure!", "great!", "of course,", "certainly,", "absolutely,",
            "here's one:", "here is a question:",
            "i'd be happy to ask:", "i would ask:",
        )
        lower = t.lower()
        for p in prefixes:
            if lower.startswith(p):
                t = t[len(p):].lstrip(" ,:.!\n")
                break

        # ── 3. Take first line only ───────────────────────────────────────────
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        t = lines[0] if lines else t

        # ── 4. Trim to first question mark ────────────────────────────────────
        if "?" in t:
            t = t[:t.index("?") + 1]

        # ── 5. Second-person corrections (possessives FIRST) ──────────────────
        # Possessive forms must come before plain noun replacements, otherwise
        # "this person's" → "you" + "'s" → "you's" (wrong).
        replacements = [
            # possessives — must be handled before plain "this person" / "their"
            (r"\bthis person's\b",    "your",      re.IGNORECASE),
            (r"\bthe person's\b",     "your",      re.IGNORECASE),
            (r"\bthe individual's\b", "your",      re.IGNORECASE),
            (r"\bthe respondent's\b", "your",      re.IGNORECASE),
            (r"\btheir\b",            "your",      re.IGNORECASE),
            (r"\bthemselves\b",       "yourself",  re.IGNORECASE),
            # plain noun replacements
            (r"\bthis person\b",      "you",       re.IGNORECASE),
            (r"\bthe person\b",       "you",       re.IGNORECASE),
            (r"\bthe individual\b",   "you",       re.IGNORECASE),
            (r"\bthe respondent\b",   "you",       re.IGNORECASE),
            # verb agreement
            (r"\bthey enjoy\b",       "you enjoy", re.IGNORECASE),
            (r"\bthey have\b",        "you have",  re.IGNORECASE),
            (r"\bthey feel\b",        "you feel",  re.IGNORECASE),
            (r"\bthey do\b",          "you do",    re.IGNORECASE),
            (r"\bthey are\b",         "you are",   re.IGNORECASE),
        ]
        for pattern, repl, flags in replacements:
            t = re.sub(pattern, repl, t, flags=flags)

        # ── 6. Fix broken grammar left by replacements ────────────────────────
        # "you's"     → "your"     (possessive escaped replacement artifact)
        # "does you"  → "do you"   (verb agreement after noun swap)
        # "is you"    → "are you"
        t = re.sub(r"\byou's\b",   "your",   t, flags=re.IGNORECASE)
        t = re.sub(r"\bdoes you\b","do you",  t, flags=re.IGNORECASE)
        t = re.sub(r"\bis you\b",  "are you", t, flags=re.IGNORECASE)
        t = re.sub(r"\bwas you\b", "were you",t, flags=re.IGNORECASE)

        # ── 7. Final cleanup ──────────────────────────────────────────────────
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            t = t[0].upper() + t[1:]

        t = t.rstrip("?.,! ") + "?"
        return t

    # ── Static fallback (last resort only) ───────────────────────────────────

    def _static_fallback(self, trait, q_no, session):
        has_context = bool(session.get("responses"))
        pool = (
            _CONTEXTUAL_FALLBACKS if has_context else _OPENING_FALLBACKS
        ).get(trait, _OPENING_FALLBACKS["_default"])

        asked  = {q["question"] for q in session.get("questions_asked", [])}
        unused = [q for q in pool if q not in asked]
        text   = random.choice(unused if unused else pool)

        session["asked_hashes"].append(self._hash(text))
        return _make_q(q_no, trait, text)

    # ── Answer submission + scoring ───────────────────────────────────────────

    def submit_answer(self, session, answer):
        if not session.get("questions_asked"):
            raise ValueError("No questions asked yet.")

        last  = session["questions_asked"][-1]
        trait = last["trait"]

        score_100 = self._score_answer(answer, trait)
        prev = session["scores"].get(trait, 50)
        session["scores"][trait] = int(prev * 0.6 + score_100 * 0.4)

        session["responses"].append({
            "trait":    trait,
            "question": last["question"],
            "answer":   answer,
            "score":    score_100,
        })
        session["current_question"] += 1

    def _score_answer(self, answer, trait):
        prompt = (
            f"Rate this answer 1–5 for '{trait}'. 1=very low, 5=very high. "
            f"One digit only.\nAnswer: \"{answer[:200]}\""
        )
        try:
            result  = self.llm.generate(
                prompt, max_tokens=5,
                system_prompt="Rate personality answers. Output only a single digit 1–5.",
            )
            m = re.search(r"[1-5]", result)
            return (int(m.group()) - 1) * 25 if m else 50
        except Exception:
            return 50

    # ── Stopping logic ────────────────────────────────────────────────────────

    def should_stop(self, session):
        if session["current_question"] < self.MIN_QUESTIONS:
            return False
        if session["current_question"] >= session["max_questions"]:
            return True
        scores = list(session["scores"].values())
        return max(scores) - min(scores) >= 25

    # ── Trait selection ───────────────────────────────────────────────────────

    def _pick_trait(self, session):
        counts = {t: 0 for t in self.traits}
        for q in session.get("questions_asked", []):
            counts[q["trait"]] += 1

        curr  = session.get("current_trait")
        depth = session.get("depth_on_trait", 0)
        if curr and depth < self.MAX_DEPTH:
            return curr

        min_count  = min(counts.values())
        candidates = [t for t, c in counts.items() if c == min_count]
        return random.choice(candidates)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()[:16]


# ── Utility ───────────────────────────────────────────────────────────────────

def _make_q(q_no, trait, question):
    return {
        "id":            f"q_{q_no}",
        "trait":         trait,
        "question":      question,
        "type":          "open_ended",
        "requires_text": True,
    }


# ── Trait themes (plain English, used in prompts only — never shown to user) ──

_TRAIT_THEMES = {
    "openness":          "their curiosity and how they engage with new ideas or experiences",
    "conscientiousness": "how they plan, organise, and follow through on things they care about",
    "extraversion":      "how they prefer to spend time and connect with others",
    "agreeableness":     "how they handle disagreement and support people around them",
    "neuroticism":       "how they respond to stress, uncertainty, and difficult situations",
}


# ── Static fallback pools — second-person, exploratory, never jargon-y ───────

_OPENING_FALLBACKS = {
    "openness": [
        "What is something you have been genuinely curious about recently?",
        "Tell me about a time you tried something completely outside your usual routine — what drew you to it?",
        "What kinds of ideas or topics tend to pull your attention when you have free time?",
    ],
    "conscientiousness": [
        "How do you typically prepare when something important is coming up?",
        "Walk me through what you usually do when you have a lot to get done and limited time.",
        "Tell me about a goal you set for yourself — how did you go about working toward it?",
    ],
    "extraversion": [
        "What does a good weekend look like for you?",
        "How do you usually feel after spending a long day around a lot of people?",
        "What kind of environment helps you feel most like yourself?",
    ],
    "agreeableness": [
        "Tell me about a time you had to navigate a disagreement with someone — how did you handle it?",
        "When someone close to you is struggling, what do you usually find yourself doing?",
        "How do you typically respond when someone asks you for something you are not sure you can do?",
    ],
    "neuroticism": [
        "How do you usually react when something unexpected disrupts your plans?",
        "Tell me about a moment that felt particularly stressful — what did you do?",
        "When things are not going well, what tends to help you get back on track?",
    ],
    "_default": [
        "Tell me about a recent experience that has stayed with you.",
        "What is something you have been thinking about quite a bit lately?",
        "Describe a situation that challenged you and how you responded to it.",
    ],
}

_CONTEXTUAL_FALLBACKS = {
    "openness": [
        "When you come across an idea that genuinely interests you, how do you usually explore it further?",
        "Can you think of a time you changed your mind about something important — what happened?",
        "What is something you have always wanted to learn more about but have not had the chance to yet?",
    ],
    "conscientiousness": [
        "How do you know when you are satisfied with the quality of your work?",
        "When a plan falls apart, how do you usually recover and move forward?",
        "Tell me about something you followed through on even when it got difficult — what kept you going?",
    ],
    "extraversion": [
        "After spending time with others, how do you usually feel — energised or ready for some quiet time?",
        "What kinds of social situations do you find most comfortable, and which do you find draining?",
        "How much does the energy of the people around you tend to affect how you feel?",
    ],
    "agreeableness": [
        "When you sense tension with someone, what is your usual instinct — to address it or let it pass?",
        "How do you balance your own needs with what others need from you?",
        "Tell me about a time you had to say no to someone — how did that feel?",
    ],
    "neuroticism": [
        "When you are going through something difficult, do you tend to talk about it or keep it to yourself?",
        "What helps you feel settled again after a stressful period?",
        "How long does it usually take you to feel calm again after something goes wrong?",
    ],
    "_default": [
        "Building on what you shared — what part of that experience stands out most to you now?",
        "That sounds like it had an impact on you — what did it teach you about yourself?",
        "What do you think motivates you most deeply in situations like that?",
    ],
}