"""Source DC voltage using NI SMU and measure the same using an NI SMU or DMM."""

import logging
import pathlib
import sys
from typing import Tuple

import click
import ni_measurement_plugin_sdk_service as nims
from _helpers import configure_logging, verbosity_option
from fal.measure_dc_voltage import MeasureDCVoltage
from fal.session_helper import initialize
from fal.source_dc_voltage import SourceDCVoltage

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "SourceMeasureDCVoltageFAL.serviceconfig",
    version="1.0.0.0",
    ui_file_paths=[service_directory / "SourceMeasureDCVoltageFAL.measui"],
)


@measurement_service.register_measurement
@measurement_service.configuration("voltage_level", nims.DataType.Double, 6.0)
@measurement_service.configuration("voltage_level_range", nims.DataType.Double, 6.0)
@measurement_service.configuration("current_limit", nims.DataType.Double, 0.1)
@measurement_service.configuration("current_limit_range", nims.DataType.Double, 0.1)
@measurement_service.configuration("source_delay", nims.DataType.Double, 0.0)
@measurement_service.configuration(
    "source_pin",
    nims.DataType.IOResource,
    "NI_DCPower_Pin",
    instrument_type=nims.session_management.INSTRUMENT_TYPE_NI_DCPOWER,
)
@measurement_service.configuration("resolution_digits", nims.DataType.Double, 5.5)
@measurement_service.configuration("measure_pin", nims.DataType.IOResource, "NI_DMM_Pin")
@measurement_service.output("measured_value", nims.DataType.Double)
def measure(
    voltage_level: float,
    voltage_level_range: float,
    current_limit: float,
    current_limit_range: float,
    source_delay: float,
    source_pin: str,
    resolution_digits: float,
    measure_pin: str,
) -> Tuple[float]:
    """Source DC voltage using NI SMU and measure the same using an NI SMU or DMM.

    Args:
        voltage_level: The voltage level to source.

        voltage_level_range: The range defines the valid values to which the voltage level can be
            set. 

        current_limit: The current limit to set.

        current_limit_range: The range defines the valid values to which the current limit can be
            set. 

        source_delay: Determines when, in seconds, the device generates the Source Complete event.

        source_pin: The pin name to which the source instrument session is connected.

        resolution_digits: The number of digits to which the measurement is rounded.

        measure_pin: The pin name to which the measure instrument session is connected.

    Returns:
        The measured voltage value.
    """
    logging.info(
        """Starting measurement: pin_names=%s voltage_level=%g voltage_level_range=%g
        current_limit=%g current_limit_range=%g source_delay=%g resolution_digits=%g""",
        [source_pin, measure_pin],
        voltage_level,
        voltage_level_range,
        current_limit,
        current_limit_range,
        source_delay,
        resolution_digits,
    )

    with initialize(
        measurement_context=measurement_service.context,
        pin_names=[source_pin, measure_pin],
    ) as sessions:
        source_session: SourceDCVoltage = sessions[source_pin]
        source_session.source_dc_voltage(
            voltage_level_range=voltage_level_range,
            voltage_level=voltage_level,
            current_limit_range=current_limit_range,
            current_limit=current_limit,
            source_delay=source_delay,
        )
        measure_session: MeasureDCVoltage = sessions[measure_pin]
        measured_value = measure_session.measure_dc_voltage(
            voltage_level_range=voltage_level_range,
            resolution_digits=resolution_digits,
        )
    return (measured_value,)


@click.command
@verbosity_option
def main(verbosity: int) -> None:
    """Source DC voltage using NI SMU and measure the same using an NI SMU or DMM."""
    configure_logging(verbosity)

    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
