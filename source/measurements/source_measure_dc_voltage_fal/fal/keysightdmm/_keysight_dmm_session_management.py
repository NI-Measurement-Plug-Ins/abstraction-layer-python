import logging

from decouple import AutoConfig
from fal.keysightdmm._keysight_dmm import Session
from fal.utilities._visa_grpc import (
    build_visa_grpc_resource_string,
    get_visa_grpc_insecure_address,
)
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient
from ni_measurement_plugin_sdk_service.session_management import (
    SessionInformation,
    SessionInitializationBehavior,
)

_logger = logging.getLogger(__name__)


class KeysightDmmSessionConstructor:
    """Measurement plug-in session constructor for Keysight DMM sessions."""

    def __init__(
        self,
        config: AutoConfig,
        discovery_client: DiscoveryClient,
        reset_device: bool,
        initialization_behavior: SessionInitializationBehavior,
    ) -> None:
        """Construct a KeysightDmmSessionConstructor."""
        self._config = config
        self._discovery_client = discovery_client
        self._initialization_behavior = initialization_behavior
        self._reset_device = reset_device

        # Hack: config is a parameter for now so TestStand code modules use the right config path.
        self._visa_dmm_simulate: bool = config(
            "MEASUREMENT_PLUGIN_VISA_DMM_SIMULATE", default=False, cast=bool
        )

        if self._visa_dmm_simulate:
            # _keysight_dmm_sim.yaml doesn't include the grpc:// resource names.
            _logger.debug("Not using NI gRPC Device Server due to simulation")
            self._address = ""
        else:
            self._address = get_visa_grpc_insecure_address(config, discovery_client)
            if self._address:
                _logger.debug("NI gRPC Device Server address: http://%s", self._address)
            else:
                _logger.debug("Not using NI gRPC Device Server")

    def __call__(self, session_info: SessionInformation) -> Session:
        """Construct a Keysight DMM session based on measurement plug-in session info."""
        resource_name = session_info.resource_name
        if self._address:
            resource_name = build_visa_grpc_resource_string(
                resource_name,
                self._address,
                session_info.session_name,
                self._initialization_behavior,
            )

        _logger.debug("Keysight resource name: %s", resource_name)
        return Session(resource_name, self._reset_device, simulate=self._visa_dmm_simulate)
