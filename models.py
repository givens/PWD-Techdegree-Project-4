"""
models.py
---------
As a user of the script, if I choose to enter a new work log,
I should be able to provide my name, a task name, a number of
minutes spent working on it, and any additional notes I want
to record.
"""

# Notes
# sqlite3 task.db
# .tables
# select * from task;
# .exit
# .create() - creates a record
# .select() - selects all
# .save() - updates record
# .get() - obtains one record
# .delete_instance() - deletes a record


import datetime

from peewee import *


db = SqliteDatabase('tasks.db')


class Task(Model):
    """Task Model"""
    employee = CharField(max_length=100)
    taskname = CharField(max_length=100)
    minutes = IntegerField(.0)
    notes = TextField(default='')
    date = DateTimeField()  # need a date like 2018-11-16 rather than a timestamp

    class Meta:
        database = db


def initialize():
    """Connect to the database and create tables"""
    db.connect()
    db.create_tables([Task], safe=True)


if __name__ == '__main__':
    pass






