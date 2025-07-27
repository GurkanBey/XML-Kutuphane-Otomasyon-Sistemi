from app.models.database import get_db


class User:
    @staticmethod
    def find_by_username(username):
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            return None
            
        return {
            'id': user['id'],
            'username': user['username'],
            'password': user['password'],
            'role': user['role']
        }
        
    @staticmethod
    def authenticate(username, password):
        user = User.find_by_username(username)
        
        if user is None or user['password'] != password:
            return None
            
        return user
