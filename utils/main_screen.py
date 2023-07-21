from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import numpy as np
from classes.plotter import Plot
from utils.constants import CHANNELS, RATE
from utils.helpers import PlotOptions
from typing import TypeVar


PlotChild = TypeVar('PlotChild', bound=Plot)


class MainScreenException(BaseException):
    pass


class MainScreen(QDialog):
    def __init__(self, plotter: type(PlotChild) = None):
        super(MainScreen, self).__init__()
        loadUi("gui.ui", self)
        self._output_data_index = 0
        self._started = False
        self._pixmap = QPixmap('background.jpg')
        self._label = QLabel(self)
        self._plot_object = plotter or Plot()

    def load_gui_data(self, devices_list: list = None):
        """
        Function that receives input/output devices list and loads GUI data.
        Devices list is used to populate a combo box/dropdown.
        :param devices_list: list of devices
        """
        # adding list of items to combo box
        if devices_list is None:
            raise MainScreenException('Not enough input arguments were given.')
        self.comboBox.addItems(devices_list)
        # setting current item
        self.start_button.clicked.connect(self._on_click_start)
        self.pause_button.clicked.connect(self._on_click_pause)
        self._label.setPixmap(self._pixmap)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.lower()
        self.setWindowTitle('Reflection Measurment')
        self.f_min.setToolTip('Minimun frequency 100Hz')
        self.f_max.setToolTip('Maximum frequency 1000Hz')
        self.t_sample.setToolTip('Sampling period in seconds. Recommended (1-10)s')
        self.radio_butt_abs.setToolTip('Select if want to plot absorption')
        self.radio_butt_ref.setToolTip('Select if want to plot reflection')
        self.radio_butt_ref.setChecked(True)
        self.start_button.setToolTip('Click to start measure')
        self.pause_button.setToolTip('Click to stop measure')

    def _on_click_start(self):
        """
        Function that runs after clicking button start. In this case it start plotting
        if isn't already.
        """
        from utils.stream import AudioStream

        mic = self.comboBox.currentIndex()
        plot_signal = PlotOptions(self.radio_butt_abs.isChecked()).value
        period = int(self.t_sample.text())

        # Plot limits
        if not self._plot_object.started:
            self._plot_object.started = True
            audio_stream = AudioStream(
                channels=CHANNELS,
                rate=RATE,
                chunk=(period * RATE),
                input_device=mic
            )

            f = np.arange(-RATE / 2, RATE / 2, RATE / (period * RATE))  # Frequency to plot

            self._plot_object.create_figures(
                x_data=f,
                y_data=np.random.rand(period * RATE)
            )

            self._plot_object.set_axis_limits(
                f_min=int(self.f_min.text()),
                f_max=int(self.f_max.text())
            )

            self._plot_object.plot(
                plot_selection=plot_signal,
                audio_stream=audio_stream,
                export_data=self.export_cb.isChecked(),
                x_data=f
            )

    def _on_click_pause(self):
        """
        Function that runs after clicking button pause. In this case it ends plotting
        if plot is open.
        """
        if self._plot_object.started:
            self._plot_object.started = False
