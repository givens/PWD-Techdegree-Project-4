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
    models.Task.create(**new_task)


def save_task(old_id, new_task):
    """Save in place a new task, or edit it."""
    task = models.Task.get(id=old_id)
    task.employee = new_task['employee']
    task.taskname = new_task['taskname']
    task.minutes = new_task['minutes']
    task.notes = new_task['notes']
    task.date = new_task['date']  # don't update date
    task.save()
    return 0


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
    """If database is empty, return True."""
    return len(models.Task.select()) == 0


def get_task(ind):
    """Get task by id"""
    return models.Task.get(id=ind)

def clear():
    """Clear screen."""
    os.system("cls" if os.name == "nt" else "clear")


def item_table_list(item_list):
    """List choices."""
    for index, item in enumerate(item_list):
        print('{} - {}'.format(index + 1, item))


def item_table_evaluation(item_list):
    """Evaluate if choice is good.  If so, return that option."""
    while True:
        choice = input("Which option do you choose?  ")
        try:
            choice = int(choice)
            if choice not in range(1, len(item_list) + 1):
                raise ValueError("Try again.")
        except ValueError as err:
            print(err)
            time.sleep(1)
            continue
        else:
            return item_list[choice - 1]


def item_table(item_list, heading=None):
    """Make an item table."""
    clear()
    if heading:
        print(heading)
    item_table_list(item_list)
    return item_table_evaluation(item_list)


def enter_item(question="Enter item:  ", item=None):
    """Generic string entry."""
    while True:
        if not item:
            item = input(question)
        if item == None:
            print("Try again.")
            continue
        return item


def enter_employee(employee=None):
    """Employee entry"""
    if employee:
        print(employee)
    return enter_item("Enter employee name:  ",
                        employee)


def enter_taskname(taskname=None):
    """Task name entry."""
    if taskname:
        print(taskname)
    return enter_item("Enter task name:  ",
                        taskname)


def enter_minutes(minutes=None):
    """Time spent in minutes entry."""
    if minutes:
        print(minutes)
    while True:
        if not minutes:
            minutes = input("Enter time spent in minutes:  ")
        try:
            minutes = int(minutes)
        except Exception:
            print("Try again.")
            continue
        return minutes


def enter_notes(notes=None):
    """Enter notes string."""
    if notes:
        print(notes)
    else:
        notes = input("Enter notes:  ")
    return notes


def enter_task(employee=None,
                taskname=None,
                minutes=None,
                notes=None,
                date=None):
    """Add an entry."""
    clear()
    if not employee:
        employee = enter_employee(employee)
    if not taskname:
        taskname = enter_taskname(taskname)
    if not minutes:
        minutes = enter_minutes(minutes)
    if not date:
        notes = enter_notes(notes)
    if not date:
        date = datetime.datetime.now().date()
    return {"employee": employee,
            "taskname": taskname,
            "minutes": minutes,
            "notes": notes,
            "date": date}

