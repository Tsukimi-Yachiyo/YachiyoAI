import sys
import os

print("框架初始化")

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import check
os.chdir(os.sep.join(current_dir.split(os.sep)[:-1]))
check.check()
os.chdir(os.sep.join(current_dir.split(os.sep)[:-1]+["src"]))

from resource import logging