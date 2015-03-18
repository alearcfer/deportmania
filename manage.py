__author__ = 'Alejandro'
#!C:\Users\Alejandro\Documents\deportmania
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deportmania.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
