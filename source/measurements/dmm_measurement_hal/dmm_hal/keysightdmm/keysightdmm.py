"""NI-VISA session wrapper for Keysight DMM."""

from __future__ import annotations

import contextlib
import pathlib
from typing import Any, Dict, Generator, Optional

from decouple import AutoConfig
from dmm_hal.dmm import DmmBase
from dmm_hal.function import Function as DmmFunction
from dmm_hal.keysightdmm import _keysight_dmm
from dmm_hal.keysightdmm._keysight_dmm_session_management import (
    KeysightDmmSessionConstructor,
)
from ni_measurement_plugin_sdk_service.session_management import (
    BaseReservation,
    SessionInitializationBehavior,
)

# Search for the `.env` file starting with the current directory.
_config = AutoConfig(str(pathlib.Path.cwd()))


class Session(DmmBase):
    """NI-VISA session wrapper for Keysight DMM."""

    @contextlib.contextmanager
    def _initialize_session(
        self,
        reservation: BaseReservation,
        reset_device: bool,
        options: Optional[Dict[str, Any]],
        initialization_behavior: SessionInitializationBehavior,
    ) -> Generator[None, None, None]:
        """Initialize a Keysight DMM session.

        Args:
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

    def configure_measurement_digits(
        self,
        measurement_function: DmmFunction,
        range: float,
        resolution_digits: float,
    ) -> None:
        """Configure the common properties of the measurement.

        Args:
            measurement_function: DMM Measurement Types.

            range: The range defines the valid values to which the measurement can be set.

            resolution_digits: The number of digits to which the measurement is rounded.
        """
        try:
            self._validate_measurement_type(measurement_function)

            """These properties include method, range, and resolution_digits."""
            keysight_dmm_function = _keysight_dmm.Function(measurement_function.value)

            self._session.configure_measurement_digits(
                keysight_dmm_function, range, resolution_digits
            )

        except ValueError:
            raise ValueError(f"Invalid function value: '{measurement_function.name}'.")

    def read(self) -> float:
        """Acquires a single measurement and returns the measured value.

        Returns:
            The measured value.
        """
        return self._session.read()

    def _validate_measurement_type(self, measurement_type: DmmFunction) -> None:
        function_names = [func.name for func in DmmFunction]
        if measurement_type.name not in function_names:
            raise ValueError(f"Invalid function value: {measurement_type.name}")
