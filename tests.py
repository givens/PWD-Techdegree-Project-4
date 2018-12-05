import datetime
import sys
import time
import unittest

from collections import OrderedDict
from unittest.mock import patch
from peewee import *

import utils
import models
import dbworklog

from utils import fmt
from models import Task

test_db = SqliteDatabase(':memory:')


MODELS = [Task]


class BaseTestCase(unittest.TestCase):
    """Base Case"""
    def setUp(self):
        """Set up for all test cases"""
        self.date = datetime.datetime.now().date()
        self.min1 = '180'
        self.min2 = '240'
        self.emp = 'test'
        self.task = 'test python'
        self.notes1 = 'unittest'
        self.notes2 = 'abcdefghijklmno'
        self.task1 = {
                'employee': self.emp,
                'taskname': self.task,
                'minutes': self.min1,
                'notes': self.notes1,
                'date': self.date
        }
        self.task2 = {
                'employee': self.emp,
                'taskname': self.task,
                'minutes': self.min2,
                'notes': self.notes2,
                'date': self.date
        }
        self.bad_task = {
                'employee': 'test',
                'taskname': 'test python',
                'notes': 'databases',
                'date': self.date
        }
        test_db.connect()
        test_db.create_tables(MODELS)
        utils.create_task(self.task1)
        utils.create_task(self.task2)
        self.menu = dbworklog.Menu(
            OrderedDict([
                ('c', utils.clear)]),
            "Menu")
        self.main_menu = dbworklog.MainMenu()
        self.reduced_main_menu = dbworklog.ReducedMainMenu()
        self.search_menu = dbworklog.SearchMenu()
        self.ids = utils.find_by_search_term(self.task)
        self.result_menu = dbworklog.ResultMenu(self.ids)

    def tearDown(self):
        """Tear down for all test cases"""
        test_db.drop_tables(MODELS)
        test_db.close()
        #for id in utils.find_by_employee(self.emp):
        #    utils.delete_task(id)

class ModelsTestCases(BaseTestCase):
    """Test models"""
    def test_initialize(self):
        """Test initialize function"""
        with self.assertRaises(Exception):
            models.initialize()
            models.initialize()

