
from datetime import datetime

class User:
    """
    Represents a user in the Habit Tracking App.
    """
    def __init__(self, username, password):
        """
        Initialize a new user with a username, password, and creation date.
        """
        self.username = username
        self.password = password  # In production, passwords should be hashed!
        self.created_at = datetime.now()

