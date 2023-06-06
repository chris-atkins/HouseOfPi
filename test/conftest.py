# content of conftest.py
import multiprocessing


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
    multiprocessing.set_start_method("fork")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    print("IN conftest.py pytest_sessionfinish(session, exitstatus)")


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    print("IN conftest.py pytest_unconfigure(config)")
