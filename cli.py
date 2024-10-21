# Import the Click library for creating command-line interfaces
import click

# Import the HabitTracker class to manage habit data
from models import HabitTracker

# Create an instance of HabitTracker to manage habits in this CLI
tracker = HabitTracker()

# Define the root command group for the CLI
@click.group()
def cli():
    pass  # The main CLI command group that holds all subcommands

# Define the "add" command for adding a new habit
@click.command()
@click.argument('name', nargs=-1)  # Accepts the habit name as an argument
@click.argument('periodicity')  # Accepts the periodicity (e.g., daily, weekly)
@click.option('--custom_frequency', default=None, type=int, help="Custom frequency in days")  # Optional custom frequency
@click.option('--grace_period', default=0, type=int, help="Grace period in days for flexible streaks")  # Optional grace period
def add(name, periodicity, custom_frequency, grace_period):
    # Join name argument to handle multi-word names
    name = ' '.join(name)
    try:
        # Add the habit to the tracker
        tracker.add_habit(name, periodicity, custom_frequency, grace_period)
        click.echo(f'Habit {name} added with {periodicity} periodicity.')  # Output confirmation
    except ValueError as e:
        click.echo(str(e))  # Output error message if the operation fails

# Define the "complete" command for completing a habit
@click.command()
@click.argument('name', nargs=-1)  # Accepts the habit name as an argument
def complete(name):
    # Join name argument to handle multi-word names
    name = ' '.join(name)
    try:
        # Mark the habit as completed in the tracker
        tracker.complete_habit(name)
        click.echo(f'Habit {name} completed.')  # Output confirmation
    except ValueError as e:
        click.echo(str(e))  # Output error message if the habit is not found

# Define the "list-habits" command for listing all habits
@click.command()
def list_habits():
    # Get all habits from the tracker
    habits = tracker.get_all_habits()
    # Output each habit's name and periodicity
    for habit in habits:
        click.echo(f'{habit.name} - {habit.periodicity}')

# Define the "list-by-periodicity" command to filter habits by periodicity
@click.command()
@click.argument('periodicity')  # Accepts the periodicity (e.g., daily, weekly) as an argument
def list_by_periodicity(periodicity):
    # Get habits that match the specified periodicity
    habits = tracker.get_habits_by_periodicity(periodicity)
    # Output each habit's name and periodicity
    for habit in habits:
        click.echo(f'{habit.name} - {habit.periodicity}')

# Define the "longest-streak" command to display the longest streak across all habits
@click.command()
def longest_streak():
    # Get the longest streak from the tracker
    streak = tracker.get_longest_streak()
    # Output the longest streak
    click.echo(f'Longest streak is {streak} periods.')

# Define the "longest-streak-for-habit" command to display the longest streak for a specific habit
@click.command()
@click.argument('name')  # Accepts the habit name as an argument
def longest_streak_for_habit(name):
    # Get the longest streak for the specified habit
    streak = tracker.get_longest_streak_for_habit(name)
    # Output the habit's longest streak
    click.echo(f'Longest streak for {name} is {streak} periods.')

# Define the "edit" command for modifying an existing habit
@click.command()
@click.argument('old_name')  # Old habit name (before edit)
@click.argument('new_name')  # New habit name
@click.argument('new_periodicity')  # New periodicity
@click.option('--custom_frequency', default=None, type=int, help="Custom frequency in days")  # Optional custom frequency
@click.option('--grace_period', default=0, type=int, help="Grace period in days for flexible streaks")  # Optional grace period
def edit(old_name, new_name, new_periodicity, custom_frequency, grace_period):
    # Edit the habit's details in the tracker
    tracker.edit_habit(old_name, new_name, new_periodicity, custom_frequency, grace_period)
    # Output confirmation
    click.echo(f'Habit {old_name} has been updated to {new_name} with {new_periodicity} periodicity.')

# Define the "delete" command for removing a habit
@click.command()
@click.argument('name')  # Accepts the habit name as an argument
def delete(name):
    # Delete the habit from the tracker
    tracker.delete_habit(name)
    # Output confirmation
    click.echo(f'Habit {name} deleted.')

# Define the "view-history" command for viewing a habit's completion history
@click.command()
@click.argument('name')  # Accepts the habit name as an argument
def view_history(name):
    try:
        # Get the habit's completion history
        history = tracker.view_habit_history(name)
        # Output the completion dates
        click.echo(f"History for '{name}':")
        for completion in history:
            click.echo(f"  Completed on {completion}")
    except ValueError as e:
        click.echo(str(e))  # Output error message if the habit is not found

# Define the "menu" command to display available commands
@click.command()
def menu():
    # Display a list of available commands
    click.echo("Available commands:")
    click.echo("  add [name] [periodicity] --custom_frequency [days] --grace_period [days] - Add a new habit")
    click.echo("  complete [name] - Complete a habit")
    click.echo("  list-habits - List of all habits")
    click.echo("  list-by-periodicity [periodicity] - List habits by periodicity")
    click.echo("  longest-streak - Get the longest streak across all habits")
    click.echo("  longest-streak-for-habit [name] - Get the longest streak for a specific habit")
    click.echo("  edit [old_name] [new_name] [new_periodicity] --custom_frequency [days] --grace_period [days] - Edit a habit")
    click.echo("  delete [name] - Delete a habit")
    click.echo("  view-history [name] - View the history of completions for a specific habit")

# Register the defined commands to the main CLI group
cli.add_command(add)
cli.add_command(complete)
cli.add_command(list_habits)
cli.add_command(list_by_periodicity)
cli.add_command(longest_streak)
cli.add_command(longest_streak_for_habit)
cli.add_command(edit)
cli.add_command(delete)
cli.add_command(view_history)
cli.add_command(menu)