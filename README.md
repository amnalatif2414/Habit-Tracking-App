# Habit Tracking App

## Description
The Habit Tracking App is a Python-based command-line tool designed to help users track their daily and weekly habits. It allows users to create habits, mark them as complete, and analyze their progress by tracking streaks. The app also provides options to delete individual habits or remove all habits at once. It uses an SQLite database to store habit data, ensuring persistence across sessions.

## Dependencies
The Habit Tracker requires the following dependencies:
- Python 3.8.8 or a compatible version 
- SQLite3 module (part of Python standard library)

## Installation and Setup
To set up and run the Habit Tracker application, follow these steps:
- Ensure that you have Python 3.8.8 or a compatible version installed on your system.
- Download the necessary files: habit_tracker.py, habit.py, main.py.
- (Optional) Download habit.db to use predefined habits with four weeks of sample data.
- Open a terminal or command prompt and navigate to the directory where the files are located.

## Usage
To start the application, run the following command:
- [main.py](main.py)
This will open a command-line menu where users can register, log in, and interact with their habits.

## Running Tests
To run tests, install unittest if it's not already installed:
pip install pytest
Then, execute the tests with:
unittest

## Features
 **User Accounts** – Users can create an account, log in, and log out.
 **Predefined Habits** – Some common habits (like Exercise, Read, and Walk) are available to select.
 **Custom Habits** – Users can create their habits with a chosen name and frequency (daily or weekly).
 **Mark Habit as Complete** – Users can mark a habit as done for the day or week.
 **Delete Habit** – Users can remove a specific habit or all habits at once.
 **View Habits** – Users can see all their habits and check which ones need to be completed.
 **Filter Habits by Frequency** – Users can filter habits based on daily or weekly tracking.
 **Track Progress** – The app records when habits are completed.
 **View Analytics** – Users can check stats like longest streak, most completed habit, and progress graphs.





