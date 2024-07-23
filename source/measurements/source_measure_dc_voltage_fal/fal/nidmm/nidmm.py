"""NI-DMM session wrapper."""

import contextlib
from typing import Any, Dict, Generator, Optional

import nidmm
from fal.initialize_session import InitializeSession
from fal.measure_dc_voltage import MeasureDCVoltage
from ni_measurement_plugin_sdk_service.measurement.service import MeasurementContext
from ni_measurement_plugin_sdk_service.session_management import (
    BaseReservation,
    SessionInitializationBehavior,
)


class Session(InitializeSession, MeasureDCVoltage):
    """NI-DMM session wrapper."""

    @contextlib.contextmanager
    def initialize_session(
        self,
        measurement_context: MeasurementContext,
        reservation: BaseReservation,
        reset_device: bool,
        options: Optional[Dict[str, Any]],
        initialization_behavior: SessionInitializationBehavior,
    ) -> Generator[None, None, None]:
        """Initialize a NI-DMM session.

        Args:
            measurement_context: This parameter is unused.

            reservation: Manages initialization for the reserved session.

            reset_device: Specifies whether to reset channel(s) during the initialization procedure.

            options: Specifies the initial value of certain properties for the session.

            initialization_behavior: Specifies whether the NI gRPC Device Server will initialize a
                new session or attach to an existing session.
        """
        with reservation.initialize_nidmm_session(
            reset_device, options, initialization_behavior=initialization_behavior
        ) as session_info:
            self._session = session_info.session
            yield

    def measure_dc_voltage(
        self,
        voltage_level_range: float,
        resolution_digits: float,
    ) -> float:
        """Gets a single voltage measurement.

        Args:
            voltage_level_range: The range defines the valid values to which the voltage level can
                be set.

            resolution_digits: The number of digits to which the measurement is rounded.

        Returns:
            The measured voltage value.
        """
        ni_dmm_function = nidmm.Function.DC_VOLTS
        self._session.configure_measurement_digits(
            ni_dmm_function, voltage_level_range, resolution_digits
        )

        return self._session.read()
