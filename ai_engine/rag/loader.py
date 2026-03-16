# ai_engine/rag/loader.py

import json
import os
from pathlib import Path


def load_documents():
    """
    Load course content documents from JSON files.

    Returns:
        List of document dictionaries with content and metadata
    """
    documents = []
    data_dir = Path(__file__).parent / "data"

    # Create data directory if it doesn't exist
    if not data_dir.exists():
        print(f"Creating data directory: {data_dir}")
        data_dir.mkdir(parents=True, exist_ok=True)
        return documents

    # Load course content JSON
    course_file = data_dir / "course_content.json"
    if course_file.exists():
        try:
            with open(course_file, 'r', encoding='utf-8') as f:
                course_data = json.load(f)

            # Process course content into documents
            for career, levels in course_data.items():
                for level, modules in levels.items():
                    for module in modules:
                        # Create document from module
                        doc_content = f"""
Career: {career}
Level: {level}
Module: {module.get('title', 'Untitled')}
Description: {module.get('description', '')}
Skills: {', '.join(module.get('skills', []))}
Duration: {module.get('duration', '')}

Theory:
{module.get('theory', '')}

Exercises:
{json.dumps(module.get('exercises', []), indent=2)}
"""

                        documents.append({
                            'content': doc_content.strip(),
                            'metadata': {
                                'career': career,
                                'level': level,
                                'title': module.get('title', ''),
                                'type': 'course_module'
                            }
                        })

            print(f"Loaded {len(documents)} documents from {course_file}")

        except json.JSONDecodeError as e:
            print(f"Error loading JSON from {course_file}: {e}")
        except Exception as e:
            print(f"Error loading documents: {e}")
    else:
        print(f"Course content file not found: {course_file}")
        print("Creating sample course_content.json...")
        _create_sample_course_content(course_file)

    # Load additional documents from data folder
    for file_path in data_dir.glob("*.json"):
        if file_path.name != "course_content.json":
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            documents.append(item)
                elif isinstance(data, dict):
                    documents.append(data)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

    return documents


def _create_sample_course_content(file_path):
    """Create a sample course_content.json file"""
    sample_data = {
        "Data Science": {
            "Beginner": [
                {
                    "title": "Introduction to Data Science",
                    "description": "Learn the fundamentals of data science and its applications",
                    "duration": "2-3 hours",
                    "skills": ["Python basics", "Data analysis concepts", "Industry overview"],
                    "theory": "Data science combines statistics, programming, and domain knowledge to extract insights from data. It involves collecting, cleaning, analyzing, and visualizing data to solve real-world problems.",
                    "exercises": [
                        {
                            "title": "Install Python Environment",
                            "description": "Set up Python and Jupyter Notebook for data science",
                            "outcome": "Working development environment"
                        }
                    ]
                },
                {
                    "title": "Python Programming Fundamentals",
                    "description": "Master Python basics for data manipulation",
                    "duration": "5-6 hours",
                    "skills": ["Variables", "Data types", "Control flow", "Functions"],
                    "theory": "Python is the primary language for data science. Understanding variables, loops, conditionals, and functions is essential for data manipulation and analysis.",
                    "exercises": [
                        {
                            "title": "Build a Calculator",
                            "description": "Create a simple calculator using Python functions",
                            "outcome": "Understanding of functions and operators"
                        }
                    ]
                }
            ],
            "Intermediate": [
                {
                    "title": "Machine Learning Fundamentals",
                    "description": "Introduction to supervised and unsupervised learning",
                    "duration": "10-12 hours",
                    "skills": ["Linear regression", "Classification", "Model evaluation"],
                    "theory": "Machine learning enables computers to learn from data. Explore supervised learning for predictions and unsupervised learning for pattern discovery.",
                    "exercises": [
                        {
                            "title": "Build a Prediction Model",
                            "description": "Create a linear regression model",
                            "outcome": "End-to-end model building experience"
                        }
                    ]
                }
            ]
        },
        "Web Development": {
            "Beginner": [
                {
                    "title": "HTML and CSS Fundamentals",
                    "description": "Build the foundation of web development",
                    "duration": "4-5 hours",
                    "skills": ["HTML structure", "CSS styling", "Responsive design"],
                    "theory": "HTML provides structure to web pages, while CSS handles presentation. Learn semantic HTML and modern CSS techniques.",
                    "exercises": [
                        {
                            "title": "Create a Portfolio Page",
                            "description": "Build a personal portfolio website",
                            "outcome": "First complete web page"
                        }
                    ]
                }
            ]
        }
    }

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        print(f"Created sample course content at: {file_path}")
    except Exception as e:
        print(f"Error creating sample file: {e}")


def load_document_from_file(file_path):
    """
    Load a single document from a file path.

    Args:
        file_path: Path to document file

    Returns:
        Document dictionary
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    if file_path.suffix == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    elif file_path.suffix == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return {
                'content': content,
                'metadata': {
                    'filename': file_path.name,
                    'type': 'text'
                }
            }

    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")


def add_custom_document(career, level, module_data):
    """
    Add a custom document to the course content.

    Args:
        career: Career field
        level: Skill level
        module_data: Module information dict

    Returns:
        bool: Success status
    """
    data_dir = Path(__file__).parent / "data"
    course_file = data_dir / "course_content.json"

    try:
        # Load existing content
        if course_file.exists():
            with open(course_file, 'r', encoding='utf-8') as f:
                course_data = json.load(f)
        else:
            course_data = {}

        # Add new module
        if career not in course_data:
            course_data[career] = {}

        if level not in course_data[career]:
            course_data[career][level] = []

        course_data[career][level].append(module_data)

        # Save back to file
        with open(course_file, 'w', encoding='utf-8') as f:
            json.dump(course_data, f, indent=2, ensure_ascii=False)

        print(f"Added custom module to {career} - {level}")
        return True

    except Exception as e:
        print(f"Error adding custom document: {e}")
        return False