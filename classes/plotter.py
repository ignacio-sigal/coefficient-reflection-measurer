from abc import ABC, abstractmethod


class Plot(ABC):
    @abstractmethod
    def __init__(self, *args):
        """
        Abstract method
        """
        ...

    @abstractmethod
    def set_axis_limits(self, **kwargs):
        """
        Abstract method
        """
        ...

    @abstractmethod
    def plot(self, **kwargs):
        """
        Abstract method
        """
        ...

    @property
    @abstractmethod
    def started(self, *args):
        """
        Property
        """
        ...
