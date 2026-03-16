# ai_engine/rag/enhanced_knowledge.py
"""
EXPANDED KNOWLEDGE BASE
- 5+ unique concepts per career per level (prevents repeated questions)
- Each concept has a full description + plausible wrong options of equal length
"""

CAREER_KNOWLEDGE = {

    "Software Engineer": {
        "beginner": {
            "Variables and Data Types": {
                "description": "Storage containers that hold different types of data: integers for whole numbers, strings for text, booleans for true/false, and floats for decimal values.",
                "why_important": "Choosing the right data type prevents bugs, improves memory efficiency, and makes code more maintainable and readable for other developers.",
                "wrong_concepts": [
                    "Variables should always use the most generic type to handle any possible future data changes in the application.",
                    "Declaring all variables as strings simplifies code since type conversion will happen automatically at runtime.",
                    "Data types are managed automatically by the compiler so developers do not need to think about them."
                ]
            },
            "Control Flow": {
                "description": "Structures like if-else statements, for and while loops, and switch cases that control the sequence in which code executes based on conditions.",
                "why_important": "Control flow enables programs to make decisions and repeat operations, which is fundamental to solving any real-world programming problem.",
                "wrong_concepts": [
                    "Deeply nested if-else blocks are preferred because they keep all related logic visible in one place on screen.",
                    "While loops should always be used instead of for loops because they offer greater flexibility in all situations.",
                    "Switch statements should replace all if-else chains to ensure code remains short and easy to maintain."
                ]
            },
            "Functions": {
                "description": "Reusable blocks of code that perform a specific task, accept inputs as parameters, process them, and optionally return an output value.",
                "why_important": "Functions enable code reuse, improve testability, make debugging easier, and organise code into logical manageable units.",
                "wrong_concepts": [
                    "Functions should always return multiple values to make them more flexible and useful in different contexts.",
                    "Global variables should be used instead of parameters to avoid the complexity of passing data between functions.",
                    "Longer functions are preferable because they reduce the overhead caused by multiple function call operations."
                ]
            },
            "Version Control with Git": {
                "description": "Using Git to track code changes, create branches for features, merge contributions, and collaborate safely with other developers.",
                "why_important": "Version control enables team collaboration, provides a full history of changes, allows rollbacks, and prevents accidental overwrites.",
                "wrong_concepts": [
                    "Committing large batches of changes at once is more efficient than making many small focused commits regularly.",
                    "The main branch is the appropriate place to develop new features since it keeps everything in one location.",
                    "Merge conflicts indicate that Git is being used incorrectly and should be resolved by reverting all changes."
                ]
            },
            "Debugging Techniques": {
                "description": "Systematic approaches to finding and fixing errors, including using print statements, debuggers, reading stack traces, and isolating bugs.",
                "why_important": "Effective debugging reduces development time, improves code quality, and builds a deeper understanding of how the program actually executes.",
                "wrong_concepts": [
                    "Adding print statements throughout the codebase is always the most reliable approach to debugging any kind of error.",
                    "If code runs without throwing exceptions it can be considered correct and does not require further investigation.",
                    "Rewriting a buggy section from scratch is always faster and more effective than tracing through existing code."
                ]
            },
        },
        "intermediate": {
            "Object-Oriented Programming": {
                "description": "A programming paradigm using objects that combine data and behaviour, with core concepts including inheritance, encapsulation, and polymorphism.",
                "why_important": "OOP models real-world entities naturally, enables code reuse through inheritance, and makes large codebases more manageable through encapsulation.",
                "wrong_concepts": [
                    "Inheritance should be the primary mechanism for sharing code between all classes regardless of their relationship.",
                    "All class attributes should be made public so they can be accessed flexibly from any part of the codebase.",
                    "Creating very deep inheritance hierarchies improves code organisation by showing clear relationships between classes."
                ]
            },
            "Database Fundamentals": {
                "description": "Understanding relational databases, writing SQL queries with SELECT, JOIN, and WHERE, using transactions, indexes, and designing normalised schemas.",
                "why_important": "Most applications store data persistently; database knowledge enables efficient data retrieval, maintains integrity, and prevents performance bottlenecks.",
                "wrong_concepts": [
                    "Adding database indexes to every column in a table improves all query types without any significant performance trade-off.",
                    "Database transactions are only necessary when multiple users are simultaneously accessing and modifying the same data.",
                    "Denormalised database schemas are always preferred because they eliminate the need for complex join operations."
                ]
            },
            "API Design": {
                "description": "Creating RESTful APIs with correct HTTP methods, status codes, versioning strategies, authentication mechanisms, and clear documentation.",
                "why_important": "APIs enable system integration; well-designed APIs are easy to use, maintain backward compatibility, and scale gracefully over time.",
                "wrong_concepts": [
                    "All API endpoints should use POST requests because they are the most flexible and secure HTTP method available.",
                    "API versioning is something that can always be added later without affecting existing consumers of the API.",
                    "Returning detailed error messages including full stack traces in API responses helps developers debug problems faster."
                ]
            },
            "Testing and Test-Driven Development": {
                "description": "Writing unit tests, integration tests, and end-to-end tests to verify code behaviour, along with the TDD practice of writing tests before code.",
                "why_important": "Tests catch bugs early, enable safe refactoring, serve as living documentation, and give confidence when deploying changes to production.",
                "wrong_concepts": [
                    "Testing should only be performed manually by QA teams after all development work on a feature is complete.",
                    "Writing tests before writing the actual code adds unnecessary complexity that slows down development significantly.",
                    "Achieving 100% code coverage guarantees that the software has no bugs and will work correctly in production."
                ]
            },
            "Design Patterns": {
                "description": "Reusable solutions to common software problems including creational patterns like Singleton, structural patterns like Adapter, and behavioural patterns like Observer.",
                "why_important": "Design patterns provide proven solutions, create a shared vocabulary for developers, and prevent reinventing solutions to problems others have already solved.",
                "wrong_concepts": [
                    "Design patterns should be applied to every part of the codebase to ensure the software is built using best practices.",
                    "The Singleton pattern is always the best approach for managing shared state and resources across an application.",
                    "Familiarity with design patterns makes them applicable to all software problems regardless of the specific context."
                ]
            },
        },
        "advanced": {
            "System Architecture": {
                "description": "Designing scalable systems using microservices or monoliths, implementing load balancing, caching strategies, message queues, and addressing distributed system challenges.",
                "why_important": "Architecture decisions determine long-term scalability, reliability, and maintainability; poor choices are very expensive to reverse later.",
                "wrong_concepts": [
                    "Microservices architecture should always be chosen from the start as it is guaranteed to scale better than a monolith.",
                    "Caching should be applied at every layer of the application stack to maximise overall system performance.",
                    "Distributed systems should always prioritise strict data consistency over availability for all types of use cases."
                ]
            },
            "Performance Optimization": {
                "description": "Profiling code, identifying bottlenecks, optimising algorithms and database queries, reducing memory footprint, and implementing effective caching strategies.",
                "why_important": "Performance directly impacts user experience and infrastructure costs; optimised systems handle more concurrent users with fewer resources.",
                "wrong_concepts": [
                    "All micro-optimisations at the code level should be addressed first before investigating architectural performance issues.",
                    "Adding more server hardware is always the most reliable solution to any application performance bottleneck encountered.",
                    "Performance optimisation work should begin at the very start of the project before any functional features are built."
                ]
            },
            "Security Best Practices": {
                "description": "Implementing input validation, SQL injection prevention, XSS protection, secure authentication, HTTPS, and following the OWASP Top 10 security guidelines.",
                "why_important": "Security vulnerabilities can cause data breaches, financial losses, and reputational damage; building security in from the start is far cheaper than retrofitting.",
                "wrong_concepts": [
                    "Security can be addressed comprehensively as a final phase at the end of the software development lifecycle.",
                    "Using a well-known web framework guarantees that all security vulnerabilities in the application are automatically handled.",
                    "Encrypting all data in the database is sufficient security and eliminates the need for other protective measures."
                ]
            },
            "Code Review and Refactoring": {
                "description": "Systematically reviewing code for quality, readability, and correctness, and continuously refactoring to improve internal structure without changing external behaviour.",
                "why_important": "Code reviews catch bugs before they reach production, share knowledge across the team, and ensure consistent code quality standards.",
                "wrong_concepts": [
                    "Code review is primarily a gatekeeping activity to check that developers have followed all coding style requirements.",
                    "Refactoring should only be done as a dedicated project phase rather than as a continuous part of development work.",
                    "Once code is working correctly and passing all tests there is no justification for spending time on refactoring."
                ]
            },
            "Cloud and DevOps Fundamentals": {
                "description": "Understanding cloud services, containerisation with Docker, orchestration with Kubernetes, CI/CD pipelines, and infrastructure as code principles.",
                "why_important": "Modern software requires cloud deployment; DevOps practices reduce deployment risk, increase release frequency, and improve team collaboration.",
                "wrong_concepts": [
                    "All applications should be deployed to Kubernetes because it provides the most robust and comprehensive deployment platform.",
                    "CI/CD pipelines are only beneficial for large engineering teams that make multiple code deployments every single day.",
                    "Cloud infrastructure automatically handles all scaling requirements so no capacity planning or configuration is needed."
                ]
            },
        }
    },

    "Data Scientist": {
        "beginner": {
            "Python for Data Science": {
                "description": "Using Python with NumPy for numerical operations, Pandas for data manipulation, and Matplotlib and Seaborn for creating visualisations.",
                "why_important": "Python's data science ecosystem makes complex analytical tasks efficient; Pandas handles millions of rows and NumPy enables fast mathematical operations.",
                "wrong_concepts": [
                    "R programming should always be chosen over Python for any serious data science work due to its statistical capabilities.",
                    "Python's NumPy library is primarily designed for web scraping and data collection rather than numerical computation.",
                    "Pandas DataFrames should be avoided for large datasets because they consume too much memory to be practical."
                ]
            },
            "Statistics Fundamentals": {
                "description": "Understanding mean, median, mode, variance, standard deviation, probability distributions, and the basics of hypothesis testing.",
                "why_important": "Statistics helps distinguish real patterns from random noise, enables evidence-based decisions, and forms the mathematical foundation for machine learning.",
                "wrong_concepts": [
                    "The arithmetic mean is always the most reliable measure of central tendency regardless of the distribution of data.",
                    "A strong correlation between two variables provides sufficient evidence to conclude that one variable causes the other.",
                    "A p-value below 0.05 always confirms that a finding has significant practical importance for business decisions."
                ]
            },
            "Data Cleaning and Preprocessing": {
                "description": "Handling missing values through imputation or removal, eliminating duplicates, correcting data types, treating outliers, and standardising formats.",
                "why_important": "Data quality directly determines model quality; poor data produces unreliable results and misleading conclusions regardless of algorithm choice.",
                "wrong_concepts": [
                    "All rows that contain any missing values should always be deleted entirely to ensure the dataset remains clean.",
                    "Outliers in any dataset are always the result of data entry errors and should therefore always be removed.",
                    "Data cleaning is a one-time step that only needs to be performed at the start of the analytical project."
                ]
            },
            "Exploratory Data Analysis": {
                "description": "Systematically examining datasets using summary statistics, distributions, correlations, and visualisations to discover patterns and generate hypotheses.",
                "why_important": "EDA reveals data quality issues, guides feature engineering decisions, and helps select appropriate modelling approaches before building models.",
                "wrong_concepts": [
                    "Exploratory analysis should be skipped when working with structured data since the patterns will emerge through modelling.",
                    "Creating as many visualisations as possible during EDA always leads to better insights and more accurate models.",
                    "Summary statistics alone provide a complete picture of the data without needing any visual exploration of distributions."
                ]
            },
            "Pandas Data Manipulation": {
                "description": "Using Pandas for filtering, grouping, aggregating, merging DataFrames, applying functions, and reshaping tabular data efficiently.",
                "why_important": "Pandas is the core tool for data manipulation in Python; mastery dramatically reduces the time required for data preparation tasks.",
                "wrong_concepts": [
                    "Using Python loops to iterate through DataFrame rows is the recommended approach for data manipulation operations.",
                    "The merge function in Pandas should always be avoided because SQL queries are always more efficient for joining data.",
                    "GroupBy operations in Pandas are only useful for simple count aggregations and cannot handle complex analytical tasks."
                ]
            },
        },
        "intermediate": {
            "Machine Learning Algorithms": {
                "description": "Supervised learning including regression and classification with decision trees and random forests, and unsupervised learning including clustering and PCA.",
                "why_important": "Different algorithms suit different problem types; selecting the right algorithm saves significant time and can dramatically improve accuracy.",
                "wrong_concepts": [
                    "Deep learning neural networks consistently and reliably outperform traditional machine learning algorithms on all datasets.",
                    "Random forest algorithms should always be used as the first and primary approach for any classification problem.",
                    "More complex models with higher training accuracy will always deliver better performance when deployed to production."
                ]
            },
            "Feature Engineering": {
                "description": "Creating new predictive features from existing data through transformations, combinations, encoding categorical variables, binning, and scaling.",
                "why_important": "Good features often improve model performance more than algorithm selection; domain knowledge expressed as features is a key competitive advantage.",
                "wrong_concepts": [
                    "Including all available features in a machine learning model always produces the best possible predictive performance.",
                    "Deep learning completely eliminates the need for manual feature engineering in all types of machine learning problems.",
                    "Feature scaling is only necessary when using neural networks and has no impact on tree-based machine learning models."
                ]
            },
            "Model Evaluation and Validation": {
                "description": "Using cross-validation, train/test splits, and metrics including accuracy, precision, recall, F1 score, and ROC-AUC to assess model performance.",
                "why_important": "Proper validation ensures models generalise to new unseen data rather than simply memorising patterns in the training examples.",
                "wrong_concepts": [
                    "Accuracy alone is always the most informative and reliable metric for evaluating any classification model's performance.",
                    "Having a sufficiently large training dataset completely eliminates the need for cross-validation or a separate test set.",
                    "The same held-out test dataset can be reused multiple times to evaluate and compare different model iterations."
                ]
            },
            "Ensemble Methods": {
                "description": "Combining multiple models through bagging like Random Forest, boosting like XGBoost and LightGBM, and stacking to improve prediction performance.",
                "why_important": "Ensemble methods reduce variance and bias compared to single models, consistently achieving better results in many real-world prediction tasks.",
                "wrong_concepts": [
                    "Ensemble methods are only useful for classification tasks and provide no benefit for regression or ranking problems.",
                    "Adding more base models to an ensemble always results in proportional improvements in overall predictive performance.",
                    "Stacking ensemble methods are straightforward to implement and are always the best starting point for any prediction task."
                ]
            },
            "Time Series Analysis": {
                "description": "Analysing temporal data using trend decomposition, stationarity tests, ARIMA models, and forecasting techniques for time-dependent data.",
                "why_important": "Many business problems involve time-ordered data; time series methods capture temporal patterns that standard ML models typically cannot.",
                "wrong_concepts": [
                    "Standard machine learning algorithms can be applied directly to time series data without any special consideration or modification.",
                    "Stationarity is a minor technical detail in time series analysis that rarely affects the quality of forecasting results.",
                    "Longer historical time series data always produces more accurate forecasts regardless of how the data patterns may change."
                ]
            },
        },
        "advanced": {
            "Deep Learning": {
                "description": "Designing neural networks with multiple layers including CNNs for image data, RNNs and LSTMs for sequences, and transformers for language tasks.",
                "why_important": "Deep learning excels at processing unstructured data like images, text, and audio where manual feature engineering is impractical.",
                "wrong_concepts": [
                    "Adding more layers to a neural network consistently and reliably improves its accuracy on previously unseen test data.",
                    "Pre-trained transformer models can be used directly without any fine-tuning for domain-specific natural language tasks.",
                    "Convolutional neural networks are the optimal architecture for modelling sequential and time-dependent text data."
                ]
            },
            "Model Deployment and MLOps": {
                "description": "Serving models as REST APIs, implementing monitoring for performance and data drift, managing model versioning, and automating retraining pipelines.",
                "why_important": "Models only create business value when deployed reliably; production systems require continuous monitoring and maintenance to remain accurate.",
                "wrong_concepts": [
                    "Once a machine learning model is successfully deployed it will maintain its predictive accuracy indefinitely without monitoring.",
                    "Model deployment is a pure DevOps responsibility and does not require any ongoing involvement from the data scientist.",
                    "Batch processing for model inference is always preferable to real-time serving because it consistently reduces infrastructure costs."
                ]
            },
            "Experiment Design and Causal Inference": {
                "description": "Designing rigorous A/B tests, understanding confounding variables, applying causal inference techniques, and measuring true treatment effects.",
                "why_important": "Observational data alone cannot prove causation; proper experiment design ensures that measured effects are genuine and not due to confounding.",
                "wrong_concepts": [
                    "A/B tests should be terminated as soon as they reach statistical significance to avoid wasting time and resources.",
                    "Observational data with sufficient sample size always provides equivalent evidence to a properly randomised controlled experiment.",
                    "Statistical significance of a result is sufficient on its own to confirm that an intervention had a meaningful causal effect."
                ]
            },
            "Natural Language Processing": {
                "description": "Processing and analysing text data using tokenisation, embeddings, sentiment analysis, named entity recognition, and transformer-based language models.",
                "why_important": "NLP unlocks insights from unstructured text, which represents a large proportion of available data in most organisations.",
                "wrong_concepts": [
                    "Bag-of-words text representation captures all linguistic meaning and context needed for high-quality NLP model performance.",
                    "Pre-trained language models always outperform simpler statistical approaches regardless of the specific task or dataset size.",
                    "More text training data always improves NLP model performance regardless of the quality or relevance of the data."
                ]
            },
            "Big Data and Distributed Computing": {
                "description": "Processing large datasets using distributed frameworks like Apache Spark, understanding data partitioning, and optimising performance at scale.",
                "why_important": "Many real-world datasets exceed single-machine memory; distributed computing enables analysis of data at any scale efficiently.",
                "wrong_concepts": [
                    "Apache Spark should always be used for data processing tasks because it performs better than Pandas for all dataset sizes.",
                    "Distributing computations across more machines always results in proportional reduction in total processing time.",
                    "Big data technologies are required for any dataset that cannot be fully displayed in a standard spreadsheet application."
                ]
            },
        }
    },

    "Data Analyst": {
        "beginner": {
            "Excel Proficiency": {
                "description": "Using pivot tables, VLOOKUP, INDEX-MATCH, conditional formatting, and formulas for data analysis, summarisation, and reporting.",
                "why_important": "Excel is ubiquitous in business; proficiency enables quick analysis and clear communication with stakeholders across all industries.",
                "wrong_concepts": [
                    "Pivot tables are only useful for financial reporting and have very limited application in general data analysis work.",
                    "VLOOKUP is always more efficient and reliable than INDEX-MATCH for retrieving values from large datasets in Excel.",
                    "Excel macros should replace all manual data manipulation tasks to ensure complete consistency and eliminate human error."
                ]
            },
            "SQL Basics": {
                "description": "Writing SELECT statements, filtering rows with WHERE, aggregating data with GROUP BY, and joining multiple tables to extract business insights.",
                "why_important": "Most business data lives in relational databases; SQL lets analysts extract data directly without depending on engineering teams.",
                "wrong_concepts": [
                    "SELECT * queries are recommended because they ensure that no potentially important columns are accidentally excluded.",
                    "SQL subqueries should always be replaced with temporary tables for better readability and consistent query performance.",
                    "Database joins should be minimised by storing all related data together in a single wide denormalised table."
                ]
            },
            "Data Visualisation Basics": {
                "description": "Choosing appropriate chart types for different data relationships, applying design principles, and creating clear visual communication of insights.",
                "why_important": "The right visualisation reveals patterns that tables of numbers obscure and enables stakeholders to make faster, better-informed decisions.",
                "wrong_concepts": [
                    "Including as much data as possible in a single chart always gives stakeholders the most complete and comprehensive picture.",
                    "Pie charts are the most effective visualisation type for comparing values across a large number of categories.",
                    "Interactive dashboards should always replace static reports to maximise stakeholder engagement with the data."
                ]
            },
            "Descriptive Statistics": {
                "description": "Calculating and interpreting mean, median, mode, standard deviation, percentiles, and frequency distributions to summarise datasets.",
                "why_important": "Descriptive statistics provide the first layer of understanding about data, revealing central tendency, spread, and shape of distributions.",
                "wrong_concepts": [
                    "The mean is always the best summary statistic for any dataset regardless of the underlying distribution or outliers.",
                    "Standard deviation is only meaningful for datasets that follow a perfectly normal distribution with no skewness.",
                    "Larger datasets always produce more meaningful descriptive statistics regardless of how the data was collected."
                ]
            },
            "Data Quality Assessment": {
                "description": "Identifying missing values, duplicates, outliers, inconsistent formats, and inaccurate records that can compromise analytical results.",
                "why_important": "Poor data quality leads to incorrect conclusions; systematic assessment before analysis prevents misleading stakeholders with wrong insights.",
                "wrong_concepts": [
                    "Data quality checks are only necessary for data collected through manual processes rather than automated systems.",
                    "A dataset from a trusted source can always be assumed to be clean and accurate without any quality validation.",
                    "Data quality issues should be corrected by the data engineering team and are not the analyst's responsibility."
                ]
            },
        },
        "intermediate": {
            "Advanced SQL": {
                "description": "Writing complex queries using window functions, CTEs, subqueries, advanced aggregations, and query optimisation techniques.",
                "why_important": "Advanced SQL transforms analysts from report consumers to insight producers, enabling complex analytical questions to be answered directly.",
                "wrong_concepts": [
                    "Window functions should be avoided because they are more complex and consistently slower than equivalent GROUP BY queries.",
                    "CTEs only improve code readability and have no impact on query performance or execution efficiency in any database.",
                    "Query optimisation is exclusively the responsibility of the database administrator and should not concern data analysts."
                ]
            },
            "Statistical Analysis": {
                "description": "Conducting A/B tests, calculating confidence intervals, applying regression analysis, and determining statistical significance of business findings.",
                "why_important": "Statistical rigour prevents false conclusions; it distinguishes random noise from genuine effects in business metrics and experiments.",
                "wrong_concepts": [
                    "A p-value below 0.05 guarantees that a finding has both statistical and practical business significance for decision-making.",
                    "A/B tests should be stopped as soon as the target statistical significance level is first reached during the experiment.",
                    "Regression analysis can only be applied when the relationship between the dependent and independent variables is linear."
                ]
            },
            "Dashboard Design": {
                "description": "Building effective dashboards in Tableau or Power BI with appropriate KPIs, filtering, drill-downs, and clear visual hierarchy for different audiences.",
                "why_important": "Well-designed dashboards enable self-service analytics, reduce ad-hoc report requests, and keep stakeholders aligned on key metrics.",
                "wrong_concepts": [
                    "A single comprehensive dashboard should be designed to serve all user roles equally to maintain consistency across the organisation.",
                    "Real-time data updates are always essential in business dashboards to ensure all decisions are based on the latest figures.",
                    "Adding more metrics to a dashboard always provides greater value and insight to the people who use it regularly."
                ]
            },
            "Python for Analytics": {
                "description": "Using Python with Pandas for data manipulation, Matplotlib and Seaborn for visualisation, and writing reusable analytical scripts.",
                "why_important": "Python enables automation of repetitive analytical tasks, handles larger datasets than Excel, and enables more sophisticated analysis.",
                "wrong_concepts": [
                    "Python is only valuable for data analysts who work exclusively with very large datasets that exceed Excel's row limits.",
                    "Seaborn and Matplotlib produce equivalent visualisation quality to professional BI tools like Tableau and Power BI.",
                    "Learning Python is only worthwhile for analysts who plan to transition into a data science or engineering role."
                ]
            },
            "Business Intelligence Reporting": {
                "description": "Designing automated reporting workflows, defining KPIs aligned to business goals, and communicating analytical findings to non-technical stakeholders.",
                "why_important": "Effective BI reporting converts data findings into business decisions; poorly communicated insights create no value regardless of their quality.",
                "wrong_concepts": [
                    "Providing all available data metrics to executives always enables them to make better and more informed business decisions.",
                    "Automated reports completely replace the need for analysts to engage directly with stakeholders about their data questions.",
                    "The primary goal of BI reporting is technical accuracy rather than clear communication of the business implications."
                ]
            },
        },
        "advanced": {
            "Business Intelligence Strategy": {
                "description": "Defining enterprise KPI frameworks, designing data warehouses, creating analytical roadmaps, and aligning data initiatives with business strategy.",
                "why_important": "Strategic BI transforms data from an operational resource into a competitive advantage, enabling evidence-based decisions at all levels.",
                "wrong_concepts": [
                    "Deploying the latest BI technology platform is the primary driver of successful enterprise analytics programme outcomes.",
                    "A single enterprise-wide dashboard should provide all employees with access to all available business metrics and data.",
                    "Real-time data pipelines are always necessary for enterprise BI because stakeholders always need the most current data."
                ]
            },
            "Predictive Analytics": {
                "description": "Building forecasting models, applying regression and classification techniques, and communicating probabilistic outcomes to business stakeholders.",
                "why_important": "Predictive analytics shifts organisations from reactive to proactive decision-making by anticipating future outcomes and risks.",
                "wrong_concepts": [
                    "Predictive models with high accuracy on historical data will always deliver reliable predictions for future business scenarios.",
                    "Presenting prediction confidence intervals to business stakeholders always confuses them and should be avoided in reports.",
                    "More complex predictive models always produce better business value than simpler interpretable approaches for stakeholders."
                ]
            },
            "Data Governance": {
                "description": "Establishing data quality standards, lineage tracking, access controls, metadata management, and compliance frameworks for organisational data.",
                "why_important": "Data governance ensures trustworthy data, enables regulatory compliance, and prevents decisions based on inconsistent or inaccurate information.",
                "wrong_concepts": [
                    "Data governance is primarily a legal and compliance function and does not significantly impact day-to-day analytical work.",
                    "Restricting data access through governance policies always reduces analyst productivity and slows down business insights.",
                    "Data quality standards should be enforced exclusively at the point of data ingestion without ongoing monitoring processes."
                ]
            },
        }
    },

    "Product Manager": {
        "beginner": {
            "User Research Basics": {
                "description": "Conducting user interviews, creating surveys, analysing support tickets and reviews, and building empathy maps to understand customer needs.",
                "why_important": "Understanding real user needs prevents building features nobody wants; research validates assumptions before expensive development begins.",
                "wrong_concepts": [
                    "Large-scale online surveys with hundreds of responses always provide more accurate insights than in-depth user interviews.",
                    "Friends and family feedback is sufficient to validate product ideas before committing to the development investment.",
                    "Quantitative data from analytics tools should always take priority over qualitative insights from user interviews."
                ]
            },
            "Roadmap Planning": {
                "description": "Prioritising features using frameworks like RICE or MoSCoW, balancing short-term wins with long-term product vision, and communicating timelines to stakeholders.",
                "why_important": "Roadmaps align teams on priorities, manage stakeholder expectations, and ensure engineering effort focuses on the highest-impact work.",
                "wrong_concepts": [
                    "Product roadmaps should commit to fixed delivery dates for every feature in order to manage stakeholder expectations effectively.",
                    "Feature requests from the company's largest revenue-generating customers should always receive the highest roadmap priority.",
                    "A detailed two-year roadmap with committed features demonstrates strong product leadership and strategic planning capability."
                ]
            },
            "Writing User Stories": {
                "description": "Defining features from the user's perspective using the format 'As a [user], I want [goal] so that [benefit]' with clear acceptance criteria.",
                "why_important": "Well-written user stories ensure the team understands who needs the feature, what they need, and how success will be measured.",
                "wrong_concepts": [
                    "User stories should describe the technical implementation approach so that engineers can begin building immediately without questions.",
                    "A user story is complete when it describes the desired outcome without any need for separate acceptance criteria documentation.",
                    "The product manager should write all user stories alone without input from engineering or design to ensure consistency."
                ]
            },
            "Competitive Analysis": {
                "description": "Researching competitor products, identifying their strengths and weaknesses, and using insights to find differentiation opportunities for your product.",
                "why_important": "Understanding the competitive landscape helps identify gaps in the market and ensures the product offers genuine value over alternatives.",
                "wrong_concepts": [
                    "The primary goal of competitive analysis is to identify all features offered by competitors and add them to your own roadmap.",
                    "Competitive analysis is a one-time exercise conducted only when a product is first being launched into the market.",
                    "Monitoring competitor pricing is the most important output of competitive analysis for most product decision-making."
                ]
            },
            "Agile and Scrum Basics": {
                "description": "Understanding sprint planning, daily standups, backlog grooming, retrospectives, and the roles of Product Owner, Scrum Master, and development team.",
                "why_important": "Agile practices enable iterative delivery, faster feedback loops, and the flexibility to adapt when requirements change or new information emerges.",
                "wrong_concepts": [
                    "Sprint velocity is the most important metric for evaluating a development team's overall productivity and quality of work.",
                    "The daily standup meeting is primarily used to report progress to management and identify team members who are falling behind.",
                    "Agile methodologies should only be adopted by software teams and are not applicable to non-technical product development."
                ]
            },
        },
        "intermediate": {
            "Metrics and KPIs": {
                "description": "Defining and tracking engagement metrics, conversion rates, retention, NPS, and using analytics tools to measure ongoing product health.",
                "why_important": "The right metrics quantify product success, enable data-driven prioritisation, and prove whether changes achieve their intended outcomes.",
                "wrong_concepts": [
                    "Tracking more metrics simultaneously always enables better product decisions and more precise understanding of user behaviour.",
                    "User acquisition metrics are always the most important indicator of overall product health and long-term business success.",
                    "Monthly active users is always the single best metric for evaluating user engagement for any type of digital product."
                ]
            },
            "Stakeholder Management": {
                "description": "Communicating effectively with executives, engineering, design, and sales teams, managing conflicting priorities, and building organisational consensus.",
                "why_important": "Product success requires cross-functional alignment; poor stakeholder management leads to scope creep, missed deadlines, and wasted effort.",
                "wrong_concepts": [
                    "Stakeholders only need to receive updates when significant project milestones have been successfully completed and delivered.",
                    "Accepting all stakeholder feature requests demonstrates good collaboration skills and maintains positive working relationships.",
                    "Engineering teams should have the final decision on product features because they understand the technical constraints best."
                ]
            },
            "Product Discovery": {
                "description": "Using techniques like problem interviews, prototyping, usability testing, and smoke tests to validate product ideas before committing to full development.",
                "why_important": "Discovery reduces the risk of building the wrong thing; validating ideas cheaply before development saves significant time and resources.",
                "wrong_concepts": [
                    "Product discovery is only necessary for entirely new products and is not required when improving an existing product feature.",
                    "A business case document with strong financial projections is sufficient validation to proceed with product development.",
                    "The product discovery phase should be as brief as possible to minimise the delay before the engineering team can start building."
                ]
            },
            "Go-to-Market Strategy": {
                "description": "Planning feature launches including positioning, messaging, target segments, pricing considerations, distribution channels, and success metrics.",
                "why_important": "Even great products fail with poor launches; GTM strategy ensures the right users know about the product and understand its value.",
                "wrong_concepts": [
                    "A product launch should target all possible user segments simultaneously to maximise the total reach of the initial announcement.",
                    "Marketing is entirely responsible for go-to-market planning and product managers do not need to be involved in the process.",
                    "The best time to begin go-to-market planning is after all product development work has been completed and tested."
                ]
            },
            "Prioritisation Frameworks": {
                "description": "Applying frameworks including RICE, ICE, Kano Model, and value versus effort matrices to make defensible decisions about what to build next.",
                "why_important": "Structured prioritisation removes politics from product decisions, helps explain trade-offs to stakeholders, and focuses effort on the highest impact work.",
                "wrong_concepts": [
                    "Prioritisation frameworks should be used mechanically to produce the roadmap without requiring any additional judgment from the PM.",
                    "The highest revenue-generating feature requests should always receive the top priority score in any scoring framework.",
                    "Applying multiple prioritisation frameworks simultaneously always produces a more accurate and reliable result than using one."
                ]
            },
        },
        "advanced": {
            "Product Strategy": {
                "description": "Defining long-term product vision, analysing market opportunities, competitive positioning, pricing strategy, and planning go-to-market execution.",
                "why_important": "Strategy provides the direction that prevents teams from building features reactively rather than solving meaningful market problems systematically.",
                "wrong_concepts": [
                    "Product strategy should focus primarily on matching all competitor features to ensure strong competitive parity in the market.",
                    "Targeting the largest possible market segment simultaneously is always the most effective approach to product strategy.",
                    "Strategy documents should provide detailed implementation instructions to give engineering teams precise guidance on execution."
                ]
            },
            "Platform and Ecosystem Strategy": {
                "description": "Designing products as platforms that enable third-party integrations, building developer ecosystems, and creating network effects that increase product value.",
                "why_important": "Platform businesses create sustainable competitive advantages through network effects that become increasingly difficult for competitors to replicate.",
                "wrong_concepts": [
                    "Every successful product should immediately be repositioned as a platform regardless of the product category or market context.",
                    "API access alone is sufficient to build a successful developer ecosystem without additional support resources or documentation.",
                    "Network effects always develop naturally without any deliberate strategic effort to seed and grow the user community."
                ]
            },
            "Revenue and Business Model Strategy": {
                "description": "Evaluating revenue models including subscription, freemium, transaction fees, and advertising, and designing pricing that aligns with customer value.",
                "why_important": "Sustainable product success requires a business model that generates value for the company proportional to the value it creates for users.",
                "wrong_concepts": [
                    "Freemium pricing models always generate more revenue than paid subscription models for any category of software product.",
                    "Lowering prices is always the most effective strategy for accelerating product adoption and growing the total customer base.",
                    "Pricing decisions should be made exclusively by the finance and sales teams without input from the product management function."
                ]
            },
        }
    },

    "UX Designer": {
        "beginner": {
            "User Research Methods": {
                "description": "Conducting user interviews, contextual inquiry, usability testing, and surveys to understand user behaviour, needs, and pain points.",
                "why_important": "Research replaces assumptions with evidence about what users actually need, preventing wasted design effort on solutions to the wrong problems.",
                "wrong_concepts": [
                    "Experienced designers can rely on their accumulated intuition instead of conducting research to make good design decisions.",
                    "Large quantitative surveys with hundreds of respondents are always more valuable than small-scale in-depth user interviews.",
                    "User research should only be conducted at the beginning of a project before any design work has started."
                ]
            },
            "Wireframing": {
                "description": "Creating low-fidelity sketches and digital wireframes to explore layout options, information hierarchy, and user flow before investing in visual design.",
                "why_important": "Wireframes enable rapid exploration of structure and layout, catching usability issues before expensive visual design work begins.",
                "wrong_concepts": [
                    "Wireframes should include realistic visual design so that stakeholders receive an accurate impression of the finished product.",
                    "Skipping wireframes and designing high-fidelity screens directly is always faster and produces better quality final designs.",
                    "Creating multiple wireframe variations wastes time that could be more productively spent on final high-fidelity design work."
                ]
            },
            "Personas and User Journey Mapping": {
                "description": "Creating evidence-based user personas that capture goals and behaviours, and mapping end-to-end journeys to identify pain points and opportunities.",
                "why_important": "Personas maintain user focus throughout design and development; journey maps reveal friction points that individual screens cannot show.",
                "wrong_concepts": [
                    "Personas should be created from demographic data alone since age, gender, and income are the primary drivers of user behaviour.",
                    "One primary persona representing the average user is always sufficient for making informed design decisions across a product.",
                    "User journey maps should only cover the happy path since edge cases and failure states are the responsibility of engineering."
                ]
            },
            "Heuristic Evaluation": {
                "description": "Systematically evaluating interfaces against Nielsen's 10 usability heuristics to identify usability problems without requiring user participants.",
                "why_important": "Heuristic evaluation is a fast cost-effective way to catch obvious usability issues early before investing in user testing sessions.",
                "wrong_concepts": [
                    "Heuristic evaluation conducted by a single expert provides more reliable results than evaluation performed by multiple reviewers.",
                    "Passing all usability heuristics guarantees that the design will be effective and usable for the intended target audience.",
                    "Heuristic evaluation is only appropriate for consumer applications and does not apply to enterprise software interfaces."
                ]
            },
            "Accessibility Fundamentals": {
                "description": "Designing for WCAG compliance including sufficient colour contrast, keyboard navigation, screen reader compatibility, and appropriate text sizing.",
                "why_important": "Accessible design serves users with disabilities, often improves usability for everyone, and is required by law in many contexts.",
                "wrong_concepts": [
                    "Accessibility features only benefit a small minority of users and therefore do not justify the additional design and development effort.",
                    "Meeting colour contrast requirements is sufficient to make a digital product fully accessible to all users with disabilities.",
                    "Accessibility should be addressed as a final polish phase after all other design and development work has been completed."
                ]
            },
        },
        "intermediate": {
            "Prototyping": {
                "description": "Building interactive prototypes in Figma or Adobe XD to simulate real product interactions for stakeholder reviews and usability testing.",
                "why_important": "Prototypes communicate design intent more effectively than static screens and validate usability assumptions before development investment.",
                "wrong_concepts": [
                    "High-fidelity prototypes with realistic visual design should always be used in usability testing to ensure authentic user reactions.",
                    "Coded prototypes are always superior to design tool prototypes for testing interactions accurately with real users.",
                    "A single prototype version is sufficient for testing; creating multiple iterations during the design process wastes valuable time."
                ]
            },
            "Design Systems": {
                "description": "Creating and maintaining component libraries, typography scales, colour systems, spacing tokens, and documentation to ensure product-wide consistency.",
                "why_important": "Design systems accelerate design and development, enforce visual consistency, and allow teams to focus on solving problems rather than recreating components.",
                "wrong_concepts": [
                    "Design systems reduce creative freedom by constraining designers to a fixed set of pre-approved visual components and patterns.",
                    "A design system must be fully completed and documented before any product design work can begin within an organisation.",
                    "Adopting an existing open-source design system without any modification is always the most efficient approach available."
                ]
            },
            "Interaction Design Patterns": {
                "description": "Applying established UI patterns like progressive disclosure, infinite scroll, form validation, onboarding flows, and empty states appropriately.",
                "why_important": "Familiar patterns reduce learning curves; knowing when to use and when to adapt established patterns leads to more intuitive experiences.",
                "wrong_concepts": [
                    "Innovative and novel interaction patterns should always be prioritised over established conventions to differentiate the product.",
                    "Interaction patterns should remain identical across mobile and desktop platforms to maintain consistency in user experience.",
                    "Once an interaction pattern is established in a product it should never be changed to avoid disrupting existing users."
                ]
            },
            "Usability Testing": {
                "description": "Moderating task-based user testing sessions, taking structured observations, identifying patterns across participants, and translating findings into design improvements.",
                "why_important": "Observing real users attempting real tasks reveals usability issues that are invisible to designers who are too close to the work.",
                "wrong_concepts": [
                    "A minimum of 30 test participants is required before any usability insights from testing sessions can be considered reliable.",
                    "Quantitative metrics from analytics tools provide richer insights than observations from qualitative usability testing sessions.",
                    "Usability testing should only be conducted after a product is fully designed and built to test the complete final experience."
                ]
            },
            "Information Architecture": {
                "description": "Organising content and navigation through card sorting, tree testing, and sitemap design to help users find what they need efficiently.",
                "why_important": "Poor information architecture is a leading cause of user failure; well-organised content makes complex products feel intuitive and discoverable.",
                "wrong_concepts": [
                    "Information architecture should reflect the internal organisational structure of the company that is building the product.",
                    "Implementing a comprehensive search feature eliminates the need for investing time in thoughtful information architecture design.",
                    "Card sorting results from user research should always be implemented exactly without any additional design interpretation."
                ]
            },
        },
        "advanced": {
            "Strategic UX": {
                "description": "Aligning UX initiatives with business objectives, measuring and communicating the return on investment of design decisions to executive stakeholders.",
                "why_important": "Strategic UX positions design as a business driver rather than a production function, giving designers influence over product direction.",
                "wrong_concepts": [
                    "UX metrics should focus exclusively on user satisfaction scores rather than on measuring business outcome improvements.",
                    "Design decisions should always prioritise aesthetic consistency over delivering measurable improvements to user experience.",
                    "Senior designers should focus entirely on craft and execution quality rather than engaging with broader business strategy."
                ]
            },
            "Service Design": {
                "description": "Mapping end-to-end service ecosystems including backstage processes, stakeholder touchpoints, and organisational capabilities using service blueprints.",
                "why_important": "Great user experiences depend on well-designed services behind the interface; service design aligns the entire organisation around the user journey.",
                "wrong_concepts": [
                    "Service design is primarily concerned with digital touchpoints and does not need to consider offline or physical interactions.",
                    "Service blueprints are internal documentation tools and do not have value as outputs for presenting to external stakeholders.",
                    "Redesigning the customer-facing interface is always sufficient to resolve service quality issues without addressing backstage processes."
                ]
            },
            "Design Leadership and Operations": {
                "description": "Building and leading design teams, establishing design processes and critique culture, managing design tooling, and advocating for design investment.",
                "why_important": "Strong design operations enable design teams to scale effectively, maintain consistent quality, and deliver impact across large organisations.",
                "wrong_concepts": [
                    "Design leaders should primarily evaluate their team's performance based on the visual quality of the work they produce.",
                    "A design team's effectiveness is best measured by the number of screens and designs produced within a given time period.",
                    "Design process standardisation reduces team agility and should be avoided in favour of allowing each designer to work independently."
                ]
            },
        }
    },

    "Marketing Manager": {
        "beginner": {
            "Marketing Fundamentals": {
                "description": "Understanding the 4 Ps of marketing — Product, Price, Place, and Promotion — and applying them to identify target audiences and create positioning strategies.",
                "why_important": "Marketing fundamentals provide the strategic framework that prevents campaigns from being reactive and ensures budget is spent effectively.",
                "wrong_concepts": [
                    "Digital marketing channels have completely replaced all traditional marketing approaches for every type of business and audience.",
                    "Marketing campaigns should always target the broadest possible audience in order to maximise total brand awareness reach.",
                    "The Promotion element of the marketing mix is always the most important factor in determining overall product market success."
                ]
            },
            "Content Marketing": {
                "description": "Creating and distributing valuable blog posts, social media content, email campaigns, and SEO-optimised content to attract and retain a target audience.",
                "why_important": "Content builds credibility and organic traffic over time, nurtures leads through the funnel, and costs less than paid advertising long-term.",
                "wrong_concepts": [
                    "Publishing content as frequently as possible across all available platforms is the most reliable growth strategy for any brand.",
                    "Content length is the primary ranking factor that determines how well any piece of content performs in search engines.",
                    "Repurposing identical content across all channels without any modification is an efficient way to maximise content production output."
                ]
            },
            "Social Media Marketing": {
                "description": "Building brand presence on relevant social platforms, creating engaging content, growing followers, and using social listening for brand monitoring.",
                "why_important": "Social media enables direct audience engagement, builds brand communities, and provides real-time feedback that informs product and content decisions.",
                "wrong_concepts": [
                    "Every brand must maintain an active presence on all social media platforms to reach all possible segments of its target audience.",
                    "Posting frequency is the single most important factor in determining social media account growth and follower engagement.",
                    "Social media marketing success is best measured exclusively through follower count and total post impressions across all platforms."
                ]
            },
            "Email Marketing": {
                "description": "Building email lists, segmenting subscribers, designing campaigns, writing compelling subject lines, and analysing open and conversion rates.",
                "why_important": "Email delivers the highest ROI of any digital marketing channel; a well-managed list is a direct audience connection owned by the business.",
                "wrong_concepts": [
                    "Sending emails to the entire mailing list every time ensures maximum reach and produces the best overall campaign results.",
                    "Subject line length is the primary factor that determines whether subscribers open or ignore marketing email messages.",
                    "Email marketing has been made obsolete by social media and messaging apps for reaching most modern consumer audiences."
                ]
            },
            "Brand Awareness Basics": {
                "description": "Understanding brand identity, positioning, voice and tone, and the difference between brand awareness and direct response marketing objectives.",
                "why_important": "Strong brand awareness reduces customer acquisition costs, enables premium pricing, and creates preference when buyers are ready to purchase.",
                "wrong_concepts": [
                    "Brand awareness campaigns should always be evaluated using the same conversion metrics applied to direct response advertising.",
                    "A recognisable logo and consistent colour palette are sufficient elements to establish strong brand awareness in any market.",
                    "Brand awareness is only a concern for large established companies; early-stage businesses should focus exclusively on conversion."
                ]
            },
        },
        "intermediate": {
            "Digital Advertising": {
                "description": "Running paid campaigns on Google Ads, Meta, and LinkedIn, optimising for CTR, CPC, and ROAS through systematic A/B testing of ad creative.",
                "why_important": "Paid advertising generates immediate targeted traffic and conversions; systematic optimisation prevents budget waste and maximises return.",
                "wrong_concepts": [
                    "Increasing the advertising budget is always the most effective way to improve underperforming campaign performance results.",
                    "Broad audience targeting in paid campaigns consistently leads to higher conversion rates than well-defined narrow targeting.",
                    "Click-through rate is always the most important metric for evaluating whether a paid advertising campaign is performing well."
                ]
            },
            "SEO Strategy": {
                "description": "Conducting keyword research, optimising on-page elements, building backlinks, improving technical site health, and tracking search ranking performance.",
                "why_important": "Organic search drives sustainable high-intent traffic without ongoing cost; strong SEO compounds over time and reduces reliance on paid channels.",
                "wrong_concepts": [
                    "Including target keywords as frequently as possible throughout content pages improves their ranking in search engine results.",
                    "Social media engagement and follower counts are significant ranking signals that search engines use to determine page position.",
                    "Technical SEO optimisations like page load speed have minimal impact on search rankings compared to keyword optimisation."
                ]
            },
            "Analytics and Attribution": {
                "description": "Using Google Analytics to track conversion funnels, applying attribution models, and measuring the true business impact of marketing campaigns.",
                "why_important": "Attribution reveals which channels actually drive conversions, enabling budget allocation based on real impact rather than assumptions.",
                "wrong_concepts": [
                    "Last-click attribution always provides the most accurate picture of which marketing channels are truly driving customer conversions.",
                    "Collecting more data about users always leads to better marketing decisions and improved campaign performance outcomes.",
                    "Direct traffic in analytics always represents users who discovered the brand through unprompted direct navigation to the website."
                ]
            },
            "Customer Journey Mapping": {
                "description": "Mapping all customer touchpoints from awareness through to purchase and retention to identify gaps and opportunities for improving conversion.",
                "why_important": "Understanding the complete customer journey reveals where prospects drop off and enables targeted improvements that increase conversion rates.",
                "wrong_concepts": [
                    "The customer journey always follows a linear sequence from awareness to purchase without any backtracking or alternative paths.",
                    "Customer journey mapping is only relevant for businesses that have a complex sales cycle with multiple stakeholders involved.",
                    "The purchase transaction is the final point in the customer journey and post-purchase experience does not affect brand loyalty."
                ]
            },
            "Marketing Automation": {
                "description": "Using platforms like HubSpot or Marketo to automate lead nurturing, email sequences, lead scoring, and CRM integration for scale.",
                "why_important": "Automation enables personalised communication at scale, ensures consistent follow-up, and frees marketers to focus on strategy over execution.",
                "wrong_concepts": [
                    "Marketing automation completely replaces the need for marketers to engage in ongoing content creation and campaign optimisation.",
                    "Automated email sequences are always more effective than manually written emails for nurturing all types of leads and prospects.",
                    "Implementing a marketing automation platform always immediately improves lead quality and conversion rates for any business."
                ]
            },
        },
        "advanced": {
            "Growth Marketing": {
                "description": "Designing viral loops, referral programmes, cohort analysis, and product-led growth strategies to achieve scalable and sustainable user acquisition.",
                "why_important": "Growth marketing focuses on sustainable compounding acquisition and retention rather than one-off campaign bursts that don't sustain momentum.",
                "wrong_concepts": [
                    "Growth hacking techniques reliably produce viral growth for any product if sufficient budget and effort are invested.",
                    "User acquisition should always take priority over retention metrics in all growth marketing strategies and budget allocations.",
                    "Referral programmes consistently generate the highest quality and highest converting leads regardless of product category."
                ]
            },
            "Brand Strategy": {
                "description": "Defining brand architecture, positioning, narrative, purpose, and values that differentiate the organisation and create lasting emotional connections.",
                "why_important": "Strong brand strategy enables premium pricing, drives word-of-mouth growth, and provides a durable competitive advantage difficult to replicate.",
                "wrong_concepts": [
                    "Brand strategy should be updated every two to three years to remain aligned with current design trends and audience preferences.",
                    "Brand positioning should be broad enough to appeal to as many different customer segments as possible simultaneously.",
                    "Brand awareness and performance marketing are entirely separate functions that should be managed with separate and distinct strategies."
                ]
            },
            "Marketing Operations": {
                "description": "Building the marketing technology stack, managing data infrastructure, defining processes, and measuring marketing performance at an organisational level.",
                "why_important": "Marketing operations is the infrastructure enabling scale; without it, marketing efforts produce inconsistent results and data that cannot be trusted.",
                "wrong_concepts": [
                    "The largest and most comprehensive marketing technology stack always produces the best marketing performance and team efficiency.",
                    "Marketing data quality issues are always the responsibility of the data engineering team rather than the marketing organisation.",
                    "Process standardisation in marketing always reduces creativity and should be avoided to maintain campaign innovation."
                ]
            },
        }
    },

    "DevOps Engineer": {
        "beginner": {
            "Linux Command Line": {
                "description": "Navigating file systems, managing processes, setting permissions, manipulating text with grep and sed, and writing basic shell scripts.",
                "why_important": "Linux powers the vast majority of servers; command line proficiency enables automation, debugging, and system administration that GUIs cannot provide.",
                "wrong_concepts": [
                    "Graphical user interfaces should always be installed on production servers because they simplify all system administration tasks.",
                    "Shell scripts are only appropriate for simple automation tasks and should be replaced with Python for anything moderately complex.",
                    "Running all commands as the root user simplifies system administration by eliminating all permission-related access issues."
                ]
            },
            "Version Control": {
                "description": "Using Git for creating and merging branches, submitting pull requests, resolving merge conflicts, and collaborating through GitHub or GitLab.",
                "why_important": "Version control enables safe team collaboration, provides complete change history, allows rollbacks, and protects against accidental overwrites.",
                "wrong_concepts": [
                    "Committing all changes directly to the main branch is acceptable for small teams because it avoids branching complexity.",
                    "Git commit messages only need to be brief since the code diff itself provides sufficient context for other developers.",
                    "Large infrequent commits are preferable to small frequent ones because they produce a cleaner and less noisy repository history."
                ]
            },
            "Networking Fundamentals": {
                "description": "Understanding TCP/IP, DNS, HTTP/HTTPS, firewalls, load balancers, and how network traffic flows between services in a distributed system.",
                "why_important": "DevOps engineers configure network infrastructure; understanding networking is essential for debugging connectivity issues and securing systems.",
                "wrong_concepts": [
                    "DNS configuration changes take effect immediately and can always be relied upon to propagate globally within a few seconds.",
                    "Firewalls that block all incoming traffic provide complete security and eliminate the need for additional security measures.",
                    "HTTP and HTTPS are functionally identical from a performance perspective and the choice between them does not affect latency."
                ]
            },
            "Infrastructure as Code Basics": {
                "description": "Using tools like Terraform or Ansible to define and provision infrastructure through version-controlled code rather than manual configuration.",
                "why_important": "IaC eliminates manual configuration drift, enables repeatable environments, and treats infrastructure with the same rigour as application code.",
                "wrong_concepts": [
                    "Infrastructure as code tools are only necessary for very large organisations with hundreds of servers to manage at once.",
                    "Manually configuring servers is more reliable than using IaC tools because it avoids the risk of automated provisioning errors.",
                    "Using IaC for all infrastructure automatically guarantees that all environments will be identical without further validation needed."
                ]
            },
            "Cloud Services Basics": {
                "description": "Understanding compute, storage, networking, and managed services offered by AWS, Azure, and GCP, and the shared responsibility security model.",
                "why_important": "Most modern infrastructure runs on cloud platforms; understanding their services and pricing is essential for making informed architecture decisions.",
                "wrong_concepts": [
                    "Migrating all workloads to the cloud always reduces infrastructure costs compared to running equivalent on-premise hardware.",
                    "Managed cloud services completely handle all security responsibilities leaving application teams with no security obligations.",
                    "Choosing the largest available instance type always ensures the best application performance for any workload requirements."
                ]
            },
        },
        "intermediate": {
            "CI/CD Pipelines": {
                "description": "Automating build, test, and deployment workflows using Jenkins, GitHub Actions, or GitLab CI for reliable and repeatable software delivery.",
                "why_important": "CI/CD accelerates release cycles, catches bugs through automated testing, and eliminates the human errors common in manual deployments.",
                "wrong_concepts": [
                    "Manual deployment processes are inherently more reliable than automated pipelines for critical production environment changes.",
                    "Running only unit tests in CI pipelines is sufficient because integration tests slow the pipeline down too significantly.",
                    "CI/CD pipelines only provide meaningful value for large teams making multiple code deployments to production each day."
                ]
            },
            "Containerisation with Docker": {
                "description": "Creating Dockerfiles, building and managing container images, using Docker Compose for local development, and understanding container networking.",
                "why_important": "Containers ensure consistent environments from development to production, simplify dependency management, and improve resource utilisation.",
                "wrong_concepts": [
                    "Docker containers provide identical security isolation to traditional virtual machines and can be treated as such for compliance.",
                    "A single Docker container should run all application services together to simplify the overall deployment architecture.",
                    "Container images should include all development tools and dependencies to ensure complete parity across all developer environments."
                ]
            },
            "Monitoring and Observability": {
                "description": "Implementing metrics collection with Prometheus, log aggregation with the ELK stack, distributed tracing, and configuring meaningful alerting.",
                "why_important": "You cannot manage what you cannot measure; observability enables fast diagnosis of production issues and proactive performance management.",
                "wrong_concepts": [
                    "Monitoring all available system metrics and logs is always better than monitoring a carefully selected set of key indicators.",
                    "Log files alone provide sufficient observability to diagnose all performance issues in a modern distributed system effectively.",
                    "Alerting thresholds should be set as low as possible to ensure that all potential issues are detected as early as possible."
                ]
            },
            "Configuration Management": {
                "description": "Managing server configuration at scale using Ansible, Chef, or Puppet to ensure consistency across all environments and eliminate configuration drift.",
                "why_important": "Configuration drift between environments causes mysterious production failures; automated configuration management prevents inconsistency at scale.",
                "wrong_concepts": [
                    "Configuration management tools are only needed for environments with more than 50 servers as smaller setups can be managed manually.",
                    "Immutable infrastructure practices completely eliminate the need for configuration management tools in cloud environments.",
                    "Configuration management should only manage application settings and should not be used for operating system-level configuration."
                ]
            },
            "Security and Compliance": {
                "description": "Implementing DevSecOps practices including static code analysis, dependency scanning, secrets management, and compliance as code.",
                "why_important": "Security built into the delivery pipeline catches vulnerabilities early when they are cheapest to fix rather than after deployment.",
                "wrong_concepts": [
                    "Security testing and compliance checks should be conducted as a separate final phase after all development work is complete.",
                    "Using well-maintained open-source dependencies guarantees that applications are free from known security vulnerabilities.",
                    "Storing configuration secrets in environment variables provides sufficient security for production application deployments."
                ]
            },
        },
        "advanced": {
            "Kubernetes Orchestration": {
                "description": "Managing containerised workloads at scale with Kubernetes including pods, services, deployments, horizontal pod autoscaling, and cluster management.",
                "why_important": "Kubernetes automates deployment, scaling, and self-healing of containerised applications, enabling reliable operation of complex distributed systems.",
                "wrong_concepts": [
                    "Kubernetes should be adopted for all applications regardless of their scale because it provides the most reliable deployment platform.",
                    "Kubernetes built-in health checks eliminate the need for any separate application monitoring or alerting infrastructure.",
                    "Horizontal pod autoscaling in Kubernetes completely eliminates the need for capacity planning or load testing before deployment."
                ]
            },
            "Site Reliability Engineering": {
                "description": "Applying SLOs, SLAs, error budgets, chaos engineering, and blameless post-mortems to build systems that are both reliable and constantly improving.",
                "why_important": "SRE practices create a mathematical framework for balancing reliability with velocity, preventing both over-engineering and unreliable systems.",
                "wrong_concepts": [
                    "Achieving 100% uptime should always be the primary reliability goal for any production service regardless of its business context.",
                    "Post-mortems are primarily useful for identifying and disciplining the individuals responsible for causing system incidents.",
                    "Error budgets are accounting mechanisms that penalise development teams for deploying features that cause production incidents."
                ]
            },
            "Platform Engineering": {
                "description": "Building internal developer platforms that abstract infrastructure complexity, provide self-service capabilities, and enable development teams to deploy independently.",
                "why_important": "Platform engineering multiplies developer productivity by standardising and automating the toil that previously slowed every development team.",
                "wrong_concepts": [
                    "Platform teams should make all infrastructure decisions centrally to ensure consistency rather than enabling developer self-service.",
                    "An internal developer platform is only valuable if it mirrors the feature set of commercial cloud provider management consoles.",
                    "Platform engineering is primarily a cost-reduction initiative rather than a productivity and developer experience improvement."
                ]
            },
        }
    },

    "Cybersecurity Analyst": {
        "beginner": {
            "Network Security Basics": {
                "description": "Understanding TCP/IP networking, firewalls, VPNs, common attack types including DDoS and man-in-the-middle attacks, and network monitoring tools.",
                "why_important": "Network security is the perimeter of organisational defence; understanding traffic flows enables identifying and preventing malicious activity.",
                "wrong_concepts": [
                    "A correctly configured firewall provides complete protection against all categories of modern cybersecurity threats and attacks.",
                    "Using a VPN connection ensures complete anonymity online and prevents all tracking of user network activity and identity.",
                    "Encrypting network traffic eliminates the need for any additional security monitoring or intrusion detection capabilities."
                ]
            },
            "Authentication and Access Control": {
                "description": "Implementing multi-factor authentication, role-based access control, principle of least privilege, and strong password policies.",
                "why_important": "Most security breaches begin with compromised credentials; robust authentication is the most critical control for preventing unauthorised access.",
                "wrong_concepts": [
                    "Enforcing complex password requirements alone is sufficient security and eliminates the need for multi-factor authentication.",
                    "Single sign-on reduces overall security risk because it means users only need to remember and protect one set of credentials.",
                    "Sharing administrator account credentials among team members improves incident response efficiency and team collaboration."
                ]
            },
            "Security Fundamentals": {
                "description": "Understanding the CIA triad of Confidentiality, Integrity, and Availability, common vulnerability types, and the security threat landscape.",
                "why_important": "Security fundamentals provide the conceptual framework for evaluating risks, prioritising controls, and communicating security decisions to stakeholders.",
                "wrong_concepts": [
                    "Availability is always the least critical component of the CIA triad for any organisation regardless of its industry or context.",
                    "Following compliance frameworks and passing audits ensures that an organisation is adequately protected from all real-world threats.",
                    "Zero-day vulnerabilities represent the greatest proportion of successful security breaches across most types of organisations."
                ]
            },
            "Malware and Threat Analysis": {
                "description": "Identifying types of malware including viruses, ransomware, and trojans, understanding how they spread, and applying controls to prevent infections.",
                "why_important": "Malware remains one of the most common attack vectors; understanding how threats operate enables effective prevention and detection strategies.",
                "wrong_concepts": [
                    "Keeping antivirus software updated and current provides complete protection against all forms of modern malware threats.",
                    "Ransomware attacks can always be fully recovered from using backups without paying the ransom or losing any business data.",
                    "Malware infections are always immediately detectable through obvious system performance degradation or visible error messages."
                ]
            },
            "Social Engineering Awareness": {
                "description": "Understanding phishing, spear phishing, vishing, and pretexting attacks, and implementing user education programmes to reduce human-factor risk.",
                "why_important": "Human factors are involved in most security breaches; educated users who recognise manipulation attempts are a critical defensive layer.",
                "wrong_concepts": [
                    "Technical security controls alone are sufficient to protect an organisation without requiring any employee security awareness training.",
                    "Phishing emails can always be identified through obvious spelling mistakes, poor grammar, or suspicious sender email addresses.",
                    "Users who fall victim to phishing attacks were careless and should be held personally responsible for the resulting security incident."
                ]
            },
        },
        "intermediate": {
            "Penetration Testing": {
                "description": "Conducting ethical hacking engagements using a structured methodology with tools like Metasploit, Burp Suite, Nmap, and Kali Linux.",
                "why_important": "Proactive penetration testing finds vulnerabilities before malicious attackers do, enabling remediation before exploitation occurs.",
                "wrong_concepts": [
                    "Automated vulnerability scanning tools can identify all security weaknesses present without any need for manual testing efforts.",
                    "Penetration testing should only be conducted on systems already known to have existing security weaknesses requiring confirmation.",
                    "One comprehensive annual penetration test provides sufficient ongoing assurance of security posture for most organisations."
                ]
            },
            "Security Information and Event Management": {
                "description": "Using SIEM platforms to collect and correlate security logs, build detection rules, and investigate suspicious patterns across the environment.",
                "why_important": "SIEMs provide centralised visibility across the attack surface, enabling analysts to detect and respond to threats that individual tools miss.",
                "wrong_concepts": [
                    "Collecting and storing all available security logs in a SIEM is always better than selecting a targeted set of high-value sources.",
                    "Out-of-the-box SIEM detection rules provide complete threat coverage without requiring any organisation-specific customisation.",
                    "A high volume of SIEM alerts indicates a mature and well-tuned security monitoring programme with comprehensive threat detection."
                ]
            },
            "Vulnerability Management": {
                "description": "Scanning for vulnerabilities using tools like Nessus, prioritising findings by risk, coordinating remediation with IT teams, and tracking progress.",
                "why_important": "Systematic vulnerability management reduces the attack surface; prioritising by risk ensures the most dangerous vulnerabilities are addressed first.",
                "wrong_concepts": [
                    "All identified vulnerabilities should be remediated immediately in order of their CVSS score from highest to lowest without exception.",
                    "Vulnerability scanning tools provide a complete inventory of all security weaknesses present in a system or network environment.",
                    "A vulnerability that has not yet been publicly exploited poses no meaningful risk and does not require priority remediation effort."
                ]
            },
        },
        "advanced": {
            "Incident Response": {
                "description": "Executing a structured incident response process covering detection, containment, eradication, recovery, and post-incident review documentation.",
                "why_important": "Fast and disciplined incident response minimises breach impact, reduces recovery time, and captures lessons that prevent future incidents.",
                "wrong_concepts": [
                    "All affected systems should be immediately shut down when a security incident is first detected to prevent further damage.",
                    "Incident response procedures should be kept strictly confidential to prevent attackers from using knowledge of them strategically.",
                    "System restoration should always take priority over forensic investigation to minimise the business disruption from an incident."
                ]
            },
            "Threat Intelligence": {
                "description": "Gathering, analysing, and operationalising threat intelligence from feeds, ISACs, and open sources to proactively defend against emerging threats.",
                "why_important": "Threat intelligence transforms reactive security into proactive defence by providing advance warning of emerging tactics and targeting.",
                "wrong_concepts": [
                    "Commercial threat intelligence feeds always provide more actionable and accurate intelligence than free open-source alternatives.",
                    "Threat intelligence is primarily useful for large enterprises and provides limited value for small and medium-sized organisations.",
                    "Sharing threat intelligence with industry peers always creates unacceptable competitive and reputational risk for an organisation."
                ]
            },
            "Security Architecture": {
                "description": "Designing defence-in-depth security architectures using zero trust principles, segmentation, least privilege access, and layered control frameworks.",
                "why_important": "Sound security architecture ensures that when individual controls fail, attackers cannot easily move laterally or access critical systems.",
                "wrong_concepts": [
                    "Zero trust architecture completely replaces the need for network perimeter security controls and traditional firewall infrastructure.",
                    "Security architecture reviews should only be conducted when new systems are being built from scratch rather than for existing ones.",
                    "Encrypting all data everywhere is sufficient to implement zero trust principles without requiring any additional architectural changes."
                ]
            },
        }
    },

    "Machine Learning Engineer": {
        "beginner": {
            "Python for Machine Learning": {
                "description": "Using scikit-learn for model training, NumPy for array operations, Pandas for data preparation, and Matplotlib for visualising model results.",
                "why_important": "Python's ML ecosystem provides tested and optimised implementations, enabling engineers to build robust models without reinventing the wheel.",
                "wrong_concepts": [
                    "All machine learning algorithms should be implemented from scratch to ensure full transparency and control over model behaviour.",
                    "Python is too slow for production machine learning and should always be replaced with C++ or Java for deployment environments.",
                    "The scikit-learn library should be used for all machine learning tasks including training large-scale deep learning models."
                ]
            },
            "Mathematics for ML": {
                "description": "Understanding linear algebra concepts like vectors and matrices, calculus for gradient computation, and probability for reasoning under uncertainty.",
                "why_important": "Mathematical foundations enable engineers to understand why algorithms work, diagnose failures, and adapt methods to novel problems.",
                "wrong_concepts": [
                    "A strong mathematical foundation is only necessary for researchers creating new algorithms rather than for practitioners applying them.",
                    "Advanced calculus knowledge is required to effectively use any modern machine learning library or framework in practice.",
                    "Matrix multiplication knowledge provides no practical benefit since all ML frameworks handle all linear algebra operations automatically."
                ]
            },
            "Data Preparation for ML": {
                "description": "Handling missing values, encoding categorical variables, normalising features, splitting data into training and test sets, and dealing with class imbalance.",
                "why_important": "ML models are highly sensitive to data quality and format; poor preparation produces unreliable models regardless of algorithm choice.",
                "wrong_concepts": [
                    "Feature normalisation is only necessary when using neural networks and provides no benefit for other types of ML algorithms.",
                    "The training and test data split ratio does not significantly affect model evaluation quality as long as the dataset is reasonably large.",
                    "Class imbalance in a dataset is a minor issue that modern machine learning algorithms handle automatically without any intervention."
                ]
            },
            "Supervised Learning Basics": {
                "description": "Training models for classification and regression tasks, understanding the bias-variance trade-off, and interpreting model outputs.",
                "why_important": "Supervised learning solves the majority of real-world prediction problems; understanding core concepts is essential for any ML practitioner.",
                "wrong_concepts": [
                    "A model that achieves the highest accuracy on the training dataset will always perform best when deployed to production.",
                    "Regression models can only be used for continuous numerical prediction targets and cannot handle any categorical output variables.",
                    "More training examples always improve model performance proportionally regardless of the quality or relevance of the additional data."
                ]
            },
            "Model Evaluation Basics": {
                "description": "Using appropriate metrics including accuracy, precision, recall, F1 score, and RMSE for evaluating model performance on held-out test data.",
                "why_important": "The right evaluation metric aligns model training with actual business objectives; the wrong metric produces models that fail in practice.",
                "wrong_concepts": [
                    "Accuracy is always the most appropriate and informative metric for evaluating any machine learning classification model.",
                    "A model evaluated on the training data provides reliable estimates of how it will perform on new unseen production data.",
                    "The evaluation metric should be chosen after model training based on whichever metric makes the results look most favourable."
                ]
            },
        },
        "intermediate": {
            "Model Validation": {
                "description": "Applying k-fold cross-validation, stratified sampling, and hyperparameter tuning with grid search and random search to build reliable models.",
                "why_important": "Proper validation prevents overfitting and ensures models generalise to real-world data rather than memorising training examples.",
                "wrong_concepts": [
                    "Model accuracy on training data is always the most reliable indicator of how well the model will perform in production.",
                    "Cross-validation eliminates the need for a separate held-out test set since it already evaluates the model on unseen data.",
                    "The same held-out test dataset can be used repeatedly to evaluate multiple model versions without introducing any evaluation bias."
                ]
            },
            "Feature Engineering for ML": {
                "description": "Creating interaction features, applying transformations, using domain knowledge, and selecting features through importance ranking and regularisation.",
                "why_important": "Thoughtful feature engineering often improves model performance more than algorithm selection or hyperparameter tuning combined.",
                "wrong_concepts": [
                    "Deep learning completely eliminates the need for manual feature engineering in all practical machine learning problem types.",
                    "Including all available features in a model always produces better results than selecting a carefully curated feature subset.",
                    "Automated feature engineering tools always produce better features than domain experts applying their subject matter knowledge."
                ]
            },
            "Ensemble Learning": {
                "description": "Implementing bagging with Random Forest, gradient boosting with XGBoost and LightGBM, and stacking to improve prediction performance.",
                "why_important": "Ensembles consistently outperform single models by reducing both variance and bias, making them essential for competitive ML applications.",
                "wrong_concepts": [
                    "Ensemble methods only provide benefits for classification tasks and offer no performance improvement for regression problems.",
                    "Adding more base learners to an ensemble always produces proportional improvements in the ensemble's predictive performance.",
                    "Stacking ensemble methods are straightforward to implement correctly and are always the recommended starting point for ML projects."
                ]
            },
            "Neural Network Fundamentals": {
                "description": "Designing feedforward neural networks, understanding backpropagation, applying activation functions, and using regularisation to prevent overfitting.",
                "why_important": "Neural networks are the foundation of deep learning; understanding their mechanics enables effective design and debugging of complex models.",
                "wrong_concepts": [
                    "Adding more hidden layers to a neural network always results in better performance regardless of the problem or dataset size.",
                    "Neural networks always outperform traditional machine learning algorithms when given sufficient data for any prediction task.",
                    "Deeper neural networks with more parameters are always more computationally efficient than shallower alternatives on the same task."
                ]
            },
            "ML Pipeline Design": {
                "description": "Building reproducible and maintainable ML pipelines using scikit-learn Pipelines, feature stores, and experiment tracking with tools like MLflow.",
                "why_important": "Well-designed pipelines prevent data leakage, enable reproducibility, and make models easier to maintain, update, and deploy reliably.",
                "wrong_concepts": [
                    "ML pipelines are unnecessary overhead for research projects and only provide value when a model is being deployed to production.",
                    "Data preprocessing steps should always be applied separately before training rather than being integrated into the model pipeline.",
                    "Experiment tracking tools add significant complexity without providing meaningful benefits for most machine learning projects."
                ]
            },
        },
        "advanced": {
            "MLOps": {
                "description": "Automating model training, implementing continuous training pipelines, versioning models and data, and monitoring for data and concept drift in production.",
                "why_important": "MLOps enables reliable and scalable deployment of ML systems, bridging the gap between experimental research and production reliability.",
                "wrong_concepts": [
                    "MLOps is simply the process of automating model deployment and requires no ongoing monitoring or maintenance after launch.",
                    "Data scientists should always be responsible for all MLOps activities since they have the deepest understanding of the models.",
                    "Models deployed to production maintain their predictive accuracy indefinitely without requiring monitoring or periodic retraining."
                ]
            },
            "Large Scale ML Systems": {
                "description": "Designing distributed training with frameworks like Ray and Horovod, optimising inference latency, and managing model serving infrastructure at scale.",
                "why_important": "Production ML systems must handle millions of predictions efficiently; distributed computing and serving optimisation enable this at acceptable cost.",
                "wrong_concepts": [
                    "Distributed training frameworks always improve model accuracy and should be used regardless of the dataset size or model complexity.",
                    "Reducing model inference latency always requires retraining the model with a smaller architecture rather than serving optimisations.",
                    "Adding more inference servers always linearly reduces prediction latency regardless of the underlying bottlenecks in the system."
                ]
            },
            "Responsible AI and Model Governance": {
                "description": "Implementing model fairness evaluation, bias detection, explainability with SHAP and LIME, and governance frameworks for high-stakes ML decisions.",
                "why_important": "AI systems have real-world impact on people; responsible development ensures models are fair, explainable, and aligned with ethical standards.",
                "wrong_concepts": [
                    "Model accuracy is the only important metric and fairness concerns are secondary considerations for most commercial ML applications.",
                    "A model trained on historical data is inherently unbiased since it reflects what actually happened in the real world objectively.",
                    "Explainability tools always reduce model performance and should only be applied when explicitly required by external regulations."
                ]
            },
        }
    },

    "Business Analyst": {
        "beginner": {
            "Requirements Gathering": {
                "description": "Conducting stakeholder interviews, facilitating workshops, documenting business needs, and writing user stories with clear acceptance criteria.",
                "why_important": "Clear requirements prevent building wrong solutions; thorough gathering saves significant time and money by catching misalignments early.",
                "wrong_concepts": [
                    "Requirements should be fully documented and formally locked down before any development work begins on any part of the project.",
                    "Stakeholders always have a clear understanding of their needs and can articulate complete and accurate requirements from the outset.",
                    "Technical specifications written by developers are sufficient substitutes for proper business requirements documents in most projects."
                ]
            },
            "Business Process Analysis": {
                "description": "Documenting current-state processes through observation and interviews, identifying inefficiencies, and designing improved future-state process flows.",
                "why_important": "Process analysis reveals the root causes of business problems and ensures proposed solutions address actual issues rather than symptoms.",
                "wrong_concepts": [
                    "Current business processes should always be automated exactly as they are before any analysis or optimisation is attempted.",
                    "A well-drawn process diagram alone is sufficient documentation to ensure a new system will be built and implemented correctly.",
                    "Involving too many stakeholders in process analysis workshops always leads to confusion and should be minimised as much as possible."
                ]
            },
            "Stakeholder Analysis": {
                "description": "Identifying all stakeholders impacted by a project, mapping their influence and interest, and tailoring communication strategies for each group.",
                "why_important": "Failing to engage the right stakeholders leads to missed requirements, resistance to change, and project failure despite technical success.",
                "wrong_concepts": [
                    "Stakeholder analysis is only necessary for large complex projects and adds no value to smaller analytical or improvement initiatives.",
                    "Senior executives are always the most important stakeholders in any project because they have the highest organisational authority.",
                    "Stakeholder engagement should be minimal to avoid scope creep since additional input always leads to expanding project requirements."
                ]
            },
            "Data Analysis Basics": {
                "description": "Using Excel, SQL, or basic Python to query datasets, calculate summary statistics, and extract insights that inform business decisions.",
                "why_important": "Business analysts need data skills to validate requirements, measure baseline performance, and provide evidence for recommendation.",
                "wrong_concepts": [
                    "Advanced data analysis skills are not necessary for business analysts since data scientists are always available to handle analytical work.",
                    "Excel pivot tables and VLOOKUP formulas are the only data skills a business analyst needs in most professional roles today.",
                    "Descriptive statistics alone are always sufficient evidence for making business recommendations without any further analytical depth."
                ]
            },
            "Use Case Development": {
                "description": "Writing detailed use cases describing actor goals, preconditions, main success scenarios, and alternative flows for system interactions.",
                "why_important": "Use cases ensure developers understand complete functional requirements including edge cases that might otherwise be discovered only in testing.",
                "wrong_concepts": [
                    "Use cases should focus only on the main happy-path scenario and alternative error flows are the responsibility of QA teams.",
                    "User stories and use cases are interchangeable formats and choosing between them has no impact on requirements quality.",
                    "A use case is complete when the primary actor's goal is described clearly without needing to document system responses."
                ]
            },
        },
        "intermediate": {
            "Process Modeling": {
                "description": "Creating BPMN diagrams, swimlane flowcharts, and value stream maps to document and communicate complex business processes to diverse audiences.",
                "why_important": "Visual process models reveal bottlenecks and redundancies, enable stakeholder communication, and provide blueprints for system development.",
                "wrong_concepts": [
                    "Process diagrams are purely documentation artefacts and have limited practical value in driving actual business improvement outcomes.",
                    "The most comprehensive process models with the greatest level of detail always produce the most value for business stakeholders.",
                    "BPMN notation is only understandable by technical analysts and should not be used when communicating with business stakeholders."
                ]
            },
            "Data Modelling": {
                "description": "Designing entity-relationship diagrams, defining data dictionaries, and collaborating with database architects to align data structures with business needs.",
                "why_important": "Correct data models prevent costly restructuring, ensure system integrity, and ensure data accurately represents real business entities and relationships.",
                "wrong_concepts": [
                    "Data modelling is an exclusively technical activity that business analysts should not be involved in or need to understand.",
                    "A physical database schema and a logical business data model are equivalent documents that can always be used interchangeably.",
                    "Adding more attributes to entities in a data model always improves data completeness and should be encouraged during design."
                ]
            },
            "Change Management": {
                "description": "Planning stakeholder communication, training programmes, and adoption strategies to ensure that new systems and processes are successfully embedded.",
                "why_important": "Technical solutions fail when people don't adopt them; change management ensures the human side of transformation is systematically addressed.",
                "wrong_concepts": [
                    "Change management is only necessary for large-scale enterprise transformation projects that affect hundreds of employees at once.",
                    "Adequate training for end users is always sufficient to ensure full adoption of new business systems and process changes.",
                    "Resistance to change always indicates that stakeholders have not understood the benefits and needs to be addressed through more communication."
                ]
            },
            "Gap Analysis": {
                "description": "Comparing current-state capabilities against future-state requirements to identify what changes are needed to achieve business objectives.",
                "why_important": "Gap analysis provides a structured foundation for project planning, ensuring solutions address the right problems and deliver measurable improvement.",
                "wrong_concepts": [
                    "Gap analysis is only necessary when an organisation is implementing entirely new technology rather than improving existing systems.",
                    "The future-state design should always be based on best practice benchmarks rather than on the specific needs of the organisation.",
                    "A gap analysis document produced by consultants is always more objective and accurate than one produced by internal analysts."
                ]
            },
            "Business Case Development": {
                "description": "Quantifying costs, benefits, and risks of proposed solutions, calculating ROI, and building compelling arguments for investment approval.",
                "why_important": "Strong business cases secure funding and organisational commitment, ensuring that analytical work translates into actionable decisions.",
                "wrong_concepts": [
                    "The primary purpose of a business case is to justify a decision that has already been made by senior leadership in the organisation.",
                    "Quantitative financial projections are the only information executives need to approve investment in a proposed business initiative.",
                    "Business cases become unnecessary once a project is approved since all important decisions have already been formally made."
                ]
            },
        },
        "advanced": {
            "Enterprise Architecture": {
                "description": "Aligning business strategy with IT capabilities using frameworks like TOGAF, defining target architectures, and managing architectural roadmaps.",
                "why_important": "Enterprise architecture prevents siloed systems and redundant investment by ensuring all technology decisions align with strategic direction.",
                "wrong_concepts": [
                    "Enterprise architecture is purely a technology function that does not require significant business strategy or process knowledge.",
                    "Adopting an enterprise architecture framework automatically produces a good architecture without requiring additional tailoring or judgement.",
                    "The enterprise architecture target state should remain fixed for at least five years to provide a stable planning horizon for all teams."
                ]
            },
            "Business Intelligence Strategy": {
                "description": "Defining KPI frameworks, designing data warehouse structures, building self-service analytics capabilities, and aligning data initiatives with business goals.",
                "why_important": "Strategic BI transforms data from a byproduct of operations into a competitive asset that drives evidence-based decision-making at scale.",
                "wrong_concepts": [
                    "Providing all employees with access to all available business data always leads to better and more informed organisational decisions.",
                    "The latest BI technology platform is the primary determinant of successful enterprise analytics programme outcomes and adoption.",
                    "Real-time data pipelines are always necessary for enterprise BI since all business decisions require access to the most current data."
                ]
            },
            "Digital Transformation Strategy": {
                "description": "Leading business capability assessments, defining digital roadmaps, managing transformation portfolios, and measuring digital maturity progression.",
                "why_important": "Organisations that fail to digitally transform face competitive disadvantage; structured transformation strategy ensures resources achieve real business outcomes.",
                "wrong_concepts": [
                    "Digital transformation is primarily a technology implementation programme and success is measured by systems successfully deployed.",
                    "Organisations should always pursue full digital transformation simultaneously across all business units to maximise speed of change.",
                    "Purchasing and implementing modern enterprise software is sufficient to complete a successful digital transformation programme."
                ]
            },
        }
    },

}


class EnhancedKnowledgeBase:
    """
    Expanded Knowledge Base for career assessments.
    5+ unique concepts per career per level ensures assessment questions
    cover different topics and do not repeat within a single session.
    """

    def __init__(self):
        self.knowledge = CAREER_KNOWLEDGE
        self.supported_careers = list(CAREER_KNOWLEDGE.keys())
        print(f"📚 Knowledge Base loaded: {len(self.supported_careers)} careers")

    def get_all_concepts(self, career, level):
        if career in self.knowledge and level in self.knowledge[career]:
            return list(self.knowledge[career][level].keys())
        return []

    def get_concept_data(self, career, level, topic):
        try:
            concepts = self.knowledge[career][level]
            if topic in concepts:
                return concepts[topic]
            for concept_name, data in concepts.items():
                if topic.lower() in concept_name.lower():
                    return data
            if concepts:
                return list(concepts.values())[0]
        except KeyError:
            pass
        return None

    def get_random_concept(self, career, level):
        import random
        concepts = self.get_all_concepts(career, level)
        return random.choice(concepts) if concepts else None