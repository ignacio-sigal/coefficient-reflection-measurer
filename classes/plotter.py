"""
Plotter class
"""
from abc import ABC, abstractmethod


class Plot(ABC):
    """
    This abc class is intended to be used when a plot must be done.
    """
    @abstractmethod
    def __init__(self, *args):
        """
        Abstract method
        """

    @abstractmethod
    def set_axis_limits(self, **kwargs):
        """
        Abstract method
        """

    @abstractmethod
    def plot(self, **kwargs):
        """
        Abstract method
        """

    @property
    @abstractmethod
    def started(self, *args):
        """
        Property
        """
