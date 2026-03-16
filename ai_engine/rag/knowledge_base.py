# ai_engine/rag/knowledge_base.py
"""
Enhanced Knowledge Base for RAG-Powered Career Assessment
Optimized for bulletproof question generation with pre-built wrong answers
"""

import random

# Main knowledge base dictionary
ENHANCED_CAREER_KNOWLEDGE = {
    "Data Scientist": {
        "beginner": {
            "concepts": {
                "Python Programming Basics": {
                    "description": "Python is the primary language for data science with rich libraries like NumPy, Pandas, and Scikit-learn",
                    "why_important": "Python enables rapid data analysis, modeling, and automation through its extensive data science ecosystem",
                    "real_world_use": "Data scientists use Python daily to load datasets, clean data, build models, and create visualizations",
                    "wrong_answers": [
                        "Only for web development and backend systems",
                        "Too slow for any real data processing work",
                        "Requires buying expensive licenses to use legally",
                        "Cannot handle datasets larger than 1000 rows"
                    ]
                },
                "Statistics Fundamentals": {
                    "description": "Statistics provides mathematical foundation for understanding distributions, variability, and making inferences",
                    "why_important": "Statistical methods distinguish real patterns from random noise and quantify uncertainty",
                    "real_world_use": "Every A/B test, hypothesis test, and model evaluation relies on statistical principles",
                    "wrong_answers": [
                        "Only needed for academic research work",
                        "Mean is always the best measure",
                        "Correlation always implies causation",
                        "Can prove anything with enough data"
                    ]
                },
                "Pandas Library": {
                    "description": "Pandas provides DataFrame structures for efficiently manipulating tabular data",
                    "why_important": "Most data comes in tables - Pandas makes transforming millions of rows fast",
                    "real_world_use": "Loading CSV files, handling missing values, aggregating data, merging datasets",
                    "wrong_answers": [
                        "Can only read CSV files exclusively",
                        "Must load entire datasets into RAM",
                        "Slower than Excel for all operations",
                        "Only works with numeric data types"
                    ]
                },
                "NumPy Arrays": {
                    "description": "NumPy enables fast mathematical operations through vectorization and C-optimized functions",
                    "why_important": "NumPy operations are 50-100x faster than Python loops",
                    "real_world_use": "Matrix multiplication, statistical calculations, array manipulations",
                    "wrong_answers": [
                        "Python lists are just as fast",
                        "Only works with integers exclusively",
                        "Requires writing C code directly",
                        "Cannot work with Pandas DataFrames"
                    ]
                },
            }
        },
        "intermediate": {
            "concepts": {
                "Feature Engineering": {
                    "description": "Feature engineering creates meaningful variables from raw data through transformations and combinations",
                    "why_important": "Good features improve model performance more than complex algorithms",
                    "real_world_use": "Creating day-of-week, polynomial features, interaction terms, binning variables",
                    "wrong_answers": [
                        "More features always means better performance",
                        "Only about creating interaction terms",
                        "AutoML eliminates this need completely",
                        "Should only use original raw features"
                    ]
                },
                "Cross Validation": {
                    "description": "K-fold cross-validation tests performance across multiple train-test splits",
                    "why_important": "Single split can be lucky - CV provides reliable estimates",
                    "real_world_use": "5-fold CV for selection, TimeSeriesSplit for temporal, Stratified for imbalanced",
                    "wrong_answers": [
                        "More folds always better regardless",
                        "Eliminates need for test set",
                        "Same approach for all data types",
                        "Only needed for large datasets"
                    ]
                },
                "SQL for Data Science": {
                    "description": "SQL extracts, filters, aggregates, and joins data from databases",
                    "why_important": "Most production data lives in databases - must extract efficiently",
                    "real_world_use": "Joining tables, calculating revenue by region, filtering date ranges",
                    "wrong_answers": [
                        "NoSQL means SQL is obsolete now",
                        "All analysis should be in Python",
                        "SQL only for database administrators",
                        "Excel replaces SQL for all tasks"
                    ]
                },
                "Machine Learning": {
                    "description": "ML algorithms learn patterns from training data to make predictions",
                    "why_important": "ML automates decisions at scale where manual review is impractical",
                    "real_world_use": "Predicting churn, classifying spam, recommending products, forecasting",
                    "wrong_answers": [
                        "Always outperforms simple models",
                        "Deep learning required for all",
                        "More data always improves accuracy",
                        "Models never need human oversight"
                    ]
                }
            }
        },
        "advanced": {
            "concepts": {
                "Deep Learning": {
                    "description": "Deep learning uses multi-layer neural networks to learn hierarchical representations",
                    "why_important": "Excels at unstructured data where manual feature engineering is difficult",
                    "real_world_use": "Image classification, language models, speech recognition, autonomous driving",
                    "wrong_answers": [
                        "Always better than traditional methods",
                        "Works well with tiny datasets",
                        "No feature engineering ever needed",
                        "Always provides interpretable results"
                    ]
                },
                "MLOps": {
                    "description": "MLOps applies DevOps practices for automated deployment, monitoring, and retraining",
                    "why_important": "Models fail without proper monitoring, versioning, and automated retraining",
                    "real_world_use": "CI/CD pipelines, feature stores, retraining, A/B testing, drift monitoring",
                    "wrong_answers": [
                        "Only about deploying models once",
                        "Models never degrade over time",
                        "Only for huge tech companies",
                        "Just means using Docker containers"
                    ]
                },
                "Model Deployment": {
                    "description": "Deployment serves predictions via REST APIs, batch processing, or embedded systems",
                    "why_important": "Models have zero value until making real-world predictions at scale",
                    "real_world_use": "REST API with Flask, batch predictions, real-time streaming, edge deployment",
                    "wrong_answers": [
                        "Final step with no maintenance",
                        "Same model works everywhere unchanged",
                        "No monitoring needed after deployment",
                        "Can deploy without considering latency"
                    ]
                },
                "A/B Testing": {
                    "description": "A/B testing uses randomized experiments to measure causal impact with statistical rigor",
                    "why_important": "Only way to prove changes cause improvements vs just correlate",
                    "real_world_use": "Testing features, model improvements, UI changes, algorithms, pricing",
                    "wrong_answers": [
                        "Higher metric variant always wins",
                        "Can peek at results early safely",
                        "More variants simultaneously is better",
                        "No significance testing needed"
                    ]
                }
            }
        }
    },
    "Software Engineer": {
        "beginner": {
            "concepts": {
                "Variables": {
                    "description": "Variables store data values in memory for reference and manipulation",
                    "why_important": "Variables let programs remember information and pass data",
                    "real_world_use": "Storing user input, results, configs, counters, responses",
                    "wrong_answers": [
                        "Only for numbers not text",
                        "Must declare before all code",
                        "Cannot change after creation",
                        "Only exist inside classes"
                    ]
                },
                "Functions": {
                    "description": "Functions are reusable code blocks that accept parameters and return values",
                    "why_important": "Reduce duplication, improve maintainability, enable testing, organize logic",
                    "real_world_use": "Calculating tax, validating emails, sending notifications, fetching data",
                    "wrong_answers": [
                        "Make code slower always",
                        "Write all in one function",
                        "Names don't matter at all",
                        "Can only return one type"
                    ]
                },
                "Loops": {
                    "description": "Loops repeat code blocks until conditions are met",
                    "why_important": "Eliminate repetitive code and process collections efficiently",
                    "real_world_use": "Processing cart items, reading files, retrying requests",
                    "wrong_answers": [
                        "Infinite loops are acceptable",
                        "Nested loops always best",
                        "Replace all with recursion",
                        "Performance never matters"
                    ]
                },
                "Conditionals": {
                    "description": "Conditionals execute different paths based on boolean expressions",
                    "why_important": "Programs need to make decisions and respond to inputs",
                    "real_world_use": "Checking permissions, validating input, handling errors",
                    "wrong_answers": [
                        "Deep nesting is good practice",
                        "Switch always better than if",
                        "Avoid and use try-catch",
                        "Ternary too complex to use"
                    ]
                }
            }
        },
        "intermediate": {
            "concepts": {
                "APIs": {
                    "description": "REST APIs use HTTP methods for system communication",
                    "why_important": "Enable applications to work together and share data",
                    "real_world_use": "Mobile to backend, microservices, integrations",
                    "wrong_answers": [
                        "REST is only API type",
                        "More endpoints is better",
                        "Versioning is optional",
                        "No security needed"
                    ]
                },
                "OOP": {
                    "description": "OOP organizes code into objects with data and behavior",
                    "why_important": "Models entities, enables reuse, hides complexity",
                    "real_world_use": "User class, Account class, Vehicle hierarchy",
                    "wrong_answers": [
                        "Everything must be objects",
                        "Inheritance always better",
                        "More classes is better",
                        "Required for all programs"
                    ]
                },
                "Testing": {
                    "description": "Testing verifies correctness through automated tests",
                    "why_important": "Catches regressions, enables refactoring, improves quality",
                    "real_world_use": "Unit tests, integration tests, E2E tests",
                    "wrong_answers": [
                        "100% coverage means no bugs",
                        "Wastes more time than saves",
                        "Only QA writes tests",
                        "Never update or delete tests"
                    ]
                },
                "Databases": {
                    "description": "Databases store data persistently with efficient querying",
                    "why_important": "Persist data beyond execution and query at scale",
                    "real_world_use": "User accounts, transactions, catalogs, events",
                    "wrong_answers": [
                        "All in one giant table",
                        "NoSQL always faster",
                        "Indexes are optional",
                        "Backups only for critical"
                    ]
                }
            }
        },
        "advanced": {
            "concepts": {
                "System Design": {
                    "description": "System design creates scalable architectures through proper distribution",
                    "why_important": "Good architecture scales while bad fails under load",
                    "real_world_use": "Netflix streaming, Uber dispatch, Twitter timeline",
                    "wrong_answers": [
                        "Start with microservices always",
                        "Bigger servers are sufficient",
                        "One database handles anything",
                        "Architecture doesn't matter yet"
                    ]
                },
                "Microservices": {
                    "description": "Microservices decompose apps into independent deployable services",
                    "why_important": "Enables team ownership, diversity, isolated scaling",
                    "real_world_use": "Auth, payments, notifications, recommendations",
                    "wrong_answers": [
                        "Solves all problems",
                        "Start from day one",
                        "Never coordinate data",
                        "Easier debugging"
                    ]
                },
                "Scalability": {
                    "description": "Scalability handles growing load through horizontal or vertical scaling",
                    "why_important": "Must grow with users without degrading",
                    "real_world_use": "Load balancing, replication, caching, CDN",
                    "wrong_answers": [
                        "Vertical gives unlimited capacity",
                        "Horizontal needs no code changes",
                        "Caching adds no benefits",
                        "Can wait until problems"
                    ]
                },
                "Security": {
                    "description": "Security protects through authentication, encryption, validation",
                    "why_important": "Breaches cost money, trust, and legal liability",
                    "real_world_use": "OAuth, RBAC, HTTPS, injection prevention",
                    "wrong_answers": [
                        "Only QA responsibility",
                        "HTTPS optional for non-finance",
                        "Skip validation for trusted",
                        "Add after launch"
                    ]
                }
            }
        }
    }
}


