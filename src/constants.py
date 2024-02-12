"""Constants used in the Automator package."""

# package details
NAME = "Iposim Automator"
VERSION = "2.0"
DESCRIPTION = "An automated Iposim simulator"
AUTHOR = "Alex Costa Machado"
BUILD_ICON_PATH = "./src/images/iposim.ico"

# driver
# HEADLESS = True
# WITH_PROXY = False
MAX_SIMULATION_TIME = 300
PAGE_LOAD_TIMEOUT = 15
LOGIN_PAGE = r"https://iposim.infineon.com/application"

# logging
LOG_FILE_NAME = "iposim.log"
MAX_LOG_FILE_SIZE = 5 * 10**6  # in mb
