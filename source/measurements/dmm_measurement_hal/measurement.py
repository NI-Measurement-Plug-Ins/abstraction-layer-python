"""Perform a measurement using an DMM."""

import logging
import pathlib
import sys
from typing import Tuple

import click
import ni_measurement_plugin_sdk_service as nims
from _helpers import configure_logging, verbosity_option
from dmm_hal.dmm import initialize
from dmm_hal.function import Function as DmmFunction

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "DmmMeasurementHAL.serviceconfig",
    version="1.0.0.0",
    ui_file_paths=[service_directory / "DmmMeasurementHAL.measui"],
)


@measurement_service.register_measurement
@measurement_service.configuration("pin_name", nims.DataType.IOResource, "NI_DMM_Pin")
@measurement_service.configuration(
    "measurement_type",
    nims.DataType.Enum,
    DmmFunction.DC_VOLTS,
    enum_type=DmmFunction,
)
@measurement_service.configuration("range", nims.DataType.Double, 10.0)
@measurement_service.configuration("resolution_digits", nims.DataType.Double, 5.5)
@measurement_service.output("measured_value", nims.DataType.Double)
def measure(
    pin_name: str,
    measurement_type: DmmFunction,
    range: float,
    resolution_digits: float,
) -> Tuple[float]:
    """Perform a measurement using an DMM."""
    
    logging.info(
        "Starting measurement: pin_name=%s measurement_type=%s range=%g resolution_digits=%g",
        pin_name,
        measurement_type,
        range,
        resolution_digits,
    )

    with initialize(measurement_context=measurement_service.context, pin_name=pin_name) as dmm:
        dmm.configure_measurement_digits(measurement_type, range, resolution_digits)
        measured_value = dmm.read()

    logging.info("Completed measurement: measured_value=%g", measured_value)
    return (measured_value,)


@click.command
@verbosity_option
def main(verbosity: int) -> None:
    """Perform a measurement using an DMM."""
    configure_logging(verbosity)

    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
