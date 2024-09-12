# Simple user interface to modify trigger configurations and apply them to the VME backplane

# Import the necessary modules
from Configuration import Configuration
import texttable
import os

max_table_width = 120
current_configuration = Configuration("","")

def load():
    print("List of available trigger configurations: sorted by modification time")
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
    table.add_row(["Index", "Filename", "Short Name", "Description"])
    for i, config_file in enumerate(files):
        config = Configuration("","")
        config.read_configuration(json_files[i])
        short_name = config.configuration["short_name"]
        description = config.configuration["description"]
        table.add_row([str(i), config_file, short_name, description])
    print(table.draw())

    #prompt the user to select a configuration
    while True:
        index = input("Select index of file to load: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < len(files):
            i = int(index)
            current_configuration.read_configuration(json_files[i])
            print("Configuration loaded from " + files[i])
            return
        else:
            print("Invalid index")

def channels():
    print("Current input signals:")
    input_signals = current_configuration.configuration["input_signals"]
    indices = []
    for i in range(96):
        if str(i) in input_signals:
            indices.append(i)
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", "c", ])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", "m", ])
    table.add_row(["#", "Name", "#", "Name", "#", "Name", "#", "Name",
                   "#", "Name", "#", "Name", "#", "Name", "#", "Name"])
    # show 8 channels per row
    for i in range(0, len(indices), 8):
        row = []
        for j in range(8):
            if i+j < len(indices):
                row.append(str(indices[i+j]))
                row.append(input_signals[str(indices[i+j])]["short_name"])
            else:
                row.append("")
                row.append("")
        table.add_row(row)
    print(table.draw())

def input_table(indices, signals, treatments):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "l"])
    table.set_cols_valign(["m", "m", "m", "m", "m"])
    table.add_row(["Channel", "Short Name", "Delay", "Gate", "Description"])
    for i in indices:
        short_name = signals[str(i)]["short_name"]
        delay = treatments[str(i)]["delay"]
        window_length = treatments[str(i)]["window_length"]
        description = signals[str(i)]["description"]
        table.add_row([str(i), short_name, delay, window_length, description])
    return table

def inputs(prompt: bool = True):
    print("Current input signals:")
    input_signals = current_configuration.configuration["input_signals"]
    input_treatments = current_configuration.configuration["input_signal_treatments"]
    indices = []
    for i in range(96):
        if str(i) in input_signals:
            indices.append(i)
    table = input_table(indices, input_signals, input_treatments)
    print(table.draw())

    #prompt the user to select a channel to modify
    while prompt:
        index = input("Enter input channel number to add/modify: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < 96:
            i = int(index)
            indices = [i]
            if index in input_signals:
                print('Channel selected:')
                table = input_table(indices, input_signals, input_treatments)
                table.add_row(["field:", "0", "1", "2", "3"])
                print(table.draw())
            else:
                # add the new channel
                current_configuration.set_signal(index, "SHORT", "Description", True)
                continue
            while True:
                command = input("Enter field # = new value: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split('=')]
                if len(fields) == 2 and fields[0].isdigit() and 0 <= int(fields[0]) <= 3:
                    short_name = input_signals[index]["short_name"]
                    delay = input_treatments[index]["delay"]
                    window_length = input_treatments[index]["window_length"]
                    description = input_signals[index]["description"]

                    field = int(fields[0])
                    value = fields[1]
                    if field == 0:
                        short_name = value
                    elif field == 1:
                        delay = value
                    elif field == 2:
                        window_length = value
                    elif field == 3:
                        description = value
                    if field in [0,3]:
                        current_configuration.set_signal(index, short_name, description, True)
                    else:
                        current_configuration.set_treatment(index, delay, window_length, True)
                else:
                    print("Invalid input")
        else:
            print("Invalid channel number")

def level_1_table(indices, logics, treatments):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c", "c", "c", "l"])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m", "m", "m"])
    table.add_row(["Index", "Short Name", "Inputs", "Invert Inputs", "Logic", "Delay", "Gate", "Description"])
    for i in indices:
        short_name = logics[str(i)]["short_name"]
        inputs = logics[str(i)]["inputs"]
        invert_inputs = logics[str(i)]["invert_inputs"]
        logic_type = logics[str(i)]["logic_type"]
        delay = treatments[str(i)]["delay"]
        window_length = treatments[str(i)]["window_length"]
        description = logics[str(i)]["description"]
        table.add_row([str(i), short_name, inputs, invert_inputs, logic_type, delay, window_length, description])
    return table

