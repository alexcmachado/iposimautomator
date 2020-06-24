import logging

import openpyxl

from constants import LOGIN_PAGE
from driver_initializer import driver_init
from helper_functions.data import create_dict_from_excel
from helper_functions.user import login
from helper_functions.simulation import run_all_simulations_and_save

logger = logging.getLogger(__name__)


def simulation_pipeline(user, password, filepath, output_dir):
    workbook = openpyxl.load_workbook(filepath)
    data = create_dict_from_excel(workbook=workbook)
    driver = driver_init()
    login(LOGIN_PAGE, user, password, driver)
    run_all_simulations_and_save(data, driver, workbook, output_dir)

