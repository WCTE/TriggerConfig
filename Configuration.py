# Define the configuration of the trigger through nested dictionaries that can be written to a JSON file
# Note that json converts dictionary integer keys to strings, so the keys are all strings

# Import the necessary modules
import json

import os
import sys
sys.path.insert(0, "../V1495_firmware")
from scripts.genRegisterHeader import getRegisterList

# Define the configuration class
class Configuration:
    # Define the constructor
    def __init__(self, short_name: str, description: str):
        # Define the configuration dictionary
        self.configuration = {
            "config_version": "0.1",
            "short name": short_name,
            "description": description,
            "input signals": {},
            "input signal treatment": {},
            "level 1 logics": {},
            "level 1 output treatment": {},
            "level 2 logics": {},
            "level 2 output treatment": {},
            "output lemo assignments": {},
            "prescalers": {},
            "deadtime veto": {}
        }
        self.maximum_delay = 255
        self.maximum_window_length = 255

        self.REGISTERS = getRegisterList("../V1495_firmware/src/V1495_regs_pkg.vhd")

    def check_int(self, serial: int, min_value: int, max_value: int):
        # check that the number is a number between the min and max values
        if not (isinstance(serial, int) and min_value <= serial <= max_value):
            print(f'invalid value {serial}. It must be a integer between {min_value} and {max_value}')
            return False
        return True

    def check_string(self, string: str, max_length: int):
        # check that the string is a string of length at most max_length
        if not isinstance(string, str) or len(string) > max_length:
            print(f'invalid string {string}. It must be a string of length at most {max_length}')
            return False
        return True

    def check_bool(self, boolean: bool):
        # check that the boolean is a boolean
        if not isinstance(boolean, bool):
            print(f'invalid boolean {boolean}. It must be a boolean')
            return False
        return True

    # Define a new signal and add to the trigger configuration
    def set_signal(self, serial: int, short_name: str, description: str, verbose: bool = True):

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
            if str(serial) in self.configuration["input signals"]:
                new_signal = False

            # Assign the signal dictionary to the configuration
            signal = {
                "short name": short_name,
                "description": description
            }
            self.configuration["input signals"][str(serial)] = signal
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

    def set_treatment(self, serial: int, delay: int = 0, window_length: int = 1, invert: bool = False, verbose: bool = True):

        fail = False
        # check that the serial number is a number between 0 and 95
        fail = fail or not self.check_int(serial, 0, 95)

        fail = fail or not self.check_int(delay, 0, self.maximum_delay)
        fail = fail or not self.check_int(window_length, 1, self.maximum_window_length)

        # check that the invert is a boolean
        fail = fail or not self.check_bool(invert)

        if not fail:
            # Define the treatment dictionary
            treatment = {
                "delay": delay,
                "window length": window_length,
                "invert": invert
            }

            # Assign the treatment dictionary to the configuration
            self.configuration["input signal treatment"][str(serial)] = treatment
            if verbose:
                print(f'treatment for signal {serial} set')

    def set_level_1_logic(self, serial:int, short_name:str, description: str, inputs: list, logic_type: str, verbose: bool = True):
        fail = False
        # check that the serial number is a number between 0 and 9
        fail = fail or not self.check_int(serial, 0, 9)

        # check that the short name is a string of length at most 10 (for printing purposes)
        fail = fail or not self.check_string(short_name, 10)

        # check that the description is a string of length at most 60 (for printing purposes)
        fail = fail or not self.check_string(description, 60)

        # check that the inputs is a list of numbers between 0 and 63
        if not all(isinstance(i, int) and 0 <= i <= 63 for i in inputs):
            fail = True
            print(f'invalid inputs {inputs}. It must be a list of numbers between 0 and 63')

        # check that the logic type is a string and either "and" or "or"
        if not isinstance(logic_type, str) or logic_type not in ["AND", "OR"]:
            fail = True
            print(f'invalid logic type {logic_type}. It must be a string and either "AND" or "OR"')

        if not fail:

            # check if the serial number is already in the configuration
            new_logic = True
            if str(serial) in self.configuration["level 1 logics"]:
                new_logic = False
                short = self.configuration["level 1 logics"][str(serial)]["short name"]
                if verbose:
                    print(f'level 1 logic {serial} ({short}) replaced by new level 1 logic {short_name}')

            # Define the logic dictionary
            logic = {
                "short name": short_name,
                "description": description,
                "inputs": inputs,
                "type": logic_type
            }
            # Assign the logic dictionary to the configuration
            self.configuration["level 1 logics"][str(serial)] = logic
            if verbose:
                print(f'level 1 logic {serial} ({short_name}) added')

            # Set the default treatment for new level 1 logics:
            if new_logic:
                self.set_level_1_treatment(serial, verbose=verbose)
                if verbose:
                    print(f'default treatment for level 1 logic output {serial} set')


    def set_level_1_treatment(self, serial: int, delay: int = 0, window_length: int = 1, invert: bool = False, verbose: bool = True):

        fail = False
        # check that the serial number is a number between 0 and 9
        fail = fail or not self.check_int(serial, 0, 9)

        fail = fail or not self.check_int(delay, 0, self.maximum_delay)
        fail = fail or not self.check_int(window_length, 0, self.maximum_window_length)

        # check that the invert is a boolean
        fail = fail or not self.check_bool(invert)

        if not fail:
            # Define the treatment dictionary
            treatment = {
                "delay": delay,
                "window length": window_length,
                "invert": invert
            }

            # Assign the treatment dictionary to the configuration
            self.configuration["level 1 output treatment"][str(serial)] = treatment
            if verbose:
                print(f'treatment for level 1 output {serial} set')


    def set_level_2_logic(self, serial:int, short_name:str, description: str, inputs: list, level_1_inputs: list, logic_type: str, verbose: bool = True):
        fail = False
        # check that the serial number is a number between 0 and 3
        fail = fail or not self.check_int(serial, 0, 3)

        # check that the short name is a string of length at most 10 (for printing purposes)
        fail = fail or not self.check_string(short_name, 10)

        # check that the description is a string of length at most 60 (for printing purposes)
        fail = fail or not self.check_string(description, 60)

        # check that the inputs is a list of numbers between 0 and 63
        if not all(isinstance(i, int) and 0 <= i <= 63 for i in inputs):
            fail = True
            print(f'invalid inputs {inputs}. It must be a list of numbers between 0 and 63')

        # check that the level_1_inputs is a list of numbers between 0 and 9
        if not all(isinstance(i, int) and 0 <= i <= 9 for i in level_1_inputs):
            fail = True
            print(f'invalid inputs {inputs}. It must be a list of numbers between 0 and 9')

        # check that the logic type is a string and either "and" or "or"
        if not isinstance(logic_type, str) or logic_type not in ["AND", "OR"]:
            fail = True
            print(f'invalid logic type {logic_type}. It must be a string and either "AND" or "OR    "')

        if not fail:

            # check if the serial number is already in the configuration
            new_logic = True
            if str(serial) in self.configuration["level 2 logics"]:
                new_logic = False
                short = self.configuration["level 2 logics"][str(serial)]["short name"]
                if verbose:
                    print(f'level 2 logic {serial} ({short}) replaced by new level 2 logic {short_name}')

            # Define the logic dictionary
            logic = {
                "short name": short_name,
                "description": description,
                "inputs": inputs,
                "level 1 inputs": level_1_inputs,
                "type": logic_type
            }
            # Assign the logic dictionary to the configuration
            self.configuration["level 2 logics"][str(serial)] = logic
            if verbose:
                print(f'level 1 logic {serial} ({short_name}) added')

            # Set the default treatment for new level 2 logics:
            if new_logic:
                self.set_level_2_treatment(serial, verbose=verbose)
                if verbose:
                    print(f'default treatment for level 2 logic output {serial} set')

    def set_level_2_treatment(self, serial: int, delay: int = 0, window_length: int = 1, invert: bool = False, verbose: bool = True):

        fail = False
        # check that the serial number is a number between 0 and 3
        fail = fail or not self.check_int(serial, 0, 3)

        fail = fail or not self.check_int(delay, 0, self.maximum_delay)
        fail = fail or not self.check_int(window_length, 0, self.maximum_window_length)

        # check that the invert is a boolean
        fail = fail or not self.check_bool(invert)

        if not fail:
            # Define the treatment dictionary
            treatment = {
                "delay": delay,
                "window length": window_length,
                "invert": invert
            }

            # Assign the treatment dictionary to the configuration
            self.configuration["level 2 output treatment"][str(serial)] = treatment
            if verbose:
                print(f'treatment for level 2 output {serial} set')

    def set_output_lemo_assignment(self, serial: int, source: str, source_serial: int, treatment: bool, verbose: bool = True):
        fail = False
        # check that the serial number (output lemo connector number) is a number between 0 and 15
        fail = fail or not self.check_int(serial, 0, 15)

        # check that the source is one of "input", "level 1", "level 2"
        if source not in ["input", "level 1", "level 2"]:
            fail = True
            print(f'invalid source {source}. It must be one of "input", "level 1", "level 2"')

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
                "source": source,
                "source serial": source_serial,
                "treatment": treatment
            }
            # Assign the output to the configuration
            self.configuration["output lemo assignments"][str(serial)] = output
            if verbose:
                print(f'output {serial} assigned to LEMO {output}')

    def set_prescaler(self, serial: int, prescaler: int, verbose: bool = True):
        fail = False
        # check that the serial number is a number between 0 and 2
        fail = fail or not self.check_int(serial, 0, 2)

        # check that the prescaler is a number between 0 and 8
        fail = fail or not self.check_int(prescaler, 0, 8)

        if not fail:
            # Assign the prescaler to the configuration
            self.configuration["prescalers"][str(serial)] = prescaler
            if verbose:
                print(f'prescaler {serial} set to {prescaler}')

    def set_deadtime_veto(self, deadtime, verbose: bool = True):
        fail = False
        # check that the deadtime is a number between 1 and 500 (in us)
        fail = fail or not self.check_int(deadtime, 0, 500)

        if not fail:
            self.configuration["deadtime veto"] = deadtime
            if verbose:
                print(f'deadtime veto set')

    # Define the get configuration method
    def get_configuration(self):
        # Return the configuration
        return self.configuration

    # Define the write configuration method
    def write_configuration(self, filename):
        # Open the file for writing
        with open(filename, "w") as file:
            # Write the configuration to the file
            json.dump(self.configuration, file, indent=4)

    # Define the read configuration method
    def read_configuration(self, filename):
        # Open the file for reading
        with open(filename, "r") as file:
            # Read the configuration from the file
            self.configuration = json.load(file)