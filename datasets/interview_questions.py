"""
Interview questions database organized by skill/technology.
Used by the AI Interview Question Generator module.
"""

INTERVIEW_QUESTIONS = {
    "python": {
        "basic": [
            "What are Python's key features that distinguish it from other languages?",
            "Explain the difference between lists, tuples, sets, and dictionaries in Python.",
            "What is PEP 8 and why is it important?",
            "What are Python decorators and how do you use them?",
            "Explain list comprehensions and generator expressions.",
            "What is the difference between *args and **kwargs?",
            "How does Python manage memory? Explain garbage collection.",
            "What are Python's built-in data types?",
            "Explain the concept of mutable vs immutable objects.",
            "What is the difference between `is` and `==` operators?"
        ],
        "intermediate": [
            "What are context managers and how do you create one using `with`?",
            "Explain Python's GIL (Global Interpreter Lock) and its implications.",
            "What are metaclasses in Python?",
            "How do you handle exceptions in Python? Explain try/except/finally/else.",
            "What is the difference between shallow copy and deep copy?",
            "Explain Python's MRO (Method Resolution Order) in multiple inheritance.",
            "What are iterators and generators? How do they differ?",
            "How does Python's `async/await` work? When would you use it?",
            "Explain the LEGB rule for variable scope in Python.",
            "What are Python slots and when would you use them?"
        ],
        "advanced": [
            "How would you optimize Python code for performance?",
            "Explain Python's descriptor protocol.",
            "What are abstract base classes (ABCs) and when would you use them?",
            "How does Python's import system work?",
            "What is duck typing and how does it relate to Python's type system?",
            "Explain the difference between multiprocessing and multithreading in Python.",
            "How would you profile and debug a slow Python application?",
            "What are data classes and how do they compare to namedtuples?",
            "Explain Python's memory model with respect to objects and references.",
            "How would you design a Python package for distribution on PyPI?"
        ]
    },

    "machine learning": {
        "basic": [
            "What is the difference between supervised and unsupervised learning?",
            "Explain the bias-variance tradeoff.",
            "What is overfitting and how do you prevent it?",
            "What is cross-validation and why is it important?",
            "Explain the difference between classification and regression.",
            "What is a confusion matrix? Explain precision, recall, and F1-score.",
            "What is gradient descent and how does it work?",
            "Explain the concept of feature engineering.",
            "What is regularization? Explain L1 vs L2 regularization.",
            "How do you handle missing data in a dataset?"
        ],
        "intermediate": [
            "Explain how Random Forest works and why it's effective.",
            "What is the curse of dimensionality and how do you address it?",
            "Explain SVM (Support Vector Machines) and the kernel trick.",
            "What is ensemble learning? Compare bagging, boosting, and stacking.",
            "How does XGBoost differ from traditional gradient boosting?",
            "Explain Principal Component Analysis (PCA) and its use cases.",
            "What is the difference between parametric and non-parametric models?",
            "How would you handle class imbalance in a dataset?",
            "What is a ROC curve and AUC score?",
            "Explain the EM algorithm for clustering."
        ],
        "advanced": [
            "How do you select and tune hyperparameters at scale?",
            "Explain model interpretability techniques (SHAP, LIME, etc.).",
            "What is concept drift and how do you monitor for it in production?",
            "How would you design an ML system for a real-time recommendation engine?",
            "Explain the trade-offs between different optimization algorithms (Adam, SGD, etc.).",
            "What is federated learning and when would you use it?",
            "How do you ensure reproducibility in ML experiments?",
            "Explain causal inference vs correlation in ML.",
            "What is multi-task learning and when is it beneficial?",
            "How would you approach an A/B test for an ML model rollout?"
        ]
    },

    "sql": {
        "basic": [
            "What is the difference between WHERE and HAVING clauses?",
            "Explain different types of JOINs (INNER, LEFT, RIGHT, FULL OUTER).",
            "What are aggregate functions? Give examples.",
            "What is the difference between DELETE, TRUNCATE, and DROP?",
            "Explain the concept of database normalization (1NF, 2NF, 3NF).",
            "What are indexes and why are they important?",
            "What is a subquery and when would you use one?",
            "Explain the difference between UNION and UNION ALL.",
            "What are constraints in SQL? Give examples.",
            "How do you group and sort data in SQL?"
        ],
        "intermediate": [
            "What are window functions in SQL? Give examples of RANK, ROW_NUMBER, LAG.",
            "Explain CTE (Common Table Expressions) and their advantages.",
            "How do you optimize a slow SQL query?",
            "What is the difference between clustered and non-clustered indexes?",
            "Explain ACID properties in database transactions.",
            "What are stored procedures and when would you use them?",
            "How do you handle NULL values in SQL?",
            "Explain the difference between OLTP and OLAP systems.",
            "What is a materialized view vs a regular view?",
            "How would you find duplicate records in a table?"
        ],
        "advanced": [
            "How would you design a schema for a social media application?",
            "Explain query execution plans and how to read them.",
            "What is database partitioning and when is it beneficial?",
            "How do you handle concurrent transactions and prevent deadlocks?",
            "What is eventual consistency in distributed databases?",
            "Explain the CAP theorem.",
            "How would you migrate a large database with zero downtime?",
            "What are the trade-offs between relational and NoSQL databases?",
            "How do you design for horizontal scalability in SQL?",
            "Explain row-level security and data masking."
        ]
    },

    "data science": {
        "basic": [
            "What is the data science lifecycle? Walk me through it.",
            "Explain exploratory data analysis (EDA) and its importance.",
            "What is the difference between correlation and causation?",
            "How do you handle outliers in a dataset?",
            "What is feature selection and why is it important?",
            "Explain the central limit theorem.",
            "What is p-value and statistical significance?",
            "How do you assess model performance for regression vs classification?",
            "What is data leakage and how do you prevent it?",
            "How would you communicate data insights to non-technical stakeholders?"
        ],
        "intermediate": [
            "Walk me through a complete data science project from problem definition to deployment.",
            "How do you approach time series forecasting?",
            "What is A/B testing and how do you design one properly?",
            "Explain the difference between frequentist and Bayesian statistics.",
            "How would you build a recommendation system from scratch?",
            "What is natural language processing (NLP) and its common tasks?",
            "How do you deal with high-dimensional data?",
            "Explain transfer learning and when you'd apply it.",
            "How would you build a fraud detection system?",
            "What is the difference between batch and online learning?"
        ],
        "advanced": [
            "How do you scale data processing to petabyte-scale datasets?",
            "Design a machine learning platform for an enterprise.",
            "How would you approach a cold-start problem in recommendation systems?",
            "Explain the ethics of AI/ML and how you'd address bias in models.",
            "How do you evaluate a generative AI model?",
            "What is MLOps and how do you implement a mature ML pipeline?",
            "How would you design a real-time anomaly detection system?",
            "Explain graph neural networks and their applications.",
            "How do you handle distribution shift in production ML models?",
            "What are the key considerations for deploying ML at the edge?"
        ]
    },

    "deep learning": {
        "basic": [
            "What is a neural network and how does backpropagation work?",
            "Explain the role of activation functions. Compare ReLU, Sigmoid, Tanh.",
            "What is the vanishing gradient problem and how is it addressed?",
            "What is batch normalization and why is it used?",
            "Explain dropout and its role in regularization.",
            "What are CNNs and what makes them suitable for image tasks?",
            "What are RNNs and LSTMs?",
            "What is transfer learning in deep learning?",
            "Explain the concept of learning rate and its importance.",
            "What are the main hyperparameters in a neural network?"
        ],
        "advanced": [
            "Explain the Transformer architecture and self-attention mechanism.",
            "What is BERT and how does it differ from GPT?",
            "Explain GAN (Generative Adversarial Networks) architecture.",
            "What is knowledge distillation?",
            "How do you handle catastrophic forgetting in neural networks?",
            "Explain attention mechanisms beyond self-attention.",
            "What are diffusion models and how do they work?",
            "How would you fine-tune a large language model?",
            "What is mixture of experts (MoE) architecture?",
            "Explain neural architecture search (NAS)."
        ]
    },

    "tensorflow": {
        "basic": [
            "What is the difference between TensorFlow 1.x and 2.x?",
            "Explain eager execution in TensorFlow.",
            "How do you define a custom layer in Keras?",
            "What is the difference between model.fit() and a custom training loop?",
            "How do you save and load a TensorFlow model?",
            "What are TensorFlow datasets and how do you use them?",
            "Explain the difference between Sequential and Functional Keras API.",
            "What is TensorBoard and how do you use it?",
            "How do you handle GPU training in TensorFlow?",
            "What are callbacks in Keras and name some useful ones?"
        ]
    },

    "aws": {
        "basic": [
            "What is the difference between EC2, Lambda, and ECS?",
            "Explain S3 storage classes and their use cases.",
            "What is VPC and how does it provide network isolation?",
            "How does IAM work? Explain roles, policies, and permissions.",
            "What is the difference between RDS and DynamoDB?",
            "Explain the concept of auto-scaling in AWS.",
            "What is CloudWatch and how do you use it for monitoring?",
            "What is the difference between SQS and SNS?",
            "How does AWS Lambda work and when would you use it?",
            "What are the key services for deploying ML models on AWS?"
        ]
    },

    "docker": {
        "basic": [
            "What is the difference between a Docker image and a container?",
            "Explain the Dockerfile structure and key instructions.",
            "What is Docker Compose and when would you use it?",
            "How do Docker volumes and bind mounts work?",
            "What is a Docker registry and how do you push/pull images?",
            "Explain Docker networking modes.",
            "How do you optimize Docker image size?",
            "What is a multi-stage Docker build?",
            "How do you debug a running Docker container?",
            "What is the difference between CMD and ENTRYPOINT in Dockerfile?"
        ]
    },

    "nlp": {
        "basic": [
            "What is tokenization and why is it the first step in NLP?",
            "Explain TF-IDF and its use in text analysis.",
            "What is word embedding? Compare Word2Vec, GloVe, and fastText.",
            "What is named entity recognition (NER)?",
            "Explain sentiment analysis and its challenges.",
            "What is part-of-speech tagging?",
            "What is stemming vs lemmatization?",
            "What are n-grams and how are they used?",
            "Explain the bag-of-words model and its limitations.",
            "What are stop words and should you always remove them?"
        ],
        "advanced": [
            "Explain the BERT pre-training tasks (MLM and NSP).",
            "How do you fine-tune a language model for a specific task?",
            "What is RAG (Retrieval-Augmented Generation)?",
            "Explain prompt engineering techniques for LLMs.",
            "How do you evaluate the quality of text generation?",
            "What are the challenges of multilingual NLP?",
            "Explain text summarization approaches (extractive vs abstractive).",
            "How do vector embeddings enable semantic search?",
            "What is chain-of-thought prompting?",
            "How would you build a question-answering system?"
        ]
    },

    "react": {
        "basic": [
            "What is JSX and why is it used in React?",
            "Explain the virtual DOM and how React uses it.",
            "What are React hooks? Explain useState and useEffect.",
            "What is the difference between controlled and uncontrolled components?",
            "Explain the React component lifecycle.",
            "What is prop drilling and how do you avoid it?",
            "What is React Context API?",
            "Explain the difference between class and functional components.",
            "What is React.memo and when would you use it?",
            "How does React handle events?"
        ]
    },

    "django": {
        "basic": [
            "Explain Django's MVT (Model-View-Template) pattern.",
            "What is the Django ORM and how does it simplify database operations?",
            "How does Django's URL routing work?",
            "What are Django middleware and how do they work?",
            "Explain Django REST Framework serializers.",
            "What is Django's authentication system?",
            "How do Django signals work?",
            "What is Django's migration system?",
            "Explain Django's admin interface.",
            "How do you optimize Django querysets for performance?"
        ]
    }
}

# General behavioral/soft skill questions
BEHAVIORAL_QUESTIONS = [
    "Tell me about yourself and your journey into data science/tech.",
    "Describe a challenging technical problem you solved and your approach.",
    "How do you stay current with the latest developments in your field?",
    "Tell me about a time you had to explain a technical concept to a non-technical stakeholder.",
    "How do you prioritize tasks when working on multiple projects?",
    "Describe a situation where you had to work with incomplete or messy data.",
    "Tell me about a project you're most proud of and why.",
    "How do you approach learning a new technology or framework?",
    "Describe a time when your model/code failed in production. How did you handle it?",
    "Where do you see yourself in 3-5 years?"
]
