import uuid
from app.minesweeper.minesweeper import Minesweeper


class GameSession:
    def __init__(self, session_id, name, rows, cols):
        self.minesweeper = Minesweeper(rows, cols)
        self.session_id = session_id
        self.name = name 
        
class GameService:
    def __init__(self):
        self._sessions = {}

    def create_session(self, name: str, rows: int, cols: int):
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = GameSession(session_id, name, rows, cols)
        return session_id

    def session_exists(self, session_id):
        return session_id in self._sessions

    def get_session(self, session_id) -> GameSession:
        return self._sessions.get(session_id)


