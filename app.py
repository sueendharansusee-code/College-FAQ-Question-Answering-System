"""
Flask Web Application for College FAQ Question-Answering System.
Connects SQLite database, NLP Engine, Student Chat UI, and Admin Portal APIs.
"""

from flask import Flask, render_template, request, jsonify
import database
from nlp_engine import nlp_matcher, preprocess_text
from seed_data import SUGGESTED_QUESTIONS

app = Flask(__name__)

# Initialize database on startup
database.init_db()


# ==========================================
# PAGE ROUTES
# ==========================================

@app.route('/')
def index():
    """Renders Student Chat Interface."""
    return render_template('index.html')


@app.route('/admin')
def admin():
    """Renders Admin Management Dashboard."""
    return render_template('admin.html')


# ==========================================
# STUDENT QA & SEARCH APIS
# ==========================================

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Primary Question-Answering API endpoint.
    Accepts student question, runs TF-IDF + Cosine Similarity matching,
    and returns answer with confidence metrics.
    """
    data = request.get_json() or {}
    user_query = data.get('question', '').strip()

    if not user_query:
        return jsonify({
            "error": True,
            "message": "Please enter a valid question."
        }), 400

    result = nlp_matcher.match(user_query)
    return jsonify(result)


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Retrieves all FAQ categories with item counts."""
    categories = database.get_all_categories()
    return jsonify({"success": True, "categories": categories})


@app.route('/api/suggested-questions', methods=['GET'])
def get_suggested_questions():
    """Retrieves sample suggested questions for quick chat chips."""
    return jsonify({"success": True, "suggestions": SUGGESTED_QUESTIONS})


@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    """Retrieves FAQs filtered by category or search term."""
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', type=str)
    faqs = database.get_all_faqs(category_id=category_id, search_term=search)
    return jsonify({"success": True, "faqs": faqs, "count": len(faqs)})


# ==========================================
# ADMIN CRUD APIS
# ==========================================

@app.route('/api/admin/faq', methods=['POST'])
def add_faq():
    """Adds a new FAQ entry and reindexes the NLP TF-IDF model."""
    data = request.get_json() or {}
    category_id = data.get('category_id')
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    keywords = data.get('keywords', '').strip()

    if not category_id or not question or not answer:
        return jsonify({"success": False, "message": "Category, question, and answer are required."}), 400

    faq_id = database.add_faq(category_id, question, answer, keywords)

    # Trigger NLP vectorizer reindex
    nlp_matcher.reindex()

    return jsonify({"success": True, "message": "FAQ created successfully!", "id": faq_id})


@app.route('/api/admin/faq/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    """Updates an existing FAQ entry and reindexes the NLP model."""
    data = request.get_json() or {}
    category_id = data.get('category_id')
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    keywords = data.get('keywords', '').strip()

    if not category_id or not question or not answer:
        return jsonify({"success": False, "message": "Category, question, and answer are required."}), 400

    updated = database.update_faq(faq_id, category_id, question, answer, keywords)
    if not updated:
        return jsonify({"success": False, "message": "FAQ not found."}), 404

    # Trigger NLP vectorizer reindex
    nlp_matcher.reindex()

    return jsonify({"success": True, "message": "FAQ updated successfully!"})


@app.route('/api/admin/faq/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    """Deletes an FAQ entry and reindexes the NLP model."""
    deleted = database.delete_faq(faq_id)
    if not deleted:
        return jsonify({"success": False, "message": "FAQ not found."}), 404

    # Trigger NLP vectorizer reindex
    nlp_matcher.reindex()

    return jsonify({"success": True, "message": "FAQ deleted successfully!"})


@app.route('/api/admin/history', methods=['GET'])
def get_history():
    """Retrieves question history log."""
    status_filter = request.args.get('status', type=str)
    limit = request.args.get('limit', default=100, type=int)
    history = database.get_query_history(limit=limit, status_filter=status_filter)
    return jsonify({"success": True, "history": history, "count": len(history)})


@app.route('/api/admin/history', methods=['DELETE'])
def clear_history():
    """Clears query history logs."""
    database.clear_query_history()
    return jsonify({"success": True, "message": "Query history cleared."})


@app.route('/api/admin/analytics', methods=['GET'])
def get_analytics():
    """Retrieves dashboard summary stats."""
    summary = database.get_analytics_summary()
    return jsonify({"success": True, "analytics": summary})


@app.route('/api/admin/test-similarity', methods=['POST'])
def test_similarity_sandbox():
    """
    Sandbox endpoint for admin to test a query against all stored FAQs
    and see exact ranked cosine similarity scores.
    """
    data = request.get_json() or {}
    test_query = data.get('query', '').strip()

    if not test_query:
        return jsonify({"success": False, "message": "Query is required."}), 400

    if not nlp_matcher.is_indexed or not nlp_matcher.faq_list:
        nlp_matcher.reindex()

    processed = preprocess_text(test_query)
    q_vec = nlp_matcher.vectorizer.transform([processed if processed else test_query])
    from sklearn.metrics.pairwise import cosine_similarity
    scores = cosine_similarity(q_vec, nlp_matcher.tfidf_matrix)[0]

    ranked_results = []
    for idx, score in enumerate(scores):
        faq_item = nlp_matcher.faq_list[idx]
        ranked_results.append({
            "id": faq_item['id'],
            "question": faq_item['question'],
            "category": faq_item['category_name'],
            "similarity_score": round(float(score), 4),
            "score_percentage": f"{round(float(score) * 100, 1)}%"
        })

    # Sort descending by score
    ranked_results.sort(key=lambda x: x['similarity_score'], reverse=True)

    return jsonify({
        "success": True,
        "query": test_query,
        "processed_tokens": processed,
        "results": ranked_results[:10]  # Top 10 matches
    })


if __name__ == '__main__':
    print("\n=======================================================")
    print("  College FAQ Question-Answering System Running!")
    print("  Student Chat UI: http://127.0.0.1:5000/")
    print("  Admin Dashboard: http://127.0.0.1:5000/admin")
    print("=======================================================\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
