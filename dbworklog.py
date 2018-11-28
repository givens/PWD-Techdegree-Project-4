"""
views.py
--------
View for Database Worklog
"""

from collections import OrderedDict
import datetime
import sys
import time

import utils
import models
from utils import fmt


class Menu:
    """Menu template"""

    def __init__(self, menu=None, heading=None):
        self.menu = menu
        self.heading = heading

    def menu_loop(self):
        """Show the menu."""
        choice = None
        while True:
            utils.clear()
            print(self.heading)
            for k, v in self.menu.items():
                print('{} - {}'.format(k, v.__doc__))
            choice = input("Which option do you choose?  ").lower().strip()

            if choice in self.menu:
                self.menu[choice]()


class MainMenu(Menu):
    """Main menu"""

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
        dict = utils.enter_task()
        utils.create_task(dict)

    @staticmethod
    def search_menu():
        """Search entries."""
        SearchMenu().menu_loop()
#        search_menu()

    @staticmethod
    def quit():
        """Quit."""
        print("Quit.")
        sys.exit(0)

class ReducedMainMenu(Menu):
    """Main menu without search menu because db is empty"""
    def __init__(self):
        super().__init__(
            OrderedDict([
                ('a', self.enter_task),
                ('q', self.quit)]),
            "Main Menu")

    @staticmethod
    def enter_task():
        """Add an entry."""
        dict = utils.enter_task()
        utils.create_task(dict)
        MainMenu().menu_loop()

    @staticmethod
    def quit():
        """Quit."""
        print("Quit.")
        sys.exit(0)


class SearchMenu(Menu):
    """Result menu"""

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
        MainMenu().menu_loop()

    def find_employee(self):
        """Find by employee."""
        # List unique employees in order
        # Provide choice
        # User selects choice
        # Choice is searched for
        # Go to ResultMenu
        employees = utils.find_unique_employees()
        employee = utils.item_table(employees, "Employees")
        ids = utils.find_by_employee(employee)
        if ids:
            ResultMenu(ids).menu_loop()
        else:
            print("No entries.")
            time.sleep(1)

    def find_date(self):
        """Find by date."""
        dates = utils.find_unique_dates()
        date = utils.item_table(dates, "Dates")
        date = datetime.datetime.strptime(date, fmt).date()
        ids = utils.find_by_date(date)
        if ids:
            ResultMenu(ids).menu_loop()
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
            ResultMenu(ids).menu_loop()
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
                ResultMenu(ids).menu_loop()
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
            ResultMenu(ids).menu_loop()
        else:
            print("No entries.")
            time.sleep(1)


class ResultMenu(Menu):
    """Result menu"""

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
        SearchMenu().menu_loop()

    @staticmethod
    def main_menu():
        """Go to main menu."""
        MainMenu().menu_loop()

    @staticmethod
    def reduced_main_menu():
        ReducedMainMenu().menu_loop()

    def menu_loop(self):
        """Show the menu."""
        choice = None
        while True:
            utils.clear()
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
            if not utils.test_empty_database():
                self.search_menu()
            else:
                self.reduced_main_menu()
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
        if self.index >= len(self):
            self.index = 0

    def prev(self):
        """Go to previous task."""
        self.index -= 1
        if self.index <= 0:
            self.index = len(self) - 1

    def edit(self):
        """Edit current task."""
        old_id = self.ids[self.index]
        new_task = utils.enter_task()
        utils.save_task(old_id, new_task)

    def delete(self):
        """Delete current task."""
        utils.delete_task(self.ids[self.index])
        del self.ids[self.index]
        # if deleting last one, loop around
        # otherwise, maintain index
        if self.index >= len(self):
            self.index = 0

def run():
    models.initialize()
    tasks = models.Task.select()
    if not utils.test_empty_database():
        MainMenu().menu_loop()
    else:
        ReducedMainMenu().menu_loop()

if __name__ == '__main__':
    run()


