"""
views.py
--------
View for Database Worklog
"""

from collections import OrderedDict
import datetime
import os
import sys
import time

import utils
import models
from utils import fmt


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


def result_menu(ids):
    """Result menu."""
    result = ResultMenu(ids)
    result.menu_loop()


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
                self.menu[choice]()


class MainMenu(Menu):

    def __init__(self):
        super().__init__(
            OrderedDict([
                ('a', self.enter_task),
                ('s', self.search_menu),
                ('q', self.quit)]),
            "Main Menu")

    @staticmethod
    def enter_task():
        """Add an entry."""
        dict = enter_task()
        utils.create_task(dict)

    @staticmethod
    def search_menu():
        """Search entries."""
        search = SearchMenu()
        search.menu_loop()
#        search_menu()

    @staticmethod
    def quit():
        """Quit."""
        print("Quit.")
        sys.exit(0)

class SearchMenu(Menu):

    def __init__(self):
        super().__init__(
            OrderedDict([
                ('e', self.find_employee),
                ('d', self.find_date),
                ('r', self.find_date_range),
                ('t', self.find_time_spent),
                ('s', self.find_search_term),
                ('m', self.main_menu)]),
            "Search Menu")

    @staticmethod
    def main_menu():
        """Go to main menu."""
        main = MainMenu()
        main.menu_loop()

    def find_employee(self):
        """Find by employee."""
        # List unique employees in order
        # Provide choice
        # User selects choice
        # Choice is searched for
        # Go to ResultMenu
        employees = utils.find_unique_employees()
        employee = item_table(employees, "Employees")
        ids = utils.find_by_employee(employee)
        if ids:
            result_menu(ids)
        else:
            print("No entries.")
            time.sleep(1)


    def find_date(self):
        """Find by date."""
        dates = utils.find_unique_dates()
        date = item_table(dates, "Dates")
        date = datetime.datetime.strptime(date, fmt).date()
        ids = utils.find_by_date(date)
        if ids:
            result_menu(ids)
        else:
            print("No entries.")
            time.sleep(1)


    def find_date_range(self):
        """Find by date range."""
        while True:
            start_date = input("Enter start date (YYYYMMDD):  ")
            try:
                start_date = datetime.datetime.strptime(start_date, fmt).date()
            except Exception:
                print("Try again.")
            else:
                break

        while True:
            end_date = input("Enter end date (YYYYMMDD):  ")
            try:
                end_date = datetime.datetime.strptime(end_date, fmt).date()
            except Exception:
                print("Try again.")
            else:
                break

        ids = utils.find_by_date_range(start_date, end_date)
        if ids:
            result_menu(ids)
        else:
            print("No entries.")
            time.sleep(1)


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
            ids = utils.find_by_time_spent(minutes)
            if ids:
                result_menu(ids)
            else:
                print("No entries.")
                time.sleep(1)


    def find_search_term(self):
        """Find by search term."""
        # Enter query
        # Query is searched for in title and notes
        # Go to ResultMenu
        query = input("Enter search term:  ")
        ids = utils.find_by_search_term(query)
        if ids:
            result_menu(ids)
        else:
            print("No entries.")
            time.sleep(1)


class ResultMenu(Menu):

    def __init__(self, ids):
        super().__init__(
            OrderedDict([
                ('n', self.next),
                ('p', self.prev),
                ('e', self.edit),
                ('d', self.delete),
                ('s', self.search_menu),
                ('m', self.main_menu)]),
            "Result Menu")
        self.ids = ids
        self.index = 0


    @staticmethod
    def search_menu():
        """Go to search menu."""
        search = SearchMenu()
        search.menu_loop()


    @staticmethod
    def main_menu():
        """Go to main menu."""
        main = MainMenu()
        main.menu_loop()


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
                self.menu[choice]()


    def __len__(self):
        return len(self.ids)


    def display(self):
        """Display a result including
        employee, task, minutes, notes, and date."""
        if not self.ids:
            self.search_menu()
        task = utils.get_task(self.ids[self.index])
        print("\nEntry {} out of {}".format(self.index + 1, len(self)))
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
        old_id = self.ids[self.index]
        new_task = enter_task()
        utils.save_task(old_id, new_task)


    def delete(self):
        """Delete current task."""
        utils.delete_task(self.ids[self.index])
        del self.ids[self.index]
        # if deleting last one, loop around
        # otherwise, maintain index
        if self.index>=len(self):
            self.index = 0


if __name__ == '__main__':

    models.initialize()
    main_menu = MainMenu()
    main_menu.menu_loop()