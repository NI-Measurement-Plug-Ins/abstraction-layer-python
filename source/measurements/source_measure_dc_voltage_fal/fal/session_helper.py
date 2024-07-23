"""Defines the session initialization functions."""

import contextlib
import importlib
from typing import Any, Dict, Generator, Iterable, List, Optional, Union

from fal.initialize_session import InitializeSession
from ni_measurement_plugin_sdk_service.measurement.service import MeasurementContext
from ni_measurement_plugin_sdk_service.session_management import (
    PinMapContext,
    SessionInformation,
    SessionInitializationBehavior,
    SessionManagementClient,
)


def _get_instrument_session(instrument_type_id: str) -> Any:
    """Creates a FAL object based on the instrument type id."""
    try:
        driver_module_path = f"fal.{instrument_type_id}.{instrument_type_id}".lower()
        driver_module = importlib.import_module(driver_module_path)
        session = getattr(driver_module, "Session")
        return session()

    except ImportError:
        raise ValueError(f"No driver found for instrument type: '{instrument_type_id}'.")


@contextlib.contextmanager
def initialize(
    measurement_context: MeasurementContext,
    pin_names: Union[Iterable[str], str],
    reset_device: bool = False,
    options: Optional[Dict[str, Any]] = None,
    initialization_behavior: SessionInitializationBehavior = SessionInitializationBehavior.AUTO,
) -> Generator[Dict[str, Any], None, None]:
    """Initialize the instrument session(s).

    Args:
        measurement_context: Proxy for the Measurement Service's context-local state.

        pin_names: Pin names to initialize the respective instrument session(s).

        reset_device: Specifies whether to reset channel(s) during the initialization procedure.

        options: Specifies the initial value of certain properties for the session. If this argument
            is not specified, the default value is an empty dict.

        initialization_behavior: Specifies whether the NI gRPC Device Server will initialize a new
            session or attach to an existing session.

    Yields:
        A dictionary of pin names and their corresponding session objects.
    """
    with contextlib.ExitStack() as stack:
        reservation = stack.enter_context(measurement_context.reserve_sessions(pin_names))
        sessions_by_pin_names = {}
        for session_info in reservation.session_info:
            session: InitializeSession = _get_instrument_session(session_info.instrument_type_id)
            stack.enter_context(
                session.initialize_session(
                    measurement_context, reservation, reset_device, options, initialization_behavior
                )
            )

            for channel in session_info.channel_mappings:
                sessions_by_pin_names[channel.pin_or_relay_name] = session

        yield sessions_by_pin_names


@contextlib.contextmanager
def create_instrument_sessions(
    session_management_client: SessionManagementClient,
    pin_map_context: PinMapContext,
    reset_device: bool = True,
    options: Optional[Dict[str, Any]] = None,
    initialization_behavior: SessionInitializationBehavior = SessionInitializationBehavior.INITIALIZE_SESSION_THEN_DETACH,
) -> Generator[List[SessionInformation], None, None]:
    """Initialize all the available instrument session(s).

    Args:
        session_management_client: Client for accessing the measurement plug-in session management
            service.

        pin_map_context: Container for the pin map and sites.

        reset_device: Specifies whether to reset channel(s) during the initialization procedure.

        options: Specifies the initial value of certain properties for the session. If this argument
            is not specified, the default value is an empty dict.

        initialization_behavior: Specifies whether the NI gRPC Device Server will initialize a new
            session or attach to an existing session.

    Yields:
        A List of session information.
    """
    measurement_context = MeasurementContext()
    with session_management_client.reserve_sessions(pin_map_context) as reservation:
        for session_info in reservation.session_info:
            session: InitializeSession = _get_instrument_session(session_info.instrument_type_id)
            with session.initialize_session(
                measurement_context, reservation, reset_device, options, initialization_behavior
            ):
                pass
        yield reservation.session_info


@contextlib.contextmanager
def destroy_instrument_sessions(
    session_management_client: SessionManagementClient,
    reset_device: bool = False,
    options: Optional[Dict[str, Any]] = None,
    initialization_behavior: SessionInitializationBehavior = SessionInitializationBehavior.ATTACH_TO_SESSION_THEN_CLOSE,
) -> Generator[List[SessionInformation], None, None]:
    """Destroy the existing instrument session(s).

    Args:
        session_management_client: Client for accessing the measurement plug-in session management
            service. 

        reset_device: Specifies whether to reset channel(s) during the initialization procedure.

        options: Specifies the initial value of certain properties for the session. If this argument
            is not specified, the default value is an empty dict.

        initialization_behavior: Specifies whether the NI gRPC Device Server will initialize a new
            session or attach to an existing session.

    Yields:
        A List of session information.
    """
    measurement_context = MeasurementContext()
    with session_management_client.reserve_all_registered_sessions() as reservation:
        for session_info in reservation.session_info:
            session: InitializeSession = _get_instrument_session(session_info.instrument_type_id)
            with session.initialize_session(
                measurement_context, reservation, reset_device, options, initialization_behavior
            ):
                pass
        yield reservation.session_info
