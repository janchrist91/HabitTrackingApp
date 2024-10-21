import json
from datetime import datetime, timedelta

# Class representing a single habit
class Habit:
    def __init__(self, name, periodicity, custom_frequency=None, grace_period=0):
        # Initialize the habit with name, periodicity (e.g., daily/weekly), custom frequency (optional), and grace
        # period
        self.name = name
        self.periodicity = periodicity
        self.custom_frequency = custom_frequency  # If periodicity is custom, this sets how many days per completion
        self.grace_period = grace_period  # Grace period in days for flexibility in streak calculation
        self.creation_date = datetime.now()  # Timestamp for when the habit was created
        self.completions = []  # List to store timestamps of habit completions

    # Method to mark the habit as completed (logs current datetime)
    def complete_task(self):
        self.completions.append(datetime.now())

    # Method to get the most recent completion timestamp
    def last_completion(self):
        return self.completions[-1] if self.completions else None

    # Method to calculate the current streak of completed tasks
    def streak(self):
        streak, current_streak = 0, 0
        now = datetime.now()
        period_delta = self.get_period_delta()  # Get the period delta based on periodicity

        # Grace period to allow some flexibility in streak calculation
        grace_delta = timedelta(days=self.grace_period)

        # Loop through completed timestamps in reverse order to calculate streak
        for completion in reversed(self.completions):
            if now - completion <= (period_delta + grace_delta):  # Check if completion falls within the period + grace
                current_streak += 1  # Continue the streak
                now = completion  # Move the time marker back to the completion time
            else:
                streak = max(streak, current_streak)  # Store the max streak
                current_streak = 1  # Start a new streak
                now = completion  # Reset the marker
        return max(streak, current_streak)  # Return the maximum streak

    # Method to get the appropriate time delta based on the habit's periodicity
    def get_period_delta(self):
        if self.periodicity == 'daily':
            return timedelta(days=1)
        elif self.periodicity == 'weekly':
            return timedelta(weeks=1)
        elif self.periodicity == 'monthly':
            return timedelta(days=30)
        elif self.custom_frequency:
            return timedelta(days=self.custom_frequency)  # Custom number of days
        return timedelta(days=365)  # Default to yearly if not specified

# Class to manage a collection of habits
class HabitTracker:
    def __init__(self, data_file='habits.json'):
        self.habits = []  # List to store all the user's habits
        self.data_file = data_file  # File path for saving/loading habits
        self.load_habits()  # Load any existing habits from the file on initialization

    # Method to add a new habit to the tracker
    def add_habit(self, name, periodicity, custom_frequency=None, grace_period=0):
        # Ensure periodicity is valid
        if periodicity not in ['daily', 'weekly', 'monthly', 'yearly'] and custom_frequency is None:
            raise ValueError("Invalid periodicity. Choose 'daily', 'weekly', 'monthly', 'yearly' or provide a custom "
                             "frequency in days.")
        # Add the habit to the list
        self.habits.append(Habit(name, periodicity, custom_frequency, grace_period))
        self.save_habits()  # Save the habits to file

    # Retrieve a specific habit by name
    def get_habit(self, name):
        return next((habit for habit in self.habits if habit.name == name), None)

    # Mark a habit as completed by name
    def complete_habit(self, name):
        habit = self.get_habit(name)
        if habit:
            habit.complete_task()  # Log completion
            self.save_habits()  # Save updated habit list
        else:
            raise ValueError(f"Habit '{name}' not found.")

    # Retrieve all habits
    def get_all_habits(self):
        return self.habits

    # Retrieve habits filtered by periodicity (e.g., daily, weekly)
    def get_habits_by_periodicity(self, periodicity):
        return [habit for habit in self.habits if habit.periodicity == periodicity]

    # Get the longest streak across all habits
    def get_longest_streak(self):
        return max((habit.streak() for habit in self.habits), default=0)

    # Get the longest streak for a specific habit by name
    def get_longest_streak_for_habit(self, name):
        habit = self.get_habit(name)
        return habit.streak() if habit else 0

    # Edit an existing habit's details
    def edit_habit(self, old_name, new_name, new_periodicity, custom_frequency=None, grace_period=0):
        if new_periodicity not in ['daily', 'weekly', 'monthly', 'yearly'] and custom_frequency is None:
            raise ValueError("Invalid periodicity.")
        habit = self.get_habit(old_name)
        if habit:
            habit.name = new_name  # Update habit name
            habit.periodicity = new_periodicity  # Update periodicity
            habit.custom_frequency = custom_frequency  # Update custom frequency
            habit.grace_period = grace_period  # Update grace period
            self.save_habits()  # Save changes

    # Delete a habit by name
    def delete_habit(self, name):
        self.habits = [habit for habit in self.habits if habit.name != name]  # Remove habit from list
        self.save_habits()  # Save updated list

    # View the history of completions for a specific habit
    def view_habit_history(self, name):
        habit = self.get_habit(name)
        if habit:
            return habit.completions  # Return the list of completion timestamps
        else:
            raise ValueError(f"Habit '{name}' not found.")

    # Save the list of habits to a file
    def save_habits(self):
        data = [{'name': habit.name, 'periodicity': habit.periodicity, 'custom_frequency': habit.custom_frequency,
                 'grace_period': habit.grace_period, 'creation_date': habit.creation_date.isoformat(),
                 'completions': [c.isoformat() for c in habit.completions]} for habit in self.habits]
        with open(self.data_file, 'w') as f:
            json.dump(data, f)  # Serialize and save as JSON

    # Load habits from a file (if it exists)
    def load_habits(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                for habit_data in data:
                    habit = Habit(habit_data['name'], habit_data['periodicity'],
                                  custom_frequency=habit_data.get('custom_frequency'),
                                  grace_period=habit_data.get('grace_period', 0))
                    habit.creation_date = datetime.fromisoformat(habit_data['creation_date'])
                    habit.completions = [datetime.fromisoformat(c) for c in habit_data['completions']]
                    self.habits.append(habit)  # Add loaded habit to the list
        except FileNotFoundError:
            self.initialize_predefined_habits()  # If no file exists, initialize predefined habits

    # Initialize a few predefined habits for testing purposes
    def initialize_predefined_habits(self):
        predefined_habits = [
            ('run 5km', 'weekly'),
            ('read a book', 'daily'),
            ('meditation', 'daily'),
            ('eat breakfast', 'daily'),
            ('wake up early', 'daily')
        ]

        now = datetime.now()

        # Generate past completion data for predefined habits
        for name, periodicity in predefined_habits:
            habit = Habit(name, periodicity)

            if periodicity == 'daily':
                for i in range(28):  # 28 days of data
                    habit.completions.append(now - timedelta(days=i))

            elif periodicity == 'weekly':
                for i in range(4):  # 4 weeks of data
                    habit.completions.append(now - timedelta(weeks=i))

            self.habits.append(habit)

        self.save_habits()  # Save predefined habits
