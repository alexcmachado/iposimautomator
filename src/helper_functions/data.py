import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ColumnUnavailable(Exception):
    pass


def generate_url(df, row_number):
    try:
        dc_voltage = str(df["DC Link Voltage [V]"][row_number])
        blocking_voltage = str(df["Blocking Voltage [V]"][row_number])
        current = "{:.2f}".format((df["Output Current [A]"][row_number]))
        output_frequency = str(df["Output Frequency [Hz]"][row_number])
        sw_frequency = str(df["Switching Frequency [Hz]"][row_number])
        modi = str(df["Modulation Index"][row_number])
        power_factor = str(df["Power Factor"][row_number])
        module = str(df["Module"][row_number])
        hs_temp = str(df["Heatsink Temperature [°C]"][row_number])
        gate_res = str(df["Gate Resistor [Ohm]"][row_number])
        url = (
            "https://iposim.infineon.com/application/en/results?topology:DC-AC_3P_2L,inputs:(mod_scheme:2,Vdc:{},"
            "Vblock:{},Irms:{},fout:{},fsw:{},t_pulse:180,modi:{},cos_phi:{},load_cycle:False),devices:({}:(thermal:("
            "model:3,Tc:{}),advanced:(Rgon_1:{},Rgoff_1:{}))),diode:(),package:All,search:{},isOld:0,"
            "appdatatab:tab-advanced,interpolation:!t,cycle_defined:!f,cycle_count:5,sim_bvr:1,mode:normal,lcp:"
            "none ".format(
                dc_voltage,
                blocking_voltage,
                current,
                output_frequency,
                sw_frequency,
                modi,
                power_factor,
                module,
                hs_temp,
                gate_res,
                gate_res,
                module,
            )
        )
        logger.info(
            "--------------------------------------------------------------------\nParameters:"
        )
        logger.info(
            "    Module: {} / DC Link Voltage: {} V / Current: {} A".format(
                module, dc_voltage, current
            )
        )
        logger.info(
            "    Output Frequency: {} Hz / Switching Frequency: {} Hz / Modulation Index: {}".format(
                output_frequency, sw_frequency, modi
            )
        )
        logger.info(
            "    Power Factor: {} / Heatsink Temperature: {} °C / Gate Resistor: {} Ohm".format(
                power_factor, hs_temp, gate_res
            )
        )
        return url
    except KeyError as e:
        raise ColumnUnavailable(f"Column {e} not found, please correct the column name on the input file and retry.")


def create_dict_from_excel(workbook):
    sheet = workbook.active
    return {col[0]: col[1:] for col in zip(*sheet.values)}


def add_column(worksheet, column):
    new_column = worksheet.max_column + 1

    for rowy, value in enumerate(column, start=1):
        worksheet.cell(row=rowy, column=new_column, value=value)

    return worksheet


def append_results_and_save(workbook, results_dict, output_dir=None):
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
    logger.info(f"Results saved to {output_path}")
