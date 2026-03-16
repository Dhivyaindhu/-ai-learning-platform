# ai_engine/psychology/scoring.py

from .traits import PERSONALITY_TRAITS


class PsychologyScoring:
    """
    Handles scoring logic for psychology assessment
    """

    def __init__(self, traits):
        """
        traits: PSYCHOLOGICAL_TRAITS dictionary
        """
        self.traits = traits

    # ----------------------------------
    # INITIAL SCORE SETUP
    # ----------------------------------
    def initialize_scores(self):
        """
        Initialize all trait scores to zero
        """
        return {trait: 0 for trait in self.traits.keys()}

    # ----------------------------------
    # SCORE UPDATE (LIKERT SCALE)
    # ----------------------------------
    def update_score(self, scores, trait, response_value):
        """
        Update score based on user response

        response_value scale:
        1 → Strongly Disagree
        2 → Disagree
        3 → Neutral
        4 → Agree
        5 → Strongly Agree
        """

        if trait not in scores:
            return scores

        # Normalize response (convert to score weight)
        weight_map = {
            1: -2,
            2: -1,
            3: 0,
            4: 1,
            5: 2
        }

        scores[trait] += weight_map.get(response_value, 0)
        return scores

    # ----------------------------------
    # OPEN TEXT RESPONSE SCORING (LLM READY)
    # ----------------------------------
    def score_text_response(self, scores, trait, confidence_score):
        """
        confidence_score (int): 0–10
        Can be produced by LLM sentiment/analysis later
        """

        if trait not in scores:
            return scores

        scores[trait] += confidence_score
        return scores

    # ----------------------------------
    # NORMALIZATION
    # ----------------------------------
    def normalize_scores(self, scores):
        """
        Convert raw scores into positive range
        """
        min_score = min(scores.values())

        if min_score < 0:
            for trait in scores:
                scores[trait] += abs(min_score)

        return scores

    # ----------------------------------
    # FINAL SCORING PIPELINE
    # ----------------------------------
    def finalize_scores(self, scores):
        """
        Prepare scores for engine consumption
        """
        scores = self.normalize_scores(scores)
        return scores


# ----------------------------------
# STANDALONE FUNCTION FOR ASSESSMENT SERVICE
# ----------------------------------
def calculate_trait_scores(answers):
    """
    Calculate trait scores from conversational assessment answers

    Args:
        answers: List of answer dictionaries with 'trait' and score/analysis

    Returns:
        Dictionary of trait scores (0-10 scale)
    """
    # Initialize scores for all traits
    trait_scores = {trait: [] for trait in PERSONALITY_TRAITS.keys()}

    # Collect scores for each trait
    for answer in answers:
        trait = answer.get('trait')

        # Get the score (could be from LLM analysis or keyword analysis)
        # The score should already be 1-10 from submit_answer()
        score = answer.get('score', 5)  # Default to 5 if no score

        if trait in trait_scores:
            trait_scores[trait].append(score)

    # Average the scores for each trait
    final_scores = {}
    for trait, scores in trait_scores.items():
        if scores:
            # Average of all scores for this trait
            avg_score = sum(scores) / len(scores)
            final_scores[trait] = round(avg_score, 1)
        else:
            # Default score if no answers for this trait
            final_scores[trait] = 5.0

    return final_scores