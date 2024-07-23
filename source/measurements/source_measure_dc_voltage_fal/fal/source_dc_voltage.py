"""An abstract class to source DC voltage."""

from abc import ABC, abstractmethod


class SourceDCVoltage(ABC):
    """An abstract class to source DC voltage."""

    @abstractmethod
    def source_dc_voltage(
        self,
        voltage_level_range: float,
        voltage_level: float,
        current_limit_range: float,
        current_limit: float,
        source_delay: float,
    ) -> None:
        """Sources a DC voltage."""
        pass
