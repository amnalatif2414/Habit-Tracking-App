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

## Running the Program
To start the application, run the following command:
python main.py
This will open a command-line menu where users can register, log in, and interact with their habits.

## Running Tests
To run tests, install unittest if it's not already installed:
pip install unittest
Then, execute the tests with:
unittest

## Features
- **Add habits** with daily or weekly periodicity.
- **Complete habits** for the current date.
- **Track progress** by viewing streaks of consecutive habit completions.
- **Delete a specific habit** or **delete all habits**.
- **View longest streak** of any habit.
- **Filter habits by periodicity** (daily/weekly).
- **Persistent storage** of habits using SQLite.

## Installation

### Prerequisites
- Python 3.7 or later should be installed on your machine.
- SQLite is part of Python's standard library, so no external database setup is required.

