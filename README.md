# TriggerConfig
This package provides the tools for defining and adjusting the WCTE trigger configuration
 * "Configuration" class:
   * defines all elements of the WCTE trigger configuration in terms of nested dictionaries
   * provides methods for adjusting the configuration
   * provides methods for saving and loading configurations using JSON files
   * provides a method to convert the configuration to a JSON files with register values for the WCTE trigger logic module (V1495) and the constant fraction discriminator (CFD) modules (V812)
 * "initialization" module:
   * provides methods that produce default WCTE trigger configurations
 * "console" module:
   * provides a command line interface for
     * viewing and adjusting all elements of the trigger configuration
     * saving and loading configurations using JSON files
     * saving JSON files with register values for the WCTE trigger logic module (V1495) and the constant fraction discriminator (CFD) modules (V812)

## Installation
To install the package, clone WCTE/TriggerConfig repository in a folder that also contains the V1495_firmware
(WCTE/V1495_firmware). This is necessary because the package uses the V1495_firmware to find the correct register addresses.

Dependencies:
 * V1495_firmware
 * texttable

To install texttable:
```sudo apt-get install python3-texttable```

## Usage

```python3 console.py```

```
Welcome to the WCTE trigger configuration console. Version tc-1.0
The default action is shown in square brackets. Press enter to execute the default action.

Enter command: [help] 
Available commands:
+-------------+---------------------------------------------------------------+
| Command     | Action                                                        |
+-------------+---------------------------------------------------------------+
| help        | Display this help message                                     |
+-------------+---------------------------------------------------------------+
| load        | Load a trigger configuration                                  |
+-------------+---------------------------------------------------------------+
| channels    | Show the input signal channels in compact form                |
+-------------+---------------------------------------------------------------+
| cfds        | Show/modify the constant fraction discriminator VME addresses |
+-------------+---------------------------------------------------------------+
| inputs      | Show/modify the input signal properties                       |
+-------------+---------------------------------------------------------------+
| level1      | Show/modify the level 1 logic properties                      |
+-------------+---------------------------------------------------------------+
| level2      | Show/modify the level 2 logic properties                      |
+-------------+---------------------------------------------------------------+
| outputs     | Show/modify the output lemo assignments                       |
+-------------+---------------------------------------------------------------+
| spills      | Show/modify the spill signal assignments                      |
+-------------+---------------------------------------------------------------+
| deadtime    | Show/modify the deadtime properties                           |
+-------------+---------------------------------------------------------------+
| connections | Show/modify the connections to the trigger/digitizer boards   |
+-------------+---------------------------------------------------------------+
| patches     | Show/modify the connections to the patch panel                |
+-------------+---------------------------------------------------------------+
| show        | Show all elements of the current configuration                |
+-------------+---------------------------------------------------------------+
| save        | Save the current configuration (config and register settings) |
+-------------+---------------------------------------------------------------+
| update      | Write the current register settings to current_registers.json |
+-------------+---------------------------------------------------------------+
| exit        | Exit the program                                              |
+-------------+---------------------------------------------------------------+
```
### Loading an existing trigger configuration
```
Enter command: [help] load
List of available trigger configurations: sorted by modification time
+-------+--------------------+------------+------------+-----------------------------------+
| Index |      Filename      | TC Version | Short Name |            Description            |
+-------+--------------------+------------+------------+-----------------------------------+
|   0   | tp_v12_config.json |   tc-1.0   |   TP v12   | Tagged Photon Trigger version 1.2 |
+-------+--------------------+------------+------------+-----------------------------------+
|   1   | le_v12_config.json |   tc-1.0   |   LE v12   |  Low Energy Trigger version 1.2   |
+-------+--------------------+------------+------------+-----------------------------------+
|   2   | la_v12_config.json |   tc-1.0   |   LA v12   |     Laser Trigger version 1.2     |
+-------+--------------------+------------+------------+-----------------------------------+
Select index of file to load: [cancel] 1
Configuration loaded from le_v12_config.json
Enter command: [help] 
```
The folder "configurations" contains the JSON trigger configuration files listed in this example. 

