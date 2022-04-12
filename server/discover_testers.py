#!/usr/bin/python3.6

"""A program to discover all the affected tests from a moudule."""

import os
import sys

import requests

PATH_PREFIX = "/source_code/src/python"
BASE_URL = "http://10.0.2.2:5555/testing_targets"

GREEN = '\033[92m'
END = '\033[0m'


def show_testers(module):
    """Prints the testing programs for the passed in module.

    :param str module: The name of the module to find tests for.
    """
    print(GREEN + "Module" + END, module)

    response = requests.get(f"{BASE_URL}{module}")
    assert response.status_code == 200
    affected_tests = response.json()["affected_tests"]
    print(GREEN + "Affected tests" + END)
    for fn in affected_tests:
        print(fn.replace(".", "/") + ".py")
    print(GREEN + "Total number of affected tests" + END, len(affected_tests))


if __name__ == '__main__':
    filename = sys.argv[1]
    cwd = os.getcwd().replace(PATH_PREFIX, "")
    show_testers(os.path.join(cwd, filename))


