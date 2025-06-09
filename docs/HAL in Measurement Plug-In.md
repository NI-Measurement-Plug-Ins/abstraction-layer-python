# Creating a HAL for Use in Measurement Plug-ins

- [What is HAL?](#what-is-hal)
- [Pre-requisites](#pre-requisites)
- [Steps to implement HAL for a new instrument type](#steps-to-implement-hal-for-a-new-instrument-type)
- [Directory structure of HAL](#directory-structure-of-hal)
- [Migrate existing Instrument Abstraction implementations](#Migrate-existing-Instrument-Abstraction-implementations)
- [Notes](#notes)

## What is HAL?

Hardware Abstraction Layer (HAL) enables users to develop applications agnostic of instrument models
of a type (like DMM). HAL in Measurement Plug-ins allows users to work with different instrument
models without modifying the implementation. This HAL implementation leverages pins from the pin map.

## Pre-requisites

- Fundamentals of HAL
- Intermediate-level expertise in Python
- Understanding of the [session management](https://www.ni.com/docs/en-US/bundle/measurementplugins/page/session-management.html) in the Measurement Plug-ins

## Steps to implement HAL for a new instrument type

![HAL Structure](<./Images/HAL/HAL Structure.png>)

1. To implement HAL for a instrument type, create a new directory to contain all files
   related to the HAL implementation as the first step. This newly created directory will serve as
   the root directory for the HAL implementation.
   1. Follow the recommended [directory structure of HAL](#directory-structure-of-hal) when creating
      directories for the implementation.
   2. Add an `__init__.py` file to this directory. This marks the directory as a Python package,
      allowing you to import the HAL modules into your measurement plug-in.
2. In the root directory, create a Python file named after the specific instrument type. Example:
   `dmm.py` for digital multimeter.
3. In the `<instrument_type>.py` file, define an abstract base class `class <InstrumentType>Base(ABC):` that declares all methods required for instruments of that type. Example: `_initialize_session()`,
   `configure_measurement_digits()` and `read()` methods for a digital multimeter.
   1. Additionally, implement functions to:
      1. Reserve and initialize instrument session for the provided pin name in the measurement.
      2. [Optional] Create and destroy methods for instrument sessions that can be used in the
      TestStand fixture module.
   2. Refer to the `dmm.py` file in this HAL
   [example](https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python/blob/main/source/measurements/dmm_measurement_hal/dmm_hal)
   for more insight.
4. Within the root directory, create subdirectories for each instrument model that requires child
   class implementation. Example: `nidmm` and `keysightdmm`.
   1. Refer to the table with directory names for NI and non-NI instruments in the [Note](#note) section.
5. Each of these subdirectories must contain a module (`.py` file) with the same name as the
   directory.
   1. The module must have a `Session` class which inherits the abstract base class and implements
      its methods.

## Directory structure of HAL

The recommended directory structure for HAL is shown below:

``` bash

<hal_root_directory>
   ├── __init__.py
   ├── <instrument_type>.py
   ├── <instrument_model_1>
   │   └── <instrument_model_1>.py
   ├── <instrument_model_2>
   │   ├── <instrument_model_2>.py
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

## Migrate existing Instrument Abstraction implementations

If an class-based implementation of Hardware Abstraction Layer exists, the following steps are recommended,
1. Review the example implementation of the HAL in this repo
1. Understand the difference in class implementation between the example and existing codebase
1. Take the example from this repo as starter
1. Extend the implementation to use the existing codebase by importing and calling at appropriate locations or copying core logic into the new structure.
1. Package the HAL implementation and deploy for seamless reusability (not covered in this example)

If a non-class-based implementation of Hardware Abstraction Layer exists, the following steps are recommended,
1. Take the example from this repo as starter
1. Extend the implementation to use the existing codebase by importing and calling at appropriate locations or copying core logic into the new structure.
1. Package the HAL implementation and deploy for seamless reusability (not covered in this example)

## Using HAL in Measurement Plug-ins
The following diagram depicts the high level process to use a HAL developed as per the above recommendations in Measurement Plug-ins,
![Measurement Plug-in Workflow](<./Images/HAL/Measurement with HAL workflow.png>)

## Notes

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

2. The `INSTRUMENT_TYPE_ID` for custom instruments should be a **single word**, adhering to Python standards.
   Accordingly, the directories for the instrument models should also be in lowercase. Example:
   [`keysightdmm`](../source/measurements/dmm_measurement_hal/dmm_hal/keysightdmm/keysightdmm.py).
