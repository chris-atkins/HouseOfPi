import multiprocessing
from time import sleep

from mock_services.mock_hue_server import build_mock_hue_server
from mock_services.mock_ip_address_server import build_mock_ip_address_server
from mock_services.mock_my_house_server import build_mock_myhouse_server
from mock_services.mock_thermostat_server import build_mock_thermostat_server

mock_ip_server_thread = None
mock_myhouse_server_thread = None
mock_hue_server_thread = None
mock_thermostat_server_thread = None


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    print("IN conftest.py pytest_configure(config)")


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print("IN conftest.py pytest_sessionstart(session)")
    # subprocess.run(["../env-setup/run-mock-servers"])
    multiprocessing.set_start_method("fork")

    global mock_ip_server_thread
    mock_ip_server_thread = build_mock_ip_address_server()

    global mock_myhouse_server_thread
    mock_myhouse_server_thread = build_mock_myhouse_server()

    global mock_hue_server_thread
    mock_hue_server_thread = build_mock_hue_server()

    global mock_thermostat_server_thread
    mock_thermostat_server_thread = build_mock_thermostat_server()

    sleep(1)


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    print("IN conftest.py pytest_unconfigure(config)")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    print("IN conftest.py pytest_sessionfinish(session, exitstatus)")
    global mock_ip_server_thread
    mock_ip_server_thread.terminate()
    mock_ip_server_thread.join()

    global mock_myhouse_server_thread
    mock_myhouse_server_thread.terminate()
    mock_myhouse_server_thread.join()

    global mock_hue_server_thread
    mock_hue_server_thread.terminate()
    mock_hue_server_thread.join()

    global mock_thermostat_server_thread
    mock_thermostat_server_thread.terminate()
    mock_thermostat_server_thread.join()

