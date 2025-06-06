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

![HAL Structure](<./HAL Structure.png>)

1. To implement HAL for a specific instrument type, create a new directory to contain all files
   related to the HAL implementation as the first step. This newly created directory will serve as
   the root directory for the HAL implementation.
   1. Follow the recommended [directory structure for HAL](#directory-structure-of-hal) when
      creating the directories for the implementation.
   2. Add an `__init__.py` file to this directory. This marks the directory as a Python package,
      allowing you to import the HAL modules into your measurement plug-in.
2. In the root directory, create a python file named after the specific instrument type. Example:
   `dmm.py` for digital multimeter.
3. In the above created file, define an abstract class that specifies the required methods for any
   instrument model of that instrument type such as session initialization, configuration, and
   reading measurements.
   1. This module will additionally contain an initialize method that will reserve and initialize
   instrument session for the provided pin name, and create and destroy methods that will initialize
   and close instrument sessions in the measurement using the TestStand fixture module.
   2. Refer to this
   [example](https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python/blob/main/source/measurements/dmm_measurement_hal/dmm_hal/dmm.py)
   for more insights.
4. Within the root directory create subdirectories for each instrument model.
   1. For naming the directory, you can refer to the table with directory names for NI and custom
      instruments in the [Note](#note) section.
   2. Following this convention, we have named the subdirectories as `nidmm` and `keysightdmm` in
      the above mentioned example..
5. Each of these created subdirectories must contain a module (`.py` file) with the same name as the
   directory.
   1. The module must have a `Session` class which inherits the abstract base class and implements
      its methods.

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
