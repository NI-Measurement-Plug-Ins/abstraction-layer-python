# Creating a FAL for Use in Measurement Plug-ins

- [What is FAL?](#what-is-fal)
- [Pre-requisites](#pre-requisites)
- [Steps to implement FAL for another instrument function](#steps-to-implement-fal-for-another-instrument-function)
- [Directory structure of FAL](#directory-structure-of-fal)
- [Migrate the existing instrument class to Measurement Plug-In](#migrate-existing-instrument-abstraction-implementations)
- [Using FAL in Measurement Plug-ins](#using-fal-in-measurement-plug-ins)
- [Note](#notes)

## What is FAL?

The Functional Abstraction Layer (FAL) is a higher-level abstraction layer that provides a more
functional view of the system. It focuses on abstracting the functionality rather than the
hardware, allowing software components to interact with each other through well-defined interfaces.

## Pre-requisites

- Fundamentals of FAL
- Intermediate-level expertise in Python
- Understanding of the [session management](https://www.ni.com/docs/en-US/bundle/measurementplugins/page/session-management.html) in the measurement plug-ins

## Steps to implement FAL for another instrument function

![FAL Structure](<./Images/FAL/FAL Structure.png>)

1. To implement FAL, create a new directory to contain all files related to the FAL implementation. This newly created directory will serve as the root directory for the FAL implementation.
   1. Follow the recommended [directory structure of FAL](#directory-structure-of-fal) when creating
      directories for the implementation.
   2. Add an `__init__.py` file to this directory. This marks the directory as a Python package,
      allowing you to import the FAL modules into your measurement plug-in.
2. In the root directory, create `session_helper.py` and implement initialize method that will reserve and initialize
   instrument sessions for the provided pin names in the measurement.
   1. [Optional] Additionally, implement *create* and *destroy* methods for instrument sessions that can
      be used in the TestStand fixture module.
   2. Refer to the `session_helper.py` file in this FAL
   [example](https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python/blob/main/source/measurements/source_measure_dc_voltage_fal/fal)
   for more insight.
4. Create abstract classes for the required instrument functionalities (such as *source voltage*,
   *measure voltage*, *source current*, *measure current*, etc.,) as separate Python files in the root
   directory. Example: `source_dc_voltage.py` and `measure_dc_voltage.py`.
5. Within the root directory, create subdirectories for each instrument model. Example: `nidcpower`, `nidmm` and `keysightdmm`.
   1. For naming the subdirectory, refer to the table with directory names for NI and custom
   instruments in the [Notes](#notes) section.
6. Each of these subdirectories must contain a module (`.py` file) with the same name as the
   directory.
   1. The module must have a `Session` class which inherits the abstract classes of the required
      instrument functionalities and implements its methods.

![FAL Implementation](<./Images/FAL/FAL Implementation.png>)

## Directory structure of FAL

The recommended directory structure for FAL is shown below:

``` bash

   <fal_root_directory>
   ├── __init__.py
   ├── session_helper.py
   ├── initialize_session.py
   ├── <functionality_1_abstract_class>.py
   ├── <functionality_2_abstract_class>.py
   .
   ├── <functionality_n_abstract_class>.py
   .
   .
   .
   ├── <instrument_model_1>
   │   └── <instrument_model_1>.py
   ├── <instrument_model_2>
   │   ├── <instrument_model_2>.py
   │   └── <driver session related files>
   .
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

## Migrate existing Instrument Abstraction implementations

If an class-based implementation of Functional Abstraction Layer exists, the following steps are recommended,
1. Review the example implementation of the FAL in this repo
1. Understand the difference in class implementation between the example and existing codebase
1. Take the example from this repo as starter
1. Extend the implementation to use the existing codebase by importing and calling at appropriate locations or copying core logic into the new structure.
1. Package the FAL implementation and deploy for seamless reusability (not covered in this example)

If a non-class-based implementation of Functional Abstraction Layer exists, the following steps are recommended,
1. Take the example from this repo as starter
1. Extend the implementation to use the existing codebase by importing and calling at appropriate locations or copying core logic into the new structure.
1. Package the FAL implementation and deploy for seamless reusability (not covered in this example)

## Using FAL in Measurement Plug-ins
The following diagram depicts the high level process to use a FAL developed as per the above recommendations in Measurement Plug-ins,
![Measurement Plug-in Workflow](<./Images/FAL/Measurement with FAL workflow.png>)

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

2. The `INSTRUMENT_TYPE_ID` for custom instruments should be a single word, adhering to Python standards.
   Accordingly, the directories for the instrument models should also be in lowercase. Example:
   [`keysightdmm`](../source/measurements/source_measure_dc_voltage_fal/fal/keysightdmm/keysightdmm.py).
