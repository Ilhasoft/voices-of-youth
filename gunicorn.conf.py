import os
import multiprocessing

current_path = os.path.dirname(os.path.abspath(__file__))
bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2
name = 'voy'
env = 'DJANGO_SETTINGS_MODULE=voicesofyouth.settings'
proc_name = 'voy'
default_proc_name = proc_name
chdir = current_path
loglevel = 'info'
timeout = 120
