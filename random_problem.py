#!/usr/bin/env python3
import os
import random
import sys
import webbrowser

valid_args = {"-e": "easy", "-m": "medium", "-h": "hard"}
difficulty = "easy"
if len(sys.argv) == 2:
    if sys.argv[1] in valid_args:
        difficulty = valid_args[sys.argv[1]]
elif len(sys.argv) > 2:
    print("Did not recognize command line argument.  Valid options are -e -m -h")
    exit(1)

repo_root = os.getcwd()
reroll = ""
problems = os.listdir(f"{repo_root}/{difficulty}")
selected_problem_idx = 0
while reroll != "y":
    selected_problem_idx = random.randrange(0, len(problems))

    webbrowser.open(f"file://{repo_root}/{difficulty}/{problems[selected_problem_idx]}")

    reroll = ""
    while reroll != "y" and reroll != "n":
        reroll = input("Would you like to do the selected problem? y/n\n> ")
        if reroll != "y" and reroll != "n":
            print("Failed to understand argument. Please enter y/n")


py_filename = problems[selected_problem_idx].replace("html", "py").replace("-", "_")
module_name = py_filename[0:-3]

with open(f"{repo_root}/solutions/{difficulty}/{py_filename}", "w+") as f:
    content = f"""def {module_name}(input):
    return True"""
    f.write(content)

with open(f"{repo_root}/solutions/test/{difficulty}/test_{py_filename}", "w+") as f:
    py_filename_arr = list(module_name)
    idx = 0
    py_filename_arr[0] = py_filename_arr[0].upper()
    while idx < len(py_filename_arr):
        if py_filename_arr[idx] == "_":
            py_filename_arr[idx] = ""
            py_filename_arr[idx + 1] = py_filename_arr[idx + 1].upper()
            idx += 2
        else:
            idx += 1
    class_name = "".join(py_filename_arr)
    content = f"""import unittest
from {difficulty}.{module_name} import {module_name}

class Test{class_name}(unittest.TestCase):

    def test_{module_name}(self):
        self.assertEquals({module_name}(None), False)"""
    f.write(content)