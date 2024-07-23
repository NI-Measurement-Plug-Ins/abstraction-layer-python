"""Declares an abstract class for the DMM HAL and defines DMM session initialization functions."""

import contextlib
import importlib
from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Optional

from dmm_hal.function import Function as DmmFunction
from ni_measurement_plugin_sdk_service.measurement.service import MeasurementContext
from ni_measurement_plugin_sdk_service.session_management import (
    BaseReservation,
    PinMapContext,
    SessionInformation,
    SessionInitializationBehavior,
    SessionManagementClient,
)


class DmmBase(ABC):
    """Simplified interface for the DMM instrument session."""

    @abstractmethod
    @contextlib.contextmanager
    def _initialize_session(
        self,
        reservation: BaseReservation,
        reset_device: bool,
        options: Optional[Dict[str, Any]],
        initialization_behavior: SessionInitializationBehavior,
    ) -> Generator[None, None, None]:
        """Initialize a DMM session."""
        pass

    @abstractmethod
    def configure_measurement_digits(
        self,
        measurement_function: DmmFunction,
        range: float,
        resolution_digits: float,
    ) -> None:
        """Configure the common properties of the measurement."""
        pass

    @abstractmethod
    def read(self) -> float:
        """Acquires a single measurement and returns the measured value."""
        pass


def _get_instrument_session(instrument_type_id: str) -> DmmBase:
    """Creates a DMM HAL object based on the instrument type id."""
    try:
        driver_module_path = f"dmm_hal.{instrument_type_id}.{instrument_type_id}".lower()
        driver_module = importlib.import_module(driver_module_path)
        session = getattr(driver_module, "Session")
        return session()

    except ImportError:
        raise ValueError(f"No driver found for instrument type: '{instrument_type_id}'.")


@contextlib.contextmanager
def initialize(
    measurement_context: MeasurementContext,
    pin_name: str,
    reset_device: bool = False,
    options: Optional[Dict[str, Any]] = None,
    initialization_behavior: SessionInitializationBehavior = SessionInitializationBehavior.AUTO,
) -> Generator[DmmBase, None, None]:
    """Initialize a DMM session.

    Args:
        measurement_context: Proxy for the Measurement Service's context-local state.

        pin_name: The pin name to which the instrument session need to be connected.

        reset_device: Specifies whether to reset channel(s) during the initialization procedure.

        options: Specifies the initial value of certain properties for the session. If this argument
            is not specified, the default value is an empty dict.

        initialization_behavior: Specifies whether the NI gRPC Device Server will initialize a new
            session or attach to an existing session.

    Yields:
        A DMM session.
    """
    with measurement_context.reserve_session(pin_name) as reservation:
        session = _get_instrument_session(reservation.session_info.instrument_type_id)
        with session._initialize_session(
            reservation, reset_device, options, initialization_behavior
        ):
            yield session


@contextlib.contextmanager
def create_dmm_sessions(
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
    with session_management_client.reserve_sessions(pin_map_context) as reservation:
        for session_info in reservation.session_info:
            session = _get_instrument_session(session_info.instrument_type_id)
            with session._initialize_session(
                reservation, reset_device, options, initialization_behavior
            ):
                pass
        yield reservation.session_info


@contextlib.contextmanager
def destroy_dmm_sessions(
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
    with session_management_client.reserve_all_registered_sessions() as reservation:
        for session_info in reservation.session_info:
            session = _get_instrument_session(session_info.instrument_type_id)
            with session._initialize_session(
                reservation, reset_device, options, initialization_behavior
            ):
                pass
        yield reservation.session_info
