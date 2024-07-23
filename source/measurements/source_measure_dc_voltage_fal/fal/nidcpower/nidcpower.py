"""NI-DCPower session wrapper."""

import contextlib
import threading
import time
from typing import Any, Dict, Generator, Optional

import grpc
import hightime
import nidcpower
from fal.initialize_session import InitializeSession
from fal.measure_dc_voltage import MeasureDCVoltage
from fal.source_dc_voltage import SourceDCVoltage
from ni_measurement_plugin_sdk_service.measurement.service import MeasurementContext
from ni_measurement_plugin_sdk_service.session_management import (
    BaseReservation,
    SessionInitializationBehavior,
)

_NIDCPOWER_WAIT_FOR_EVENT_TIMEOUT_ERROR_CODE = -1074116059
_NIDCPOWER_TIMEOUT_EXCEEDED_ERROR_CODE = -1074097933
_NIDCPOWER_TIMEOUT_ERROR_CODES = [
    _NIDCPOWER_WAIT_FOR_EVENT_TIMEOUT_ERROR_CODE,
    _NIDCPOWER_TIMEOUT_EXCEEDED_ERROR_CODE,
]


class Session(InitializeSession, SourceDCVoltage, MeasureDCVoltage):
    """NI-DCPower session Wrapper."""

    @contextlib.contextmanager
    def initialize_session(
        self,
        measurement_context: MeasurementContext,
        reservation: BaseReservation,
        reset_device: bool,
        options: Optional[Dict[str, Any]],
        initialization_behavior: SessionInitializationBehavior,
    ) -> Generator[None, None, None]:
        """Initialize an NI-DCPower session.

        Args:
            measurement_context: Proxy for the Measurement Service's context-local state.

            reservation: Manages initialization for the reserved session.

            reset_device: Specifies whether to reset channel(s) during the initialization procedure.

            options: Specifies the initial value of certain properties for the session.

            initialization_behavior: Specifies whether the NI gRPC Device Server will initialize a
                new session or attach to an existing session.
        """
        with reservation.initialize_nidcpower_session(
            reset_device, options, initialization_behavior
        ) as session_info:
            self._measurement_context = measurement_context
            self._channel_list = session_info.channel_list
            self._session = session_info.session
            yield
            self._session.abort()  # Aborts any ongoing sourcing before closing the session.

    def source_dc_voltage(
        self,
        voltage_level_range: float,
        voltage_level: float,
        current_limit_range: float,
        current_limit: float,
        source_delay: float,
    ) -> None:
        """Sources a DC voltage.

        Args:
            voltage_level_range: The range defines the valid values to which the voltage level can
                be set.

            voltage_level: Specifies the voltage level, in volts, that the device attempts to
                generate on the specified channel(s).

            current_limit_range: The range defines the valid values to which the current limit can
                be set.

            current_limit: Specifies the current limit, in amps, that the output cannot exceed when
                generating the desired voltage level on the specified channel(s).

            source_delay: Determines when, in seconds, the device generates the Source Complete
                event.
        """
        channels = self._session.channels[self._channel_list]
        channels.abort()  # Abort any ongoing sourcing from these channels.
        channels.source_mode = nidcpower.SourceMode.SINGLE_POINT
        channels.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        channels.voltage_level_range = voltage_level_range
        channels.voltage_level = voltage_level
        channels.source_delay = hightime.timedelta(seconds=source_delay)
        channels.current_limit = current_limit
        channels.current_limit_range = current_limit_range
        timeout = source_delay + 10.0
        channels.initiate()
        self._wait_for_event(channels, threading.Event(), nidcpower.Event.SOURCE_COMPLETE, timeout)

    def measure_dc_voltage(
        self,
        voltage_level_range: float,
        resolution_digits: float,
    ) -> float:
        """Gets a single voltage measurement.

        Args:
            voltage_level_range: This parameter is unused.

            resolution_digits: This parameter is unused.

        Returns:
            The measured voltage value.
        """
        channels = self._session.channels[self._channel_list]
        voltage_measurement: float = channels.measure(nidcpower.MeasurementTypes.VOLTAGE)
        return voltage_measurement

    def _wait_for_event(
        self,
        channels: nidcpower.session._SessionBase,
        cancellation_event: threading.Event,
        event_id: nidcpower.Event,
        timeout: float,
    ) -> None:
        """Wait for a NI-DCPower event or until error/cancellation occurs."""
        grpc_deadline = time.time() + self._measurement_context.time_remaining
        user_deadline = time.time() + timeout

        while True:
            if time.time() > user_deadline:
                raise TimeoutError("User timeout expired.")
            if time.time() > grpc_deadline:
                self._measurement_context.abort(
                    grpc.StatusCode.DEADLINE_EXCEEDED, "Deadline exceeded."
                )
            if cancellation_event.is_set():
                self._measurement_context.abort(
                    grpc.StatusCode.CANCELLED, "Client requested cancellation."
                )

            try:
                channels.wait_for_event(event_id, timeout=100e-3)
                break
            except nidcpower.errors.DriverError as e:
                if e.code in _NIDCPOWER_TIMEOUT_ERROR_CODES:
                    pass
                raise
