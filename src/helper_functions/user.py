"""This module contains functions for logging in to Iposim."""

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from helper_functions.driver import wait_and_get_element

logger = logging.getLogger(__name__)


class UnableToLogin(Exception):
    """Exception raised when unable to log in to Iposim."""


def login(login_page, user, password, driver):
    """Log in to Iposim using the provided credentials."""
    try:
        logger.info("Requesting access to Iposim.")
        driver.get(login_page)

        wait_and_get_element(".image-fluid", driver=driver)

        username_field = wait_and_get_element("#identifierInput", driver=driver)
        logger.info("Sending user information.")
        username_field.send_keys(user)

        button = wait_and_get_element("#btnOk", driver=driver)
        ActionChains(driver).move_to_element(button).click(button).perform()

        button = wait_and_get_element("#onetrust-accept-btn-handler", driver=driver)
        ActionChains(driver).move_to_element(button).click(button).perform()

        password_field = wait_and_get_element("#password", driver=driver)
        password_field.send_keys(password)

        keep_logged = wait_and_get_element("#myDevice", driver=driver)
        ActionChains(driver).move_to_element(keep_logged).click(keep_logged).perform()

        button = driver.find_element("css selector", "#btnOk")
        ActionChains(driver).move_to_element(button).click(button).perform()
        logger.info("Iposim authentication successful.")
        logger.info(
            r"""
            ____                 _         
           /  _/___  ____  _____(_)___ ___ 
           / // __ \/ __ \/ ___/ / __ `__ \
         _/ // /_/ / /_/ (__  ) / / / / / /
        /___/ .___/\____/____/_/_/ /_/ /_/ 
           /_/ 
        """
        )
    except TimeoutException as exc:
        raise UnableToLogin(
            "Unable to login. Check your e-mail and password or internet connection and try again."
        ) from exc
