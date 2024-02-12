"""Contains functions to run simulations and retrieve results from Iposim."""

import logging
import time
from selenium.common.exceptions import TimeoutException

from constants import MAX_SIMULATION_TIME
from helper_functions.data import generate_url, append_results_and_save
from helper_functions.driver import wait_and_get_element, get_css_from_table

logger = logging.getLogger(__name__)


class ParametersNotOkError(Exception):
    """Exception raised when the parameters are not ok."""


class SimulationTookTooLongError(Exception):
    """Exception raised when the simulation took too long."""


def check_for_empty_page(driver):
    """Check if the page is empty."""
    try:
        wait_and_get_element(
            "#app > div.application--wrap > main > div > div > div > "
            "div.flex.main-container.xs12 > div.container.fluid.tabs__results > "
            "div > div.flex.content.content-large > div.layout.mt-2.mx-1.row.wrap "
            "> div:nth-child(1) > div > div.flex.md5.xs12.mx-0 > div > img",
            time_to_wait=30,
            driver=driver,
        )
    except TimeoutException as exc:
        raise ParametersNotOkError from exc


def check_for_results_table(driver):
    """Check if the results table is present."""
    try:
        wait_and_get_element(
            ".sim-main-content > div:nth-child(3) > div:nth-child(1) > img:nth-child(2)",
            time_to_wait=MAX_SIMULATION_TIME,
            driver=driver,
        )
    except TimeoutException as exc:
        raise SimulationTookTooLongError from exc


def get_results(driver):
    """Get the results from the simulation results page."""
    temp_switch = driver.find_element_by_css_selector(
        get_css_from_table("Maximum Junction Temperature", "Switch")
    )
    temp_diode = driver.find_element_by_css_selector(
        get_css_from_table("Maximum Junction Temperature", "Diode")
    )
    loss_switch = driver.find_element_by_css_selector(
        get_css_from_table("Total Losses", "Switch")
    )
    loss_diode = driver.find_element_by_css_selector(
        get_css_from_table("Total Losses", "Diode")
    )

    temp_switch = float(temp_switch.text[:-3])
    temp_diode = float(temp_diode.text[:-3])
    loss_switch = float(loss_switch.text[:-2])
    loss_diode = float(loss_diode.text[:-2])

    logger.info(
        "--------------------------------------------------------------------\nResults:"
    )
    logger.info("    Maximum Junction Temperature:")
    logger.info("    Switch: %s / Diode: %s", temp_switch, temp_diode)
    logger.info("    Total Losses:")
    logger.info("    Switch: %s / Diode: %s\n", loss_switch, loss_diode)

    return temp_switch, temp_diode, loss_switch, loss_diode


def create_simulation_and_retrieve_result(url, driver):
    """Create a simulation and retrieve the results."""
    try:
        driver.get(url)
        check_for_empty_page(driver)
        check_for_results_table(driver)
        return get_results(driver)
    except SimulationTookTooLongError:
        logger.info(
            "--------------------------------------------------------------------\nResults:"
        )
        logger.info(
            "Simulation lasted longer than %s seconds. Try changing the parameters.",
            MAX_SIMULATION_TIME,
        )
        return (
            "Simulation lasted longer than %s seconds",
            MAX_SIMULATION_TIME,
        ) * 4
    except ParametersNotOkError:
        logger.info(
            "--------------------------------------------------------------------\nResults:"
        )
        logger.info("Incorrect parameters. Try changing the parameters.")
        return ("Incorrect parameters") * 4


def run_all_simulations_and_save(data, driver, workbook, output_dir):
    """Run all simulations and save the results to an excel file."""
    start = time.time()
    results_dict = {
        "Maximum Junction Temperature": {"Switch": [], "Diode": []},
        "Total Losses": {"Switch": [], "Diode": []},
    }
    try:
        number_of_rows = len(next(iter(data.values())))
        for row_number in range(0, number_of_rows):
            logger.info(
                "--------------------------------------------------------------------"
            )
            logger.info("Running simulation %s of %s", row_number + 1, number_of_rows)

            url = generate_url(data, row_number)
            (
                temp_switch,
                temp_diode,
                loss_switch,
                loss_diode,
            ) = create_simulation_and_retrieve_result(url, driver)

            results_dict["Maximum Junction Temperature"]["Switch"].append(temp_switch)
            results_dict["Maximum Junction Temperature"]["Diode"].append(temp_diode)
            results_dict["Total Losses"]["Switch"].append(loss_switch)
            results_dict["Total Losses"]["Diode"].append(loss_diode)

    except Exception:
        logger.error(
            "An error occurred during the simulations, ending it earlier and generating results..."
        )
        raise
    finally:
        append_results_and_save(workbook, results_dict, output_dir)
        driver.quit()
        finish = time.time()
        duration = finish - start
        logger.info("Total simulation time: %.1f seconds", duration)
        logger.info("End of simulations")


def inputs_ok(user, password, filename, output_dir):
    """Check if the inputs are ok."""
    inputs_missing = []
    if filename == "No file selected" or not filename:
        inputs_missing.append("No input file selected")
    if output_dir == "No folder selected" or not output_dir:
        inputs_missing.append("No output folder selected")
    if not user:
        inputs_missing.append("Please input your Iposim username")
    if not password:
        inputs_missing.append("Please input your Iposim password")
    if inputs_missing:
        for missing_message in inputs_missing:
            logger.error(missing_message)
        return False
    return True
