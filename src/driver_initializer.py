import logging
import os
import platform
import json

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options as chrome_opt
from selenium.webdriver.firefox.options import Options as firefox_opt

from constants import BROWSER_NAME, PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)


def driver_init():

    kwargs = {}
    driver_class = None
    driver_name = ""
    driver_extension = ""
    driver_version = ""
    driver_options = None
    log_dir = os.devnull

    if BROWSER_NAME == "FIREFOX":
        driver_class = webdriver.Firefox
        driver_name = "geckodriver"
        driver_options = firefox_opt()
        kwargs.update(
            {"firefox_options": driver_options, "service_log_path": log_dir,}
        )
    elif BROWSER_NAME == "CHROME":
        driver_class = webdriver.Chrome
        driver_name = "chromedriver"
        driver_options = chrome_opt()
        kwargs.update(
            {"chrome_options": driver_options,}
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