def level_1(prompt: bool = True):
    print("Current level 1 logic:")
    level_1_logics = current_configuration.configuration["level_1_logics"]
    level_1_treatments = current_configuration.configuration["level_1_output_treatments"]
    indices = []
    for i in range(10):
        if str(i) in level_1_logics:
            indices.append(i)
    table = level_1_table(indices, level_1_logics, level_1_treatments)
    print(table.draw())

    #prompt the user to select an index to modify
    while prompt:
        index = input("Enter level 1 logic index to add/modify: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < 10:
            i = int(index)
            indices = [i]
            if index in level_1_logics:
                print('Level 1 logic selected:')
                table = level_1_table(indices, level_1_logics, level_1_treatments)
                table.add_row(["field:", "0", "1", "2", "3", "4", "5", "6"])
                print(table.draw())
            else:
                # add the new level 1 logic
                current_configuration.set_level_1_logic(index, "SHORT", "Description", "[0,1,2,3]", "[]","AND", True)
                continue
            while True:
                command = input("Enter field # = new value: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split('=')]
                if len(fields) == 2 and fields[0].isdigit() and 0 <= int(fields[0]) <= 6:
                    short_name = level_1_logics[str(i)]["short_name"]
                    inputs = level_1_logics[str(i)]["inputs"]
                    invert_inputs = level_1_logics[str(i)]["invert_inputs"]
                    logic_type = level_1_logics[str(i)]["logic_type"]
                    delay = level_1_treatments[str(i)]["delay"]
                    window_length = level_1_treatments[str(i)]["window_length"]
                    description = level_1_logics[str(i)]["description"]

                    field = int(fields[0])
                    value = fields[1]
                    if field == 0:
                        short_name = value
                    elif field == 1:
                        inputs = value
                    elif field == 2:
                        invert_inputs = value
                    elif field == 3:
                        logic_type = value
                    elif field == 4:
                        delay = value
                    elif field == 5:
                        window_length = value
                    elif field == 6:
                        description = value

                    if field in [0,1,2,3,6]:
                        current_configuration.set_level_1_logic(index, short_name, description, inputs, invert_inputs, logic_type, True)
                    else:
                        current_configuration.set_level_1_treatment(index, delay, window_length, True)
                else:
                    print("Invalid input")
        else:
            print("Invalid index number")


def level_2_table(indices, logics):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c", "c", "c", "l"])
    table.set_cols_valign(["m", "m",  "m", "m", "m", "m", "m", "m"])
    table.add_row(["Index", "Short Name", "Inputs", "Invert Inputs", "L1 inputs", "Invert L1 inputs", "Logic", "Description"])
    for i in indices:
        short_name = logics[str(i)]["short_name"]
        inputs = logics[str(i)]["inputs"]
        invert_inputs = logics[str(i)]["invert_inputs"]
        level_1_inputs = logics[str(i)]["level_1_inputs"]
        invert_level_1_inputs = logics[str(i)]["invert_level_1_inputs"]
        logic_type = logics[str(i)]["logic_type"]
        description = logics[str(i)]["description"]
        table.add_row([str(i), short_name, inputs, invert_inputs, level_1_inputs, invert_level_1_inputs, logic_type, description])
    return table


def level_2(prompt: bool = True):
    print("Current level 2 logic:")
    level_2_logics = current_configuration.configuration["level_2_logics"]
    indices = []
    for i in range(4):
        if str(i) in level_2_logics:
            indices.append(i)
    table = level_2_table(indices, level_2_logics)
    print(table.draw())

    # prompt the user to select an index to modify
    while prompt:
        index = input("Enter level 2 logic index to add/modify: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < 4:
            i = int(index)
            indices = [i]
            if index in level_2_logics:
                print('Level 2 logic selected:')
                table = level_2_table(indices, level_2_logics)
                table.add_row(["field:", "0", "1", "2", "3", "4", "5", "6"])
                print(table.draw())
            else:
                # add the new level 2 logic
                current_configuration.set_level_2_logic(index, "SHORT", "Description", "[0,1,2,3]", "[]", "[0]", "[]", "AND", True)
                continue
            while True:
                command = input("Enter field # = new value: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split('=')]
                if len(fields) == 2 and fields[0].isdigit() and 0 <= int(fields[0]) <= 6:
                    short_name = level_2_logics[str(i)]["short_name"]
                    inputs = level_2_logics[str(i)]["inputs"]
                    invert_inputs = level_2_logics[str(i)]["invert_inputs"]
                    level_1_inputs = level_2_logics[str(i)]["level_1_inputs"]
                    invert_level_1_inputs = level_2_logics[str(i)]["level_1_inputs"]
                    logic_type = level_2_logics[str(i)]["logic_type"]
                    description = level_2_logics[str(i)]["description"]

                    field = int(fields[0])
                    value = fields[1]
                    if field == 0:
                        short_name = value
                    elif field == 1:
                        inputs = value
                    elif field == 2:
                        invert_inputs = value
                    elif field == 3:
                        level_1_inputs = value
                    elif field == 4:
                        invert_level_1_inputs = value
                    elif field == 5:
                        logic_type = value
                    elif field == 6:
                        description = value

                    current_configuration.set_level_2_logic(index, short_name, description, inputs, invert_inputs, level_1_inputs, invert_level_1_inputs, logic_type, True)

                else:
                    print("Invalid input")
        else:
            print("Invalid index number")

def output_table(indices, olas):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c", "l"])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m"])
    table.add_row(["Index", "Short Name", "Source", "Source Serial", "Treatment", "Description"])
    for i in indices:
        short_name = olas[str(i)]["short_name"]
        source = olas[str(i)]["source"]
        source_serial = olas[str(i)]["source_serial"]
        treatment = olas[str(i)]["treatment"]
        description = olas[str(i)]["description"]
        table.add_row([str(i), short_name, source, source_serial, treatment, description])
    return table

def outputs(prompt: bool = True):
    print("Current output lemo assignments:")
    output_lemo_assignments = current_configuration.configuration["output_lemo_assignments"]
    indices = []
    for i in range(8): # CURRENTLY 8 -> will go to 16
        if str(i) in output_lemo_assignments:
            indices.append(i)
    table = output_table(indices, output_lemo_assignments)
    print(table.draw())

    # prompt the user to select an index to modify
    while prompt:
        index = input("Enter output lemo assignment index to add/modify: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < 8:
            i = int(index)
            indices = [i]
            if index in output_lemo_assignments:
                print('Output lemo assignment:')
                table = output_table(indices, output_lemo_assignments)
                table.add_row(["field:", "0", "1", "2", "3", "4"])
                print(table.draw())
            else:
                # add the new lemo assignment
                current_configuration.set_output_lemo_assignment(index, "SHORT", "Description", "input", "0", "False", True)
                continue
            while True:
                command = input("Enter field # = new value: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split('=')]
                if len(fields) == 2 and fields[0].isdigit() and 0 <= int(fields[0]) <= 4:
                    short_name = output_lemo_assignments[str(i)]["short_name"]
                    source = output_lemo_assignments[str(i)]["source"]
                    source_serial = output_lemo_assignments[str(i)]["source_serial"]
                    treatment = output_lemo_assignments[str(i)]["treatment"]
                    description = output_lemo_assignments[str(i)]["description"]

                    field = int(fields[0])
                    value = fields[1]
                    if field == 0:
                        short_name = value
                    elif field == 1:
                        source = value
                    elif field == 2:
                        source_serial = value
                    elif field == 3:
                        treatment = value
                    elif field == 4:
                        description = value

                    current_configuration.set_output_lemo_assignment(index, short_name, description, source, source_serial, treatment, True)

                else:
                    print("Invalid input")
        else:
            print("Invalid index number")

def prescalers_table(indices, prescalers):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c"])
    table.set_cols_valign(["m", "m"])
    table.add_row(["Index", "Prescale"])
    for i in indices:
        value = prescalers[str(i)]
        table.add_row([str(i), value])
    return table

def prescalers(prompt: bool = True):
    print("Current prescaler values:")
    prescalers = current_configuration.configuration["prescalers"]
    indices = []
    for i in range(8):
        if str(i) in prescalers:
            indices.append(i)
    table = prescalers_table(indices, prescalers)
    print(table.draw())

    # prompt the user to select an index to modify
    while prompt:
        index = input("Enter prescaler index to add/modify: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < 10:
            i = int(index)
            indices = [i]
            if index in prescalers:
                print('Prescaler selected:')
                table = prescalers_table(indices, prescalers)
                print(table.draw())
            else:
                # add the new prescaler
                current_configuration.set_prescaler(index, "1", True)
                continue
            while True:
                command = input("Enter new prescale: [cancel] ")
                if command == "":
                    break
                if command.isdigit():
                    current_configuration.set_prescaler(index, command, True)

                else:
                    print("Invalid input")
        else:
            print("Invalid index number")

def spills_table(spills):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c"])
    table.set_cols_valign(["m", "m"])
    table.add_row(["Pre-spill channel", "End-spill channel"])
    pre_spill = spills.get("pre_spill", "None")
    end_spill = spills.get("end_spill", "None")
    table.add_row([pre_spill, end_spill])
    return table

def spills(prompt: bool = True):
    print("Current spill signal assignments:")
    spills = current_configuration.configuration["spill_channels"]
    table = spills_table(spills)
    print(table.draw())

    # prompt the user to modify the spill signals
    while prompt:
        command = input("Enter pre-spill, end-spill: [cancel] ")
        if command == "":
            return
        fields = [c.strip() for c in command.split(',')]
        if len(fields) == 2 and fields[0].isdigit() and fields[1].isdigit():
            pre_spill = fields[0]
            end_spill = fields[1]
            if 0 <= int(pre_spill) < 96 and 0 <= int(end_spill) < 96:
                current_configuration.set_spill_channel(pre_spill, end_spill, True)
            else:
                print("Invalid spill channel")

        else:
            print("Invalid input")

def deadtime_table(deadtime):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c"])
    table.set_cols_valign(["m"])
    table.add_row(["Deadtime"])
    table.add_row([deadtime])
    return table

def deadtime(prompt: bool = True):
    print("Current deadtime value:")
    deadtime = current_configuration.configuration["deadtime"]
    if deadtime is None:
        deadtime = "None"
    table = deadtime_table(deadtime)
    print(table.draw())

    # prompt the user to modify the deadtime value
    while prompt:
        command = input("Enter deadtime: [cancel] ")
        if command == "":
            return
        if command.isdigit():
            deadtime_value = command
            current_configuration.set_deadtime_veto(deadtime_value, True)
        else:
            print("Invalid input")

def show_all():
    inputs(False)
    print()
    channels()
    print()
    level_1(False)
    print()
    level_2(False)
    print()
    outputs(False)
    print()
    prescalers(False)
    print()
    spills(False)
    print()
    deadtime(False)

def save():
    while True:
        command = input("Enter new short name (10 characters max): [cancel] ")
        if command == "":
            return
        if len(command) <= 10:
            current_configuration.configuration["short_name"] = command
            break
        else:
            print("Short name too long")
    while True:
        command = input("Enter new description (60 characters max): [cancel] ")
        if command == "":
            return
        if len(command) <= 60:
            current_configuration.configuration["description"] = command
            break
        else:
            print("Description too long")
    while True:
        command = input("Enter filename prefix (do not include _config.json): [cancel] ")
        if command == "":
            return
        current_configuration.save(command)
        return

def update():
    current_configuration.update()

def help():
    print("Available commands:")
    print("help: Display this help message")
    print("load: Load a trigger configuration")
    print("channels: Show the input signal channels in compact form")
    print("inputs: Show/modify the input signal properties")
    print("level1: Show/modify the level 1 logic properties")
    print("level2: Show/modify the level 2 logic properties")
    print("outputs: Show/modify the output lemo assignments")
    print("prescalers: Show/modify the prescaler properties")
    print("spills: Show/modify the spill signal assignments")
    print("deadtime: Show/modify the deadtime properties")
    print("show: Show all elements of the current configuration")
    print("save: Save the current configuration (config and register settings)")
    print("update: Write the current register settings to current_registers.json")
    print("exit: Exit the program")

def main():

    commands = {
        "help": help,
        "load": load,
        "channels": channels,
        "inputs": inputs,
        "level1": level_1,
        "level2": level_2,
        "outputs": outputs,
        "prescalers": prescalers,
        "spills": spills,
        "deadtime": deadtime,
        "show": show_all,
        "save": save,
        "update": update,
        "exit": exit
    }

    while True:
        command = input("Enter command: [help] ")
        if command == "":
            command = "help"
        if command in commands:
            commands[command]()
        else:
            print("Invalid command. Type 'help' for a list of available commands.")

if __name__ == "__main__":
    main()