When saving  a configuration, the filename prefix, short name, and description are specified, and the file is saved in the "configurations" folder,
and the corresponding register settings are saved in the "register_settings" folder.
Existing files cannot be overwritten.

The TC Version is the version of the TriggerConfig package that was used to create the configuration file.
Only files with the same version as the current package can be loaded. Previous versions of the package can be
modified to be compatible with the current version by adjusting the JSON file.
Version numbers in the filename, short name, and description relate to the version of the trigger configuration
itself, and are not associated with the TC Version.

### Compact summary of input signal channels using shortnames
```
Enter command: [help] channels
Current CFD modules and input signals:
CFD module: 0 VME address: 8800:
+---+------+---+------+----+------+----+--------+----+-------+----+-------+----+-------+----+-------+
| # | Name | # | Name | #  | Name | #  |  Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  |
+---+------+---+------+----+------+----+--------+----+-------+----+-------+----+-------+----+-------+
| 0 | T00  | 1 | T01  | 2  | T02  | 3  |  T03   | 4  |  T10  | 5  |  T11  | 6  |  T12  | 7  |  T13  |
+---+------+---+------+----+------+----+--------+----+-------+----+-------+----+-------+----+-------+
| - |  -   | 9 | HC0  | 10 | HC1  | 11 | ACTEVD | 12 | ACT00 | 13 | ACT01 | 14 | ACT10 | 15 | ACT11 |
+---+------+---+------+----+------+----+--------+----+-------+----+-------+----+-------+----+-------+
CFD module: 1 VME address: 8801:
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| 16 | ACT20 | 17 | ACT21 | 18 | ACT30 | 19 | ACT31 | 20 | ACT40 | 21 | ACT41 | 22 | ACT50 | 23 | ACT51 |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| 24 | MUT0  | 25 | MUT1  | 26 |  BSW  | 27 |  BSE  | 28 | LASER | 29 | XTRIG | 30 | TOF0F | 31 | TDCT0 |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
CFD module: 2 VME address: 8802:
+---+------+---+------+---+------+---+------+---+------+---+------+---+------+---+------+
| # | Name | # | Name | # | Name | # | Name | # | Name | # | Name | # | Name | # | Name |
+---+------+---+------+---+------+---+------+---+------+---+------+---+------+---+------+
| - |  -   | - |  -   | - |  -   | - |  -   | - |  -   | - |  -   | - |  -   | - |  -   |
+---+------+---+------+---+------+---+------+---+------+---+------+---+------+---+------+
| - |  -   | - |  -   | - |  -   | - |  -   | - |  -   | - |  -   | - |  -   | - |  -   |
+---+------+---+------+---+------+---+------+---+------+---+------+---+------+---+------+
CFD module: 4 VME address: 8804:
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| 64 | TOF00 | 65 | TOF01 | 66 | TOF02 | 67 | TOF03 | 68 | TOF04 | 69 | TOF05 | 70 | TOF06 | 71 | TOF07 |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| 72 | TOF08 | 73 | TOF09 | 74 | TOF0A | 75 | TOF0B | 76 | TOF0C | 77 | TOF0D | 78 | TOF0E | 79 | TOF0F |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
CFD module: 5 VME address: 8805:
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  | #  | Name  |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| 80 | TOF10 | 81 | TOF11 | 82 | TOF12 | 83 | TOF13 | 84 | TOF14 | 85 | TOF15 | 86 | TOF16 | 87 | TOF17 |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
| 88 | TOF18 | 89 | TOF19 | 90 | TOF1A | 91 | TOF1B | 92 | TOF1C | 93 | TOF1D | 94 | TOF1E | 95 | TDCT0 |
+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+----+-------+
Enter command: [help] 
```

### Viewing and adjusting the CFD module addresses
```
Enter command: [help] cfds
Current CFD modules:
+-------+---------+
| Index | Address |
+-------+---------+
|   0   |  8800   |
+-------+---------+
|   1   |  8801   |
+-------+---------+
|   2   |  8802   |
+-------+---------+
|   4   |  8804   |
+-------+---------+
|   5   |  8805   |
+-------+---------+
Enter CFD module index to add/modify: [cancel] 
```

