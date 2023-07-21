from abc import ABC, abstractmethod


class Plot(ABC):
    @abstractmethod
    def __init__(self, *args):
        """
        Abstract method
        """
        pass

    @abstractmethod
    def set_axis_limits(self, **kwargs):
        """
        Abstract method
        """
        pass

    @abstractmethod
    def plot(self, **kwargs):
        """
        Abstract method
        """
        pass

    @property
    @abstractmethod
    def started(self, *args):
        """
        Property
        """
        pass
