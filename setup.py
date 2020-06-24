import sys
sys.path.append('./src')

from cx_Freeze import setup, Executable

from constants import BUILD_ICON_PATH, NAME, VERSION, DESCRIPTION, AUTHOR


include_files = [
    "./src/drivers/geckodriver.exe",
    "./example/input.xlsx",
    "./example/results.xlsx",
    "./src/config.json",
    BUILD_ICON_PATH,
    "./src/images/example.png",
    "./src/images/inverter.png",
    "./README.html",
]
include_files_pairs = [(file_path, file_path) for file_path in include_files]

build_exe_options = {"include_files": include_files_pairs}

shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory_
        NAME,  # Name
        "TARGETDIR",  # Component_
        "[TARGETDIR]iposim.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        False,  # ShowCmd
        "TARGETDIR",  # WkDir
    )
]

# controla o que aparece no control panel
bdist_msi_options = {
    "install_icon": BUILD_ICON_PATH,
    "data": {"Shortcut": shortcut_table},
}

# para que nao abra o CMD quando executar o exe
base = None
if sys.platform == "win32":
    base = "Win32GUI"

shortcutName = NAME
shortcutDir = "DesktopFolder"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=[
        Executable(
            "./src/iposim.py",
            base=base,
            shortcutName=shortcutName,
            shortcutDir=shortcutDir,
            icon=BUILD_ICON_PATH,
        )
    ],  # icon controla o que aparece no desktop
)