class EnhancedKnowledgeBase:
    """Enhanced KB for RAG"""
    
    def __init__(self):
        self.knowledge = ENHANCED_CAREER_KNOWLEDGE
    
    def get_all_concepts(self, career, level):
        try:
            return list(self.knowledge[career][level]["concepts"].keys())
        except KeyError:
            return []
    
    def build_rag_context(self, career, level, topic):
        try:
            concepts = self.knowledge[career][level]["concepts"]
            concept = concepts.get(topic)
            
            if not concept:
                for name, details in concepts.items():
                    if topic.lower() in name.lower():
                        concept = details
                        break
            
            if not concept:
                concept = list(concepts.values())[0]
            
            context = f"""CONCEPT: {topic}

Description: {concept['description']}

Why it matters: {concept['why_important']}

Real-world use: {concept['real_world_use']}

Wrong answers:
"""
            for wrong in concept.get('wrong_answers', [])[:4]:
                context += f"- {wrong}\n"
            
            return context.strip()
        except:
            return ""


_kb = None

def get_enhanced_knowledge_base():
    global _kb
    if _kb is None:
        _kb = EnhancedKnowledgeBase()
        print(f"✅ Enhanced KB: {len(ENHANCED_CAREER_KNOWLEDGE)} careers loaded")
    return _kb