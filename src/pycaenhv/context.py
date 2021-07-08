from typing import Any

from pycaenhv.wrappers import init_system, deinit_system
from pycaenhv.enums import CAENHV_SYSTEM_TYPE, LinkType


class HVContext:
    def __init__(self,
                 system: str,
                 link: str,
                 argument: Any,
                 user: str = '',
                 password: str = ''):
        self.system = system
        self.link = link
        self.argument = argument
        self.user = user
        self.password = password
        self.handle: int = -1

    def start(self):
        system = CAENHV_SYSTEM_TYPE[self.system.upper()]
        link = LinkType[self.link.upper()]
        self.handle = init_system(system, link, self.argument, self.user,
                                  self.password)

    def __enter__(self):
        self.start()
        return self

    def close(self) -> None:
        deinit_system(self.handle)

    def __exit__(self, type, value, traceback):
        self.close()