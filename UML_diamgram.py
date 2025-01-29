"""
+-------------------+          +---------------------+
|      Habit        |<-------->|    HabitTracker      |
+-------------------+          +---------------------+
| - name            |          | - habits (list)      |
| - periodicity     |          | - conn (sqlite3)     |
| - created_at      |          +---------------------+
| - completed_dates |          | + create_tables()    |
+-------------------+          | + add_habit()        |
| + complete_habit()|          | + complete_habit()   |
| + streak()        |          | + delete_habit()     |
+-------------------+          | + delete_all_habits()|
                               | + get_longest_streak()|
                               | + get_habits_by_periodicity()|
                               +---------------------+

"""