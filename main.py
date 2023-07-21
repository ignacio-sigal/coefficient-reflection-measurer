"""
Main file
"""
import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from utils.helpers import get_input_output_devices_names
from utils.main_screen import MainScreen
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from utils.plot import ReflectionPlot


def main_app():
    """
    This function is executed after installing dependencies. It instantiate the necessary classes
    and then shows the main screen.
    """
    # Getting list of input devices
    devices_list = get_input_output_devices_names()

    # Defining application
    app = QApplication(sys.argv)

    # Instantiate ReflectionPlot class
    reflection_plot = ReflectionPlot()

    # Instantiate and build main screen
    main_screen = MainScreen(reflection_plot)
    main_screen.load_gui_data(devices_list)

    # Instantiate widget and setting values to show.
    widget = QStackedWidget()
    widget.addWidget(main_screen)
    widget.setFixedWidth(WINDOW_WIDTH)
    widget.setFixedHeight(WINDOW_HEIGHT)
    widget.show()
    try:
        sys.exit(app.exec())
    except SystemExit as error:
        print(error)
