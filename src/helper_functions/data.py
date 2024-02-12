"""Parses the input file and generates the URL for the simulation."""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ColumnUnavailable(Exception):
    """Exception raised when a column is not available in the input file."""


def generate_url(df, row_number):
    """Generates the URL for the simulation based on the input file data."""
    try:
        dc_voltage = str(df["DC Link Voltage [V]"][row_number])
        blocking_voltage = str(df["Blocking Voltage [V]"][row_number])
        current = f"{df["Output Current [A]"][row_number]:.2f}"
        output_frequency = str(df["Output Frequency [Hz]"][row_number])
        sw_frequency = str(df["Switching Frequency [Hz]"][row_number])
        modi = str(df["Modulation Index"][row_number])
        power_factor = str(df["Power Factor"][row_number])
        module = str(df["Module"][row_number])
        hs_temp = str(df["Heatsink Temperature [°C]"][row_number])
        gate_res = str(df["Gate Resistor [Ohm]"][row_number])
        url = (
            "https://iposim.infineon.com/application/en/results?"
            f"topology:DC-AC_3P_2L,simType:steady-state,appDataTab:tab-advanced,"
            f"loadcycle:(lcp:none,filename:none),common:(Vdc_d:{dc_voltage},"
            f"Vblock:{blocking_voltage},Inom:{current},package:All,mod_scheme:1,"
            f"Vdc:{dc_voltage},Irms:{current},fout:{output_frequency},fsw:{sw_frequency},"
            f"t_pulse:180,modi:{modi},cos_phi:{power_factor},cos_phi_sign:2,"
            f"Parts:{module},Tref:{hs_temp},good_voltage_threshold:420),"
            f"setups:(Setup%201:(primary_device:{module},heatsink_model:3,"
            f"heatsink_coefficient:0.5,cooling_method:2,heatsink:3,ph_Ta:40,"
            f"Rth_ca:0.63,ph_tau:40,ud_Ta:40,Rth:!((Rth:0.36,Tao:70),(Rth:0,Tao:1),"
            f"(Rth:0,Tao:1),(Rth:0,Tao:1),(Rth:0,Tao:1)),t_heatsink:{hs_temp},"
            f"cooling_method_atv:1,flow_rate:!n,t_coolant:65,advanced_param_options:standard,"
            f"Switch1Rgon:{gate_res},Switch1Rgoff:{gate_res},r_g_on_fast:{gate_res},"
            f"r_g_on_slow:{gate_res},r_g_off_fast:{gate_res},r_g_off_slow:{gate_res},"
            f"i_2l_src:10,Rgon_slow:{gate_res},Rgoff_slow:{gate_res},Switch1TvjopMax:150,"
            f"Diode1TvjopMax:150,Switch1Inom:100))"
        )
        logger.info(
            "--------------------------------------------------------------------\nParameters:"
        )
        logger.info(
            "    Module: %s / DC Link Voltage: %s V / Current: %s A",
            module,
            dc_voltage,
            current,
        )
        logger.info(
            "    Output Frequency: %s Hz / Switching Frequency: %s Hz / Modulation Index: %s",
            output_frequency,
            sw_frequency,
            modi,
        )
        logger.info(
            "    Power Factor: %s / Heatsink Temperature: %s °C / Gate Resistor: %s Ohm",
            power_factor,
            hs_temp,
            gate_res,
        )
        return url
    except KeyError as exc:
        raise ColumnUnavailable(
            f"Column {exc} not found, please correct the column name on the input file and retry."
        ) from exc


def create_dict_from_excel(workbook):
    """Create a dictionary from the input file data."""
    sheet = workbook.active
    return {col[0]: col[1:] for col in zip(*sheet.values)}


def add_column(worksheet, column):
    """Add a column to the output file."""
    new_column = worksheet.max_column + 1

    for rowy, value in enumerate(column, start=1):
        worksheet.cell(row=rowy, column=new_column, value=value)

    return worksheet


def append_results_and_save(workbook, results_dict, output_dir=None):
    """Append the results to the output file and save it to the output directory."""
    if not output_dir:
        output_dir = os.getcwd()

    sheet = workbook.active

    max_switch_jun_temp_col = [
        "Maximum Switch Junction Temperature [°C]",
        *results_dict["Maximum Junction Temperature"]["Switch"],
    ]
    max_diode_jun_temp_col = [
        "Maximum Diode Junction Temperature [°C]",
        *results_dict["Maximum Junction Temperature"]["Diode"],
    ]
    total_switch_losses_col = [
        "Total Switch Losses [W]",
        *results_dict["Total Losses"]["Switch"],
    ]
    total_diode_losses_col = [
        "Total Diode Losses [W]",
        *results_dict["Total Losses"]["Diode"],
    ]

    add_column(sheet, max_switch_jun_temp_col)
    add_column(sheet, max_diode_jun_temp_col)
    add_column(sheet, total_switch_losses_col)
    add_column(sheet, total_diode_losses_col)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(output_dir, f"results_{dt_string}.xlsx")
    workbook.save(filename=output_path)
    logger.info("Results saved to %s", output_path)
