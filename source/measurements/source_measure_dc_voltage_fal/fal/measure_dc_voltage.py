"""An abstract class to measure DC voltage."""

from abc import ABC, abstractmethod


class MeasureDCVoltage(ABC):
    """An abstract class to measure DC voltage."""

    @abstractmethod
    def measure_dc_voltage(
        self,
        voltage_level_range: float,
        resolution_digits: float,
    ) -> float:
        """Acquires and returns a single measurement value."""
        pass
