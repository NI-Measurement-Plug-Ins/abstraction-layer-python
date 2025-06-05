# Creating a HAL for Use in Measurement Plug-ins

- [Creating a HAL for Use in Measurement Plug-ins](#creating-a-hal-for-use-in-measurement-plug-ins)
  - [What is HAL?](#what-is-hal)
  - [Pre-requisites](#pre-requisites)
  - [Steps to implement HAL for a new instrument type](#steps-to-implement-hal-for-a-new-instrument-type)
  - [Directory structure of HAL](#directory-structure-of-hal)
  - [Migrate the existing instrument class to Measurement Plug-In](#migrate-the-existing-instrument-class-to-measurement-plug-in)
  - [Note](#note)

## What is HAL?

Hardware Abstraction Layer (HAL) enables users to develop applications agnostic of instrument models
of a type (like DMM). HAL in measurement plug-ins allows users to work with various instrument
models without modifying the implementation. This HAL implementation leverages pins from the pin map.

## Pre-requisites

- Intermediate-level expertise in Python.
- Understanding of the [session management](https://www.ni.com/docs/en-US/bundle/measurementplugins/page/session-management.html) in the measurement plug-ins.
- Fundamentals of HAL.

## Steps to implement HAL for a new instrument type

1. To implement HAL for a specific instrument type, create a directory to hold the modules related to the HAL implementation.
2. Create a python file named after the instrument type. Example: `dmm.py`.
3. In the above created file, add an abstract class with the methods that should be called using the
   instrument session. This module will additionally contain create and destroy methods to
   initialize and close instrument sessions in the measurement using the TestStand fixture module. Refer to this [example](https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python/blob/main/source/measurements/dmm_measurement_hal/dmm_hal/dmm.py) for more insights.
4. Within the root directory create directories for each instrument model. You can refer to the
   table with directory names for NI and custom instruments in the [Note](#note) section. Following
   this, we have named the directories as `nidmm` and `keysightdmm`.
5. Each of these directories must have a module with the same name as the directory. The module
   must have a `Session` class which inherits and implements the methods from the abstract class
   created in the root directory.

## Directory structure of HAL

1. The recommended directory structure for HAL is shown below:

``` bash

<hal_root_directory>
   ├── __init__.py
   ├── <instrument_type>.py
   ├── <NI_instrument_type>
   │   └── <NI_instrument_type>.py
   ├── <instrument_model_1>
   │   ├── <instrument_model_1>.py
   │   └── <driver session related files>
   ├── <other instrument model(s)>
   .
   .
   .
   ├── teststand_helper.py
   └── utilities
       └── _visa_grpc.py

```

Example:

``` bash

dmm_hal
   ├── __init__.py
   ├── dmm.py
   ├── function.py
   ├── keysightdmm
   │   ├── keysightdmm.py
   │   └── <driver session related files>
   ├── nidmm
   │   └── nidmm.py
   ├── teststand_helper.py
   └── utilities
       └── _visa_grpc.py

```

## Migrate the existing instrument class to Measurement Plug-In

- Create a measurement plug-in by following the steps mentioned in
  [Developing a measurement plug-in with python](https://github.com/ni/measurement-plugin-python?tab=readme-ov-file#developing-measurements-quick-start) or migrate your existing measurement into measurement plug-in by following the steps mentioned in [Migrating a measurement to Plug-In](https://github.com/ni/measurement-plugin-converter-python/tree/main/src/converter).
- Copy the existing HAL classes and modules by following the steps from [Steps to create a new HAL based measurement](#steps-to-implement-hal-for-a-new-instrument-type) to migrate the existing HAL implementation.
- Update the `measurement.py` with the HAL modules and run the measurement.
![Measurement Plug-in Workflow](Measurement%20with%20HAL%20workflow.png)

## Note

1. Directory names for different NI instrument types.

   Instrument type | Directory name
   --- | ---
   NI-DCPower | nidcpower
   NI-DMM | nidmm
   NI-Digital Pattern | nidigitalpattern
   NI-SCOPE | niscope
   NI-FGEN | nifgen
   NI-DAQmx | nidaqmx
   NI-SWITCH | nirelaydriver

2. The instrument type id for custom instruments should be a single word, adhering to Python standards.
   Accordingly, the directories for the instrument models should also be in lowercase. Example:
   [`keysightdmm`](../source/measurements/dmm_measurement_hal/dmm_hal/keysightdmm/keysightdmm.py).
