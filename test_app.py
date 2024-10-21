import unittest
import os  # To handle file operations like deletion
from datetime import datetime, timedelta
from models import Habit, HabitTracker


class TestHabit(unittest.TestCase):

    def setUp(self):
        # Create a habit object before each test
        self.habit = Habit(name="exercise", periodicity="daily")

    def test_habit_creation(self):
        # Test that a habit is created with the correct attributes
        self.assertEqual(self.habit.name, "exercise")
        self.assertEqual(self.habit.periodicity, "daily")
        self.assertEqual(self.habit.completions, [])

    def test_complete_task(self):
        # Test that completing a task adds the current date to completions
        self.habit.complete_task()
        self.assertEqual(len(self.habit.completions), 1)
        self.assertAlmostEqual(self.habit.completions[0], datetime.now(), delta=timedelta(seconds=1))

    def test_streak(self):
        # Test streak calculation for daily habits
        # Simulate completing the habit for 3 consecutive days
        for i in range(3):
            self.habit.completions.append(datetime.now() - timedelta(days=i))
        self.assertEqual(self.habit.streak(), 3)

    def test_streak_with_grace_period(self):
        # Test streak calculation with a grace period
        self.habit.grace_period = 1  # Allow one extra day for flexibility
        # Simulate completing the habit with a gap of 1 day
        self.habit.completions.append(datetime.now() - timedelta(days=1))
        self.habit.completions.append(datetime.now() - timedelta(days=3))
        self.assertEqual(self.habit.streak(), 2)


class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        # Create a HabitTracker object before each test
        self.test_data_file = "test_habits.json"  # Define the test file
        self.tracker = HabitTracker(data_file=self.test_data_file)  # Use a test file to avoid overwriting real data
        self.tracker.habits = []  # Start with an empty habit list

    def tearDown(self):
        # Clean up by deleting the test JSON file after each test
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)  # Delete the test file if it exists

    def test_add_habit(self):
        # Test adding a habit to the tracker
        self.tracker.add_habit(name="meditation", periodicity="daily")
        self.assertEqual(len(self.tracker.habits), 1)
        self.assertEqual(self.tracker.habits[0].name, "meditation")

    def test_complete_habit(self):
        # Test completing a habit
        self.tracker.add_habit(name="meditation", periodicity="daily")
        self.tracker.complete_habit(name="meditation")
        self.assertEqual(len(self.tracker.habits[0].completions), 1)

    def test_get_habit(self):
        # Test retrieving a habit by name
        self.tracker.add_habit(name="meditation", periodicity="daily")
        habit = self.tracker.get_habit(name="meditation")
        self.assertIsNotNone(habit)
        self.assertEqual(habit.name, "meditation")

    def test_get_longest_streak(self):
        # Test the longest streak calculation for a habit
        # Add a habit and simulate 4 days of completion
        self.tracker.add_habit(name="meditation", periodicity="daily")
        for i in range(4):
            self.tracker.habits[0].completions.append(datetime.now() - timedelta(days=i))
        self.assertEqual(self.tracker.get_longest_streak(), 4)

    def test_initialize_predefined_habits(self):
        # Test loading predefined habits and checking their streaks
        self.tracker.initialize_predefined_habits()  # Load predefined habits

        # Check the number of predefined habits
        self.assertEqual(len(self.tracker.habits), 5)

        # Test streak of a daily habit (should be 28 days)
        daily_habit = self.tracker.get_habit("read a book")
        self.assertEqual(daily_habit.streak(), 28)

        # Test streak of a weekly habit (should be 4 weeks)
        weekly_habit = self.tracker.get_habit("run 5km")
        self.assertEqual(weekly_habit.streak(), 4)


if __name__ == '__main__':
    unittest.main()