### Viewing and adjusting input signals: (CFD enabled and CFD threshold) and logic delays and gate widths
```
Enter command: [help] inputs
Current input signals:
+---------+------------+---------+-----------+-------+------+-----------------------------------------------+
| Channel | Short Name | Enabled | Threshold | Delay | Gate | Description                                   |
+---------+------------+---------+-----------+-------+------+-----------------------------------------------+
|    0    |    T00     |  True   |    16     |   0   |  1   | Upstream trigger scintillator 0 channel 0     |
+---------+------------+---------+-----------+-------+------+-----------------------------------------------+
|    1    |    T01     |  True   |    16     |   7   |  3   | Upstream trigger scintillator 0 channel 1     |
+---------+------------+---------+-----------+-------+------+-----------------------------------------------+
|    2    |    T02     |  True   |    16     |   0   |  1   | Upstream trigger scintillator 0 channel 2     |
+---------+------------+---------+-----------+-------+------+-----------------------------------------------+
|    3    |    T03     |  True   |    16     |  255  |  3   | Upstream trigger scintillator 0 channel 3     |

...

|   94    |   TOF1E    |  True   |    16     |   0   |  1   | TOF module 1 channel 14                       |
+---------+------------+---------+-----------+-------+------+-----------------------------------------------+
|   95    |   TDCT0    |  True   |    16     |   0   |  1   | TDC stop signal for TDC2                      |
+---------+------------+---------+-----------+-------+------+-----------------------------------------------+
Enter input channel number to add/modify: [cancel] 1
Channel selected:
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
| Channel | Short Name | Enabled | Threshold | Delay | Gate | Description                               |
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
|    1    |    T01     |  False  |    16     |   7   |  3   | Upstream trigger scintillator 0 channel 1 |
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
| field:  |     0      |    1    |     2     |   3   |  4   | 5                                         |
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
Enter field # = new value: [cancel] 4=8
treatment for signal 1 set
Enter field # = new value: [cancel] 
Enter input channel number to add/modify: [cancel] 1
Channel selected:
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
| Channel | Short Name | Enabled | Threshold | Delay | Gate | Description                               |
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
|    1    |    T01     |  False  |    16     |   7   |  8   | Upstream trigger scintillator 0 channel 1 |
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
| field:  |     0      |    1    |     2     |   3   |  4   | 5                                         |
+---------+------------+---------+-----------+-------+------+-------------------------------------------+
Enter field # = new value: [cancel] 
Enter input channel number to add/modify: [cancel] 
Enter command: [help] 
```
 * The Enabled field is used to enable or disable the CFD input
 * The Threshold field sets the CFD threshold in mV
 * The delay and gate widths are specified in the fundamental clock period for WCTE: 8 ns.

The treatments to the input signals are applied before any subsequent trigger logic.

The FPGA is phase locked to the 125 MHz clock of the trigger mainboard which is phase locked to the shared 25 MHz clock.
The maximum delay and maximum gate width are 255 * 8 ns = 2.040 us.

### Viewing and adjusting the level 1 logic
```
Enter command: [help] level1
Current level 1 logic:
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
| Index | Short Name |  Inputs   | Invert Inputs | Logic | Delay | Gate | Description            |
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
|   0   |   T0 L1    | [0,1,2,3] |      []       |  AND  |   0   |  1   | T0 coincidence         |
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
|   1   |   T1 L1    | [4,5,6,7] |      []       |  AND  |   0   |  1   | T1 coincidence         |
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
|   2   |    ATCe    |  [12,13]  |      []       |  OR   |   3   |  7   | ATC electron           |
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
|   3   |   ATCeps   |  [12,13]  |      []       |  OR   |   0   |  1   | ATC electron prescaled |
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
|   4   |   HC L1    |  [9,10]   |      []       |  OR   |   0   |  1   | Hole counter           |
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
|   5   |    MUON    |  [24,25]  |      []       |  AND  |   0   |  1   | Muon tagger            |
+-------+------------+-----------+---------------+-------+-------+------+------------------------+
Enter level 1 logic index to add/modify: [cancel]  
```
There are 10 level 1 logic elements. They are referenced by their index (0-9).

 * The invert inputs specify the input signals that are inverted before the logic operation.

