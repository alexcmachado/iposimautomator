# Iposim Automator

This program automates semiconductor loss simulations performed through Iposim, a simulation tool from the Infineon company.

Simulations are conducted using the topology of a 2-level three-phase inverter, as shown in the image below:

![Inverter Topology](src/images/inverter.png)

## Tutorial

The instructions below will provide the necessary information to install and run the program correctly.

### Prerequisites

To run this program, you need to have Mozilla Firefox version 60 or higher, which can be downloaded [here](https://www.mozilla.org/pt-BR/firefox/new/).

### Installation

Download and install the file available [here](https://www.dropbox.com/sh/lt8700hnuhdy7km/AAAf3Y26jIrxC3CnyxlRQFg2a).

### Using the program

1. Open the program from the shortcut generated on the desktop.

2. Using the **"Select input file"** button, choose the file with the table containing the information for the simulations you want to run. An example file is provided in the **"examples"** folder where the program was installed. It is important that the names of the pre-existing columns in the simulation file <ins>are not changed</ins>.

3. Use the **"Select output folder"** button to define the folder where the simulation results file will be saved.

4. Enter your Iposim website login details in the **"Iposim e-mail"** and **"Iposim password"** fields. If you don't have an account, you can create a new one [here](https://www.infineon.com/cms/en/#register).

5. After entering the data, use the **"Simulate"** button and wait for the simulation to finish, observing the information on the screen. At the end, the results file will be available in the chosen folder.

![Example](src/images/example.png)

## Authors

- **Alex Costa Machado**
