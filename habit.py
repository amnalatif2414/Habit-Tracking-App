import sqlite3
from datetime import datetime

class Habit:
    """
    Represents a habit, which can be completed daily or weekly.
    It stores the name, periodicity, creation date, and a list of completion dates.
    """
    def __init__(self, name, periodicity, user_id):
        """
        Initialize a new habit with a name, periodicity (daily/weekly),
        creation date, and the associated user_id.
        """
        self.name = name
        self.periodicity = periodicity
        self.created_at = datetime.now()
        self.user_id = user_id
        self.completed_dates = []

    def complete_habit(self):
        """
        Mark the habit as completed for the current date.
        Adds the current date to the completed_dates list.
        """
        completion_date = datetime.now().date()
        self.completed_dates.append(completion_date)

    def streak(self):
        """
        Calculate the current streak of consecutive completions based on the habit's periodicity (daily/weekly).
        Returns the streak length (number of consecutive days or weeks).
        """
        if not self.completed_dates:
            return 0

        self.completed_dates.sort()
        streak = 1

        for i in range(1, len(self.completed_dates)):
            delta = (self.completed_dates[i] - self.completed_dates[i - 1]).days

            if self.periodicity == 'daily' and delta == 1:
                streak += 1
            elif self.periodicity == 'weekly' and delta == 7:
                streak += 1
            else:
                break  # Streak is broken
        return streak
