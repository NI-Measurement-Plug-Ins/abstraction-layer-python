# Creating a FAL for Use in Measurement Plug-ins

- [Creating a FAL for Use in Measurement Plug-ins](#creating-a-fal-for-use-in-measurement-plug-ins)
  - [What is FAL?](#what-is-fal)
  - [Pre-requisites](#pre-requisites)
  - [Steps to implement FAL for another instrument function](#steps-to-implement-fal-for-another-instrument-function)
  - [Directory structure of FAL](#directory-structure-of-fal)
  - [Steps to migrate FAL implementations from other frameworks](#steps-to-migrate-fal-implementations-from-other-frameworks)
  - [Note](#note)

## What is FAL?

The Functional Abstraction Layer (FAL) is a higher-level abstraction layer that provides a more
functional view of the system. It focuses on abstracting the functionality rather than the
hardware, allowing software components to interact with each other through well-defined interfaces.

## Pre-requisites

- Fundamental knowledge of FAL.
- Understanding of the session management in the measurement plug-ins.
- Intermediate working experience in Python.

## Steps to implement FAL for another instrument function

1. To implement FAL for a specific instrument type, create a directory to hold the modules related
   to the FAL implementation.
2. Create a Python file with a generic name that does not specify the type of instrument.
   Example: session_helper.py.
3. This module contains an initialize method which will reserve and initialize the respective
   instrument sessions. This module will additionally contain methods to initialize instrument
   sessions in the measurement and create and destroy methods that can be used in the TestStand
   fixture module.
4. Create abstract classes for each instrument functionality in separate files such as source
   voltage, measure voltage, source current, measure current etc. Example: `source_dc_voltage` and
   `measure_dc_voltage`.
5. Within the root directory create directories for each instrument model. You can refer to the
   table with directory names for NI and custom instruments in the [Note](#note) section. Following
   this, we have named the directories as `nidcpower`, `nidmm` and `keysightdmm`.
6. Each directory must have a module with the same name as the directory. The module
   must have a `Session` class which inherits and implements the methods from the appropriate
   functionality abstract classes created in the root directory.

## Directory structure of FAL

1. The recommended directory structure for FAL is shown below:

``` bash

   <fal_root_directory>
   ├── __init__.py
   ├── session_helper.py
   ├── initialize_session.py
   ├── <functionality_abstract_classes>.py
   .
   .
   .
   ├── <instrument_model_1>
   │   └── <instrument_model_1>.py
   ├── <instrument_model_2>
   │   ├── <instrument_model_2>.py
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

   fal
   ├── __init__.py
   ├── session_helper.py
   ├── initialize_session.py
   ├── source_dc_voltage.py
   ├── measure_dc_voltage.py
   ├── keysightdmm
   │   ├── keysightdmm.py
   │   └── <driver session related files>
   ├── nidmm
   │   └── nidmm.py
   ├── nidcpower
   │   └── nidcpower.py
   ├── teststand_helper.py
   └── utilities
       └── _visa_grpc.py

```

## Steps to migrate FAL implementations from other frameworks

- Create a measurement plug-in by following the steps mentioned in
  [Developing a measurement plug-in with python](https://github.com/ni/measurement-plugin-python?tab=readme-ov-file#developing-measurements-quick-start).
- Copy the existing FAL classes and modules by following the steps from [Steps to create a new FAL based measurement](#steps-to-implement-fal-for-another-instrument-function) to migrate the existing FAL implementation.
  
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
   [`keysightdmm`](../source/measurements/source_measure_dc_voltage_fal/fal/keysightdmm/keysightdmm.py).
