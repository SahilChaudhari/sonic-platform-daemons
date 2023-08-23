from sonic_platform_base import chassis_base
from sonic_py_common import logger

class MockEventHandler(logger.Logger):
    def __init__(self):
        super(MockEventHandler, self).__init__()
        self.is_event_started = False

    def start(self):
        self.is_event_started = True

    def stop(self):
        self.is_event_started = False

class MockInterruptHandler(logger.Logger):
    def __init__(self):
        super(MockInterruptHandler, self).__init__()

    def interrupt_get(self):
        interrupt_info_list = [
            {
                "Name" : 1,
                "Description" : "interrupt",
                "Count" : 2,
                "Severity" : 1,
                "timestamp" : "20230807 04:52:04"
            },
            {
                "Name" : 2,
                "Description" : "interrupt",
                "Count" : 1,
                "Severity" : 4,
                "timestamp" : "20230807 05:23:04"
            },
        ]
        msg = "Success"
        return True, interrupt_info_list, msg

class MockErrorInterruptHandler(logger.Logger):
    def __init__(self):
        super(MockErrorInterruptHandler, self).__init__()
        self.status = False
        self.interrupt_info_list = None
        self.msg = None

    def interrupt_get(self):
        return self.status, self.interrupt_info_list, self.msg

class MockChassis(chassis_base.ChassisBase):
    def __init__(self):
        super(MockChassis, self).__init__()
        self._name = None
        self._presence = True
        self._model = 'Chassis Model'
        self._serial = 'Chassis Serial'
        self._status = True
        self._position_in_parent = 1
        self._replaceable = False

        self._is_chassis_system = False
        self._interrupt_handler = MockInterruptHandler()
        self._event_handler = MockEventHandler()

    def make_error_interrupt(self):
        interrupt_handler = MockErrorInterruptHandler()
        self._interrupt_handler = interrupt_handler
        self._interrupt_handler.msg = "Failed to get interrupts"

    def make_error_refresh_interrupt(self):
        interrupt_handler = MockErrorInterruptHandler()
        self._interrupt_handler = interrupt_handler
        self._interrupt_handler.status = True
        self._interrupt_handler.interrupt_info_list = [{}]
        self._interrupt_handler.msg = "error"

    def is_modular_chassis(self):
        return self._is_chassis_system

    def set_modular_chassis(self, is_true):
        self._is_chassis_system = is_true

    def get_interrupt_handler(self):
        return self._interrupt_handler

    def get_event_handler(self):
        return self._event_handler

    # Methods inherited from DeviceBase class and related setters
    def get_name(self):
        return self._name

    def get_presence(self):
        return self._presence

    def set_presence(self, presence):
        self._presence = presence

    def get_model(self):
        return self._model

    def get_serial(self):
        return self._serial

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_position_in_parent(self):
        return self._position_in_parent

    def is_replaceable(self):
        return self._replaceable

