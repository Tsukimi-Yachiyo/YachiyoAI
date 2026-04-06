"""
    智能体模块
"""
import builtins

import logging
from .state import State
builtins.__dict__["State"] = State
builtins.__dict__["logging"] = logging
