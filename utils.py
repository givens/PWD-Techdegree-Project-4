"""
utils.py
--------------
Utility methods for the Database Work Log
"""

import datetime
import os
import time

import models

fmt = '%Y%m%d'


def create_task(new_task):
    """Create/add a new task."""
    try:
        models.Task.create(**new_task)
    except IntegrityError:
        # Don't add duplicates
        pass


def save_task(old_id, new_task):
    """Save in place a new task, or edit it."""
    task = models.Task.get(id=old_id)
    task.employee = new_task['employee']
    task.taskname = new_task['taskname']
    task.minutes = new_task['minutes']
    task.notes = new_task['notes']
    #task.date = new_task['date']  # don't update date
    task.save()


def delete_task(old_id):
    """Delete a task."""
    old_task = models.Task.get(id=old_id)
    old_task.delete_instance()


def find_by_date_range(start_date, end_date):
    """Find ids for tasks with dates in between start and end date."""
    extended_end_date = end_date + \
        datetime.timedelta(seconds=1)  # add one second to be inclusive
    return [task.id for task in models.Task.select(models.Task.id).where(
        models.Task.date.between(
            start_date, extended_end_date)).order_by(models.Task.date)]


def find_by_time_spent(minutes):
    """Find ids for tasks with exact minutes."""
    return [task.id for task in
            models.Task.select(models.Task.id).where(
                models.Task.minutes == minutes).order_by(models.Task.id)]


def find_by_search_term(query):
    """Find ids for tasks where query wildcard in taskname or notes."""
    return [task.id for task in
            models.Task.select(models.Task.id).where(
                models.Task.taskname.contains(query) |
                models.Task.notes.contains(query)).order_by(models.Task.id)]


def find_by_employee(query):
    """Find ids for tasks where query exactly matches query."""
    return [task.id for task in
            models.Task.select(models.Task.id).where(
                models.Task.employee == query)]


def find_unique_employees():
    """Find unique employees in db."""
    return [task.employee for task in
            models.Task.select(models.Task.employee).distinct().order_by(
                models.Task.employee)]


def find_unique_dates():
    """Find unique dates in db."""
    return [task.date.strftime(fmt) for task in
            models.Task.select(models.Task.date).distinct().order_by(
                models.Task.date)]


def find_by_date(date):
    """Find ids for tasks with exact date in query."""
    return [task.id for task in models.Task.select(models.Task.id).where(
        models.Task.date == date).order_by(models.Task.id)]

def test_empty_database():
    return len(models.Task.select()) == 0


def get_task(ind):
    """Get task by id"""
    return models.Task.get(id=ind)

def clear():
    """Clear screen."""
    os.system("cls" if os.name == "nt" else "clear")


def item_table(item_list, heading=None):
    """Make an item table."""
    clear()
    print(heading)
    for index, item in enumerate(item_list):
        print('{} - {}'.format(index + 1, item))
    choice = input('Which option do you choose?  ')
    try:
        choice = int(choice)
        if choice not in range(1, len(item_list) + 1):
            raise ValueError("Invalid choice.")
    except ValueError as err:
        print(err)
        time.sleep(1)
        return item_table(item_list, heading)
    else:
        return item_list[choice - 1]


def enter_task():
    """Add an entry."""
    clear()
    # Employee
    while True:
        employee = input("Employee name:  ")
        if employee is not None:
            break
        else:
            print("Try again.")
    # Taskname
    while True:
        taskname = input("Task name:  ")
        if taskname is not None:
            break
        else:
            print("Try again.")
    # Minutes
    while True:
        minutes = input("Minutes spent:  ")
        try:
            minutes = int(minutes)
        except Exception:
            print("Try again.")
        else:
            break
    # Notes
    notes = input("Any notes:  ")
    if not notes:
        notes = "none"

    # Date
    date = datetime.datetime.now().date()
    return {"employee": employee,
            "taskname": taskname,
            "minutes": minutes,
            "notes": notes,
            "date": date}


if __name__ == '__main__':
    pass
