# DMM Measurement

This is a measurement plug-in example that performs a measurement using a DMM with Hardware
Abstraction Layer (HAL).

## Features

- The HAL (Hardware Abstraction Layer) is implemented to provide interchangeability between
  different models of the same instrument type. This is achieved using the pins from the pin map.
  - At present, there are two distinct models, NI-DMM and VISA-DMM, both of which fall under the DMM
    type. To accommodate these models, separate classes have been created. These classes are derived
    from a base class, which has been designed to provide HAL support for all DMM type instrument
    models.
- Pin-aware, supporting one session and one pin
  - Uses the same selected measurement function and range for all selected pin/site combinations.
- Uses the NI gRPC Device Server to allow sharing instrument sessions with other measurement
  services when running measurements from TestStand.

## Files Overview

- The below files are generated using `ni-measurement-plugin-generator`
  - _helpers.py
  - DmmMeasurementHAL.measproj
  - DmmMeasurementHAL.measui
  - DmmMeasurementHAL.serviceconfig
  - measurement.py
  - start.bat

- The below files are created for `DMM HAL` implementation
  - dmm.py
  - nidmm.py
  - keysightdmm.py
  - _keysight_dmm_session_management.py
  - _keysight_dmm_sim.yaml
  - _keysight_dmm.py
  - function.py

- The below file is duplicated to enable session sharing via the gRPC device server.
  - _visa_grpc.py

- The below file is added to create and destroy instrument sessions in the TestStand sequence.
  - teststand_helper.py

- The below files are created for dependency management
  - poetry.toml
  - pyproject.toml

## Required Software

- InstrumentStudio Professional 2024 Q3 or later
- NI-DMM 2023 Q1 or later
- NI-VISA 2024 Q1 or later
- NI-488.2 and/or NI-Serial
- Recommended: TestStand 2021 SP1 or later

## Required Hardware

Supported instrument models:

- NI-DMM (e.g. PXIe-4081).
- Keysight 34401A DMM.

## To use a physical instrument

- Connect the instrument to a supported interface on the computer, such as GPIB or serial.
- Launch NI MAX or NI Hardware Configuration Utility.
- Update the alias of the NI-DMM instrument to `NI-DMM`.
- Update the alias of Keysight 34401A DMM to `VISA-DMM`.

## To simulate NI-DMM and Keysight DMM Using PyVISA-sim

By default, this example uses a physical instrument or a simulated instrument
created in NI MAX. To automatically simulate an instrument without using NI MAX,
follow the steps below:

- Create a `.env` file in the measurement service's directory or one of its
  parent directories (such as the root of your Git repository or
  `C:\ProgramData\National Instruments\Plug-Ins\Measurements` for statically
  registered measurement services).
- Add the following options to the `.env` file to enable simulation via the
  driver's option string:

  ```bash
  MEASUREMENT_PLUGIN_NIDMM_SIMULATE=1
  MEASUREMENT_PLUGIN_NIDMM_BOARD_TYPE=PXIe
  MEASUREMENT_PLUGIN_NIDMM_MODEL=4081

  MEASUREMENT_PLUGIN_VISA_DMM_SIMULATE=1
  ```

- The `_keysight_dmm.py` instrument driver implements simulation using PyVISA-sim.
  [`_keysight_dmm_sim.yaml`](./dmm_hal/keysightdmm/_keysight_dmm_sim.yaml) defines the behavior of the
  simulated instrument.
- Select `Sim_Keysight_DMM_Pin` pin to use the simulated Keysight 34401A DMM.

## NOTE

- - The `.\demo_files\DmmMeasurementHAL.pinmap` for this measurement includes two custom DMM instruments:
  `GPIB0::3::INSTR (simulated)` and `VISA-DMM (physical)`, both identified with the instrument
  type ID `KeysightDmm`. Currently, the `create_dmm_sessions` and `destroy_dmm_sessions methods`
  only support initializing a single session of a specific instrument type ID. Therefore, before
  executing the TestStand sequence, ensure to remove the simulated instrument (GPIB0::3::INSTR) if
  you have a physical instrument (VISA-DMM) connected, or vice versa. Otherwise, you will encounter
  an error stating, "Too many reserved sessions matched instrument type ID 'KeysightDmm'. Expected
  single session, got 2 sessions."
