import os
import sys
import multiprocessing
from imp import load_source  # TODO: Replace with importlib once we no longer need to support Python 2

# TODO: Clean this up once we no longer need to support Python 2
if sys.version_info.major == 3:
    from unittest import mock
else:
    import mock

import pytest
tests_path = os.path.dirname(os.path.abspath(__file__))

# Add mocked_libs path so that the file under test can load mocked modules from there
mocked_libs_path = os.path.join(tests_path, 'mocked_libs')
sys.path.insert(0, mocked_libs_path)


import swsscommon
# Check we are using the mocked package
assert len(swsscommon.__path__) == 1
assert(os.path.samefile(swsscommon.__path__[0], os.path.join(mocked_libs_path, 'swsscommon')))

from sonic_py_common import daemon_base

from .mock_platform import MockChassis, MockEventHandler, MockInterruptHandler

daemon_base.db_connect = mock.MagicMock()

# Add path to the file under test so that we can load it
modules_path = os.path.dirname(tests_path)
scripts_path = os.path.join(modules_path, 'scripts')
sys.path.insert(0, modules_path)

load_source('interruptd', os.path.join(scripts_path, 'interruptd'))
import interruptd

INTERRUPT_INFO_TABLE_NAME = 'INTERRUPT_INFO'


@pytest.fixture(scope='function', autouse=True)
def configure_mocks():
    interruptd.InterruptUpdater.log_debug = mock.MagicMock()
    interruptd.InterruptUpdater.log_warning = mock.MagicMock()

    yield

    interruptd.InterruptUpdater.log_debug.reset()
    interruptd.InterruptUpdater.log_warning.reset()


class TestInterruptMonitor(object):
    """
    Test cases to cover functionality in InterruptMonitor class
    """
    def test_main(self):
        mock_chassis = MockChassis()
        interrupt_monitor = interruptd.InterruptMonitor(mock_chassis)
        interrupt_monitor.interrupt_updater.update = mock.MagicMock()

        interrupt_monitor.main()
        assert interrupt_monitor.interrupt_updater.update.call_count == 1

class TestInterruptUpdater(object):
    """
    Test cases to cover functionality in InterruptUpdater class
    """
    def test_deinit(self):
        chassis = MockChassis()
        interrupt_updater = interruptd.InterruptUpdater(chassis, multiprocessing.Event())
        interrupt_updater.interrupt_status_dict = {'key1': 'value1', 'key2': 'value2'}
        interrupt_updater.table._del = mock.MagicMock()

        interrupt_updater.deinit()
        assert interrupt_updater.table._del.call_count == 2
        expected_calls = [mock.call('key1'), mock.call('key2')]
        interrupt_updater.table._del.assert_has_calls(expected_calls, any_order=True)
        
    def test_update_interrupt_with_exception(self):
        chassis = MockChassis()
        chassis.make_error_interrupt()
        interrupt_updater = interruptd.InterruptUpdater(chassis, multiprocessing.Event())
        interrupt_updater.update()

        chassis.make_error_refresh_interrupt()
        interrupt_updater = interruptd.InterruptUpdater(chassis, multiprocessing.Event())
        interrupt_updater.update()

        assert interrupt_updater.log_warning.call_count == 2

        # TODO: Clean this up once we no longer need to support Python 2
        if sys.version_info.major == 3:
            expected_calls = [
                mock.call("Failed to get interrupts"),
                mock.call("Failed to update Interrupt values for N/A - KeyError('Name')")
            ]
        else:
            expected_calls = [
                mock.call("Failed to get interrupts"),
                mock.call("Failed to update Interrupt values for N/A - KeyError('Name')")
            ]
        assert interrupt_updater.log_warning.mock_calls == expected_calls

    def test_update_interrupt(self):
        """
        status = True
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
        """
        chassis = MockChassis()
        
        interrupt_updater = interruptd.InterruptUpdater(chassis, multiprocessing.Event())
        interrupt_updater._refresh_interrupt_status = mock.MagicMock()
        interrupt_updater.update()
        assert interrupt_updater._refresh_interrupt_status.call_count == 2
        assert interrupt_updater.log_warning.call_count == 0


class TestEventListener(object):
    """
    Test cases to cover functionality in EventListener class
    """
        
    def test_main(self):
        mock_chassis = MockChassis()
        event_listener = interruptd.EventListener(mock_chassis)
        event_listener.event_handler.start = mock.MagicMock()
        event_listener.main()
        assert event_listener.event_handler.start.call_count == 1

def test_daemon_run():
    daemon_interruptd = interruptd.InterruptDaemon()
    daemon_interruptd.stop_event.wait = mock.MagicMock(return_value=True)
    ret = daemon_interruptd.run()
    daemon_interruptd.deinit() # Deinit becuase the test will hang if we assert
    assert ret is False

    daemon_interruptd = interruptd.InterruptDaemon()
    daemon_interruptd.stop_event.wait = mock.MagicMock(return_value=False)
    ret = daemon_interruptd.run()
    daemon_interruptd.deinit() # Deinit becuase the test will hang if we assert
    assert ret is True


def test_try_get():
    def good_callback():
        return 'good result'

    def unimplemented_callback():
        raise NotImplementedError

    ret = interruptd.try_get(good_callback)
    assert ret == 'good result'

    ret = interruptd.try_get(unimplemented_callback)
    assert ret == interruptd.NOT_AVAILABLE

    ret = interruptd.try_get(unimplemented_callback, 'my default')
    assert ret == 'my default'


@mock.patch('interruptd.InterruptDaemon.run')
def test_main(mock_run):
    mock_run.return_value = False

    ret = interruptd.main()
    assert mock_run.call_count == 1
    assert  ret != 0