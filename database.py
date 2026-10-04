"""
Database Module for College FAQ System.
Handles SQLite database connection, table initialization, seeding, and CRUD operations.
"""

import sqlite3
import os
from datetime import datetime
from seed_data import CATEGORIES, SAMPLE_FAQS

DB_PATH = os.path.join(os.path.dirname(__file__), 'college_faq.db')

def get_db_connection():
    """Establishes and returns a row-factory SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes schema and populates seed data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            icon TEXT DEFAULT 'fa-folder'
        )
    ''')

    # 2. Create FAQs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            keywords TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    ''')

    # 3. Create query history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            matched_faq_id INTEGER,
            matched_question TEXT,
            matched_answer TEXT,
            similarity_score REAL DEFAULT 0.0,
            category_name TEXT,
            status TEXT DEFAULT 'ANSWERED',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (matched_faq_id) REFERENCES faqs (id) ON DELETE SET NULL
        )
    ''')

    conn.commit()

    # Seed categories if table is empty
    cursor.execute('SELECT COUNT(*) as count FROM categories')
    if cursor.fetchone()['count'] == 0:
        print("[Database] Seeding categories...")
        for cat in CATEGORIES:
            cursor.execute(
                'INSERT INTO categories (name, description, icon) VALUES (?, ?, ?)',
                (cat['name'], cat['description'], cat['icon'])
            )
        conn.commit()

    # Seed FAQs if table is empty
    cursor.execute('SELECT COUNT(*) as count FROM faqs')
    if cursor.fetchone()['count'] == 0:
        print("[Database] Seeding sample FAQs...")
        for faq in SAMPLE_FAQS:
            cursor.execute('SELECT id FROM categories WHERE name = ?', (faq['category'],))
            cat_row = cursor.fetchone()
            if cat_row:
                cursor.execute(
                    '''INSERT INTO faqs (category_id, question, answer, keywords) 
                       VALUES (?, ?, ?, ?)''',
                    (cat_row['id'], faq['question'], faq['answer'], faq['keywords'])
                )
        conn.commit()

    conn.close()
    print("[Database] Database initialized and verified.")

def get_all_categories():
    """Returns all categories with FAQ counts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, COUNT(f.id) as faq_count
        FROM categories c
        LEFT JOIN faqs f ON c.id = f.category_id
        GROUP BY c.id
        ORDER BY c.name ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_faqs(category_id=None, search_term=None):
    """Returns all FAQs with optional category filter and keyword search."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
        SELECT f.*, c.name as category_name, c.icon as category_icon
        FROM faqs f
        JOIN categories c ON f.category_id = c.id
        WHERE 1=1
    '''
    params = []

    if category_id:
        query += ' AND f.category_id = ?'
        params.append(category_id)

    if search_term:
        query += ' AND (f.question LIKE ? OR f.answer LIKE ? OR f.keywords LIKE ?)'
        pattern = f'%{search_term}%'
        params.extend([pattern, pattern, pattern])

    query += ' ORDER BY f.id DESC'

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_faq_by_id(faq_id):
    """Returns a single FAQ by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.*, c.name as category_name
        FROM faqs f
        JOIN categories c ON f.category_id = c.id
        WHERE f.id = ?
    ''', (faq_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_faq(category_id, question, answer, keywords=""):
    """Adds a new FAQ entry."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO faqs (category_id, question, answer, keywords, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (category_id, question.strip(), answer.strip(), keywords.strip(), now, now))
    faq_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return faq_id

def update_faq(faq_id, category_id, question, answer, keywords=""):
    """Updates an existing FAQ entry."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        UPDATE faqs
        SET category_id = ?, question = ?, answer = ?, keywords = ?, updated_at = ?
        WHERE id = ?
    ''', (category_id, question.strip(), answer.strip(), keywords.strip(), now, faq_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_faq(faq_id):
    """Deletes an FAQ entry."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM faqs WHERE id = ?', (faq_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def log_query(user_query, matched_faq_id, matched_question, matched_answer, similarity_score, category_name, status):
    """Logs a student query and NLP resolution result to query_history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO query_history 
        (user_query, matched_faq_id, matched_question, matched_answer, similarity_score, category_name, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_query, matched_faq_id, matched_question, matched_answer, round(similarity_score, 4), category_name, status, now))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return log_id

def get_query_history(limit=100, status_filter=None):
    """Retrieves query history with optional status filter."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM query_history WHERE 1=1'
    params = []

    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)

    query += ' ORDER BY id DESC LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_query_history():
    """Clears all query history records."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM query_history')
    conn.commit()
    conn.close()

def get_analytics_summary():
    """Computes summary statistics for the Admin Dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total_faqs FROM faqs')
    total_faqs = cursor.fetchone()['total_faqs']

    cursor.execute('SELECT COUNT(*) as total_queries FROM query_history')
    total_queries = cursor.fetchone()['total_queries']

    cursor.execute("SELECT COUNT(*) as answered_queries FROM query_history WHERE status = 'ANSWERED'")
    answered_queries = cursor.fetchone()['answered_queries']

    cursor.execute("SELECT COUNT(*) as low_confidence FROM query_history WHERE status = 'UNANSWERED'")
    low_confidence = cursor.fetchone()['low_confidence']

    cursor.execute('SELECT COUNT(*) as total_categories FROM categories')
    total_categories = cursor.fetchone()['total_categories']

    resolution_rate = round((answered_queries / total_queries * 100), 1) if total_queries > 0 else 100.0

    conn.close()

    return {
        "total_faqs": total_faqs,
        "total_queries": total_queries,
        "answered_queries": answered_queries,
        "low_confidence_queries": low_confidence,
        "total_categories": total_categories,
        "resolution_rate": resolution_rate
    }
