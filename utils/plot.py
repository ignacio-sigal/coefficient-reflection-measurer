"""
This file contains the definition of ReflectionPlot class with its methods along with
the definition of custom exception
In order to be used properly certain criteria must be met.
The builder pattern that must be followed is the following:
    1. Call the create_figures method in order to define subplots.

    2. Call set_axis_limits to set figures sizes.

    3. Start plotting by calling plot method.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils.helpers import decode, process_raw_data, PlotOptions
from utils.constants import CHANNELS, MIN_FREQUENCY, MAX_FREQUENCY
from classes.plotter import Plot
from utils.stream import AudioStream


class PlotException(BaseException):
    """Custom exception"""


class ReflectionPlot(Plot):
    """
    This class is the one intended to plot the coefficient measurement.
    """

    def __init__(self):
        super().__init__()
        self._plot_started = False
        self.reflection_coefficient = np.ndarray(0)
        self.absorption_coefficient = 1 - abs(self.reflection_coefficient) ** 2
        self.y_axis_fft = None
        self.absorption = None
        self.output_data_index = 0
        self.fig = None
        self.line = None
        self.line2 = None
        self.f_min = 100
        self.f_max = 1000
        pass

    @property
    def started(self) -> bool:
        """
        Property. Returns True if the plot is active, False if not.
        """
        return self._plot_started

    @started.setter
    def started(self, status: bool = None):
        """
        Setter of the property started.
        """
        if not isinstance(status, bool):
            raise PlotException(
                f"Wrong datatype was given. Expected bool got {type(status)}"
            )
        self._plot_started = status

    def _show_plot(self, plot_selection: int):
        """
        Function to show data obtained from input source.
        :param plot_selection: Used to decide whether absorption or reflection has to be plotted
        """
        plot_data = (
            self.reflection_coefficient
            if plot_selection == PlotOptions.REFLECTION_COEFFICIENT.value
            else (1 - abs(self.reflection_coefficient) ** 2)
        )
        self.line.set_ydata(abs(plot_data))
        self.line2.set_ydata(abs(self.y_axis_fft))
        self.fig.canvas.flush_events()
        self.fig.canvas.draw()

    def _export_data(self, plot_selection: int, f: list):
        """
        THis function exports plot data to a csv.
        :param plot_selection:
        :param f:
        """
        # Exporting plot data to CSV file
        f_round = [round(item, 1) for item in f]
        low_freq = list(f_round).index(float(self.f_min))
        high_freq = list(f_round).index(float(self.f_max))

        export_data = (
            self.reflection_coefficient
            if (plot_selection == PlotOptions.REFLECTION_COEFFICIENT.value)
            else self.absorption_coefficient
        )

        output_data = {
            "Frequency": f[low_freq:high_freq],
            PlotOptions(plot_selection).name.lower(): abs(
                export_data[low_freq:high_freq]
            ),
        }

        output_data_pd = pd.DataFrame(output_data)
        file_name = f"{PlotOptions(plot_selection).name.lower().lower()}_{self.output_data_index}.csv"
        output_data_pd.to_csv(file_name, index=False, sep=";")

    def init_figures(
        self,
        x_data,
        y_data,
        f_min,
        f_max,
        coef_lower: float = 0,
        coef_higher: float = 1.25,
        power_lower: float = 0,
        power_higher: float = 0.025,
    ):
        """
        This function is the one in charge of creating and defining plot size.
        :param x_data:
        :param y_data:
        :param f_min:
        :param f_max:
        :param coef_lower:
        :param coef_higher:
        :param power_lower:
        :param power_higher:
        """
        self.fig, (self.plot_r, self.plot_power) = plt.subplots(2, figsize=(15, 7))
        (self.line,) = self.plot_r.semilogx(x_data, y_data, "-", lw=2)
        (self.line2,) = self.plot_power.semilogx(x_data, y_data, "-", lw=2)
        self.f_min = (
            f_min if f_min in range(MIN_FREQUENCY, MAX_FREQUENCY) else self.f_min
        )
        self.f_max = f_max if f_max in range(self.f_min, MAX_FREQUENCY) else self.f_max
        self.plot_r.set_ylim(coef_lower, coef_higher)
        self.plot_r.set_xlim(self.f_min, self.f_max)
        self.plot_power.set_ylim(power_lower, power_higher)
        self.plot_power.set_xlim(self.f_min, self.f_max)

    def plot(
        self,
        plot_selection: int,
        audio_stream: type(AudioStream),
        export_data: bool,
        x_data: type(np.ndarray),
    ):
        """
        This function will update plot information with AudioStream data.
        :param plot_selection:
        :param audio_stream:
        :param export_data:
        :param x_data:
        """
        plt.show(block=False)
        while self._plot_started:
            # Binary data
            data = audio_stream.input_data
            decoded_data = decode(data, audio_stream.chunk, CHANNELS)

            self.output_data_index += 1

            self.reflection_coefficient, self.y_axis_fft = process_raw_data(
                x_data, decoded_data
            )
            self._show_plot(plot_selection)
            if export_data:
                self._export_data(plot_selection, x_data)
        plt.close()
        audio_stream.close()
