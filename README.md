# Habit Tracker App

A simple command-line application to track users habits, calculate streaks, and manage your daily goals. This CLI tool allows user to add habits with different periodicities, mark them as completed, and view statistics like the longest streak for each habit.

## Features

- Add new habits with daily, weekly, monthly, or custom periodicity.
- Track your habit completions and calculate streaks.
- View your longest streak across all habits or for specific habits.
- Edit and delete habits.
- View a history of completed habits.

## Installation

### Prerequisites

Make sure that Python is installed on your system (version 3.6 or above).

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/janchrist91/habit-tracker-cli.git
   ```
   
2. Navigate to the project directory:
   ```bash
   cd habit-tracker-cli
   ```

3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
* On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
* On Windows:
  ```bash
  .\venv\Scripts\activate
  ```
  
5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
6. Run the application:
   ```bash
   python main.py menu
   ```
   
## Usage
You can use the main.py file to interact with the Habit Tracker through the command-line interface.

### Commands

1. Add a new habit:
   ```bash
   python main.py add "habit_name" periodicity [--custom_frequency N] [--grace_period N]
   ```
* habit_name: The name of the habit (can be multiple words)
* periodicity: Can be daily, weekly, monthly, or yearly
* --custom_frequency: Optional, number of days for a custom frequency
* --grace_period: Optional, the number of grace days allowed for streak continuation

    #### Example:
    ```bash 
    python main.py add "exercise" daily --grace_period 1
    ```

2. Complete a habit:
    ```bash 
   python main.py complete "habit_name" 
   ```
 
     #### Example:
    ```bash 
    python main.py complete "exercise"
   ```
   
3. List all habits:
    ```bash
    python main.py list-habits
   ```
4. List habits by periodicity:
   ```bash
    python main.py list-by-periodicity periodicity
   ```
   #### Example:
    ```bash
   python main.py list-by-periodicity daily
   ```
5. View the longest streak across all habits:
    ```bash
   python main.py longest-streak
   ```
6. View the longest streak for a specific habit:
   ```bash
   python main.py longest-streak-for-habit "habit_name"
   ```
7. Edit a habit:
   ```bash
   python main.py edit "old_name" "new_name" new_periodicity [--custom_frequency N] [--grace_period N]
   ```
8. Delete a habit:
   ```bash 
   python main.py delete "habit_name"
   ```
9. View a habit’s completion history:
    ```bash
   python main.py view-history "habit_name"
   ```
10. View the available commands:
    ```bash
    python main.py menu
    ```
    
## Running Tests
Unit tests are included to verify the core functionality of the Habit Tracker.

### To run the tests:
```bash
python -m unittest test_habit_tracker.py
```
### The tests will:
* Validate the creation and management of habits
* Ensure streak calculations are accurate
* Verify that the predefined habit data is correctly initialized and tracked

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! If you find bugs or have suggestions, feel free to open an issue or submit a pull request.
