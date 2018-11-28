"""
utils.py
--------------
Utility methods for the Database Work Log
"""

import datetime

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
    #task.date = new_task['date']
    task.save()


def delete_task(old_id):
    """Delete a task."""
    old_task = models.Task.get(id=old_id)
    old_task.delete_instance()


def find_by_date_range(start_date, end_date):
    """Find ids for tasks with dates in between start and end date."""
    extended_end_date = end_date + datetime.timedelta(days=1)  # add one day to be inclusive
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


def get_task(ind):
    return models.Task.get(id=ind)


if __name__ == '__main__':

    a = {'employee': 'a',
         'taskname': 'task a',
         'minutes': 15,
         'notes': 'abcdef',
         'date':  datetime.datetime.now().date()}
    b = {'employee': 'b',
         'taskname': 'task b',
         'minutes': 20,
         'notes': 'abcdef',
         'date':  datetime.datetime.now().date()}
    c = {'employee': 'c',
         'taskname': 'task c',
         'minutes': 15,
         'notes': 'zyxwvu',
         'date':  datetime.datetime.now().date()}
    d = {'employee': 'a',
         'taskname': 'task d',
         'minutes': 20,
         'notes': 'abcdef',
         'date':  datetime.datetime.now().date()}

    models.Task.create(**a)
    models.Task.create(**b)
    models.Task.create(**c)
    models.Task.create(**d)

    tasks_id = find_by_employee('b')

    for task_id in tasks_id:
        task = models.Task.get(id=task_id)
        print(task.id)
        print(task.employee)
        print(task.taskname)
