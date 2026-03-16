from ai_engine.psychology.traits import PSYCHOLOGICAL_TRAITS


class CareerService:
    """
    Converts psychological traits into career paths
    """

    def recommend(self, sorted_traits):
        recommendations = []

        for trait, _ in sorted_traits[:2]:
            careers = PSYCHOLOGICAL_TRAITS.get(trait, {}).get("careers", [])
            recommendations.extend(careers)

        return list(set(recommendations))
