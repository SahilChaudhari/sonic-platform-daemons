"""
    Mock implementation of sonic_platform package for unit testing
"""

# TODO: Clean this up once we no longer need to support Python 2
import sys
if sys.version_info.major == 3:
    from unittest import mock
else:
    import mock

from sonic_platform_base.chassis_base import ChassisBase


class Chassis(ChassisBase):
    def __init__(self):
        ChassisBase.__init__(self)
        self._eeprom = mock.MagicMock()
        self._interrupt_handler = mock.MagicMock()
        self._event_handler = mock.MagicMock()

    def get_interrupt_handler(self):
        return self._interrupt_handler

    def get_event_handler(self):
        return self._event_handler
