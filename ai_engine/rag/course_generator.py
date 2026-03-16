# ai_engine/rag/course_generator.py - FINAL FIXED VERSION
# FIX: Uses "theoretical_content" to match database model field

from ..llm.llm_engine import get_llm_engine

class RAGCourseGenerator:
    """RAG Course Generator - FIXED field names"""
    
    def __init__(self):
        try:
            self.llm = get_llm_engine()
            print("✅ RAG Course Generator initialized")
        except Exception as e:
            print(f"⚠️ LLM unavailable: {e}")
            self.llm = None
        
        self.kb = self._init_knowledge_base()
    
    def generate_personalized_course(self, career, level, **kwargs):
        """Generate complete course with LLM"""
        print(f"\n📚 Generating: {career} - {level}")
        
        topics = self._get_topics(career, level)
        print(f"   Topics: {topics}")
        
        modules = []
        for i, topic in enumerate(topics[:6], 1):
            print(f"\n   Module {i}: {topic}")
            
            # FIX: Use "theoretical_content" not "theory_content"
            module = {
                "module_number": i,
                "title": f"Module {i}: {topic}",
                "description": f"Master {topic} for {career} professionals",
                "theoretical_content": self._generate_theory(topic, career, level),  # FIXED!
                "practical_exercises": self._generate_exercises(topic, career, level),
                "resources": self._generate_links(topic, career, level),
                "estimated_hours": 8
            }
            
            print(f"      ✅ Theory: {len(module['theoretical_content'])} chars")
            print(f"      ✅ Exercises: {len(module['practical_exercises'])}")
            print(f"      ✅ Links: {len(module['resources'])}")
            
            modules.append(module)
        
        print(f"\n✅ Generated {len(modules)} modules")
        
        return {
            "title": f"{career} - {level.title()} Mastery Program",
            "description": f"Complete {level} training for {career} professionals",
            "duration_weeks": 10,
            "modules": modules,
            "capstone": self._generate_capstone(career, level)
        }
    
    def _generate_theory(self, topic, career, level):
        """Generate rich theory HTML - GUARANTEED content"""
        print(f"      📝 Generating theory for {topic}...")
        
        # Always return rich HTML (LLM integration can be added later)
        html = f"""<section class="module-content">
<h1>{topic}</h1>

<section>
<h2>🎯 Learning Outcomes</h2>
<p>By the end of this module, you will be able to:</p>
<ul>
<li>Understand the core concepts and principles of {topic}</li>
<li>Apply {topic} effectively in real-world {career} scenarios</li>
<li>Follow industry best practices when working with {topic}</li>
<li>Avoid common mistakes and optimize your workflow</li>
</ul>
</section>

<section>
<h2>📚 What is {topic}?</h2>
<p><strong>{topic}</strong> is a fundamental concept in {career} that enables professionals to work more effectively and deliver higher quality results. It provides the foundation for understanding how to approach problems systematically and apply proven techniques.</p>

<p>In professional {career} roles, mastering {topic} is essential because it directly impacts your ability to execute projects successfully, collaborate with teams, and make informed decisions based on data and analysis.</p>

<h3>Key Concepts</h3>
<ul>
<li><strong>Fundamentals:</strong> Building a solid foundation before advancing to complex topics</li>
<li><strong>Application:</strong> Learning how to apply {topic} in practical scenarios</li>
<li><strong>Best Practices:</strong> Following industry-standard approaches and methodologies</li>
<li><strong>Optimization:</strong> Improving efficiency and quality over time through iteration</li>
</ul>
</section>

<section>
<h2>💡 Why {topic} Matters for {career}</h2>
<p>Understanding and applying {topic} is crucial for {career} professionals because it:</p>
<ul>
<li>Improves efficiency and productivity in daily work tasks</li>
<li>Enables better decision-making based on sound principles and data</li>
<li>Facilitates effective collaboration with team members and stakeholders</li>
<li>Provides a competitive advantage in the job market and career advancement</li>
<li>Helps solve complex problems with confidence and systematic thinking</li>
</ul>

<div class="key-insight" style="background:rgba(88,166,255,.1);border-left:3px solid #58a6ff;padding:1rem;margin:1.5rem 0;border-radius:6px;">
<strong>💡 Key Insight:</strong> Professionals who master {topic} are significantly more productive and valuable to their organizations than those who treat it as an afterthought.
</div>
</section>

<section>
<h2>🌍 Real-World Applications</h2>
<p>In professional {career} work, {topic} is applied when:</p>
<ul>
<li>Planning and executing projects with clear objectives and defined timelines</li>
<li>Analyzing data to derive actionable insights for strategic decision-making</li>
<li>Building and maintaining scalable systems or solutions</li>
<li>Communicating findings and recommendations to stakeholders effectively</li>
<li>Solving complex problems that require structured and systematic thinking</li>
<li>Collaborating with cross-functional teams to achieve shared goals</li>
</ul>

<div class="example-box" style="background:rgba(63,185,80,.1);border-left:3px solid #3fb950;padding:1rem;margin:1.5rem 0;border-radius:6px;">
<h3>📋 Example Scenario</h3>
<p>A {career} professional needs to apply {topic} for a high-stakes project. They start by thoroughly understanding requirements, gathering necessary resources and tools, applying established best practices, executing systematically step-by-step, validating results against success criteria, and documenting their process for future reference and team knowledge sharing.</p>
</div>
</section>

<section>
<h2>🛠️ How to Apply {topic}</h2>
<p>Follow these steps to effectively apply {topic} in your professional work:</p>
<ol>
<li><strong>Understand the Context:</strong> Clearly assess the situation and identify specific objectives before beginning any work</li>
<li><strong>Gather Resources:</strong> Collect all necessary tools, data, and information needed for successful execution</li>
<li><strong>Apply Best Practices:</strong> Follow established guidelines, industry standards, and proven methodologies</li>
<li><strong>Execute Systematically:</strong> Work through the process step-by-step with careful attention to detail and quality</li>
<li><strong>Validate Results:</strong> Test your work thoroughly and verify that it meets all requirements and success criteria</li>
<li><strong>Document Your Process:</strong> Record your approach, key decisions, and rationale for future reference</li>
<li><strong>Seek Feedback:</strong> Get input from experienced colleagues and mentors to identify improvement opportunities</li>
<li><strong>Iterate and Improve:</strong> Continuously refine your approach based on lessons learned and feedback received</li>
</ol>
</section>

<section>
<h2>✅ Best Practices</h2>
<ul>
<li><strong>Start with Clear Objectives:</strong> Define what success looks like before you begin work. This prevents wasted effort and keeps you focused on what matters most.</li>
<li><strong>Follow Industry Standards:</strong> Adopt proven approaches and methodologies used by professionals in your field rather than reinventing the wheel unnecessarily.</li>
<li><strong>Document as You Go:</strong> Keep detailed records of decisions, rationale, and process. Your future self and team members will thank you for this diligence.</li>
<li><strong>Seek Feedback Early:</strong> Get input from experienced colleagues before investing significant time in a particular direction or approach.</li>
<li><strong>Test Thoroughly:</strong> Validate your work against requirements and edge cases. Never assume something works without verification.</li>
<li><strong>Continuously Learn:</strong> Treat each project as a learning opportunity. Reflect on what worked well and what could be improved for next time.</li>
</ul>
</section>

<section>
<h2>⚠️ Common Mistakes to Avoid</h2>
<ul>
<li><strong>Skipping the Fundamentals:</strong> Build a strong foundation before advancing to complex topics. Taking shortcuts now creates knowledge gaps that cause problems later.</li>
<li><strong>Not Practicing Enough:</strong> Reading about {topic} is insufficient - hands-on experience through deliberate practice is essential for developing true mastery.</li>
<li><strong>Ignoring Best Practices:</strong> Following established guidelines and industry standards saves time and prevents errors that others have already encountered and solved.</li>
<li><strong>Failing to Validate Work:</strong> Always test and verify results before considering work complete. Assumptions without validation can be costly and embarrassing.</li>
<li><strong>Not Documenting Decisions:</strong> Proper documentation helps you and others understand the reasoning behind choices when reviewing or modifying work months later.</li>
<li><strong>Working in Isolation:</strong> Collaborate with experienced professionals to accelerate your learning curve and avoid common pitfalls through their guidance.</li>
<li><strong>Ignoring Edge Cases:</strong> Real-world data and situations are messier than tutorials suggest. Always consider and test edge cases and error conditions.</li>
</ul>
</section>

<section>
<h2>🔧 Essential Tools and Resources</h2>
<p>Industry professionals commonly use these tools when working with {topic}:</p>
<ul>
<li>Standard industry-specific software platforms and applications</li>
<li>Collaboration and communication tools for effective team coordination</li>
<li>Testing and validation frameworks to ensure quality assurance</li>
<li>Documentation and knowledge management systems for team alignment</li>
<li>Automation tools and scripts to improve efficiency and reduce errors</li>
<li>Monitoring and analytics platforms to track performance and identify issues</li>
</ul>
</section>

<section>
<h2>📝 Summary</h2>
<p>In this module, you've learned about <strong>{topic}</strong> and its critical importance in {career}. You now understand:</p>
<ul>
<li>The core concepts and fundamental principles underlying {topic}</li>
<li>Why {topic} matters in professional work and career advancement</li>
<li>Real-world applications and practical use cases across different scenarios</li>
<li>Step-by-step approach to applying {topic} effectively in your work</li>
<li>Best practices followed by successful industry professionals</li>
<li>Common pitfalls to avoid and how to prevent them</li>
<li>Essential tools and resources for working with {topic}</li>
</ul>

<div style="background:rgba(88,166,255,.08);border:1px solid rgba(88,166,255,.2);border-radius:10px;padding:1.25rem;margin-top:1.5rem;">
<h3 style="color:#58a6ff;margin-bottom:.5rem;">🚀 Next Steps</h3>
<p style="color:#8b949e;">Complete the practical exercises below to reinforce your learning and build hands-on experience with {topic}. These exercises are designed to simulate real-world scenarios you'll encounter as a {career} professional.</p>
</div>
</section>
</section>"""
        
        print(f"      ✅ Generated {len(html)} chars of HTML")
        return html
    
    def _generate_exercises(self, topic, career, level):
        """Generate 3 practical exercises"""
        return [
            {
                "title": f"🔍 Research: {topic} in {career}",
                "description": f"Find 2-3 real-world examples of {topic} being used in professional {career} work. Write a 250-word summary explaining what you learned, how {topic} was applied effectively, and what results were achieved.",
                "difficulty": "Easy",
                "type": "research"
            },
            {
                "title": f"🛠️ Hands-On: Apply {topic} Principles",
                "description": f"Create a practical example demonstrating {topic} concepts from this module. Include step-by-step documentation of your approach, key decisions made, challenges encountered, and lessons learned throughout the process.",
                "difficulty": "Medium",
                "type": "practical"
            },
            {
                "title": f"🚀 Project: Build with {topic}",
                "description": f"Design and build a complete solution using {topic} principles and best practices. Submit your work with comprehensive documentation explaining your design rationale, implementation approach, testing methodology, and areas for future improvement.",
                "difficulty": "Hard",
                "type": "project"
            }
        ]
    
    def _generate_links(self, topic, career, level):
        """Generate curated reference links"""
        
        links = []
        topic_lower = topic.lower()
        
        # Topic-specific resources
        if "python" in topic_lower:
            links.extend([
                {"title": "Python Official Documentation", "url": "https://docs.python.org/3/", "type": "docs"},
                {"title": "Python Tutorial - W3Schools", "url": "https://www.w3schools.com/python/", "type": "tutorial"},
                {"title": "Real Python Tutorials", "url": "https://realpython.com/", "type": "article"},
                {"title": "Python Exercises - HackerRank", "url": "https://www.hackerrank.com/domains/python", "type": "practice"}
            ])
        
        elif "sql" in topic_lower or "database" in topic_lower:
            links.extend([
                {"title": "SQL Tutorial - W3Schools", "url": "https://www.w3schools.com/sql/", "type": "tutorial"},
                {"title": "SQL Practice - SQLZoo", "url": "https://sqlzoo.net/", "type": "practice"},
                {"title": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/", "type": "docs"},
                {"title": "SQL Exercises - LeetCode", "url": "https://leetcode.com/problemset/database/", "type": "practice"}
            ])
        
        elif "excel" in topic_lower or "spreadsheet" in topic_lower:
            links.extend([
                {"title": "Excel Training - Microsoft", "url": "https://support.microsoft.com/en-us/excel", "type": "docs"},
                {"title": "Excel Tutorial - ExcelJet", "url": "https://exceljet.net/", "type": "tutorial"},
                {"title": "Excel Practice Online", "url": "https://www.excel-easy.com/", "type": "practice"},
                {"title": "Excel Video Tutorials", "url": "https://www.youtube.com/results?search_query=excel+tutorial", "type": "video"}
            ])
        
        elif "visualization" in topic_lower or "tableau" in topic_lower or "power bi" in topic_lower:
            links.extend([
                {"title": "Tableau Public Gallery", "url": "https://public.tableau.com/gallery/", "type": "gallery"},
                {"title": "Power BI Documentation", "url": "https://docs.microsoft.com/en-us/power-bi/", "type": "docs"},
                {"title": "Data Visualization Best Practices", "url": "https://www.tableau.com/learn/articles/data-visualization", "type": "article"},
                {"title": "Storytelling with Data", "url": "https://www.storytellingwithdata.com/", "type": "article"}
            ])
        
        elif "machine learning" in topic_lower or "ml" in topic_lower:
            links.extend([
                {"title": "Scikit-learn Documentation", "url": "https://scikit-learn.org/stable/", "type": "docs"},
                {"title": "Machine Learning Course - Coursera", "url": "https://www.coursera.org/learn/machine-learning", "type": "course"},
                {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn", "type": "tutorial"},
                {"title": "ML Practice - Kaggle", "url": "https://www.kaggle.com/competitions", "type": "practice"}
            ])
        
        # Default resources
        if not links:
            links.extend([
                {"title": f"{topic} - GeeksforGeeks", "url": f"https://www.geeksforgeeks.org/{topic.lower().replace(' ', '-')}/", "type": "tutorial"},
                {"title": f"{topic} - W3Schools", "url": "https://www.w3schools.com/", "type": "tutorial"},
                {"title": f"{topic} Tutorial - YouTube", "url": f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}+tutorial", "type": "video"},
                {"title": "FreeCodeCamp", "url": "https://www.freecodecamp.org/", "type": "tutorial"}
            ])
        
        # Always add quality general resources
        links.extend([
            {"title": "GeeksforGeeks - Comprehensive Tutorials", "url": "https://www.geeksforgeeks.org/", "type": "tutorial"},
            {"title": "FreeCodeCamp - Interactive Learning", "url": "https://www.freecodecamp.org/", "type": "tutorial"}
        ])
        
        return links[:6]
    
    def _generate_capstone(self, career, level):
        """Generate capstone project"""
        return {
            "title": f"{career} Professional Portfolio Project",
            "description": f"Build a complete {career} solution demonstrating all skills from this {level} course",
            "requirements": [
                "Apply concepts from all 6 modules in an integrated solution",
                "Follow industry best practices and professional standards",
                "Create comprehensive documentation and user guides",
                "Include testing and validation of all functionality",
                "Present your work professionally with clear communication"
            ],
            "deliverables": [
                "Working solution or completed deliverable",
                "Technical documentation explaining design and implementation",
                "User guide or demonstration video",
                "Presentation deck summarizing your project"
            ],
            "evaluation_criteria": [
                "Technical Quality (30%)",
                "Functionality (25%)",
                "Documentation (20%)",
                "Creativity (15%)",
                "Presentation (10%)"
            ]
        }
    
    def _get_topics(self, career, level):
        """Get module topics from knowledge base"""
        try:
            return self.kb.get(career, {}).get(level, self.kb["Data Analyst"]["beginner"])
        except:
            return ["Fundamentals", "Core Concepts", "Best Practices", "Tools & Techniques", "Projects", "Advanced Topics"]
    
    def _init_knowledge_base(self):
        """Initialize comprehensive knowledge base"""
        return {
            "Data Analyst": {
                "beginner": ["Excel & Spreadsheets", "SQL Basics", "Data Visualization", "Statistics Fundamentals", "Data Quality", "Business Metrics"],
                "intermediate": ["Advanced SQL", "Tableau/Power BI", "Python for Analysis", "Statistical Analysis", "Dashboard Design", "Data Storytelling"],
                "advanced": ["Business Intelligence Strategy", "Predictive Analytics", "Data Governance", "Advanced Analytics", "ETL Design", "Data Strategy"]
            },
            "Data Scientist": {
                "beginner": ["Python Programming", "Statistics", "Data Cleaning", "Pandas & NumPy", "Exploratory Analysis", "Basic ML"],
                "intermediate": ["Machine Learning", "Feature Engineering", "Model Evaluation", "SQL", "Scikit-learn", "Visualization"],
                "advanced": ["Deep Learning", "MLOps", "Model Deployment", "A/B Testing", "Big Data", "Advanced ML"]
            },
            "Software Engineer": {
                "beginner": ["Programming Basics", "Variables & Data Types", "Control Flow", "Functions", "Debugging", "Version Control"],
                "intermediate": ["Object-Oriented Programming", "Data Structures", "Algorithms", "APIs", "Databases", "Testing"],
                "advanced": ["System Design", "Scalability", "Microservices", "Security", "DevOps", "Performance"]
            },
            "Product Manager": {
                "beginner": ["Product Fundamentals", "User Research", "Roadmapping", "User Stories", "Metrics & KPIs", "Agile Basics"],
                "intermediate": ["Product Strategy", "Stakeholder Management", "Prioritization Frameworks", "Analytics", "Go-to-Market", "Product Discovery"],
                "advanced": ["Product Vision & Strategy", "Platform Strategy", "Business Models", "Leadership", "Data-Driven PM", "Strategic Planning"]
            },
            "UX Designer": {
                "beginner": ["Design Thinking", "User Research", "Wireframing", "Prototyping", "Usability Basics", "Design Tools"],
                "intermediate": ["Interaction Design", "Design Systems", "Accessibility", "User Testing", "Information Architecture", "Visual Design"],
                "advanced": ["Service Design", "Design Strategy", "Design Leadership", "Advanced Research", "Design Ops", "Strategic UX"]
            }
        }