# Source Measure DC Voltage Measurement

An example measurement plug-in to demonstrate Functional Abstraction Layer (FAL) by sourcing a DC
voltage and measuring the same using a mix of instrument types.

## Features

- The FAL (Functional Abstraction Layer) is implemented to provide interchangeability between
  different instrument types.
  - Currently, the FAL supports three instrument models namely, NI-DCPower, NI-DMM and VISA-DMM.
    Individual classes named `Session` are created to manage these instrument sessions.
- Pin-aware, supporting multiple pins and multiple sessions for different instruments
  - Uses a DC-Power instrument connected to a specific pin for sourcing DC Voltage.
  - Uses the same DC-Power instrument or a different instrument for measuring the DC Voltage for all
    selected pin/site combinations.
- Includes a TestStand sequence that demonstrates configuring the pin map, registering instrument
  sessions with the session management service, and executing a measurement.
  - The TestStand sequence manages the pin map, along with the registration and deregistration of
    sessions, within the `Setup` and `Cleanup` parts of the main sequence. For scenarios involving
    **Test UUTs** and the batch processing model, it's recommended to relocate these actions to the
    ProcessSetup and ProcessCleanup callbacks.
- Uses the NI gRPC Device Server to allow sharing instrument sessions with other measurement
  services when running measurements from TestStand.

## Files Overview

- The below files are generated using `ni-measurement-plugin-sdk-generator`
  - _helpers.py
  - SourceMeasureDCVoltageFAL.measproj
  - SourceMeasureDCVoltageFAL.measui
  - SourceMeasureDCVoltageFAL.serviceconfig
  - measurement.py
  - start.bat

- The below files are created for the `FAL` implementation
  - session_helper.py
  - initialize_session.py
  - source_dc_voltage.py
  - measure_dc_voltage.py
  - nidcpower.py
  - nidmm.py
  - keysightdmm.py
  - _keysight_dmm.py
  - _keysight_dmm_session_management.py
  - _keysight_dmm_sim.yaml

- The below file is duplicated to enable session sharing via the gRPC device server.
  - _visa_grpc.py

- The below file is added to create and destroy instrument sessions in the TestStand sequence.
  - teststand_helper.py

- The below files are created for dependency management
  - poetry.toml
  - pyproject.toml

## Required Software

- InstrumentStudio Professional 2024 Q3 or later
- NI-DCPower 2024 Q2 or later
- NI-DMM 2023 Q4 or later
- NI-VISA 2024 Q1 or later
- NI-488.2 and/or NI-Serial

## Required Hardware

Supported instrument models:

- NI-DCPower (e.g. PXIe-4141)
- NI-DMM (e.g. PXIe-4081)
- Keysight 34401A DMM
- Recommended: TestStand 2021 SP1 or later

## To use a physical instrument

- Connect the instrument to a supported interface on the computer, such as GPIB or serial.
- Launch NI-MAX or NI Hardware Configuration Utility.
- Update the alias of NI DCPower to `NI-DCPower`.
- Update the alias of NI DMM to `NI-DMM`.
- Update the alias of Keysight 34401A DMM to `VISA-DMM`.

## To simulate NI-DCPower, NI-DMM and Keysight DMM Using PyVISA-sim

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
  MEASUREMENT_PLUGIN_NIDCPOWER_SIMULATE=1 
  MEASUREMENT_PLUGIN_NIDCPOWER_BOARD_TYPE=PXIe
  MEASUREMENT_PLUGIN_NIDCPOWER_MODEL=4141
  
  MEASUREMENT_PLUGIN_NIDMM_SIMULATE=1
  MEASUREMENT_PLUGIN_NIDMM_BOARD_TYPE=PXIe
  MEASUREMENT_PLUGIN_NIDMM_MODEL=4081

  MEASUREMENT_PLUGIN_VISA_DMM_SIMULATE=1
  ```

- The `_keysight_dmm.py` instrument driver implements simulation using PyVISA-sim.
  [`_keysight_dmm_sim.yaml`](./fal/keysightdmm/_keysight_dmm_sim.yaml) defines the
  behavior of the simulated instrument.
- Select `Sim_Keysight_DMM_Pin` pin to use the simulated Keysight 34401A DMM.

## NOTE

- This measurement uses the `SourceMeasureDCVoltageFAL.pinmap` file, which includes one DC-Power
  instrument and two custom DMM instruments: `GPIB0::3::INSTR (simulated)` and `VISA-DMM(physical)`,
  both identified with the instrument type ID `KeysightDmm`. Currently, the `create_dmm_sessions`
  and `destroy_dmm_sessions methods` only support initializing a single session of a specific
  TestStand sequence, ensure to remove the simulated instrument (GPIB0::3::INSTR) if you have a
  physical instrument (VISA-DMM) connected, or vice versa. Otherwise, you will encounter an error
  stating, "Too many reserved sessions matched instrument type ID 'KeysightDmm'. Expected single
  session, got 2 sessions."