# Simple user interface to modify trigger configurations and apply them to the VME backplane

# Import the necessary modules
from Configuration import Configuration
import texttable
import os

max_table_width = 120
current_configuration = Configuration("","")

def load():
    print("List of available trigger configurations:")
    #show a list of available configurations in a texttable
    # get a list of .json files in the configurations directory oldest first

    #search_dir = "configurations"
    #files = filter(os.path.isfile, os.listdir(search_dir))
    #files = [os.path.join(search_dir, f) for f in files]  # add path to each file
    #files.sort(key=lambda x: os.path.getmtime(x))

    path = "configurations"
    name_list = os.listdir(path)
    full_list = [os.path.join(path, i) for i in name_list]
    full_list_sorted = sorted(full_list, key=os.path.getmtime)
    json_files = [i for i in full_list_sorted if i.endswith(".json")]
    files = [os.path.basename(i) for i in json_files]

    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m"])
    table.add_row(["index", "filename", "shortname", "description"])
    for i, config_file in enumerate(files):
        config = Configuration("","")
        config.read_configuration(json_files[i])
        short_name = config.configuration["short name"]
        description = config.configuration["description"]
        table.add_row([str(i), config_file, short_name, description])
    print(table.draw())

    #prompt the user to select a configuration
    while True:
        index = input("Select index to load (blank to cancel): ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < len(files):
            i = int(index)
            current_configuration.read_configuration(json_files[i])
            print("Configuration loaded from " + files[i])
            return
        else:
            print("Invalid index")


def inputs():
    print("Available input signals:")
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c", "l"])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m"])
    table.add_row(["Channel", "Short Name", "Delay", "Window", "Invert", "Description"])
    input_signals = current_configuration.configuration["input signals"]
    input_treatments = current_configuration.configuration["input signal treatment"]
    for i in range(96):
        if str(i) in input_signals:
            short_name = input_signals[str(i)]["short name"]
            delay = input_treatments[str(i)]["delay"]
            window = input_treatments[str(i)]["window length"]
            invert = input_treatments[str(i)]["invert"]
            description = input_signals[str(i)]["description"]
            table.add_row([str(i), short_name, delay, window, invert, description])
    print(table.draw())

    #prompt the user to select a channel to modify
    while True:
        index = input("Select channel to modify (blank to cancel): ")
        if index == "":
            return
        if index.isdigit() and index in input_signals:
            i = int(index)
            print('Channel selected:')
            table = texttable.Texttable(max_width=max_table_width)
            table.add_row(["Channel", "Short Name", "Delay", "Window", "Invert", "Description"])
            short_name = input_signals[str(i)]["short name"]
            delay = input_treatments[str(i)]["delay"]
            window = input_treatments[str(i)]["window length"]
            invert = input_treatments[str(i)]["invert"]
            description = input_signals[str(i)]["description"]
            table.add_row([str(i), short_name, delay, window, invert, description])
            table.add_row(["field:", "0", "1", "2", "3", "4"])
            print(table.draw())
            while True:
                command = input("Enter field #, new value (blank to cancel): ")
                if command == "":
                    return
                fields = command.split(',')
                if len(fields) == 2 and fields[0].isdigit() and 0 <= int(fields[0]) <= 4:
                    field = int(fields[0])
                    value = fields[1]
                    if field == 0:
                        short_name = value
                    elif field == 1:
                        delay = int(value)
                    elif field == 2:
                        window = int(value)
                    elif field == 3:
                        invert = bool(value)
                    elif field == 4:
                        description = value
                    if field in [0,4]:
                        current_configuration.set_signal(i, short_name, description, True)
                    else:
                        current_configuration.set_treatment(i, delay, window, invert, True)
                else:
                    print("Invalid input")

def help():
    print("Available commands:")
    print("help: Display this help message")
    print("load: Load a trigger configuration")
    print("inputs: List/modify the available input signals")

def main():

    commands = {
        "help": help,
        "load": load,
        "inputs": inputs,
        "set": set,
        "exit": exit
    }

    while True:
        command = input("Enter command: ")
        if command in commands:
            commands[command]()
        else:
            print("Invalid command. Type 'help' for a list of available commands.")

if __name__ == "__main__":
    main()