# Creating a HAL for Use in Measurement Plug-Ins

Hardware Abstraction Layer (HAL) enables users to develop applications agnostic of instrument models
of a type (like DMM). HAL in measurement plug-ins allows users to work with various instrument
models without modifying the implementation. This HAL implementation leverages pins from the pin map.

## Pre-requisites

* Fundamental knowledge of HAL.
* Understanding of the session management in the measurement plug-in.
* Intermediate working experience in Python.

## Steps to implement HAL for a new instrument type

1. To implement HAL for a specific instrument type, create a directory to hold the modules related
   to the HAL implementation.
2. Create a python file named after the instrument type. Example: dmm.py.
3. In the above created file, add an abstract class with the methods that should be called using the
   instrument session. This module will additionally contain create and destroy methods to
   initialize and close instrument sessions in the measurement using the TestStand fixture module.
4. Within the root directory create directories for each instrument model. You can refer to the
   table with directory names for NI and custom instruments in the [Note](#note) section. Following
   this, we have named the directories as `nidmm` and `keysightdmm`.
5. Each of these directories must have a module with the same name as the directory. The module
   must have a `Session` class which inherits and implements the methods from the abstract class
   created in the root directory.

## Directory structure of HAL

1. The recommended directory structure for HAL is shown below:

``` bash

<instrument_type>_hal
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

## NOTE

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
