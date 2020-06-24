import logging
import os
import platform
import json

from custom.webdriver import WebDriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.firefox.options import Options as firefox_opt

from constants import PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)


def driver_init():

    kwargs = {}
    driver_extension = ""
    driver_version = ""
    log_dir = os.devnull

    driver_class = WebDriver
    driver_name = "geckodriver"
    driver_options = firefox_opt()
    kwargs.update(
        {"firefox_options": driver_options, "service_log_path": log_dir,}
    )

    driver_options.add_argument("--no-sandbox")

    with open('./src/config.json') as config_file:
        config = json.load(config_file)
        headless = config['headless']

    if headless:
        driver_options.add_argument("--headless")

    if platform.system() == "Windows":
        driver_extension = ".exe"
    if platform.platform() == "Windows-7-6.1.7601-SP1" and driver_name == "CHROME":
        driver_version = "79"

    driver_path = f"src/drivers/{driver_name}{driver_version}{driver_extension}"
    logger.debug(f"The driver path is: {driver_path}")

    kwargs.update({"executable_path": driver_path})
    try:
        driver = driver_class(**kwargs)
    except SessionNotCreatedException:
        raise SessionNotCreatedException("Please try installing Mozilla Firefox version 60 or higher to run this application")

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver
