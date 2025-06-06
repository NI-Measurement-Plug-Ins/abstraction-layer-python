# Creating a FAL for Use in Measurement Plug-ins

- [Creating a FAL for Use in Measurement Plug-ins](#creating-a-fal-for-use-in-measurement-plug-ins)
  - [What is FAL?](#what-is-fal)
  - [Pre-requisites](#pre-requisites)
  - [Steps to implement FAL for another instrument function](#steps-to-implement-fal-for-another-instrument-function)
  - [Directory structure of FAL](#directory-structure-of-fal)
  - [Migrate the existing instrument class to Measurement Plug-In](#migrate-the-existing-instrument-class-to-measurement-plug-in)
  - [Note](#note)

## What is FAL?

The Functional Abstraction Layer (FAL) is a higher-level abstraction layer that provides a more
functional view of the system. It focuses on abstracting the functionality rather than the
hardware, allowing software components to interact with each other through well-defined interfaces.

## Pre-requisites

- Intermediate-level expertise in Python.
- Understanding of the [session management](https://www.ni.com/docs/en-US/bundle/measurementplugins/page/session-management.html) in the measurement plug-ins.
- Fundamentals of FAL.

## Steps to implement FAL for another instrument function

![FAL Structure](<./Images/FAL/FAL Structure.png>)

1. To implement FAL, create a new directory to contain all files related to the FAL implementation
   as the first step. This newly created directory will serve as the root directory for the FAL
   implementation.
   1. Follow the recommended [directory structure of FAL](#directory-structure-of-fal) when creating
      directories for the implementation.
   2. Add an `__init__.py` file to this directory. This marks the directory as a Python package,
      allowing you to import the FAL modules into your measurement plug-in.
2. In the root directory, create a Python file with a generic name that does not specify the
   instrument type, to abstract the instrument type details. Example: `session_helper.py`.
3. In the `session_helper.py` file, implement initialize method that will reserve and initialize
   instrument sessions for the provided pin names in the measurement.
   1. [Optional] Additionally, implement create and destroy methods for instrument sessions that can
      be used in the TestStand fixture module.
   2. Refer to the `session_helper.py` file in this FAL
   [example](https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python/blob/main/source/measurements/source_measure_dc_voltage_fal/fal)
   for more insights.
4. Create abstract classes for the required instrument functionalities (such as source voltage,
   measure voltage, source current, measure current etc) as separate Python files in the root
   directory. Example: `source_dc_voltage.py` and `measure_dc_voltage.py`.
5. Within the root directory, create subdirectories for each instrument model that requires child
   class implementation. Example: `nidcpower`, `nidmm` and `keysightdmm`.
   1. For naming the subdirectory, refer to the table with directory names for NI and custom
   instruments in the [Note](#note) section.
6. Each of these subdirectories must contain a module (`.py` file) with the same name as the
   directory.
   1. The module must have a `Session` class which inherits the abstract classes of the required
      instrument functionalities and implements its methods.

![FAL Implementation](<./Images/FAL/FAL Implementation.png>)

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

## Migrate the existing instrument class to Measurement Plug-In

- Create a measurement plug-in by following the steps mentioned in [Developing a measurement plug-in with python](https://github.com/ni/measurement-plugin-python?tab=readme-ov-file#developing-measurements-quick-start) or migrate your existing measurement into measurement plug-in by following the steps mentioned in [Migrating a measurement to Plug-In](https://github.com/ni/measurement-plugin-converter-python/tree/main/src/converter).
- Copy the existing FAL classes and modules by following the steps from [Steps to create a new FAL based measurement](#steps-to-implement-fal-for-another-instrument-function) to migrate the existing FAL implementation.
- Update the `measurement.py` with the FAL modules and run the measurement.

![Measurement Plug-in Workflow](<./Images/FAL/Measurement with FAL workflow.png>)

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
