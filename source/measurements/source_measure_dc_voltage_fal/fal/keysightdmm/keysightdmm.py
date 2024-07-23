"""NI-VISA session wrapper for Keysight DMM."""

from __future__ import annotations

import contextlib
import pathlib
from typing import Any, Dict, Generator, Optional

from decouple import AutoConfig
from fal.initialize_session import InitializeSession
from fal.keysightdmm import _keysight_dmm
from fal.keysightdmm._keysight_dmm_session_management import (
    KeysightDmmSessionConstructor,
)
from fal.measure_dc_voltage import MeasureDCVoltage
from ni_measurement_plugin_sdk_service.measurement.service import MeasurementContext
from ni_measurement_plugin_sdk_service.session_management import (
    BaseReservation,
    SessionInitializationBehavior,
)

# Search for the `.env` file starting with the current directory.
_config = AutoConfig(str(pathlib.Path.cwd()))


class Session(InitializeSession, MeasureDCVoltage):
    """NI-VISA session wrapper for Keysight DMM."""

    @contextlib.contextmanager
    def initialize_session(
        self,
        measurement_context: MeasurementContext,
        reservation: BaseReservation,
        reset_device: bool,
        options: Optional[Dict[str, Any]],
        initialization_behavior: SessionInitializationBehavior,
    ) -> Generator[None, None, None]:
        """Initialize a Keysight DMM session.

        Args:
            measurement_context: This parameter is unused.

            reservation: Manages initialization for the reserved session.

            reset_device: Specifies whether to reset channel(s) during the initialization procedure.

            options: This parameter is unused.

            initialization_behavior: Specifies whether the NI gRPC Device Server will initialize a
                new session or attach to an existing session.
        """
        session_constructor = KeysightDmmSessionConstructor(
            _config, reservation._discovery_client, reset_device, initialization_behavior
        )
        with reservation.initialize_session(
            session_constructor, _keysight_dmm.INSTRUMENT_TYPE_ID
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
        keysight_dmm_function = _keysight_dmm.Function.DC_VOLTS
        self._session.configure_measurement_digits(
            keysight_dmm_function, voltage_level_range, resolution_digits
        )
        return self._session.read()
