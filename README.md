# College FAQ Question-Answering System 🎓🤖

An intelligent, full-stack NLP-powered question answering application designed for higher education institutions. The system allows students to ask natural language questions about college admissions, examination schedules, attendance rules, fee structures, hostel policies, library hours, placement records, department details, and campus facilities.

The matching mechanism utilizes **NLTK preprocessing**, **scikit-learn TF-IDF Vectorization**, and **Cosine Similarity** retrieval over an **SQLite** database.

---

## 🌟 Key Features

### Student Interface
- **Natural Language Question Answering**: Instant answer retrieval using TF-IDF and Cosine Similarity.
- **Confidence Scoring & Badges**: Every response displays an explicit match percentage and confidence rating (*High*, *Medium*, *Low*, or *Unreliable*).
- **Fallback Threshold Safeguard**: Queries with confidence scores below 20% gracefully return:  
  `"Sorry, I could not find a reliable answer."` along with top close suggestions.
- **NLP Breakdown Expander**: Detailed view showing original query, NLTK preprocessed tokens, matched FAQ question, and similarity score.
- **Category Filter Pills**: Easily browse FAQs across 9 distinct categories.
- **Suggested Question Chips**: Quick one-click prompt suggestions.
- **Theme Switcher**: Instant Light / Dark mode toggle with persistent local storage.

### Admin Management Portal
- **KPI Analytics Dashboard**: Track total indexed FAQs, total queries asked, resolution rate (%), and active categories.
- **FAQ CRUD Operations**: Create, edit, and delete FAQ entries with real-time NLP TF-IDF index retraining.
- **Query History & Audit Logs**: Inspect student queries, matched FAQs, similarity scores, timestamps, and status ratings (*ANSWERED* vs *UNANSWERED*).
- **Live Vector Sandbox**: Test any custom prompt against the corpus and inspect rank-ordered cosine similarity matrices.

---

## 📁 9 Pre-seeded Categories (36+ FAQs Included)

1. **Admissions**: Application process, eligibility criteria, required documents, deadlines, scholarships.
2. **Departments**: Engineering & science streams, HOD contacts, branch transfer rules, research labs.
3. **Examination**: End-semester datesheets, hall ticket download, re-evaluation, backlog exams.
4. **Attendance**: 75% minimum rule, medical leave submission, condonation, detention rules.
5. **Library**: Operating hours, book borrowing limits, digital e-journal access (IEEE/Springer), late fines.
6. **Fees**: Semester payment modes (UPI/NetBanking/DD), fee breakdown, due dates, refund policy.
7. **Hostel**: Room allotment, night curfew timings, outpass procedure, mess meal schedules.
8. **Placements**: Recruitment statistics, average salary packages, visiting top firms, eligibility rules.
9. **Campus**: Wi-Fi access, 24/7 health center & ambulance, sports complex, cafeteria options.

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3 (Variables, Flexbox/Grid, Dark/Light Mode), Vanilla JavaScript (ES6+ Fetch API, DOM manipulation).
- **Backend**: Python 3.9+ Flask.
- **NLP Engine**: NLTK (Tokenization, Stopwords removal, Lemmatization) + `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`).
- **Database**: SQLite3 (`college_faq.db`).

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
Ensure Python 3.8+ is installed on your system:
```bash
python --version
```

### 2. Navigate to Project Directory
```bash
cd C:\Users\sueen\.gemini\antigravity\scratch\college_faq_system
```

### 3. Install Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

Start the Flask application server:
```bash
python app.py
```

Upon launching, the system will initialize the SQLite database (`college_faq.db`), seed the 36+ FAQs, and start the local development server at:

- **Student Chat Interface**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Admin Management Portal**: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

---

## 📊 API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Renders Student Chat Interface |
| `GET` | `/admin` | Renders Admin Portal Dashboard |
| `POST` | `/api/ask` | Process student query through NLP matcher |
| `GET` | `/api/categories` | Get all FAQ categories with counts |
| `GET` | `/api/faqs` | Search/filter FAQs by category or query |
| `GET` | `/api/suggested-questions` | Get recommended question chips |
| `POST` | `/api/admin/faq` | Create new FAQ & retrain TF-IDF model |
| `PUT` | `/api/admin/faq/<id>` | Update existing FAQ & retrain model |
| `DELETE` | `/api/admin/faq/<id>` | Delete FAQ & retrain model |
| `GET` | `/api/admin/history` | Retrieve student query logs & scores |
| `DELETE` | `/api/admin/history` | Clear query history logs |
| `GET` | `/api/admin/analytics` | Get summary dashboard KPI metrics |
| `POST` | `/api/admin/test-similarity` | Test cosine similarity vector rank sandbox |

---

## 🧪 Verification & Testing

### Automated NLP Unit Test
Run the standalone NLP test script to verify tokenization, TF-IDF vectorization, cosine similarity scores, and threshold fallbacks:
```bash
python -c "from nlp_engine import nlp_matcher; print(nlp_matcher.match('What is the minimum attendance requirement?'))"
```

Expected Output:
```json
{
  "success": true,
  "confidence_level": "High",
  "score_percentage": "85.4%",
  "status": "ANSWERED",
  "category": "Attendance"
}
```

### Unreliable Query Test
```bash
python -c "from nlp_engine import nlp_matcher; print(nlp_matcher.match('How to fly a rocket into space?'))"
```

Expected Output:
```json
{
  "success": false,
  "answer": "Sorry, I could not find a reliable answer.",
  "status": "UNANSWERED"
}
```

---

## 📁 Project Structure

```
college_faq_system/
├── app.py                  # Flask Web Server & REST API Routes
├── nlp_engine.py           # Preprocessing (NLTK) & Vector Matcher (scikit-learn)
├── database.py             # SQLite Schema Management & CRUD Operations
├── seed_data.py            # Initial Seed Dataset (9 Categories, 36+ FAQs)
├── requirements.txt        # Dependencies (Flask, scikit-learn, NLTK, NumPy)
├── README.md               # Complete System Documentation
├── static/
│   ├── css/
│   │   └── style.css       # Responsive Stylesheet & Dark Mode Variables
│   └── js/
│       ├── app.js          # Student Chat Interactivity & Dynamic Messaging
│       └── admin.js        # Admin Portal CRUD, History, & Vector Sandbox
└── templates/
    ├── index.html          # Student Chat UI HTML Template
    └── admin.html          # Admin Portal Management HTML Template
```

---

## 📄 License
This project is open-source and available under the MIT License.
