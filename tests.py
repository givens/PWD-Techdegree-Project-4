import datetime
import sys
import unittest

from collections import OrderedDict
from unittest.mock import patch

import utils
import models
import dbworklog

fmt = '%Y%m%d'


#class TestBackend(unittest.TestCase):
#    def test_mode_first(self):
#        self.assertEqual(Abc().function1(), 30)

#    @patch('builtins.input')
#    def test_mode_second(self, mocked_input):
#        mocked_input.return_value = "QWE"

#        result = Abc().function2()
#        self.assertEqual(result, "QWE1")

class TestCase(unittest.TestCase):
    pass

class ModelsTestCases(TestCase):
    """Test models"""
    def test_initialize(self):
        with self.assertRaises(Exception):
            models.initialize()
            models.initialize()

class UtilsTestCase(TestCase):
    """Test utils"""
    def setUp(self):
        self.date = datetime.datetime.now().date()
        self.min1 = 180
        self.min2 = 240
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
        for id in utils.find_by_employee(self.emp):
            utils.delete_task(id)

    def test_find_by_date_range(self):
        out = utils.find_by_date_range(self.date, self.date)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_find_by_time_spent(self):
        out = utils.find_by_time_spent(self.min1)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_find_by_search_term(self):
        out = utils.find_by_search_term(self.task)
        self.assertIsInstance(out, list)
        out = utils.find_by_search_term(self.notes2)
        self.assertIsInstance(out, list)

    def test_find_by_employee(self):
        out = utils.find_by_employee(self.emp)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_find_unique_employees(self):
        out = utils.find_unique_employees()
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], str)

    def test_find_unique_dates(self):
        out = utils.find_unique_dates()
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], str)

    def test_find_by_date(self):
        out = utils.find_by_date(self.date)
        self.assertIsInstance(out, list)
        self.assertIsInstance(out[0], int)

    def test_empty_database(self):
        assert not utils.test_empty_database()

    def test_get_task(self):
        out = utils.find_by_date(self.date)
        task= utils.get_task(out[0])
        self.assertEqual(task.date,
            datetime.datetime.strptime(self.date.strftime(fmt), fmt))

    def test_table_evaluation(self):
        item_list = ['a']
        choice = 2
        with self.assertRaises(Exception):
            utils.item_table_evaluation(choice, item_list)

    def test_item_table(self):
        item_list = ['a', 'b']
        with patch('builtins.input', side_effect=['0','1']):
            out = utils.item_table(item_list)
            assert out == item_list[0]

    def test_enter_item(self):
        item = 'a'
        out = utils.enter_item("Question:  ", item)
        assert out == item

    def test_enter_employee(self):
        name = 'bg'
        out = utils.enter_employee(name)
        assert out == name

    def test_name(self):
        name = 'task1'
        out = utils.enter_taskname(taskname=name)
        assert out == name

    def test_enter_minute(self):
        minutes = 15
        #bad_minutes = 'five'
        out = utils.enter_minutes(minutes)
        assert out == minutes
        #with self.assertRaises(Exception):
        #    utils.enter_minutes(bad_minutes)

    def test_enter_notes(self):
        out = utils.enter_notes(self.notes1)
        assert out == self.notes1

    def test_enter_task(self):
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
        with self.assertRaises(Exception):
            utils.create_task(self.bad_task)

    def test_save_class(self):
        with self.assertRaises(Exception):
            utils.save_task(9999999999999999, self.task1)
        ids = utils.find_by_search_term(self.notes2)
        out = utils.save_task(ids[0], self.task2)
        assert out == 0

    def test_delete_task(self):
        with self.assertRaises(Exception):
            utils.delete_task(9999999999999999)