The delay and gate widths are applied prior to subsequent trigger logic (at level 2).

### Viewing and adjusting the level 2 logic
```
Enter command: [help] level2
Current level 2 logic:
+-------+------------+--------+---------------+-----------+------------------+-------+---------------------------------+
| Index | Short Name | Inputs | Invert Inputs | L1 inputs | Invert L1 inputs | Logic | Description                     |
+-------+------------+--------+---------------+-----------+------------------+-------+---------------------------------+
|   0   |   LE psV   |   []   |      []       |   [0,1]   |      [3,4]       |  AND  | Low Energy Trigger prescaled    |
|       |            |        |               |           |                  |       | eVeto                           |
+-------+------------+--------+---------------+-----------+------------------+-------+---------------------------------+
|   1   |   LE nV    |   []   |      []       |   [0,1]   |       [4]        |  AND  | Low Energy Trigger without      |
|       |            |        |               |           |                  |       | eVeto                           |
+-------+------------+--------+---------------+-----------+------------------+-------+---------------------------------+
|   2   |    LE e    |   []   |      []       |  [0,1,2]  |       [4]        |  AND  | Low Energy Trigger with         |
|       |            |        |               |           |                  |       | electron                        |
+-------+------------+--------+---------------+-----------+------------------+-------+---------------------------------+
|   3   |   LE mu    |   []   |      []       |  [0,1,5]  |      [2,4]       |  AND  | Low Energy Trigger with muon    |
+-------+------------+--------+---------------+-----------+------------------+-------+---------------------------------+
Enter level 2 logic index to add/modify: [cancel] 
```
There are 4 level 2 logic elements. They are referenced by their index (0-3).

The level 2 logic can take the treated inputs and the treated level 1 logic outputs to form the trigger condition.
This example includes veto conditions for "electrons" and for signals in the "hole counters".

```
### Viewing and adjusting the output lemo assignments

Enter command: [help] outputs
Current output lemo assignments:
+-------+------------+---------+---------------+-----------+----------------------------------+
| Index | Short Name | Source  | Source Serial | Treatment | Description                      |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   0   |   TDCT0    | level 2 |       0       |   True    | Event trigger (TDC_STOP)         |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   1   |   EL TAG   | level 2 |       2       |   True    | Electron tagged                  |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   2   |   MU TAG   | level 2 |       3       |   True    | Muon tagged                      |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   3   |   BSWarn   |  input  |      26       |   True    | Beam spill warning               |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   4   |   BSEnd    |  input  |      27       |   True    | Beam spill end                   |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   5   |   LASER    |  input  |      28       |   True    | Laser signal                     |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   6   |   XTRIG    |  input  |      29       |   True    | Other trigger                    |
+-------+------------+---------+---------------+-----------+----------------------------------+
|   7   |   LE nV    | level 2 |       1       |   True    | Low Energy Trigger without eVeto |
+-------+------------+---------+---------------+-----------+----------------------------------+
Enter output lemo assignment index to add/modify: [cancel] 
```

There are 16 lemo outputs on the front panel of the trigger module. These are referenced by their index (0-15).

Input signals and trigger logic outputs can be assigned to the lemo outputs. 
The treatment specifies whether the corresponding delay and gate width treatment is applied before output.
For level 2, if treatment is False, the width corresponds to the width that the trigger condition was met, but
if True, the width is one time bin. No adjustable delay is applied to the level 2 outputs.

The output of LEMO 0 (the bottom-most LEMO connector on the mezzanine card) is considered to be
the master trigger signal (TDC stop) and optionally has a deadtime veto and a inter-spill veto. 
A configuration which has the deadtime veto period shorter than the gate width of the master trigger signal will
produce an oscillating signal on the master trigger output (as the deadtime veto logic is being applied) which
should be avoided. The LEMO 0 output is also subject to the out-of-spill veto, if that is enabled.

