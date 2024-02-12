import os
import platform
import threading
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.ttk import *

from ttkthemes import ThemedTk

from constants import NAME, BUILD_ICON_PATH
from helper_functions.encryption import save_credentials, get_key, load_credentials
from helper_functions.simulation import inputs_ok
from logging_initializer import logger_init
from terminal_implementation import ConsoleUi
from web_scraper import simulation_pipeline


def threaded_button_simulation():
    if inputs_ok(
        user=user.get(),
        password=password.get(),
        filename=filename.get(),
        output_dir=output_dir.get(),
    ):
        save_credentials(
            credentials_file_path=CREDENTIALS_FILE_PATH,
            key=key,
            password=password.get(),
            filename=filename.get(),
            output_dir=output_dir.get(),
            user=user.get(),
        )
        logger.info("Starting simulation, please wait...")
        threading.Thread(target=run_simulation, daemon=True).start()


def run_simulation():
    try:
        sim_button.config(state="disabled")
        simulation_pipeline(
            user.get(), password.get(), filename.get(), output_dir.get()
        )
    except Exception as e:
        logger.error(e)
        logger.debug(
            e, exc_info=sys.exc_info()
        )  # printa mais informações para o arquivo de erro
    finally:
        sim_button.config(state="normal")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def browse_data():
    filename.set(askopenfilename(initialdir=curr_dir, title="Select simulation file"))


def get_output_dir():
    output_dir.set(askdirectory(initialdir=curr_dir, title="Select output path"))


logger = logger_init()

curr_dir = os.getcwd()
logger.debug(curr_dir)
root = ThemedTk(
    theme="breeze"
)  # themes: https://ttkthemes.readthedocs.io/en/latest/themes.html
root.title(NAME)

if platform.system() == "Windows":  # pq no linux nao consegue utilizar esse comando
    root.iconbitmap(BUILD_ICON_PATH)

user = StringVar()
password = StringVar()
filename = StringVar()
filename.set("No file selected")
output_dir = StringVar()
output_dir.set("No folder selected")

CREDENTIALS_FILE_PATH = f"{os.getenv('APPDATA')}/Iposim Automator/credentials.json"
KEY_FILE_PATH = f"{os.getenv('APPDATA')}/Iposim Automator/key.key"

key = get_key(KEY_FILE_PATH)

load_credentials(
    credentials_file_path=CREDENTIALS_FILE_PATH,
    key=key,
    password=password,
    filename=filename,
    output_dir=output_dir,
    user=user,
)

mf = Frame(root)
mf.pack(fill="both", expand=True)

input_select = Frame(master=mf)
input_select.pack(fill=X)

output_select = Frame(master=mf)
output_select.pack(fill=X)

login_info = Frame(master=mf)
login_info.pack(fill=X)

console = Frame(master=mf)
console.pack(fill="both", expand="yes")

# cria um estilo novo de texto negrito que é usado pelo botao de simulate
s = Style()
s.configure("Bold.TButton", font=("Sans", "9", "bold"))

Label(login_info, text="Iposim e-mail:").pack(padx=4, pady=4, side=LEFT)
Entry(login_info, textvariable=user, width=35).pack(padx=4, pady=4, side=LEFT)

Label(login_info, text="Iposim password:").pack(padx=4, pady=4, side=LEFT)
Entry(login_info, textvariable=password, width=34, show="*").pack(
    padx=4, pady=4, side=LEFT
)

sim_button = Button(
    login_info,
    text="Simulate",
    width=20,
    command=threaded_button_simulation,
    style="Bold.TButton",
)
sim_button.pack(fill="both", padx=4, pady=4, side=LEFT)

Button(input_select, text="Select input file", command=browse_data, width=20).pack(
    padx=4, pady=4, side=LEFT
)
Entry(input_select, textvariable=filename, state="disabled", width=101).pack(
    padx=4, pady=4, side=LEFT
)

Button(
    output_select, text="Select output folder", command=get_output_dir, width=20
).pack(padx=4, pady=4, side=LEFT)
Entry(output_select, textvariable=output_dir, state="disabled", width=101).pack(
    padx=4, pady=4, side=LEFT
)

ConsoleUi(console)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
