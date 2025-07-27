from app.models.database import get_db


class Book:
    @staticmethod
    def get_all():
        db = get_db()
        books = db.execute(
            'SELECT * FROM books ORDER BY title'
        ).fetchall()
        
        result = []
        for book in books:
            result.append({
                'id': book['id'],
                'title': book['title'],
                'author': book['author'],
                'year': book['year'],
                'isbn': book['isbn'],
                'publisher': book['publisher'],
                'category': book['category'],
                'description': book['description']
            })
            
        return result
        
    @staticmethod
    def get_by_id(book_id):
        db = get_db()
        book = db.execute(
            'SELECT * FROM books WHERE id = ?', (book_id,)
        ).fetchone()
        
        if book is None:
            return None
            
        return {
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'year': book['year'],
            'isbn': book['isbn'],
            'publisher': book['publisher'],
            'category': book['category'],
            'description': book['description']
        }
        
    @staticmethod
    def create(book_data):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO books (title, author, year, isbn, publisher, category, description) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (book_data['title'], book_data['author'], book_data['year'], book_data['isbn'],
             book_data.get('publisher', ''), book_data.get('category', ''), 
             book_data.get('description', ''))
        )
        db.commit()
        return cursor.lastrowid
        
    @staticmethod
    def delete(book_id):
        db = get_db()
        db.execute('DELETE FROM books WHERE id = ?', (book_id,))
        db.commit()
        return True
