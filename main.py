from habit_tracker import HabitTracker
from habit import Habit
from datetime import datetime, timedelta  # Fix added here

def preload_habits_with_data(tracker):
    """
    Preload predefined habits with example tracking data for 4 weeks.
    This can be used for testing purposes or to initialize the app with sample data.
    """
    predefined_habits = [
        {"name": "Exercise", "periodicity": "daily"},
        {"name": "Meditate", "periodicity": "daily"},
        {"name": "Read", "periodicity": "daily"},
        {"name": "Walk", "periodicity": "daily"},
        {"name": "Drink Water", "periodicity": "daily"}
    ]

    user_id = tracker.current_user.id if tracker.current_user else None
    if not user_id:
        print("No user is logged in. Please log in first.")
        return

    for habit_data in predefined_habits:
        habit = Habit(habit_data["name"], habit_data["periodicity"], user_id)
        tracker.add_habit(habit)

        # Add example completion data for the past 4 weeks
        if habit_data["periodicity"] == "daily":
            completion_dates = [
                (datetime.now() - timedelta(days=i)).date()
                for i in range(28)  # Consecutive daily completions for 4 weeks
            ]
        elif habit_data["periodicity"] == "weekly":
            completion_dates = [
                (datetime.now() - timedelta(weeks=i)).date()
                for i in range(4)  # Weekly completions for 4 weeks
            ]

        print(f"Preloading data for habit: {habit_data['name']}")  # Debugging line
        for completion_date in completion_dates:
            print(f"- Adding completion date: {completion_date}")  # Debugging line
            tracker.conn.execute("""
                INSERT INTO completions (habit_id, completion_date)
                VALUES ((SELECT id FROM habits WHERE name = ? AND user_id = ?), ?)
            """, (habit.name, user_id, completion_date))
        tracker.conn.commit()


def main():
    """
    Command-line interface to interact with the HabitTracker app.
    Allows users to create accounts, log in, add, complete, delete, analyze, and manage habits.
    """
    tracker = HabitTracker()

    predefined_habits = ["Exercise", "Meditate", "Read", "Walk", "Drink Water"]

    while True:
        if tracker.current_user:
            print(f"\nLogged in as: {tracker.current_user.username}")
            print("\nMenu:")
            print("1. Add a habit")
            print("2. Mark habit as complete")
            print("3. Delete a specific habit")
            print("4. Delete all habits")
            print("5. Analyze habits")
            print("6. Preload predefined habits with data")
            print("7. Logout")
            print("8. Exit")
        else:
            print("\nMenu:")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

        choice = input("Choose an option: ")

        if not tracker.current_user:
            if choice == '1':
                # Register a new user
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                tracker.create_user(username, password)

            elif choice == '2':
                # Login an existing user
                username = input("Enter username: ")
                password = input("Enter password: ")
                tracker.login_user(username, password)

            elif choice == '3':
                # Exit the application
                print("Exiting the Habit Tracking App. Goodbye!")
                break

            else:
                print("Invalid choice, try again.")

        else:
            if choice == '1':
                # Add a new habit
                print("\nWould you like to:")
                print("1. Select a predefined habit")
                print("2. Enter a custom habit name")
                sub_choice = input("Choose an option: ")

                if sub_choice == '1':
                    print("\nPredefined Habits:")
                    for i, habit_name in enumerate(predefined_habits, start=1):
                        print(f"{i}. {habit_name}")
                    habit_index = input("Select a habit by number: ")
                    if habit_index.isdigit() and 1 <= int(habit_index) <= len(predefined_habits):
                        name = predefined_habits[int(habit_index) - 1]
                    else:
                        print("Invalid selection. Returning to main menu.")
                        continue
                elif sub_choice == '2':
                    name = input("Enter habit name: ")
                else:
                    print("Invalid choice. Returning to main menu.")
                    continue

                periodicity = input("Enter periodicity (daily/weekly): ").lower()
                if periodicity not in ['daily', 'weekly']:
                    print("Invalid periodicity. Please enter 'daily' or 'weekly'.")
                    continue

                habit = Habit(name, periodicity, tracker.current_user.id)
                tracker.add_habit(habit)

            elif choice == '2':
                # Complete a habit
                name = input("Enter habit name to complete: ")
                tracker.complete_habit(name)

            elif choice == '3':
                # Delete a specific habit
                name = input("Enter habit name to delete: ")
                tracker.delete_habit(name)

            elif choice == '4':
                # Delete all habits
                confirmation = input("Are you sure you want to delete all habits? (yes/no): ")
                if confirmation.lower() == 'yes':
                    tracker.delete_all_habits()

            elif choice == '5':
                # Analyze habits
                print("\nAnalyze Habits Menu:")
                print("1. List all currently tracked habits")
                print("2. List habits with specified periodicity")
                print("3. Longest streak of all habits")
                print("4. Longest streak for a specific habit")
                print("5. Return to main menu")

                analyze_choice = input("Choose an analysis option: ")

                if analyze_choice == '1':
                    habits = tracker.get_user_habits()
                    if habits:
                        print("Currently tracked habits:")
                        for habit in habits:
                            print(f"- {habit.name} ({habit.periodicity})")
                    else:
                        print("No habits found.")

                elif analyze_choice == '2':
                    periodicity = input("Enter periodicity to filter (daily/weekly): ").lower()
                    if periodicity not in ['daily', 'weekly']:
                        print("Invalid periodicity. Please enter 'daily' or 'weekly'.")
                        continue
                    habits = tracker.get_habits_by_periodicity(periodicity)
                    if habits:
                        print(f"Habits with periodicity '{periodicity}': {', '.join(habits)}")
                    else:
                        print(f"No habits found with periodicity '{periodicity}'.")

                elif analyze_choice == '3':
                    habit, streak = tracker.get_longest_streak()
                    if habit:
                        print(f"Longest streak: '{habit}' with {streak} consecutive completions.")
                    else:
                        print("No habits found to calculate streaks.")

                elif analyze_choice == '4':
                    name = input("Enter habit name to check longest streak: ")
                    habits = tracker.get_user_habits()
                    habit_found = next((h for h in habits if h.name == name), None)
                    if habit_found:
                        completions = tracker.conn.execute("""
                            SELECT completion_date FROM completions
                            WHERE habit_id = ?
                            ORDER BY completion_date ASC
                        """, (habit_found.id,)).fetchall()
                        habit_found.completed_dates = [
                            datetime.strptime(row[0], "%Y-%m-%d").date() for row in completions
                        ]
                        print(f"Loaded completion dates: {habit_found.completed_dates}")  # Debugging line
                        streak = habit_found.streak()
                        print(f"Longest streak for '{name}': {streak} consecutive completions.")
                    else:
                        print(f"Habit '{name}' not found.")

                elif analyze_choice == '5':
                    continue

                else:
                    print("Invalid choice, returning to main menu.")

            elif choice == '6':
                # Preload predefined habits with data
                preload_habits_with_data(tracker)

            elif choice == '7':
                # Logout the current user
                tracker.logout_user()

            elif choice == '8':
                # Exit the application
                print("Exiting the Habit Tracking App. Goodbye!")
                break

            else:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
