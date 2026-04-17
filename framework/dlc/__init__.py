import framework.library as library
import public_modules
import builtins
import logging

builtins.__dict__["library"] = library
builtins.__dict__["public_modules"] = public_modules
builtins.__dict__["logging"] = logging

from abc import ABC, abstractmethod

class Main(ABC):

    name : str = "Main"

    init_order : int = 0
    build_order : int = 0

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def build(self):
        pass


class Decorator(ABC):

    @abstractmethod
    def build(self):
        pass

builtins.__dict__["BaseMain"] = Main
builtins.__dict__["Decorator"] = Decorator

