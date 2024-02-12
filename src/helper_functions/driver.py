"""This module contains helper functions for the driver."""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


def wait_and_get_element(css_selector=None, time_to_wait=30, driver=None):
    """Wait and get element from webdriver."""
    return WebDriverWait(driver, time_to_wait).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )


def get_css_from_table(table_header, table_index):
    """Get the css selector for the table in the simulation results page."""
    table_header_dict = {
        "headers": {"Maximum Junction Temperature": 1, "Total Losses": 4},
        "indexes": {"Switch": 1, "Diode": 2},
    }
    return (
        "#content-solution > td > table:nth-child(2) > tr:nth-child(2) > td > div > ul > "
        "li.v-expansion-panel__container.v-expansion-panel__container--active > "
        "div.v-expansion-panel__body > div > div > table > "
        f"tr:nth-child({table_header_dict["headers"][table_header]}) > td > div > "
        f"table > tbody > tr:nth-child({table_header_dict["indexes"][table_index]}) > "
        "td.result-cell.result-cell-right"
    )
