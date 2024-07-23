"""An abstract class to initialize an instrument session."""

import contextlib
from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, Optional

from ni_measurement_plugin_sdk_service.measurement.service import MeasurementContext
from ni_measurement_plugin_sdk_service.session_management import (
    BaseReservation,
    SessionInitializationBehavior,
)


class InitializeSession(ABC):
    """An abstract class to initialize an instrument session."""

    @abstractmethod
    @contextlib.contextmanager
    def initialize_session(
        self,
        measurement_context: MeasurementContext,
        reservation: BaseReservation,
        reset_device: bool,
        options: Optional[Dict[str, Any]],
        initialization_behavior: SessionInitializationBehavior,
    ) -> Generator[None, None, None]:
        """Initializes an instrument session."""
        pass
