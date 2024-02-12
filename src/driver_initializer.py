"""Driver initialization."""

import logging
import os
import json

from selenium.webdriver import Firefox
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


from constants import PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)


def driver_init():
    """Initialize driver."""
    with open("./src/config.json", encoding="utf8") as config_file:
        config = json.load(config_file)
        headless = config["headless"]

    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    options.add_argument("--no-sandbox")
    if headless:
        options.add_argument("--headless")

    service = Service(
        executable_path="src/drivers/geckodriver.exe", service_log_path=os.devnull
    )

    try:
        driver = Firefox(options=options, service=service)
    except SessionNotCreatedException as exc:
        logger.exception(exc)
        raise SessionNotCreatedException(
            "Please try installing Mozilla Firefox version 60 or higher to run this application"
        ) from exc

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver
