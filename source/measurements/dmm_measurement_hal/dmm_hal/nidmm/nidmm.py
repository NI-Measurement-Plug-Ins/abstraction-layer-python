"""NI-DMM session wrapper."""

import contextlib
from typing import Any, Dict, Generator, Optional

import nidmm
from dmm_hal.dmm import DmmBase
from dmm_hal.function import Function as DmmFunction
from ni_measurement_plugin_sdk_service.session_management import (
    BaseReservation,
    SessionInitializationBehavior,
)


class Session(DmmBase):
    """NI-DMM session wrapper."""

    @contextlib.contextmanager
    def _initialize_session(
        self,
        reservation: BaseReservation,
        reset_device: bool,
        options: Optional[Dict[str, Any]],
        initialization_behavior: SessionInitializationBehavior,
    ) -> Generator[None, None, None]:
        """Initialize an NI-DMM session.

        Args:
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
            ni_dmm_function = nidmm.Function(measurement_function.value)

            self._session.configure_measurement_digits(ni_dmm_function, range, resolution_digits)

        except ValueError:
            raise ValueError(f"Invalid function value: '{measurement_function.name}'.")

    def read(self) -> float:
        """Acquires a single measurement and returns the measured value.

        Returns:
            The measured value.
        """
        return self._session.read()

    def _validate_measurement_type(self, measurement_type: DmmFunction) -> None:
        function_names = [func.name for func in nidmm.Function]
        if measurement_type.name not in function_names:
            raise ValueError(f"Invalid function value: {measurement_type.name}")
