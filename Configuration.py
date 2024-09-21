# Define the configuration of the trigger through nested dictionaries that can be written to a JSON file

# Note that json converts any dictionary integer key to a string, so all keys strings
# To produce simpler code for the console application, the dictionary values are all strings
# Use the convention that all keys refer to variables with the identical name and use "snake case"

# Import the necessary modules
import json

import sys
sys.path.insert(0, "../V1495_firmware")
from scripts.genRegisterHeader import getRegisterList

# Define the configuration class
class Configuration:
    # Define the constructor
    def __init__(self, short_name: str, description: str):
        # Define the configuration dictionary
        self.configuration = {
            "config_version": self.get_version(),
            "short_name": short_name,
            "description": description,
            "input_signals": {},
            "input_signal_treatments": {},
            "level_1_logics": {},
            "level_1_output_treatments": {},
            "level_2_logics": {},
            "output_lemo_assignments": {},
            "trigger_digitizer_board_connections": {},
            "patch_panel_connections": {},
            "prescalers": {},
            "spill_channels": {},
            "deadtime": None,
        }
        self.maximum_delay = 255
        self.maximum_window_length = 255

        self.register_list = getRegisterList("../V1495_firmware/src/V1495_regs_pkg.vhd")
        self.register_settings = {}

    # Get the version number (change when the configuration format changes)
    @staticmethod
    def get_version():
        return "1.0"

    def check_int(self, serial: str, min_value: int, max_value: int):
        # check that the number is a string between the min and max values
        if not (serial.isdigit() and min_value <= int(serial) <= max_value):
            print(f'*** invalid value {serial}. It must be a integer between {min_value} and {max_value}')
            return False
        return True

    def check_string(self, string: str, max_length: int):
        # check that the string is a string of length at most max_length
        if not isinstance(string, str) or len(string) > max_length:
            print(f'*** invalid string {string}. It must be a string of length at most {max_length}')
            return False
        return True

    def check_bool(self, boolean: str):
        # check that the boolean is a string that converts to boolean
        if boolean not in ["True", "False"]:
            print(f'*** invalid boolean {boolean}. It must be either "True" or "False"')
            return False
        return True

    # Define a new signal and add to the trigger configuration
    def set_signal(self, serial: str, short_name: str, description: str, verbose: bool = True):

        fail = False
        # check that the serial number is a number between 0 and 95
        fail = fail or not self.check_int(serial, 0, 95)

        # check that the short name is a string of length at most 10 (for printing purposes)
        fail = fail or not self.check_string(short_name, 10)

        # check that the description is a string of length at most 60 (for printing purposes)
        fail = fail or not self.check_string(description, 60)

        if not fail:

            # check if the serial number is already in the configuration
            new_signal = True
            if serial in self.configuration["input_signals"]:
                new_signal = False

            # Assign the signal dictionary to the configuration
            signal = {
                "short_name": short_name,
                "description": description
            }
            self.configuration["input_signals"][serial] = signal
            if verbose:
                if new_signal:
                    print(f'signal {serial} ({short_name}) added')
                else:
                    print(f'signal {serial} ({short_name}) modified')

            # Set the default treatment for new signals:
            if new_signal:
                self.set_treatment(serial, verbose=verbose)
                if verbose:
                    print(f'default treatment for signal {serial} set')

    def set_treatment(self, serial: str, delay: str = "0", window_length: str = "1", verbose: bool = True):

        fail = False
        # check that the serial number is a number between 0 and 95
        fail = fail or not self.check_int(serial, 0, 95)

        fail = fail or not self.check_int(delay, 0, self.maximum_delay)
        fail = fail or not self.check_int(window_length, 1, self.maximum_window_length)

        if not fail:
            # Define the treatment dictionary
            treatment = {
                "delay": delay,
                "window_length": window_length
            }

            # Assign the treatment dictionary to the configuration
            self.configuration["input_signal_treatments"][serial] = treatment
            if verbose:
                print(f'treatment for signal {serial} set')

    def set_level_1_logic(self, serial:str, short_name:str, description: str, inputs: str, invert_inputs: str, logic_type: str, verbose: bool = True):
        fail = False
        # check that the serial number is a number between 0 and 9
        fail = fail or not self.check_int(serial, 0, 9)

        # check that the short name is a string of length at most 10 (for printing purposes)
        fail = fail or not self.check_string(short_name, 10)

        # check that the description is a string of length at most 60 (for printing purposes)
        fail = fail or not self.check_string(description, 60)

        # check that inputs and invert_inputs are both str that translates to a python list of numbers between 0 and 63
        for inputs_str in [inputs, invert_inputs]:
            check_brackets = inputs_str[0] == '[' and inputs_str[-1] == ']'
            str_list = inputs_str.strip().strip('[]').split(',')
            if not check_brackets and all(i.isdigit() and 0 <= int(i) <= 63 for i in str_list):
                fail = True
                print(f'*** invalid specification: {inputs_str}. It must be a list of numbers between 0 and 63')

        # check that the logic type is a string and either "AND" or "OR"
        if logic_type not in ["AND", "OR"]:
            fail = True
            print(f'*** invalid logic type {logic_type}. It must be either "AND" or "OR"')

        if not fail:

            # check if the serial number is already in the configuration
            new_logic = True
            if serial in self.configuration["level_1_logics"]:
                new_logic = False
                short_old = self.configuration["level_1_logics"][serial]["short_name"]
                if verbose:
                    print(f'level 1 logic {serial} ({short_old}) replaced by new level 1 logic ({short_name})')

            # Define the logic dictionary
            logic = {
                "short_name": short_name,
                "description": description,
                "inputs": inputs,
                "invert_inputs": invert_inputs,
                "logic_type": logic_type
            }
            # Assign the logic dictionary to the configuration
            self.configuration["level_1_logics"][serial] = logic
            if verbose:
                print(f'level 1 logic {serial} ({short_name}) added')

            # Set the default treatment for new level 1 logics:
            if new_logic:
                self.set_level_1_treatment(serial, verbose=verbose)
                if verbose:
                    print(f'default treatment for level 1 logic output {serial} set')


    def set_level_1_treatment(self, serial: str, delay: str = "0", window_length: str = "1", verbose: bool = True):
        fail = False
        # check that the serial number is a number between 0 and 9
        fail = fail or not self.check_int(serial, 0, 9)

        fail = fail or not self.check_int(delay, 0, self.maximum_delay)
        fail = fail or not self.check_int(window_length, 0, self.maximum_window_length)

        if not fail:
            # Define the treatment dictionary
            treatment = {
                "delay": delay,
                "window_length": window_length
            }

            # Assign the treatment dictionary to the configuration
            self.configuration["level_1_output_treatments"][serial] = treatment
            if verbose:
                print(f'treatment for level 1 output {serial} set')


    def set_level_2_logic(self, serial:str, short_name:str, description: str, inputs: str, invert_inputs: str, level_1_inputs: str, invert_level_1_inputs: str, logic_type: str, verbose: bool = True):
        fail = False
        # check that the serial number is a number between 0 and 3
        fail = fail or not self.check_int(serial, 0, 3)

        # check that the short name is a string of length at most 10 (for printing purposes)
        fail = fail or not self.check_string(short_name, 10)

        # check that the description is a string of length at most 60 (for printing purposes)
        fail = fail or not self.check_string(description, 60)

        # check that the inputs and invert_inputs are both lists of numbers between 0 and 63
        for inputs_str in [inputs, invert_inputs]:
            check_brackets = inputs_str[0] == '[' and inputs_str[-1] == ']'
            str_list = inputs_str.strip().strip('[]').split(',')
            if not check_brackets and all(i.isdigit() and 0 <= int(i) <= 63 for i in str_list):
                fail = True
                print(f'*** invalid specification {inputs_str}. It must be a list of numbers between 0 and 63')

        # check that level_1_inputs and invert_level_1_inputs are both lists of numbers between 0 and 9
        for level_1_inputs_str in [level_1_inputs, invert_level_1_inputs]:
            check_brackets = level_1_inputs_str[0] == '[' and level_1_inputs_str[-1] == ']'
            str_list = level_1_inputs_str.strip().strip('[]').split(',')
            if not check_brackets and all(i.isdigit() and 0 <= int(i) <= 9 for i in str_list):
                fail = True
                print(f'*** invalid specification {level_1_inputs_str}. It must be a list of numbers between 0 and 9')

        # check that the logic type is a string and either "AND" or "OR"
        if logic_type not in ["AND", "OR"]:
            fail = True
            print(f'*** invalid logic type {logic_type}. It must be either "AND" or "OR"')

        if not fail:

            # check if the serial number is already in the configuration
            new_logic = True
            if serial in self.configuration["level_2_logics"]:
                new_logic = False
                short_old = self.configuration["level_2_logics"][serial]["short_name"]
                if verbose:
                    print(f'level 2 logic {serial} ({short_old}) replaced by new level 2 logic ({short_name})')

            # Define the logic dictionary
            logic = {
                "short_name": short_name,
                "description": description,
                "inputs": inputs,
                "invert_inputs": invert_inputs,
                "level_1_inputs": level_1_inputs,
                "invert_level_1_inputs": invert_level_1_inputs,
                "logic_type": logic_type
            }
            # Assign the logic dictionary to the configuration
            self.configuration["level_2_logics"][serial] = logic
            if verbose:
                print(f'level 2 logic {serial} ({short_name}) added')

    def set_output_lemo_assignment(self, serial: str, short_name:str, description: str, source: str, source_serial: str, treatment: str, verbose: bool = True):
        fail = False
        # check that the serial number (output lemo connector number) is a number between 0 and 15
        fail = fail or not self.check_int(serial, 0, 15)

        # check that the short name is a string of length at most 10 (for printing purposes)
        fail = fail or not self.check_string(short_name, 10)

        # check that the description is a string of length at most 60 (for printing purposes)
        fail = fail or not self.check_string(description, 60)

        # check that the source is one of "input", "level 1", "level 2"
        if source not in ["input", "level 1", "level 2"]:
            fail = True
            print(f'*** invalid source {source}. It must be one of "input", "level 1", "level 2"')

        # check that the source serial number is valid
        if source == "input":
            fail = fail or not self.check_int(source_serial, 0, 95)
        elif source == "level 1":
            fail = fail or not self.check_int(source_serial, 0, 9)
        elif source == "level 2":
            fail = fail or not self.check_int(source_serial, 0, 3)

        # check that the treatment is a boolean (specifies if the treatment is applied or not)
        fail = fail or not self.check_bool(treatment)

        if not fail:
            # Define the output dictionary
            output = {
                "short_name": short_name,
                "description": description,
                "source": source,
                "source_serial": source_serial,
                "treatment": treatment
            }
            # Assign the output to the configuration
            self.configuration["output_lemo_assignments"][serial] = output
            if verbose:
                extra = "with treatment" if treatment == "True" else "without treatment"
                print(f'{source}-{source_serial} {extra} assigned to LEMO {serial}')

    def set_trigger_board_connection(self, board: str, channel: str, source: str, source_serial: str, verbose: bool = True):
        fail = False
        # check that the board number is a number between 0 and 2
        fail = fail or not self.check_int(board, 0, 2)

        if board in ["0", "1"]:
            # check that the channel number is a number between 0 and 9
            fail = fail or not self.check_int(channel, 0, 9)
        elif board == "2":
            # check that the channel number is 0
            fail = fail or not self.check_int(channel, 0, 0)

        # check that source is one of "lemo" or "patch panel" or "other"
        if source not in ["lemo", "patch panel", "other"]:
            fail = True
            print(f'*** invalid source {source}. It must be one of "lemo", "patch panel", "other"')

        # check that the source serial number is valid
        if source == "lemo":
            fail = fail or not self.check_int(source_serial, 0, 15)
        elif source == "patch panel":
            fail = fail or not self.check_int(source_serial, 0, 15)

        if not fail:
            # Define the connection dictionary
            connection = {
                "board": board,
                "channel": channel,
                "source": source,
                "source_serial": source_serial
            }
            # Assign the connection to the configuration
            serial = str(int(board)*20 + int(channel))
            self.configuration["trigger_digitizer_board_connections"][serial] = connection
            if verbose:
                print(f'{source}-{source_serial} connected to trigger board {board} channel {channel}')

    def set_digitizer_board_connection(self, board: str, channel: str, source: str, source_serial: str, verbose: bool = True):
        fail = False
        # check that the board number is a number between 0 and 2
        fail = fail or not self.check_int(board, 0, 2)

        if board in ["0", "1"]:
            # check that the channel number is a number between 10 and 19
            fail = fail or not self.check_int(channel, 10, 19)
        elif board == "2":
            # check that the channel number is a number between 1 and 19
            fail = fail or not self.check_int(channel, 1, 19)

        # check that source is one of "input" or "other"
        if source not in ["input", "other"]:
            fail = True
            print(f'*** invalid source {source}. It must be one of "input" or "other"')

        # check that the source serial number is valid
        if source == "input":
            fail = fail or not self.check_int(source_serial, 0, 95)

        if not fail:
            # Define the connection dictionary
            connection = {
                "board": board,
                "channel": channel,
                "source": source,
                "source_serial": source_serial
            }
            # Assign the connection to the configuration
            serial = str(int(board)*20 + int(channel))
            self.configuration["trigger_digitizer_board_connections"][serial] = connection
            if verbose:
                print(f'{source}-{source_serial} connected to digitizer board {board} channel {channel}')

    def set_patch_panel_connection(self, serial: str, source: str, source_serial: str, verbose: bool = True):
        fail = False

        # check that the serial number is a number between 0 and 15
        fail = fail or not self.check_int(serial, 0, 15)

        # check that source is one of "lemo" or "other"
        if source not in ["lemo", "other"]:
            fail = True
            print(f'*** invalid source {source}. It must be one of "lemo", "patch panel", "other"')

        # check that the source serial number is valid
        if source == "lemo":
            fail = fail or not self.check_int(source_serial, 0, 15)

        if not fail:
            # Define the connection dictionary
            connection = {
                "source": source,
                "source_serial": source_serial
            }
            # Assign the connection to the configuration
            self.configuration["patch_panel_connections"][serial] = connection
            if verbose:
                print(f'{source}-{source_serial} connected to patch panel position {serial}')

    def set_prescaler(self, serial: str, prescale: str, verbose: bool = True):
        fail = False
        # check that the serial number is a number between 0 and 9 (level 1 logic output)
        fail = fail or not self.check_int(serial, 0, 9)

        # check that the prescale is a number between 0 and 255
        fail = fail or not self.check_int(prescale, 0, 256)

        if not fail:
            # Assign the prescale to the configuration
            self.configuration["prescalers"][serial] = prescale
            if verbose:
                print(f'prescaler {serial} set to {prescale}')

    def set_spill_channel(self, pre_spill: str, end_spill: str, enabled: str, verbose: bool = True):
        fail = False
        # check that the pre_spill and end_spill are numbers between 0 and 63
        fail = fail or not self.check_int(pre_spill, 0, 63)
        fail = fail or not self.check_int(end_spill, 0, 63)
        # check that the enabled is a boolean (specifies if the out of spill veto is applied)
        fail = fail or not self.check_bool(enabled)

        if not fail:
            # Assign the spill channel to the configuration
            self.configuration["spill_channels"]["pre_spill"] = pre_spill
            self.configuration["spill_channels"]["end_spill"] = end_spill
            self.configuration["spill_channels"]["enabled"] = enabled
            if verbose:
                print(f'(pre- and end-) spill channels set to ({pre_spill} and {end_spill} with enabled {enabled}')

    def set_deadtime_veto(self, deadtime: str, verbose: bool = True):
        fail = False
        # check that the deadtime is a number between 1 and 2 million
        fail = fail or not self.check_int(deadtime, 0, 2000000)

        if not fail:
            self.configuration["deadtime"] = deadtime
            if verbose:
                print(f'deadtime veto set to {deadtime}')

    # Define the get configuration method
    def get_configuration(self):
        # Return the configuration
        return self.configuration

    # Define the write configuration method
    def write_configuration(self, filename):
        # Check that there is no file with this name
        try:
            with open(filename, "r") as file:
                print(f'*** file {filename} already exists - please choose a different name')
                return False
        except FileNotFoundError:
            pass
        # Open the file for writing
        with open(filename, "w") as file:
            # Write the configuration to the file
            json.dump(self.configuration, file, indent=4)
        return True

    # Define the read configuration method
    def read_configuration(self, filename):
        # Open the file for reading
        with open(filename, "r") as file:
            # Read the configuration from the file
            self.configuration = json.load(file)

    # Define the write register_settings method
    def write_register_settings(self, filename, overwrite: bool = False):
        if not overwrite:
            # Check that there is no file with this name
            try:
                with open(filename, "r") as file:
                    print(f'*** file {filename} already exists - please choose a different name')
                    return False
            except FileNotFoundError:
                pass
        # Open the file for writing
        with open(filename, "w") as file:
            # Write the configuration to the file
            json.dump(self.register_settings, file, indent=4)
        return True

    # Define the save method that writes both the configuration  and register values to json files
    def save(self, filename, verbose: bool = True):
        # Write the configuration to a json file
        config_filename = 'configurations/' + filename + '_config.json'
        success = self.write_configuration(config_filename)
        if success:
            if verbose:
                print('Saved configuration to ' + config_filename)
            # Set and write the register values to a json file
            self.set_registers()
            register_settings_filename = 'register_settings/' + filename + '_registers.json'
            success2 = self.write_register_settings(register_settings_filename)
            if success2 and verbose:
                print('Saved register settings to ' + register_settings_filename)
                return True
        return False

    # Define the update method - used to update the registration settings for a quick change of settings
    def update(self, verbose: bool = True):
        # Set and write the register values to a json file
        self.set_registers()
        register_settings_filename = 'register_settings/current_registers.json'
        success = self.write_register_settings(register_settings_filename, overwrite=True)
        if success and verbose:
            print('Saved register settings to ' + register_settings_filename)

    def set_registers(self):
        # Work out the values for the VME module registers
        # Note: write a value to every register - so that previous settings are overwritten
        reg = {}
        register_type = 'read/write'
        # 8 bit value registers: delays and window lengths
        register_names = {'ARW_DELAY_PRE':{"config_category":"input_signal_treatments", "config_key":"delay", "number":64},
                          'ARW_GATE_PRE':{"config_category":"input_signal_treatments", "config_key":"window_length", "number":64},
                          'ARW_DELAY_LEVEL1':{"config_category":"level_1_output_treatments", "config_key":"delay"},
                          'ARW_GATE_LEVEL1':{"config_category":"level_1_output_treatments", "config_key":"window_length"},
                          }

        for register_name in register_names:
            register_addresses = self.register_list[register_type][register_name]['addresses']
            config_category = register_names[register_name]["config_category"]
            config_key = register_names[register_name]["config_key"]
            # initialize registers to 0 (all registers must be written to)
            for register_address in register_addresses:
                reg[hex(register_address)] = hex(0)
            for ist in self.configuration[config_category]:
                if "number" not in register_names[register_name] or int(ist) < register_names[register_name]["number"]:
                    value = int(self.configuration[config_category][ist][config_key])
                    register_index = int(ist)//4
                    register_address = hex(register_addresses[register_index])
                    register_offset = (int(ist)%4)*8
                    reg_value = int(reg[register_address], 16)
                    reg_value |= value << register_offset
                    reg[register_address] = hex(reg_value)

        # 1 bit value registers: invert_inputs (INV) and inputs for logic (MASK)
        one_bit_regs = {'INV': {'L1':['A','B'], 'L2':['A','B','L1']},
                        'MASK': {'L1':['A','B'], 'L2':['A','B','L1']}}
        for spec in one_bit_regs:
            for logic_level in one_bit_regs[spec]:
                for source in one_bit_regs[spec][logic_level]:
                    register_name = f'ARW_{source}{spec}_{logic_level}'
                    register_addresses = self.register_list[register_type][register_name]['addresses']
                    config_category = {'L1':'level_1_logics', 'L2':'level_2_logics'}[logic_level]
                    config_key = 'invert_inputs' if spec == 'INV' else 'inputs'
                    if source == 'L1':
                        config_key = 'invert_level_1_inputs' if spec == 'INV' else 'level_1_inputs'
                    offset = {'A':0, 'B':32, 'L1':0}[source]
                    # initialize registers to 0 (all registers must be written to)
                    for register_address in register_addresses:
                        reg[hex(register_address)] = hex(0)
                    for ist in self.configuration[config_category]:
                        inputs_str = self.configuration[config_category][ist][config_key]
                        inputs_split = inputs_str.strip().strip('[]').split(',')
                        value = 0
                        if len(inputs_split[0]) > 0:
                            inputs_list = [int(i) for i in inputs_split]
                            for input in inputs_list:
                                if offset <= input < offset + 32:
                                    shift = input - offset
                                    value |= 1 << shift
                        register_index = int(ist)
                        register_address = hex(register_addresses[register_index])
                        reg[register_address] = hex(value)

        # Logic type for level 1 and level 2 logics
        register_name = 'ARW_LOGIC_TYPE'
        register_address = self.register_list[register_type][register_name]['addresses'][0]
        value = 0
        for ist in self.configuration['level_1_logics']:
            logic_type = 0 if self.configuration['level_1_logics'][ist]['logic_type'] == 'AND' else 1
            value |= logic_type << int(ist)
        for ist in self.configuration['level_2_logics']:
            logic_type = 0 if self.configuration['level_2_logics'][ist]['logic_type'] == 'AND' else 1
            value |= logic_type << (int(ist)+10)
        reg[hex(register_address)] = hex(value)

        # Output assignments: LEMO in port E and F: lemo 0 is the lowest lemo in port F
        for register_name, lemo_offset in zip(['ARW_F', 'ARW_E'], [0, 8]):
            register_addresses = self.register_list[register_type][register_name]['addresses']
            # initialize registers to 0 (all registers must be written to)
            for register_address in register_addresses:
                reg[hex(register_address)] = hex(0)
            for ist in self.configuration["output_lemo_assignments"]:
                if 0 + lemo_offset <= int(ist) < lemo_offset + 8:
                    source = self.configuration["output_lemo_assignments"][ist]["source"]
                    offset = {'input':0, 'level 1':96, 'level 2':107}[source]
                    source_serial = int(self.configuration["output_lemo_assignments"][ist]["source_serial"])
                    treatment = 1 << 7 if self.configuration["output_lemo_assignments"][ist]["treatment"] == "True" else 0
                    value = offset + source_serial + treatment
                    pointer = int(ist) - lemo_offset
                    reg[hex(register_addresses[pointer])] = hex(value)

        # Prescalers
        register_name = 'ARW_POST_L1_PRESCALE'
        register_addresses = self.register_list[register_type][register_name]['addresses']
        # initialize registers to 0 (all registers must be written to)
        for register_address in register_addresses:
            reg[hex(register_address)] = hex(0)
        for ist in self.configuration["prescalers"]:
            value = int(self.configuration["prescalers"][ist])
            reg[hex(register_addresses[int(ist)])] = hex(value)

        # Spill channels
        register_name = 'ARW_SPILL'
        register_address = self.register_list[register_type][register_name]['addresses'][0]
        value = 0
        value += int(self.configuration["spill_channels"].get("pre_spill",50))
        value += int(self.configuration["spill_channels"].get("end_spill", 51)) << 8
        if self.configuration["spill_channels"].get("enabled", "False") == "True":
            value += 1 << 16

        reg[hex(register_address)] = hex(value)

        # Deadtime veto
        register_name = 'ARW_DEADTIME'
        register_address = self.register_list[register_type][register_name]['addresses'][0]
        value_str = self.configuration["deadtime"]
        if value_str is None:
            value = 1
        else:
            value = min(1,int(value_str))
        reg[hex(register_address)] = hex(value)

        self.register_settings = reg