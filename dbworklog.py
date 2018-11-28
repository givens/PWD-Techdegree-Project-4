"""
views.py
--------
View for Database Worklog
"""

from collections import OrderedDict
import datetime
import os
import pdb
import sys

from utils import *
import models

fmt = '%Y%m%d'


def clear():
    """Clear screen."""
    os.system("clear") # assuming Mac


def item_table(item_list, heading=None):
    """Make an item table."""
    clear()
    print(heading)
    for index, item in enumerate(item_list):
        print('{} - {}'.format(index+1, item))
    choice = input('Which option do you choose?  ')
    try:
        choice = int(choice)
        if choice not in range(1, len(item_list)+1):
            raise ValueError("Invalid choice.")
    except ValueError as err:
        print(err)
        time.sleep(1)
        return item_table(item_list, heading)
    else:
        return item_list[choice-1]


def main_menu():
    """Main menu."""
    main = MainMenu()
    main.menu_loop()


def search_menu():
    """Search menu."""
    search = SearchMenu()
    search.menu_loop()


def result_menu(tasks_id):
    """Result menu."""
    result = ResultMenu(tasks_id)
    result.menu_loop()


    utils enter_task({
        "employee": employee,
        "taskname": taskname,
        "minutes": minutes,
        "notes": notes,
        "date": date,
    })

def enter_task():
    """Add an entry."""

    # Enter a new task from keyboard.
    # Create in db.

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
    print("Enter any notes.  Press ctrl-d when finished.")
    notes = sys.stdin.read().strip()

    # Date
    date = datetime.datetime.now().date()

    return {"employee": employee,
            "taskname": taskname,
            "minutes": minutes,
            "notes": notes,
            "date": date}

def quit():
    """Quit work log."""
    print("Quit.")
    sys.exit(0)


class Menu:

    def __init__(self, menu=None, heading=None):
        self.menu = menu
        self.heading = heading

    def menu_loop(self):
        """Show the menu."""
        choice = None
        while True:
            clear()
            print(self.heading)
            for k, v in self.menu.items():
                print('{} - {}'.format(k, v.__doc__))
            choice = input("Which option do you choose?  ").lower().strip()

            if choice in self.menu:
                #pdb.set_trace()
                self.menu[choice]()


class MainMenu(Menu):

    def __init__(self):
        super().__init__(
            OrderedDict([
                ('a', self.enter_task),
                ('s', self.search_menu),
                ('q', self.quit)]),
            "Main Menu")

    def enter_task(self):
        dict = enter_task()
        create_task(dict)

    def search_menu(self):
        search_menu()

    def quit(self):
        quit()

class SearchMenu(Menu):

    def __init__(self):
        super().__init__(
            OrderedDict([
                ('e', self.find_employee),
                ('d', self.find_date),
                ('r', self.find_date_range),
                ('t', self.find_time_spent),
                ('s', self.find_search_term),
                ('m', main_menu)]),
            "Search Menu")

    def find_employee(self):
        """Find by employee."""
        # List unique employees in order
        # Provide choice
        # User selects choice
        # Choice is searched for
        # Go to ResultMenu
        employees = find_unique_employees()
        employee = item_table(employees)
        tasks_id = find_by_employee(employee)
        result_menu(tasks_id)


    def find_date(self):
        """Find by date."""
        # List unique dates in order
        # Provide choice
        # User selects choice
        # Choice is searched for
        # Go to ResultMenu
        dates = find_unique_dates()
        date = item_table(dates)
        tasks_id = find_by_date(date)
        result_menu(tasks_id)


    def find_date_range(self):
        """Find by date range."""
        # Enter start date
        # Enter end date
        # Date range is searched for
        # Go to ResultMenu

        # Start Date
        while True:
            start_date = input("Enter start date (YYYYMMDD):  ")
            try:
                start_date = datetime.datetime.strptime(start_date, fmt)
            except Exception:
                print("Try again.")
            else:
                break
        # End date
        while True:
            end_date = input("Enter end date (YYYYMMDD):  ")
            try:
                end_date = datetime.datetime.strptime(end_date, fmt)
            except Exception:
                print("Try again.")
            else:
                break
        # Find and show
        tasks_id = find_by_date_range(start_date, end_date)
        result_menu(tasks_id)


    def find_time_spent(self):
        """Find by minutes spent."""
        # Enter minutes
        # Exact minutes is searched for
        # Go to ResultMenu
        minutes = input("Enter minutes:  ")
        try:
            minutes = int(minutes)
        except Exception:
            print("Try again.")
            return self.find_time_spent()
        else:
            tasks_id = find_by_time_spent(minutes)
            result_menu(tasks_id)


    def find_search_term(self):
        """Find by search term."""
        # Enter query
        # Query is searched for in title and notes
        # Go to ResultMenu
        query = input("Enter search term:  ")
        tasks_id = find_by_search_term(query)
        result_menu(tasks_id)


class ResultMenu(Menu):

    def __init__(self, tasks_id):
        pdb.set_trace()
        super().__init__(
            OrderedDict([
                ('n', self.next),
                ('p', self.prev),
                ('e', self.edit),
                ('d', self.delete),
                ('s', search_menu),
                ('m', main_menu)]),
            "Result Menu")
        self.tasks_id = tasks_id
        self.index = 0


    def menu_loop(self):
        """Show the menu."""
        choice = None
        while True:
            clear()
            print(self.heading)
            self.display()
            for k, v in self.menu.items():
                print('{} - {}'.format(k, v.__doc__))
            choice = input("Which option do you choose?  ").lower().strip()

            if choice in self.menu:
                #pdb.set_trace()
                self.menu[choice]()


    def __len__(self):
        return len(self.tasks_id)


    def display(self):
        """Display a result including
        employee, task, minutes, notes, and date."""
        task = get_task(self.tasks_id[self.index])
        print("\nEmployee:  " + task.employee)
        print("Taskname:  " + task.taskname)
        print("Minutes:   " + str(task.minutes))
        print("Notes:     " + task.notes)
        print("Date:      " + task.date.strftime(fmt) + "\n")


    def next(self):
        """Go to next task."""
        self.index += 1
        if self.index>=len(self):
            self.index = 0


    def prev(self):
        """Go to previous task."""
        self.index -= 1
        if self.index<=0:
            self.index = len(self) - 1


    def edit(self):
        """Edit current task."""
        old_task_id = self.tasks_id[self.index]
        new_task = enter_task()
        save_task(old_task_id, new_task)


    def delete(self):
        """Delete current task."""
        delete_task(self.tasks_id[self.index])
        del self.tasks_id[self.index]
        # if deleting last one, loop around
        # otherwise, maintain index
        if self.index>=len(self):
            self.index = 0


if __name__ == '__main__':

    models.initialize()
    main_menu = MainMenu()
    main_menu.menu_loop()