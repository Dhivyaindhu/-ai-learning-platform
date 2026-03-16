# ai_engine/psychology/traits.py

"""
Personality traits definitions based on Big Five model
"""

PERSONALITY_TRAITS = {
    'openness': {
        'name': 'Openness to Experience',
        'description': 'Imagination, creativity, curiosity, and willingness to try new things',
        'high_indicators': [
            'Creative and imaginative',
            'Curious about new experiences',
            'Open to different perspectives',
            'Appreciates art and beauty',
            'Enjoys abstract thinking'
        ],
        'low_indicators': [
            'Prefers routine and familiarity',
            'Practical and conventional',
            'Down-to-earth',
            'Prefers concrete facts',
            'Traditional in approach'
        ]
    },

    'conscientiousness': {
        'name': 'Conscientiousness',
        'description': 'Organization, responsibility, dependability, and goal-oriented behavior',
        'high_indicators': [
            'Organized and methodical',
            'Reliable and dependable',
            'Goal-oriented',
            'Detail-focused',
            'Plans ahead'
        ],
        'low_indicators': [
            'Spontaneous and flexible',
            'Adaptable to change',
            'Comfortable with ambiguity',
            'Goes with the flow',
            'Less concerned with schedules'
        ]
    },

    'extraversion': {
        'name': 'Extraversion',
        'description': 'Sociability, assertiveness, energy in social situations, and outgoing behavior',
        'high_indicators': [
            'Outgoing and social',
            'Energized by people',
            'Talkative and expressive',
            'Enjoys group activities',
            'Assertive in social settings'
        ],
        'low_indicators': [
            'Reserved and reflective',
            'Prefers solitude or small groups',
            'Thinks before speaking',
            'Energized by alone time',
            'Observant listener'
        ]
    },

    'agreeableness': {
        'name': 'Agreeableness',
        'description': 'Compassion, cooperation, trust, and concern for others',
        'high_indicators': [
            'Empathetic and caring',
            'Cooperative team player',
            'Trusting of others',
            'Conflict-avoidant',
            'Puts others first'
        ],
        'low_indicators': [
            'Direct and frank',
            'Competitive',
            'Skeptical of others',
            'Prioritizes own needs',
            'Challenges status quo'
        ]
    },

    'neuroticism': {
        'name': 'Emotional Stability',
        'description': 'Emotional sensitivity, stress response, and mood stability',
        'high_indicators': [
            'Emotionally aware',
            'Sensitive to stress',
            'Experiences strong emotions',
            'Worried about outcomes',
            'Self-reflective'
        ],
        'low_indicators': [
            'Emotionally stable',
            'Calm under pressure',
            'Resilient to stress',
            'Even-tempered',
            'Confident in outcomes'
        ]
    }
}

# Career mappings based on personality traits
CAREER_RECOMMENDATIONS = {
    'openness': {
        'high': [
            'UI/UX Designer',
            'Content Creator',
            'Research Scientist',
            'Innovation Consultant',
            'Creative Director',
            'Product Designer',
            'Artist',
            'Writer',
            'Marketing Strategist',
            'Entrepreneur'
        ],
        'low': [
            'Accountant',
            'Data Entry Specialist',
            'Quality Control Inspector',
            'Administrative Assistant',
            'Operations Coordinator'
        ]
    },

    'conscientiousness': {
        'high': [
            'Project Manager',
            'Data Analyst',
            'Software Engineer',
            'Quality Assurance Specialist',
            'Operations Manager',
            'Financial Analyst',
            'Systems Administrator',
            'Compliance Officer',
            'Research Analyst',
            'Business Analyst'
        ],
        'low': [
            'Creative Director',
            'Performer',
            'Sales Representative',
            'Event Coordinator',
            'Emergency Responder'
        ]
    },

    'extraversion': {
        'high': [
            'Sales Manager',
            'Marketing Specialist',
            'Public Relations Manager',
            'Event Coordinator',
            'Customer Success Manager',
            'Business Development',
            'Teacher',
            'HR Manager',
            'Recruiter',
            'Consultant'
        ],
        'low': [
            'Software Developer',
            'Data Analyst',
            'Writer',
            'Researcher',
            'Accountant',
            'Librarian',
            'Lab Technician'
        ]
    },

    'agreeableness': {
        'high': [
            'Human Resources Manager',
            'Counselor',
            'Social Worker',
            'Teacher',
            'Healthcare Provider',
            'Customer Support Specialist',
            'Therapist',
            'Nurse',
            'Mediator',
            'Community Manager'
        ],
        'low': [
            'Lawyer',
            'Executive',
            'Scientist',
            'Analyst',
            'Auditor',
            'Critic',
            'Journalist'
        ]
    },

    'neuroticism': {
        'high': [
            'Psychologist',
            'Writer',
            'Researcher',
            'Quality Control Analyst',
            'Risk Analyst',
            'Editor',
            'Artist',
            'Therapist'
        ],
        'low': [
            'Emergency Responder',
            'Pilot',
            'Surgeon',
            'Military Officer',
            'Crisis Manager',
            'Trader',
            'Executive'
        ]
    }
}

# Trait score interpretation
TRAIT_LEVELS = {
    'very_low': (0, 2),
    'low': (2, 4),
    'moderate': (4, 6),
    'high': (6, 8),
    'very_high': (8, 10)
}


def get_trait_level(score):
    """
    Convert numerical score to descriptive level

    Args:
        score: Float between 0 and 10

    Returns:
        String describing the trait level
    """
    if score < 2:
        return 'very_low'
    elif score < 4:
        return 'low'
    elif score < 6:
        return 'moderate'
    elif score < 8:
        return 'high'
    else:
        return 'very_high'


def get_trait_description(trait, score):
    """
    Get human-readable description of trait based on score

    Args:
        trait: Trait name (e.g., 'openness')
        score: Trait score (0-10)

    Returns:
        String description
    """
    level = get_trait_level(score)
    trait_info = PERSONALITY_TRAITS.get(trait, {})

    if level in ['high', 'very_high']:
        indicators = trait_info.get('high_indicators', [])
    else:
        indicators = trait_info.get('low_indicators', [])

    return {
        'trait_name': trait_info.get('name', trait),
        'level': level,
        'score': score,
        'indicators': indicators[:3]  # Top 3 indicators
    }