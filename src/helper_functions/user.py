from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from helper_functions.driver import wait_and_get_element
import logging

logger = logging.getLogger(__name__)

class UnableToLogin(Exception):
    pass

def login(login_page, user, password, driver):
    try:
        logger.info("Requesting access to Iposim.")
        driver.get(login_page)

        username_field = wait_and_get_element("#identifierInput", driver=driver)
        logger.info("Sending user information.")
        username_field.send_keys(user)

        button = driver.find_element_by_css_selector("#postButton > a")
        ActionChains(driver).move_to_element(button).click(button).perform()

        password_field = wait_and_get_element("#password", driver=driver)
        password_field.send_keys(password)

        button = driver.find_element_by_css_selector(
            "body > div > div.ping-body-container > div:nth-child(1) > form > div.ping-buttons > a"
        )
        ActionChains(driver).move_to_element(button).click(button).perform()
        button = wait_and_get_element("button.btn:nth-child(2)", driver=driver,)
        button.click()
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
    except TimeoutException:
        raise UnableToLogin("Unable to establish login. Check your e-mail and password or internet connection and try again.")
