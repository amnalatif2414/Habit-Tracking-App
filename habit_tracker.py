
import sqlite3
from datetime import datetime
from habit import Habit
from user import User

class HabitTracker:
    """
    Manages multiple users and their habits. Allows adding, completing, deleting habits,
    and analyzing them (like getting streaks). It uses an SQLite database for persistence.
    """
    def __init__(self):
        """
        Initialize the HabitTracker with a connection to the SQLite database and create tables if they don't exist.
        """
        self.conn = sqlite3.connect('habits.db')
        self.create_tables()
        self.current_user = None  # Holds the User object of the logged-in user

    def create_tables(self):
        """
        Create the database tables for storing users, habits, and completions.
        """
        with self.conn:
            # Create the 'users' table to store user information
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            # Drop the old habits table if it exists to fix the missing user_id column
            self.conn.execute("DROP TABLE IF EXISTS habits")

            # Create the 'habits' table to store habits linked to users
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    periodicity TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            # Create the 'completions' table to store habit completion dates
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completion_date TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits (id)
                )
            """)

    # User Management Methods

    def create_user(self, username, password):
        """
        Create a new user with the given username and password.
        """
        user = User(username, password)
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO users (username, password, created_at)
                    VALUES (?, ?, ?)
                """, (user.username, user.password, user.created_at))
            print(f"User '{username}' created successfully.")
            return True
        except sqlite3.IntegrityError:
            print(f"Username '{username}' is already taken.")
            return False

    def login_user(self, username, password):
        """
        Log in a user by verifying the username and password.
        """
        cursor = self.conn.execute("""
            SELECT id, username, password FROM users WHERE username = ?
        """, (username,))
        result = cursor.fetchone()
        if result and result[2] == password:
            self.current_user = User(result[1], result[2])
            self.current_user.id = result[0]  # Assign the user ID from the database
            print(f"User '{username}' logged in successfully.")
            return True
        else:
            print("Invalid username or password.")
            return False

    def logout_user(self):
        """
        Log out the current user.
        """
        if self.current_user:
            print(f"User '{self.current_user.username}' logged out.")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    # Habit Management Methods

    def add_habit(self, habit):
        """
        Add a new habit to the current user.
        """
        if not self.current_user:
            print("No user is logged in. Please log in first.")
            return

        self.conn.execute("""
            INSERT INTO habits (name, periodicity, created_at, user_id)
            VALUES (?, ?, ?, ?)
        """, (habit.name, habit.periodicity, habit.created_at, self.current_user.id))
        self.conn.commit()
        print(f"Habit '{habit.name}' added successfully for user '{self.current_user.username}'.")

    def get_user_habits(self):
        """
        Retrieve all habits for the current user.
        """
        if not self.current_user:
            print("No user is logged in. Please log in first.")
            return []

        cursor = self.conn.execute("""
            SELECT id, name, periodicity, created_at FROM habits
            WHERE user_id = ?
        """, (self.current_user.id,))
        habits = []
        for row in cursor.fetchall():
            habit = Habit(row[1], row[2], self.current_user.id)
            habit.id = row[0]
            habit.created_at = row[3]
            habits.append(habit)
        return habits

    def complete_habit(self, habit_name):
        """
        Mark a habit as completed for the current user.
        """
        if not self.current_user:
            print("No user is logged in. Please log in first.")
            return

        cursor = self.conn.execute("""
            SELECT id FROM habits WHERE name = ? AND user_id = ?
        """, (habit_name, self.current_user.id))
        result = cursor.fetchone()
        if result:
            habit_id = result[0]
            completion_date = datetime.now().date()
            self.conn.execute("""
                INSERT INTO completions (habit_id, completion_date)
                VALUES (?, ?)
            """, (habit_id, completion_date))
            self.conn.commit()
            print(f"Habit '{habit_name}' marked as completed on {completion_date}.")
        else:
            print(f"Habit '{habit_name}' not found for user '{self.current_user.username}'.")

    def delete_habit(self, habit_name):
        """
        Delete a specific habit for the current user.
        """
        if not self.current_user:
            print("No user is logged in. Please log in first.")
            return

        cursor = self.conn.execute("""
            SELECT id FROM habits WHERE name = ? AND user_id = ?
        """, (habit_name, self.current_user.id))
        result = cursor.fetchone()
        if result:
            habit_id = result[0]
            with self.conn:
                self.conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
                self.conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            print(f"Habit '{habit_name}' has been deleted for user '{self.current_user.username}'.")
        else:
            print(f"Habit '{habit_name}' not found for user '{self.current_user.username}'.")

    def delete_all_habits(self):
        """
        Delete all habits for the current user.
        """
        if not self.current_user:
            print("No user is logged in. Please log in first.")
            return

        with self.conn:
            self.conn.execute("DELETE FROM completions WHERE habit_id IN (SELECT id FROM habits WHERE user_id = ?)", (self.current_user.id,))
            self.conn.execute("DELETE FROM habits WHERE user_id = ?", (self.current_user.id,))
        print(f"All habits have been deleted for user '{self.current_user.username}'.")

    def get_longest_streak(self):
        """
        Return the habit with the longest streak for the current user.
        """
        if not self.current_user:
            print("No user is logged in. Please log in first.")
            return None, 0

        habits = self.get_user_habits()
        longest_streak = 0
        longest_habit = None

        for habit in habits:
            completions = self.conn.execute("""
                SELECT completion_date FROM completions
                WHERE habit_id = ?
                ORDER BY completion_date ASC
            """, (habit.id,)).fetchall()
            habit.completed_dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in completions]
            current_streak = habit.streak()
            if current_streak > longest_streak:
                longest_streak = current_streak
                longest_habit = habit.name

        return longest_habit, longest_streak

    def get_habits_by_periodicity(self, periodicity):
        """
        Return a list of habit names that match the specified periodicity for the current user.
        """
        if not self.current_user:
            print("No user is logged in. Please log in first.")
            return []

        cursor = self.conn.execute("""
            SELECT name FROM habits WHERE periodicity = ? AND user_id = ?
        """, (periodicity, self.current_user.id))
        return [row[0] for row in cursor.fetchall()]