To ensure timing consistency for LEMO 0 output, it should have a gate width of 1 (for level 2 outputs, that is
achieved by setting the treatment to True).

### Viewing and adjusting the prescaler properties (DO NOT USE)
```
Enter command: [help] prescalers
Current prescaler values:
+-------+----------+--------+
| Index | Prescale | Select |
+-------+----------+--------+
|   3   |    16    | False  |
+-------+----------+--------+
Enter prescaler index to add/modify: [cancel] 
```

#### Prescalers not currently working

The prescaler function is not currently reliable. The electron veto prescale is implemented by another mechanism.

The prescalers reduce the rate of level 1 triggers for the logic unit specified by the Index, by rejecting
a fraction of the triggers.

The most significant bit of the prescale value determines the prescale factor. The maximum prescale factor is 128.

If Select is True, a prescale factor of 4 means that every fourth trigger is accepted, and the other three are rejected.
This is appropriate if the logic unit is used to identify an event selection, and the rate of those selected
events needs to be reduced.

If Select is False, a prescale factor of 4 means that every fourth trigger is rejected, and the other three are accepted.
This is appropriate if the logic unit is used to identify a veto condition (for example, the electron veto) and a
for a fraction of events, the veto should not be applied (so as to accept some electrons).

To disable the prescaler, set the Select field to True and the Prescale value to 1.

### Viewing and adjusting the spill signal assignments
```
Enter command: [help] spills
Current spill signal assignments:
+-------------------+-------------------+---------+
| Pre-spill channel | End-spill channel | Enabled |
+-------------------+-------------------+---------+
|        26         |        27         |  True   |
+-------------------+-------------------+---------+
Enter pre-spill, end-spill: [cancel] 
```

The spill signals are assigned to the input channels that correspond to the beam spill warning and beam spill end signals.
With enabled set to True then between spills, the master trigger output (LEMO 0) is vetoed and all counters are frozen.
This ensures that the number of master triggers during a spill is well established, that the counters reflect the rate
of beam related signals, and that resetting the counters can be done at any time between spills.

To disable the special spill treatment, set the Enabled field to False.

### Viewing and adjusting the deadtime
```
Enter command: [help] deadtime
Current deadtime value:
+----------+
| Deadtime |
+----------+
|   625    |
+----------+
Enter deadtime: [cancel] 
```

The deadtime is applied to signals directed to the master trigger output (LEMO 0). 
Signals are blocked for the specified number of clock cycles after the master trigger signal is generated.
The value 625 corresponds to 5 us, which is the nominal deadtime being considered for the WCTE trigger.
The minimum deadtime is 1 (8 ns).

### Viewing and adjusting the connections to the trigger/digitizer boards
```
Enter command: [help] connections
Current trigger/digitizer board connections:
+-------+-------+---------+--------+---------------+-------------------+
| Index | Board | Channel | Source | Source Serial | Source Short Name |
+-------+-------+---------+--------+---------------+-------------------+
|   0   |   0   |    0    | other  |     TDCT0     |         -         |
+-------+-------+---------+--------+---------------+-------------------+
|   1   |   0   |    1    |  lemo  |       1       |      EL TAG       |
+-------+-------+---------+--------+---------------+-------------------+
|   2   |   0   |    2    |  lemo  |       2       |      MU TAG       |
+-------+-------+---------+--------+---------------+-------------------+
|   3   |   0   |    3    |  lemo  |       3       |      BSWarn       |
+-------+-------+---------+--------+---------------+-------------------+
|   4   |   0   |    4    |  lemo  |       4       |       BSEnd       |
+-------+-------+---------+--------+---------------+-------------------+
|   5   |   0   |    5    |  lemo  |       5       |       LASER       |
+-------+-------+---------+--------+---------------+-------------------+
|   6   |   0   |    6    |  lemo  |       6       |       XTRIG       |
+-------+-------+---------+--------+---------------+-------------------+
|  10   |   0   |   10    | input  |       0       |        T00        |
+-------+-------+---------+--------+---------------+-------------------+
|  11   |   0   |   11    | input  |       1       |        T01        |
+-------+-------+---------+--------+---------------+-------------------+
|  12   |   0   |   12    | input  |       2       |        T02        |
+-------+-------+---------+--------+---------------+-------------------+
|  13   |   0   |   13    | input  |       3       |        T03        |

...

```
This information shows the connections to the trigger/digitizer boards.
This part of the configuration does not affect the register values for the WCTE trigger FPGA, but is
recorded in the configuration file as an important reference for the signals being sampled by the
trigger/digitizer boards.

