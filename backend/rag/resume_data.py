"""
Structured representation of Chris Bhaila's resume + portfolio content.
This is the source of truth the matcher grounds all claims against —
nothing gets drafted into a bullet point that isn't traceable to an entry here.
"""

SKILLS = {
    "ai_ml": ["PyTorch", "scikit-learn", "Sentence-BERT", "Transformers", "NumPy", "Pandas", "Keras"],
    "programming": ["Python", "JavaScript", "PHP", "Java", "C", "C#"],
    "data": ["Web Scraping (BeautifulSoup)", "Data Cleaning", "MySQL", "PostgreSQL", "Matplotlib", "Plotly"],
    "web_backend": ["Django", "Laravel", "REST APIs", "FastAPI"],
    "tools": ["Git", "Jupyter", "MATLAB", "Docker"],
}

EXPERIENCE = [
    {
        "id": "nahusha_internship",
        "title": "Full-Stack Developer Intern",
        "org": "Nahusha Investment Pvt. Ltd.",
        "period": "2026",
        "bullets": [
            "Developed FloraNepal, a nursery management web application, using Laravel, Blade, Tailwind CSS, and Alpine.js",
            "Implemented token-based authentication with Laravel Sanctum and Google SSO via Laravel Socialite",
            "Engineered SPA-like navigation using Alpine.js and custom X-Dashboard-Navigate headers, reducing full-page reloads",
        ],
    },
]

PROJECTS = [
    {
        "id": "traffic_hotspot",
        "name": "Traffic Hotspot Detection System",
        "stack": ["Python", "Django", "scikit-learn", "PostgreSQL", "Leaflet.js", "Chart.js"],
        "bullets": [
            "Implemented DBSCAN from scratch using Haversine distance to detect 43 accident hotspots across 1,498 records",
            "Built an ID3 decision tree from scratch for severity prediction; evaluated results and identified class imbalance as the primary failure mode",
            "Built dual-language (English/Nepali) scrapers using Devanagari keyword dictionaries",
            "Deployed full-stack Django app on Render with PostgreSQL",
        ],
    },
    {
        "id": "cnn_image_classification",
        "name": "Image Classification with CNNs",
        "stack": ["PyTorch", "Keras", "TensorFlow"],
        "bullets": [
            "Implemented and compared CNN architectures from scratch (LeNet, ResNet, AlexNet) on MNIST",
            "Applied transfer learning with pretrained VGG16 and EfficientNetB0, including partial fine-tuning",
        ],
    },
    {
        "id": "ecommerce_scraper",
        "name": "Product Web Scraper & Data Pipeline",
        "stack": ["Python", "BeautifulSoup", "Pandas", "MySQL", "Matplotlib", "Plotly"],
        "bullets": [
            "Built a scraper to extract product data and images, exporting to CSV",
            "Cleaned and transformed data with Pandas, visualized trends with Matplotlib and Plotly",
            "Designed a MySQL storage pipeline",
        ],
    },
    {
        "id": "motovault",
        "name": "AI-powered Recommendation System (MotoVault)",
        "stack": ["Python", "SBERT", "PHP", "MySQL"],
        "bullets": [
            "Built a semantic retrieval engine using Sentence-BERT embeddings and cosine similarity",
            "Built full-stack e-commerce platform with auth, inventory management, item filtering",
            "Integrated a user rating system for recommendation refinement",
        ],
    },
    {
        "id": "integritycheck",
        "name": "IntegrityCheck – Plagiarism Detection Platform",
        "stack": ["Laravel", "Python", "FastAPI", "SBERT"],
        "bullets": [
            "Built a dual-signal similarity engine: n-gram shingling + Jaccard (lexical) and SBERT + cosine similarity (semantic)",
            "Extended detection to the open web via Google Custom Search API and a scraping pipeline",
            "Designed a role-based Laravel platform with a Python FastAPI microservice for scoring and a queued job pipeline",
            "Built a similarity report UI with source attribution distinguishing peer vs. web matches",
        ],
    },
    {
        "id": "secure_skills_hub",
        "name": "Secure Skills Hub – LMS",
        "stack": ["Laravel", "Alpine.js", "Tailwind CSS"],
        "bullets": [
            "Designed a private, instructor-led LMS as a solo client project",
            "Built token-based enrollment replacing payment infrastructure",
            "Enforced role-based access control at the middleware level",
            "Integrated Google OAuth for SSO; structured codebase around the repository pattern",
        ],
    },
    {
        "id": "dwellcasa",
        "name": "DwellCasa – Hotel Management System",
        "stack": ["Laravel", "Alpine.js", "Tailwind CSS", "MySQL"],
        "bullets": [
            "Designed a full-stack hotel platform using the repository pattern across a multi-location tenancy model",
            "Implemented a status-based availability engine handling the full reservation lifecycle, preventing double-booking",
            "Built a dual-track inventory system: consumables with usage logs, durable equipment with serial tracking",
            "Enforced role-based access control scoped per property location",
        ],
    },
]

EDUCATION = {
    "degree": "Bachelor's in Computer Application",
    "institution": "Thames International College, Tribhuvan University",
    "status": "Graduated",
    "coursework": ["Data Structures & Algorithms", "AI", "Probability & Statistics", "Web Technology", "OOP", "DBMS"],
}