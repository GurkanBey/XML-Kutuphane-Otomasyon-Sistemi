import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import os


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(app):
    # Register close_db to be called when app context ends
    app.teardown_appcontext(close_db)
    
    # Create database tables if they don't exist
    with app.app_context():
        db = get_db()
        
        # Create users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        # Create books table
        db.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                publisher TEXT,
                category TEXT,
                description TEXT
            )
        ''')
        
        # Check if sample data exists
        cursor = db.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Insert sample users
            db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("admin", "admin123", "admin"))
            db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("student", "student123", "student"))
            
        cursor = db.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            # Insert sample books
            books = [
                ("To Kill a Mockingbird", "Harper Lee", 1960, "978-0446310789", "Grand Central Publishing", "Fiction", "A novel about racial inequality"),
                ("1984", "George Orwell", 1949, "978-0451524935", "Signet Classic", "Dystopian", "A dystopian social science fiction novel"),
                ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "978-0743273565", "Scribner", "Fiction", "A novel of the Jazz Age"),
                ("The Hobbit", "J.R.R. Tolkien", 1937, "978-0618260300", "Houghton Mifflin", "Fantasy", "A fantasy novel set in Middle-earth"),
                ("The Catcher in the Rye", "J.D. Salinger", 1951, "978-0316769488", "Little, Brown and Company", "Fiction", "A novel about teenage angst and alienation")
            ]
            for book in books:
                db.execute(
                    "INSERT INTO books (title, author, year, isbn, publisher, category, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    book
                )
        
        db.commit()
