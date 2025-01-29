import unittest
import sqlite3
from datetime import datetime, timedelta
from habit import Habit
from habit_tracker import HabitTracker
from user import User


class TestHabitTracker(unittest.TestCase):
    def setUp(self):
        """Initialize a test database and tracker instance before each test"""
        self.tracker = HabitTracker()
        self.tracker.conn = sqlite3.connect(':memory:')  # Use in-memory DB for testing
        self.tracker.create_tables()
        self.user = User("testuser", "password")
        self.tracker.create_user(self.user.username, self.user.password)
        self.tracker.login_user(self.user.username, self.user.password)

    def tearDown(self):
        """Close the database connection after each test"""
        self.tracker.conn.close()

    def test_create_habit(self):
        """Test creating a new habit"""
        habit = Habit("Exercise", "daily", self.tracker.current_user.id)
        self.tracker.add_habit(habit)
        habits = self.tracker.get_user_habits()
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].name, "Exercise")

    def test_complete_habit(self):
        """Test marking a habit as completed"""
        habit = Habit("Read", "daily", self.tracker.current_user.id)
        self.tracker.add_habit(habit)
        self.tracker.complete_habit("Read")
        cursor = self.tracker.conn.execute("SELECT COUNT(*) FROM completions")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_streak_calculation(self):
        """Test streak calculation for daily habits"""
        habit = Habit("Meditate", "daily", self.tracker.current_user.id)
        self.tracker.add_habit(habit)
        habit_id = self.tracker.conn.execute("SELECT id FROM habits WHERE name = ?", (habit.name,)).fetchone()[0]

        completion_dates = [(datetime.now() - timedelta(days=i)).date() for i in range(5)]
        for date in completion_dates:
            self.tracker.conn.execute("""
                INSERT INTO completions (habit_id, completion_date)
                VALUES (?, ?)
            """, (habit_id, date))
        self.tracker.conn.commit()

        # Fetch completions from DB and update habit's completed_dates
        completions = self.tracker.conn.execute("""
            SELECT completion_date FROM completions WHERE habit_id = ? ORDER BY completion_date ASC
        """, (habit_id,)).fetchall()
        habit.completed_dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in completions]

        self.assertEqual(habit.streak(), 5)

    def test_get_longest_streak(self):
        """Test retrieving the longest streak"""
        habit1 = Habit("Walk", "daily", self.tracker.current_user.id)
        habit2 = Habit("Exercise", "daily", self.tracker.current_user.id)
        self.tracker.add_habit(habit1)
        self.tracker.add_habit(habit2)

        for i in range(3):
            date = (datetime.now() - timedelta(days=i)).date()
            self.tracker.conn.execute("""
                INSERT INTO completions (habit_id, completion_date)
                VALUES ((SELECT id FROM habits WHERE name = 'Walk'), ?)
            """, (date,))
        for i in range(5):
            date = (datetime.now() - timedelta(days=i)).date()
            self.tracker.conn.execute("""
                INSERT INTO completions (habit_id, completion_date)
                VALUES ((SELECT id FROM habits WHERE name = 'Exercise'), ?)
            """, (date,))
        self.tracker.conn.commit()
        longest_habit, longest_streak = self.tracker.get_longest_streak()
        self.assertEqual(longest_habit, "Exercise")
        self.assertEqual(longest_streak, 5)

    def test_get_habits_by_periodicity(self):
        """Test filtering habits by periodicity"""
        daily_habit = Habit("Run", "daily", self.tracker.current_user.id)
        weekly_habit = Habit("Swim", "weekly", self.tracker.current_user.id)
        self.tracker.add_habit(daily_habit)
        self.tracker.add_habit(weekly_habit)
        daily_habits = self.tracker.get_habits_by_periodicity("daily")
        self.assertIn("Run", daily_habits)
        self.assertNotIn("Swim", daily_habits)


if __name__ == "__main__":
    unittest.main()
