# Abstraction through HAL and FAL in python

This repository contains examples of Hardware and Functional abstraction layer in python.

## Overview

### Hardware Abstraction Layer

Hardware Abstraction Layer (HAL) enables users to develop applications agnostic of instrument models
of a type (like DMM). HAL in measurement plug-ins allows users to work with various instrument
models without modifying the implementation. This HAL implementation leverages pins from the pin map.

### Functional Abstraction Layer

The Functional Abstraction Layer (FAL) is a higher-level abstraction layer that provides a more
functional view of the system. It focuses on abstracting the functionality rather than the
hardware, allowing software components to interact with each other through well-defined interfaces.

## Software Dependencies

- InstrumentStudio Professional 2024 Q3 or later
- NI-DCPower 2024 Q2 or later
- NI-DMM 2023 Q1 or later
- NI-VISA 2024 Q1 or later
- NI-488.2 and/or NI-Serial

## Hardware Dependencies

Supported instrument models:

- NI-DCPower (e.g. PXIe-4141)
- NI-DMM (e.g. PXIe-4081).
- Keysight 34401A DMM.
- Recommended: TestStand 2021 SP1 or later

## Getting Started

- When you are ready to start using the HAL layer, check out
  [`this`](./docs/Hal_in_measurement_plugin.md).
- When you are ready to start using the FAL layer, check out
  [`this`](./docs/Fal_in_measurement_plugin.md).

## Build NI Package Manager Packages

To build NI Package Manager packages for the measurement plugin, refer to
[`this`](./docs/build_and_publish.md) document.