There are 3 boards (numbered 0,1,2). Ten channels are reserved for logic channels on boards 0 and 1
(and channel 19 for board 2) which generally are connected to the lemo outputs from the trigger module.
The remaining 40 channels are generally connected to the input signals (split before the discriminator) 
from the beamline modules or other signals (for example, the laser signal).

The index is a combination of the board number and the channel number (board number * 20 + channel number).

For consistent timing of digital signals, the connections to logic channels should have a fixed gate width = 1.
A warning indication will be shown in the table if that is not the case for any of the logic channels.

### Viewing and adjusting the connections to the patch panel
```
Enter command: [help] patches
Current patch panel connections:
+-------+--------+---------------+-------------------+
| Index | Source | Source Serial | Source Short Name |
+-------+--------+---------------+-------------------+
|   0   | other  |     TDCT0     |         -         |
+-------+--------+---------------+-------------------+
|   1   | other  |     XTRIG     |         -         |
+-------+--------+---------------+-------------------+
|   2   |  lemo  |       7       |       LE nV       |
+-------+--------+---------------+-------------------+
|   8   |  lemo  |       8       |         -         |
+-------+--------+---------------+-------------------+
|   9   |  lemo  |       9       |         -         |

...
```
This information shows the connections to the patch panel that allows signalling between the T9 area and the control room.
The information does not affect the register values for the WCTE trigger FPGA, but is recorded in the configuration file
as an important reference for the signals being routed between the T9 area and the control room.

In this example, patch panel cable 0 is for the master trigger signal that is fanned out from the T9 area.
The patch panel cable 1 is for the external trigger signal that is fed as input #29 into the trigger module.
The patch panel cable 2 is for the low energy trigger without eVeto signal that can be used for accelerator tuning.

Patch panel cables 8-15 are connected to lemo channels 8-15 on the trigger module. These will be used to route signals
into the control room to determine delay and gate width settings for trigger logic, among other things.

It is assumed that there are 16 patch panel cables available for use, and they are numbered (0-15) according to the index above.

### Saving the configuration

The "save" command saves the configuration to a JSON file in the "configurations" folder.
When saving  a configuration, the filename prefix, short name, and description are specified, and the file is saved in the "configurations" folder,
and the corresponding register settings are saved in the "register_settings" folder.
Existing files cannot be overwritten to ensure that a named configuration has a unique definition.

Note that the filename prefix is appended with "_config", "_register_settings", and _cfd_register_settings for the configuration, trigger logic register settings files, 
and CFD register settings respectively, so that their purpose and association is clear.

### Writing the current register settings to current_registers.json and current_cfd_registers.json

While setting up the trigger configuration for the first time (or making significant adjustments), a large number of incremental adjustments will be made to the configuration.
Instead of saving configuration files for every step, the "update" command can be used. It writes the current trigger logic module register settings to the 
file "current_registers.json", and the current CFD register settings to the file "current_cfd_registers.json", overwriting the previous versions. 
By loading these files into the VME modules, the configuration can be set quickly and further adjustments can be made. 
Once a large set of adjustments has been made, the configuration and register setting files can be saved to new files using the "save" command (see previous section).

### Bulk copying of input and output settings

During tests of the VME modules, it can be helpful to set many input and output parameters to the same value. For those
cases, the "copy" function can be used. It will copy the settings of one input or output to other inputs or outputs.
Use the command "inputs" or "outputs" to view the current settings, and then type "c" (for copy) followed by the index of the
reference input or output (for example c0). You are then asked to enter the range of inputs or outputs 
to copy the settings to (for example 1-7).