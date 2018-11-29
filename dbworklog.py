"""
dbworklog.py
--------
Database Worklog
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

    @staticmethod
    def _run(func):
        """Run function by calling it"""
        func()

    def menu_loop(self):
        """Show the menu."""
        while True:
            func = self._loop()
            self._run(func)

    def _loop(self):
        self._print_heading()
        self._print_info()
        return self._choose_option()

    def _print_heading(self):
        """Display the heading"""
        utils.clear()
        print(self.heading)

    def _print_info(self):
        """Print menu options info."""
        for k, v in self.menu.items():
            print('{} - {}'.format(k, v.__doc__))

    def _choose_option(self):
        """Make choice among menu options."""
        choice = input("Which option do you choose?  ").lower().strip()
        if choice in self.menu:
            return self.menu[choice]


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

    def _employee_ids(self):
        """Get employee ids relating to ids in database"""
        employees = utils.find_unique_employees()
        employee = utils.item_table(employees, "Employees")
        return utils.find_by_employee(employee)

    def _show_results(self, ids):
        """Show results menu or tell the user there is no entries."""
        if ids:
            ResultMenu(ids).menu_loop()
        else:
            print("No entries.")
            time.sleep(1)
            return 0

    def find_employee(self):
        """Find by employee."""
        ids = self._employee_ids()
        self._show_results(ids)

    def _date_ids(self):
        """Get exact date ids relating to ids in database"""
        dates = utils.find_unique_dates()
        date = utils.item_table(dates, "Dates")
        date = datetime.datetime.strptime(date, fmt).date()
        return utils.find_by_date(date)

    def find_date(self):
        """Find by date."""
        ids = self._date_ids()
        self._show_results(ids)

    def _date_range_ids(self, start_date, end_date):
        """Get date range ids relating to ids in database"""
        return utils.find_by_date_range(start_date, end_date)

    def _get_date(self, question="Enter date (YYYYMMDD):  "):
        """Get date for date ranges."""
        while True:
            date = input(question)
            try:
                date = datetime.datetime.strptime(date, fmt).date()
            except Exception:
                print("Try again.")
            else:
                return date

    def _get_dates_ids(self):
        start_date = self._get_date(
            "Enter start date (YYYYMMDD):  ")
        end_date = self._get_date(
            "Enter end date (YYYYMMDD):  ")
        return self._date_range_ids(start_date, end_date)

    def find_date_range(self):
        """Find by date range."""
        ids = self._get_dates_ids()
        self._show_results(ids)

    def _get_time_spent(self):
        """Get minutes from user."""
        while True:
            minutes = input("Enter minutes:  ")
            try:
                minutes = int(minutes)
            except Exception:
                print("Try again.")
                continue
            else:
                return minutes

    def _time_spent_ids(self):
        """Get time spent ids relating to ids in database"""
        minutes = self._get_time_spent()
        return utils.find_by_time_spent(minutes)

    def find_time_spent(self):
        """Find by minutes spent."""
        ids = self._time_spent_ids()
        self._show_results(ids)

    def _search_term_ids(self):
        """Obtain search term ids relating to ids in database"""
        query = input("Enter search term:  ")
        return utils.find_by_search_term(query)

    def find_search_term(self):
        """Find by search term."""
        ids = self._search_term_ids()
        self._show_results(ids)


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

    def check(self):
        """Check if no ids left or database is empty."""
        if not self.ids:
            if not utils.test_empty_database():
                self.search_menu()
            else:
                self.reduced_main_menu()

    def _loop(self):
        """Show the result menu."""
        self.check()
        self._print_heading()
        print(str(self))
        self._print_info()
        return self._choose_option()

    def __len__(self):
        return len(self.ids)

    def __str__(self):
        """Display a result including
        employee, task, minutes, notes, and date."""
        task = utils.get_task(self.ids[self.index])
        return """
Entry {} out of {}

Employee:  {}
Taskname:  {}
Minutes:   {}
Notes:     {}
Date:      {}
""".format(self.index + 1,
    len(self),
    task.employee,
    task.taskname,
    task.minutes,
    task.notes,
    task.date.strftime(fmt))

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

    def edit(self,
                employee=None,
                taskname=None,
                minutes=None,
                notes=None,
                date=None):
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
    if not utils.test_empty_database():
        MainMenu().menu_loop()
    else:
        ReducedMainMenu().menu_loop()

if __name__ == '__main__':
    run()


