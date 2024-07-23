"""Functions to set up and tear down sessions of instrument devices in NI TestStand."""

from typing import Any

import fal.session_helper as session_helper
from _helpers import TestStandSupport
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient
from ni_measurement_plugin_sdk_service.grpc.channelpool import GrpcChannelPool
from ni_measurement_plugin_sdk_service.session_management import (
    PinMapContext,
    SessionManagementClient,
)


def create_instrument_sessions(sequence_context: Any) -> None:
    """Create and register all instrument session(s).

    Args:
        sequence_context: The SequenceContext COM object from the TestStand sequence execution.
            (Dynamically typed.)
    """
    with GrpcChannelPool() as grpc_channel_pool:
        teststand_support = TestStandSupport(sequence_context)
        pin_map_id = teststand_support.get_active_pin_map_id()
        pin_map_context = PinMapContext(pin_map_id=pin_map_id, sites=None)

        discovery_client = DiscoveryClient(grpc_channel_pool=grpc_channel_pool)
        session_management_client = SessionManagementClient(
            discovery_client=discovery_client, grpc_channel_pool=grpc_channel_pool
        )

        with session_helper.create_instrument_sessions(
            session_management_client,
            pin_map_context,
        ) as session_info:
            session_management_client.register_sessions(session_info)


def destroy_instrument_sessions() -> None:
    """Destroy and unregister all instrument session(s)."""
    with GrpcChannelPool() as grpc_channel_pool:
        discovery_client = DiscoveryClient(grpc_channel_pool=grpc_channel_pool)
        session_management_client = SessionManagementClient(
            discovery_client=discovery_client, grpc_channel_pool=grpc_channel_pool
        )
        with session_helper.destroy_instrument_sessions(
            session_management_client,
        ) as session_info:
            session_management_client.unregister_sessions(session_info)