class UtilsTestCase(BaseTestCase):
    """Test utils"""

    def test_find_by_date_range(self):
        """Test find by date range"""
        out = utils.find_by_date_range(self.date, self.date)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_find_by_time_spent(self):
        """Test find by time spent"""
        out = utils.find_by_time_spent(self.min1)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_find_by_search_term(self):
        """Test find by search term"""
        out = utils.find_by_search_term(self.task)
        self.assertIsInstance(out, list)
        out = utils.find_by_search_term(self.notes2)
        self.assertIsInstance(out, list)

    def test_find_by_employee(self):
        """Test find by employees"""
        out = utils.find_by_employee(self.emp)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_find_unique_employees(self):
        """Test find unique employees"""
        out = utils.find_unique_employees()
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], str)

    def test_find_unique_dates(self):
        """Test find unique dates"""
        out = utils.find_unique_dates()
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], str)

    def test_find_by_date(self):
        """Test find by date"""
        out = utils.find_by_date(self.date)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_empty_database(self):
        """Test empty datebase"""
        assert not utils.test_empty_database()

    def test_get_task(self):
        """Test get task"""
        out = utils.find_by_date(self.date)
        task= utils.get_task(out[0])
        self.assertEqual(task.date,
            datetime.datetime.strptime(self.date.strftime(fmt), fmt))

    def test_table_evaluation(self):
        """Test table_evaluation"""
        item_list = ['a']
        choice = 2
        with self.assertRaises(Exception):
            utils.item_table_evaluation(choice, item_list)

    def test_item_table(self):
        """Test item_table"""
        item_list = ['a', 'b']
        with patch('builtins.input', side_effect=['0','1']):
            out = utils.item_table(item_list)
            assert out == item_list[0]

    def test_enter_item(self):
        """Test enter_item"""
        item = 'a'
        with patch('builtins.input', side_effect = [item]:
            out = utils.enter_item("Q:  ")
            assert out == item

    def test_enter_employee(self):
        """Test enter_employee"""
        with patch('builtins.input', side_effect=[self.emp]):
            out = utils.enter_employee()
            assert out == self.emp

    def test_enter_minutes(self):
        """Test enter_minutes"""
        with patch('builtins.input', side_effect=[self.min1]):
            out = utils.enter_minutes()
            self.assertIsInstance(out, int)
            assert out == int(self.min1)

    def test_enter_taskname(self):
        """Test enter_taskname"""
        with patch('builtins.input', side_effect=[self.task]):
            out = utils.enter_taskname()
            assert out == self.task

    def test_enter_notes(self):
        """Test enter_notes"""
        with patch('builtins.input', side_effect=[self.notes1]):
            out = untils.enter_notes()
            assert out == self.notes1

    def test_enter_minute(self):
        """Test enter_minutes"""
        minutes = 15
        out = utils.enter_minutes(minutes)
        assert out == minutes

    def test_enter_notes(self):
        """Test enter_minutes"""
        out = utils.enter_notes(self.notes1)
        assert out == self.notes1

    def test_enter_task(self):
        """Test enter_task"""
        out = utils.enter_task(self.emp,
                            self.task,
                            self.min1,
                            self.notes1,
                            self.date)
        assert out['employee'] == self.emp
        assert out['taskname'] == self.task
        assert out['minutes'] == self.min1
        assert out['notes'] == self.notes1
        assert out['date'] == self.date

    def test_create_task(self):
        """Test create_task"""
        with self.assertRaises(Exception):
            utils.create_task(self.bad_task)

    def test_save_class(self):
        """Test save_class"""
        with self.assertRaises(Exception):
            utils.save_task(9999999999999999, self.task1)
        ids = utils.find_by_search_term(self.notes2)
        out = utils.save_task(ids[0], self.task2)
        assert out == 0

    def test_delete_task(self):
        """Test delete_task"""
        with self.assertRaises(Exception):
            utils.delete_task(9999999999999999)


class DBWorkLogTestCases(BaseTestCase):
    """Test dbworklog"""

    def test_result_menu__loop(self):
        """Test _loop in ResultMenu"""
        with patch('builtins.input', side_effect=['1', 'n']):
            func = self.result_menu._loop()
            print("print func 2")
            print(func)
            print(type(func))
            assert type(func) == type(self.result_menu.next)

    def test_result_menu_next(self):
        """Test next in ResultMenu"""
        idx = self.result_menu.index
        self.result_menu.next()
        idx2 = self.result_menu.index
        if idx == len(self.result_menu) - 1:
            assert idx2 == 0
        else:
            assert idx2 == idx + 1

    def test_result_menu_delete(self):
        """Test delete in ResultMenu"""
        idx = self.result_menu.index
        self.result_menu.delete()
        idx2 = self.result_menu.index
        if idx == len(self.result_menu) - 1:
            assert idx2 == 0
        else:
            assert idx2 == idx

    def test_result_menu_prev(self):
        """Test prev in ResultMenu"""
        idx = self.result_menu.index
        self.result_menu.prev()
        idx2 = self.result_menu.index
        if idx == 0:
            assert idx2 == len(self.result_menu) - 1
        else:
            assert idx2 == idx - 1

    def test_result_menu_edit(self):
        """Test edit in ResultMenu"""
        idx = self.result_menu.index
        self.result_menu.edit(self.emp,
                                self.task1,
                                self.min1,
                                self.notes1,
                                self.date)
        idx2 = self.result_menu.index
        assert idx2 == idx

    def test_result_menu___len__(self):
        """Test __len__ in ResultMenu"""
        assert len(self.result_menu) == len(self.ids)

    def test_main_menu__loop(self):
        """Test _loop in MainMenu"""
        with patch('builtins.input', side_effect=['1', 's']):
            func = self.main_menu._loop()
            print("print func")
            print(func)
            print(type(func))
            assert type(func) == type(self.main_menu.search_menu)

    def test_menu_type(self):
        """Test Menu is of correct type"""
        self.assertIsInstance(self.menu,
            dbworklog.Menu)

    def test_main_menu_type(self):
        """Test MainMenu is of correct type"""
        self.assertIsInstance(self.main_menu,
            dbworklog.MainMenu)

    def test_reduced_main_menu(self):
        """Test ReducedMainMenu is of correct type"""
        self.assertIsInstance(self.reduced_main_menu,
            dbworklog.ReducedMainMenu)

    def test_search_menu(self):
        """Test SearchMenu is of correct type"""
        self.assertIsInstance(self.search_menu,
            dbworklog.SearchMenu)

    def test_result_menu(self):
        """Test ResultMenu is of correct type"""
        self.assertIsInstance(self.result_menu,
            dbworklog.ResultMenu)

    def test__choose_option(self):
        """Test _choose_option in MainMenu"""
        with patch('builtins.input', side_effect='a'):
            func = self.main_menu._choose_option()
            print("func")
            print(func)
            self.assertIsInstance(func,
                type(self.main_menu.enter_task))

    def test_menu__loop(self):
        """Test _loop in Menu"""
        with patch('builtins.input', side_effect='c'):
            func = self.menu._loop()
            self.assertIsInstance(func,
                type(utils.clear))

    def test_menu__print_heading(self):
        """Test _print_heading in Menu"""
        self.menu._print_heading()
        out = sys.stdout.flush()
        self.assertIsInstance(out, type(None))

    def test_menu__print_loop(self):
        """Test _print_loop in Menu"""
        self.menu._print_info()
        out = sys.stdout.flush()
        self.assertIsInstance(out, type(None))

    def test_result_menu_str(self):
        """Test __str___ in ResultMenu"""
        out = str(self.result_menu)
        self.assertIsInstance(out, str)

    def test_search_menu__employee_ids(self):
        """Test _employee_ids in SearchMenu"""
        with patch('builtins.input', side_effect=['0','1']):
            ids = self.search_menu._employee_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__show_results(self):
        """Test _show_results in SearchMenu"""
        out = self.search_menu._show_results([])
        assert out == 0

    def test_main_menu_attribute_error(self):
        """Test for attribute error in MainMenu"""
        with self.assertRaises(AttributeError):
            self.main_menu.this_is_not_a_method()

    def test_result_menu_attribute_error(self):
        """Test for attribute error in ResultMenu"""
        with self.assertRaises(AttributeError):
            self.result_menu.this_is_not_a_method()

    def test_search_menu_attribute_error(self):
        """Test for attribute error in SearchMenu"""
        with self.assertRaises(AttributeError):
            self.search_menu.this_is_not_a_method()

    def test_reduced_menu_attribute_error(self):
        """Test for attribute error in ReducedMainMenu"""
        with self.assertRaises(AttributeError):
            self.reduced_main_menu.this_is_not_a_method()

    def test_menu_attribute_error(self):
        """Test for method attribute error in Menu"""
        with self.assertRaises(AttributeError):
            self.menu.this_is_not_a_method()

    def test_menu_attribute_error(self):
        """Test for variable attribute error in Menu"""
        with self.assertRaises(AttributeError):
            self.menu.this_is_not_an_attribute

    def test_search_menu__get_date(self):
        """Test _get_date in SearchMenu"""
        date = datetime.datetime.now().date()
        date_str = date.strftime('%Y%m%d')
        print(date_str)
        with patch('builtins.input', side_effect=['a', '2', date_str]):
            out = self.search_menu._get_date()
            assert out == date

    def test_search_menu__date_ids(self):
        """Test _date_ids in SearchMenu"""
        with patch('builtins.input', side_effect=['1']):
            ids = self.search_menu._date_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__date_ids_value_error(self):
        """Test _date_ids value error in SearchMenu"""
         with patch('builtins.input', side_effect=['0', '1']):
            ids = self.search_menu._date_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__get_dates_ids(self):
        """Test _get_dates in SearchMenu"""
        date = datetime.datetime.now().date()
        date_min = date.min
        date_max = date.max
        date_min_str = date_min.strftime(fmt)
        date_max_str = date_max.strftime(fmt)
        with patch('builtins.input', side_effect=['s', date_min_str, '1', date_max_str]):
            ids = self.search_menu._get_dates_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__search_term_ids(self):
        """Test _search_term_ids in SearchMenu"""
        with patch('builtins.input', side_effect='task'):
            ids = self.search_menu._search_term_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__time_spent_ids(self):
        """Test _time_spent_ids in SearchMenu"""
        with patch('builtins.input', side_effect=['b', 15, '15', str(self.min2), str(self.min1)]):
            ids = self.search_menu._time_spent_ids()
            self.assertIsInstance(ids, list)
            #self.assertIsInstance(ids[0], int)

    def test_menu__run(self):
        """Test _run in Menu"""
        with patch('builtins.input', side_effect = '15'):
            out = self.menu._run(utils.enter_minutes)
            print("output for test_menu__run")
            print(out)
            assert type(out) == type(None)

    def test_main_menu_enter_task(self):
        """Test enter_task in MainMenu"""
        with patch('builtins.input', side_effect =
            [self.emp, self.task, self.min1, self.notes2, self.date]):
            out = self.main_menu.enter_task()
            assert type(out) == type(None)

    #def test_reduced_menu_enter_task(self):
    #    out = self.reduced_main_menu.enter_task()
    #    assert type(out) == type(None)


if __name__ == '__main__':
    unittest.main()