class DBWorkLogTestCases(TestCase):
    """Test dbworklog"""

    def setUp(self):

        self.date = datetime.datetime.now().date()
        self.min1 = 180
        self.min2 = 240
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
        for id in utils.find_by_employee(self.emp):
            utils.delete_task(id)

    def test_result_menu__loop(self):
        with patch('builtins.input', side_effect=['1', 'n']):
            func = self.result_menu._loop()
            print("print func 2")
            print(func)
            print(type(func))
            assert type(func) == type(self.result_menu.next)

    def test_result_menu_next(self):
        idx = self.result_menu.index
        self.result_menu.next()
        idx2 = self.result_menu.index
        if idx == len(self.result_menu) - 1:
            assert idx2 == 0
        else:
            assert idx2 == idx + 1

    def test_result_menu_delete(self):
        idx = self.result_menu.index
        self.result_menu.delete()
        idx2 = self.result_menu.index
        if idx == len(self.result_menu) - 1:
            assert idx2 == 0
        else:
            assert idx2 == idx

    def test_result_menu_prev(self):
        idx = self.result_menu.index
        self.result_menu.prev()
        idx2 = self.result_menu.index
        if idx == 0:
            assert idx2 == len(self.result_menu) - 1
        else:
            assert idx2 == idx - 1

    def test_result_menu_edit(self):
        idx = self.result_menu.index
        self.result_menu.edit(self.emp,
                                self.task1,
                                self.min1,
                                self.notes1,
                                self.date)
        idx2 = self.result_menu.index
        assert idx2 == idx

    def test_result_menu___len__(self):
        assert len(self.result_menu) == len(self.ids)

    def test_main_menu__loop(self):
        with patch('builtins.input', side_effect=['1', 's']):
            func = self.main_menu._loop()
            print("print func")
            print(func)
            print(type(func))
            assert type(func) == type(self.main_menu.search_menu)

    def test_menu_type(self):
        self.assertIsInstance(self.menu,
            dbworklog.Menu)

    def test_main_menu_type(self):
        self.assertIsInstance(self.main_menu,
            dbworklog.MainMenu)

    def test_reduced_main_menu(self):
        self.assertIsInstance(self.reduced_main_menu,
            dbworklog.ReducedMainMenu)

    def test_search_menu(self):
        self.assertIsInstance(self.search_menu,
            dbworklog.SearchMenu)

    def test_result_menu(self):
        self.assertIsInstance(self.result_menu,
            dbworklog.ResultMenu)

    #def test__test_menu(self):
    #    out = self.menu._test_menu()
    #    assert out == 0

    def test__choose_option(self):
        with patch('builtins.input', side_effect='a'):
            func = self.main_menu._choose_option()
            print("func")
            print(func)
            self.assertIsInstance(func,
                type(self.main_menu.enter_task))

    #def test_main_menu_quit(self):
    #    self.main_menu.quit()
    #    output = sys.stdout.flush()
    #    assert output == "Quit."

    #def test_reduced_main_menu_quit(self):
    #    self.reduced_main_menu.quit()
    #    output = sys.stdout.flush()
    #    assert output == "Quit."

    def test_menu__loop(self):
        with patch('builtins.input', side_effect='c'):
            func = self.menu._loop()
            self.assertIsInstance(func,
                type(utils.clear))

    def test_menu__print_heading(self):
        self.menu._print_heading()
        out = sys.stdout.flush()
        self.assertIsInstance(out, type(None))
        #print("print output")
        #print(output)
        #print("print output finished")
        #assert output == "Menu"

    def test_menu__print_loop(self):
        self.menu._print_info()
        out = sys.stdout.flush()
        self.assertIsInstance(out, type(None))
        #print("print output")
        #print(out)
        #print("print output finished")
        #assert out == "c - Clear screen."

    def test_result_menu_str(self):
        out = str(self.result_menu)
        self.assertIsInstance(out, str)

    def test_search_menu__employee_ids(self):
        with patch('builtins.input', side_effect=['0','1']):
            ids = self.search_menu._employee_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__employee_ids_value_error(self):
        with patch('builtins.input', side_effect=['0', '1']):
            ids = self.search_menu._employee_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__show_results(self):
        out = self.search_menu._show_results([])
        assert out == 0

    def test_main_menu_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.main_menu.this_is_not_a_method()

    def test_result_menu_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.result_menu.this_is_not_a_method()

    def test_search_menu_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.search_menu.this_is_not_a_method()

    def test_reduced_menu_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.reduced_main_menu.this_is_not_a_method()

    def test_menu_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.menu.this_is_not_a_method()

    def test_menu_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.menu.this_is_not_an_attribute

    def test_search_menu__get_date(self):
        date = datetime.datetime.now().date()
        date_str = date.strftime('%Y%m%d')
        print(date_str)
        with patch('builtins.input', side_effect=['a', '2', date_str]):
            out = self.search_menu._get_date()
            assert out == date

    def test_search_menu__date_ids(self):
        with patch('builtins.input', side_effect=['1']):
            ids = self.search_menu._date_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__date_ids_value_error(self):
         with patch('builtins.input', side_effect=['0', '1']):
            ids = self.search_menu._date_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__get_dates_ids(self):
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
        with patch('builtins.input', side_effect='task'):
            ids = self.search_menu._search_term_ids()
            self.assertIsInstance(ids, list)
            self.assertIsInstance(ids[0], int)

    def test_search_menu__time_spent_ids(self):
        with patch('builtins.input', side_effect=['b', 15, '15', str(self.min2), str(self.min1)]):
            ids = self.search_menu._time_spent_ids()
            self.assertIsInstance(ids, list)
            #self.assertIsInstance(ids[0], int)

    def test_menu__run(self):
        with patch('builtins.input', side_effect = '15'):
            out = self.menu._run(utils.enter_minutes)
            print("output for test_menu__run")
            print(out)
            assert type(out) == type(None)

    def test_main_menu_enter_task(self):
        with patch('builtins.input', side_effect =
            [self.emp, self.task, self.min1, self.notes2, self.date]):
            out = self.main_menu.enter_task()
            assert type(out) == type(None)

    #def test_reduced_menu_enter_task(self):
    #    out = self.reduced_main_menu.enter_task()
    #    assert type(out) == type(None)


if __name__ == '__main__':
    unittest.main()












