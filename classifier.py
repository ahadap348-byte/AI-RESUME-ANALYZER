"""
Machine Learning Model for Resume Domain Classification.
Uses TF-IDF + Multinomial Naive Bayes.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Synthetic high-quality training corpus across tech sectors
TRAINING_DATA = [
    # Data Science & AI
    ("Experienced with Python, Machine Learning, TensorFlow, PyTorch, Deep Learning, Pandas, Scikit-Learn, NLP, LLM, Data Analysis, SQL, Data Pipelines, R, Statistics, Predictive Modeling.", "Data Science & AI"),
    ("Built convolutional neural networks, BERT models, computer vision pipelines, scikit-learn regression, data wrangling with pandas and numpy, feature engineering.", "Data Science & AI"),
    ("Data scientist with expertise in time-series forecasting, statistical analysis, BigQuery, Tableau, generative AI, RAG architectures, and data visualization.", "Data Science & AI"),
    # Full Stack & Web Development
    ("Full stack developer skilled in React, Node.js, Express, TypeScript, HTML, CSS, Next.js, Redux, PostgreSQL, REST APIs, Tailwind, frontend and backend development.", "Full Stack & Web Dev"),
    ("Web application engineer with Angular, Vue, JavaScript, Django, PHP, MongoDB, GraphQL, web responsive design, CSS3, webpack, UI/UX implementation.", "Full Stack & Web Dev"),
    ("Frontend UI developer building interactive web applications with React.js, Next.js, Sass, state management, RESTful services, and micro-frontends.", "Full Stack & Web Dev"),
    # Cloud & DevOps
    ("DevOps engineer with Kubernetes, Docker, AWS, CI/CD pipelines, Terraform, Jenkins, Ansible, Linux bash scripting, Prometheus, Grafana, Cloud Architecture.", "Cloud & DevOps"),
    ("Cloud architect specializing in Google Cloud Platform GCP, Azure, microservices, containerization, Helm, GitOps, infrastructure as code, cloud security.", "Cloud & DevOps"),
    ("Site reliability engineer SRE managing high availability clusters, Docker orchestration, automated deployments, monitoring, networking, and server maintenance.", "Cloud & DevOps"),
    # Mobile App Development
    ("Mobile application developer experienced in Flutter, React Native, Swift, iOS, Kotlin, Android SDK, Dart, Xcode, mobile UI design, App Store deployment.", "Mobile Development"),
    ("Android developer proficient with Java, Kotlin, Jetpack Compose, Retrofit, Room DB, SQLite, Material Design, push notifications, Google Play Store.", "Mobile Development"),
    # Cybersecurity
    ("Cybersecurity analyst skilled in penetration testing, network security, SIEM, Wireshark, vulnerability assessment, ethical hacking, firewalls, SOC, incident response.", "Cybersecurity"),
    ("Information security engineer proficient in cryptography, OWASP Top 10, ISO 27001, threat hunting, IAM, malware analysis, compliance, and zero trust architecture.", "Cybersecurity"),
    # Product & Management
    ("Product manager leading Agile Scrum teams, sprint planning, roadmap development, user stories, stakeholder management, KPI tracking, Jira, A/B testing.", "Product Management"),
    ("Scrum master and technical project manager coordinating cross-functional engineering teams, backlog grooming, risk management, and product delivery.", "Product Management")
]


class ResumeClassifier:
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('clf', MultinomialNB(alpha=0.1))
        ])
        self._train()

    def _train(self):
        texts, labels = zip(*TRAINING_DATA)
        self.model.fit(texts, labels)

    def predict(self, text: str) -> dict:
        """Predict the primary role domain and class probabilities."""
        if not text.strip():
            return {"primary_domain": "Unknown", "probabilities": {}}

        predicted_class = self.model.predict([text])[0]
        classes = self.model.classes_
        probs = self.model.predict_proba([text])[0]
        prob_dict = {cls: round(float(p) * 100, 1) for cls, p in zip(classes, probs)}
        sorted_probs = dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True))

        return {
            "primary_domain": predicted_class,
            "probabilities": sorted_probs
        }


# Singleton classifier instance
classifier = ResumeClassifier()
