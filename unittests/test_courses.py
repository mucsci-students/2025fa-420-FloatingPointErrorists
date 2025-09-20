import json
from pathlib import Path
from scheduler_cli import add_course, mod_course, del_course

#def test_add_courses():

#def test_mod_courses():

def test_del_courses():
    del_course(2)
