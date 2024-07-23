"""DMM Measurement Types."""

from enum import Enum


class Function(Enum):
    """DMM Measurement Types."""

    NONE = 0
    DC_VOLTS = 1
    AC_VOLTS = 2
    DC_CURRENT = 3
    AC_CURRENT = 4
    TWO_WIRE_RES = 5
    FOUR_WIRE_RES = 101
    FREQ = 104
    PERIOD = 105
    TEMPERATURE = 108
    AC_VOLTS_DC_COUPLED = 1001
    DIODE = 1002
    WAVEFORM_VOLTAGE = 1003
    WAVEFORM_CURRENT = 1004
    CAPACITANCE = 1005
    INDUCTANCE = 1006
