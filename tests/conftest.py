import json
from datetime import datetime

import pytest
import allure
from framework.browser.browser import Browser
from tests.utils.project_db_util import ProjectDbUtil
from tests.config.browser import BrowserConfig
from tests.config.browser import Grid
from framework.constants.date_time_constants import TEST_TIME_FORMAT


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=BrowserConfig.BROWSER,
                     help="Name of browser")
    parser.addoption("--grid_port", action="store", default=Grid.GRID_PORT,
                     help="Port of remote connection")


@pytest.fixture(scope="session")
def set_setup_and_turndown_db_params():
    ProjectDbUtil.db_util.create_connection()
    ProjectDbUtil.db_util.create_cursor(buffered=True)
    yield
    ProjectDbUtil.db_util.close_connection()
    ProjectDbUtil.db_util.close_cursor()


@pytest.fixture
def pytest_report_teststatus(report, ):
    if report.when == "call" and ('test_gmail_api' in report.nodeid):
        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
        with open("test_results.json", "w") as f:
            data_to_update = {"test_result": f"{report.outcome}"}
            file_data.update(data_to_update)
            json.dump(file_data, f)


@pytest.fixture
def pytest_sessionstart(session):
    with open("test_results.json", "w") as file:
        file.write("""{"browser": "", "test_start_time": "", "test_end_time": "", "test_result": ""}""")

    session.results = dict()


@pytest.fixture
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result


@pytest.mark.usefixtures("pytest_sessionstart", "pytest_runtest_makereport", "pytest_report_teststatus")
@pytest.fixture(scope="function")
def create_browser(request):

    with allure.MASTER_HELPER.step("Creating a browser session from a config file"):
        browser = request.config.getoption('--browser')
        Browser.get_browser().set_up_driver(browser_key=browser, grid_port=request.config.getoption('--grid_port'))
        Browser.get_browser().maximize(browser_key=browser)
        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
        with open("test_results.json", "w") as f:
            now = datetime.now()
            data_to_update = {"test_start_time": f"{now.strftime(f'{TEST_TIME_FORMAT}')}"}
            file_data.update(data_to_update)
            json.dump(file_data, f)

    yield

    with allure.MASTER_HELPER.step("Closing sessions of all browsers"):

        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
        with open("test_results.json", "w") as f:
            now = datetime.now()
            data_to_update = {"test_end_time": f"{now.strftime(f'{TEST_TIME_FORMAT}')}"}
            file_data.update(data_to_update)
            json.dump(file_data, f)

        for browser_key in list(Browser.get_browser().get_driver_names()):
            Browser.get_browser().quit(browser_key=browser_key)
