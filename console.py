# Simple user interface to modify trigger configurations and apply them to the VME backplane

# Import the necessary modules
from Configuration import Configuration
import texttable
import os

max_table_width = 120
current_configuration = Configuration("","")
configuration_changed = False

def load():
    global current_configuration, configuration_changed
    print("List of available trigger configurations: sorted by modification time")
    # show a list of available configurations in a texttable
    # get a list of .json files in the configurations directory, oldest first

    path = "configurations"
    name_list = os.listdir(path)
    full_list = [os.path.join(path, i) for i in name_list]
    full_list_sorted = sorted(full_list, key=os.path.getmtime)
    json_files = [i for i in full_list_sorted if i.endswith(".json")]
    files = [os.path.basename(i) for i in json_files]
    file_versions = []

    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m", "m"])
    table.add_row(["Index", "Filename", "TC Version", "Short Name", "Description"])
    for i, config_file in enumerate(files):
        config = Configuration("","")
        config.read_configuration(json_files[i])
        short_name = config.configuration["short_name"]
        description = config.configuration["description"]
        configuration_version = config.configuration["config_version"]
        file_versions.append(configuration_version)
        table.add_row([str(i), config_file, configuration_version, short_name, description])
    print(table.draw())

    #prompt the user to select a configuration
    while True:
        index = input("Select index of file to load: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < len(files):
            current_version = Configuration.get_version()
            if current_version != file_versions[int(index)]:
                print("*** Configuration file version mismatch - cannot load")
                continue
            if configuration_changed:
                command = input("Current configuration has been modified. Save those changes now? [y] ")
                if command.strip() not in ["n", "N", "no", "No"]:
                    save()
                    return
            i = int(index)
            current_configuration.read_configuration(json_files[i])
            print("Configuration loaded from " + files[i])
            configuration_changed = False
            return
        else:
            print("*** Invalid index")

def channels():
    global current_configuration
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

def input_table(indices, signals, cfd_settings, treatments):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c", "c", "l"])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m", "m"])
    table.add_row(["Channel", "Short Name", "Enabled", "Threshold", "Delay", "Gate", "Description"])
    for i in indices:
        short_name = signals[str(i)]["short_name"]
        enabled = cfd_settings[str(i)]["enabled"]
        threshold = cfd_settings[str(i)]["threshold"]
        delay = treatments[str(i)]["delay"]
        window_length = treatments[str(i)]["window_length"]
        description = signals[str(i)]["description"]
        table.add_row([str(i), short_name, enabled, threshold, delay, window_length, description])
    return table

def inputs(prompt: bool = True):
    global current_configuration, configuration_changed
    print("Current input signals:")
    input_signals = current_configuration.configuration["input_signals"]
    input_cfd_settings = current_configuration.configuration["input_cfd_settings"]
    input_treatments = current_configuration.configuration["input_signal_treatments"]
    indices = []
    for i in range(96):
        if str(i) in input_signals:
            indices.append(i)
    table = input_table(indices, input_signals, input_cfd_settings, input_treatments)
    print(table.draw())

    #prompt the user to select a channel to modify
    while prompt:
        index = input("Enter input channel number to add/modify: [cancel] ")
        if index == "":
            return
        if index[0] != "c" and index.isdigit() and 0 <= int(index) < 96:
            i = int(index)
            indices = [i]
            if index in input_signals:
                print('Channel selected:')
                table = input_table(indices, input_signals, input_cfd_settings, input_treatments)
                table.add_row(["field:", "0", "1", "2", "3", "4", "5"])
                print(table.draw())
            else:
                # add the new channel
                current_configuration.set_signal(index, "SHORT", "Description", True)
                configuration_changed = True
                continue
            while True:
                command = input("Enter field # = new value: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split('=')]
                if len(fields) == 2 and fields[0].isdigit() and 0 <= int(fields[0]) <= 5:
                    short_name = input_signals[index]["short_name"]
                    enabled = input_cfd_settings[index]["enabled"]
                    threshold = input_cfd_settings[index]["threshold"]
                    delay = input_treatments[index]["delay"]
                    window_length = input_treatments[index]["window_length"]
                    description = input_signals[index]["description"]

                    field = int(fields[0])
                    value = fields[1]
                    if field == 0:
                        short_name = value
                    elif field == 1:
                        enabled = value
                    elif field == 2:
                        threshold = value
                    elif field == 3:
                        delay = value
                    elif field == 4:
                        window_length = value
                    elif field == 5:
                        description = value
                    if field in [0,5]:
                        current_configuration.set_signal(index, short_name, description, True)
                        configuration_changed = True
                    elif field in [1,2]:
                        current_configuration.set_cfd_setting(index, enabled, threshold, True)
                        configuration_changed = True
                    else:
                        current_configuration.set_treatment(index, delay, window_length, True)
                        configuration_changed = True
                else:
                    print("*** Invalid input")
        elif index[0] == "c":    # allows copying a channel to a range of channels
            if index[1:].isdigit() and index[1:] in input_signals:
                reference = index[1:]
                command = input("Copy index "+index[1:]+" to i-j: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split('-')]
                if len(fields) == 2 and fields[0].isdigit() and fields[1].isdigit():
                    first = int(fields[0])
                    last = int(fields[1])
                    short_name = input_signals[reference]["short_name"]
                    enabled = input_cfd_settings[reference]["enabled"]
                    threshold = input_cfd_settings[reference]["threshold"]
                    delay = input_treatments[reference]["delay"]
                    window_length = input_treatments[reference]["window_length"]
                    description = input_signals[reference]["description"]
                    for i in range(first, last+1):
                        dest = str(i)
                        current_configuration.set_signal(dest, short_name, description, False)
                        current_configuration.set_cfd_setting(dest, enabled, threshold, False)
                        current_configuration.set_treatment(dest, delay, window_length, False)

                    configuration_changed = True
        else:
            print("*** Invalid channel number")

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
    global current_configuration, configuration_changed
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
                configuration_changed = True
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
                        configuration_changed = True
                    else:
                        current_configuration.set_level_1_treatment(index, delay, window_length, True)
                        configuration_changed = True
                else:
                    print("*** Invalid input")
        else:
            print("*** Invalid index number")


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
    global current_configuration, configuration_changed
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
                configuration_changed = True
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
                    invert_level_1_inputs = level_2_logics[str(i)]["invert_level_1_inputs"]
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
                    configuration_changed = True
                else:
                    print("*** Invalid input")
        else:
            print("*** Invalid index number")

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
    global current_configuration, configuration_changed
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
                configuration_changed = True
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
                    configuration_changed = True
                else:
                    print("*** Invalid input")
        else:
            print("*** Invalid index number")

def prescalers_table(indices, prescalers):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c"])
    table.set_cols_valign(["m", "m", "m"])
    table.add_row(["Index", "Prescale", "Select"])
    for i in indices:
        value = prescalers[str(i)]
        select = prescalers[str(i)+"_select"]
        table.add_row([str(i), value, select])
    return table

def prescalers(prompt: bool = True):
    global current_configuration, configuration_changed
    print("Current prescaler values:")
    prescalers = current_configuration.configuration["prescalers"]
    indices = []
    for i in range(10):
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
                current_configuration.set_prescaler(index, "1", "True",True)
                configuration_changed = True
                continue
            while True:
                command = input("Enter new prescale, select: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split(',')]
                if len(fields) == 2 and fields[0].isdigit() and fields[1] in ["True", "False"]:
                    prescale = fields[0]
                    select = fields[1]
                    current_configuration.set_prescaler(index, prescale, select,True)
                    configuration_changed = True
                else:
                    print("*** Invalid input (enter for example: 10, True)")
        else:
            print("*** Invalid index number")

def spills_table(spills):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c"])
    table.set_cols_valign(["m", "m", "m"])
    table.add_row(["Pre-spill channel", "End-spill channel", "Enabled"])
    pre_spill = spills.get("pre_spill", "None")
    end_spill = spills.get("end_spill", "None")
    enabled = spills.get("enabled", "False")
    table.add_row([pre_spill, end_spill, enabled])
    return table

def spills(prompt: bool = True):
    global current_configuration, configuration_changed
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
            if 0 <= int(pre_spill) < 64 and 0 <= int(end_spill) < 64:
                command = input("Enter enabled: [True] ")
                if command == "":
                    enabled = "True"
                elif command == "True" or command == "False":
                    enabled = command
                else:
                    print("*** Invalid input")
                    continue

                current_configuration.set_spill_channel(pre_spill, end_spill, enabled, True)
                configuration_changed = True
            else:
                print("*** Invalid spill channel")

        else:
            print("*** Invalid input")

def deadtime_table(deadtime):
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c"])
    table.set_cols_valign(["m"])
    table.add_row(["Deadtime"])
    table.add_row([deadtime])
    return table

def deadtime(prompt: bool = True):
    global current_configuration, configuration_changed
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
            if int(deadtime_value) < 1:
                print("*** Invalid deadtime value: must be greater than 0")
            else:
                current_configuration.set_deadtime_veto(deadtime_value, True)
                configuration_changed = True
        else:
            print("*** Invalid input")

def connection_table(indices, tdbc):
    global current_configuration
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m", "m", "m"])
    table.add_row(["Index", "Board", "Channel", "Source", "Source Serial", "Source Short Name"])
    for i in indices:
        board = tdbc[str(i)]["board"]
        channel = tdbc[str(i)]["channel"]
        source = tdbc[str(i)]["source"]
        source_serial = tdbc[str(i)]["source_serial"]
        source_short_name = "-"
        # check that gate widths are 1 for digital inputs to the trigger board
        digital_input = i in [0,1,2,3,4,5,6,7,8,9,20,21,22,23,24,25,26,27,28,29,59]
        if source == "input" and source_serial in current_configuration.configuration["input_signals"]:
            source_short_name = current_configuration.configuration["input_signals"][source_serial]["short_name"]
            if digital_input:
                # "input" in this context means the analog split for the corresponding input to the CFD
                # so this should not be connected to a digital input
                source_short_name += " *** digital !! ***"
        elif source == "lemo" and source_serial in current_configuration.configuration["output_lemo_assignments"]:
            source_short_name = current_configuration.configuration["output_lemo_assignments"][source_serial]["short_name"]
            source_source = current_configuration.configuration["output_lemo_assignments"][source_serial]["source"]
            if digital_input and source_source in ["level 1","level 2","input"]:
                treatment = current_configuration.configuration["output_lemo_assignments"][source_serial]["treatment"]
                window_length = "1"
                if source_source == "input":
                    source_source_serial = current_configuration.configuration["output_lemo_assignments"][source_serial]["source_serial"]
                    window_length = current_configuration.configuration["input_signal_treatments"][source_source_serial]["window_length"]
                elif source_source == "level 1":
                    source_source_serial = current_configuration.configuration["output_lemo_assignments"][source_serial]["source_serial"]
                    window_length = current_configuration.configuration["level_1_output_treatments"][source_source_serial]["window_length"]
                if treatment == "False" or window_length != "1":
                    source_short_name += " *** GATE WIDTH != 1 ***"

        table.add_row([str(i), board, channel, source, source_serial, source_short_name])
    return table

def connections(prompt: bool = True):
    global current_configuration, configuration_changed
    print("Current trigger/digitizer board connections:")
    board_connections = current_configuration.configuration["trigger_digitizer_board_connections"]
    indices = []
    for i in range(60): # CURRENTLY 8 -> will go to 16
        if str(i) in board_connections:
            indices.append(i)
    table = connection_table(indices, board_connections)
    print(table.draw())

    # prompt the user to select an index to modify
    while prompt:
        index = input("Enter board connection index to add/modify: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < 60:
            i = int(index)
            board = str(i // 20)
            channel = str(i % 20)
            indices = [i]
            if index in board_connections:
                print('Trigger/digitizer board connection:')
                table = connection_table(indices, board_connections)
                print(table.draw())
            else:
                # add the new board connection
                if i in [0,1,2,3,4,5,6,7,8,9,20,21,22,23,24,25,26,27,28,29,59]:
                    current_configuration.set_trigger_board_connection(board, channel,"other", "0", True)
                    configuration_changed = True
                else:
                    current_configuration.set_digitizer_board_connection(board, channel, "other", "0", True)
                    configuration_changed = True
                continue

            while True:
                command = input("Enter source, source_serial: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split(',')]
                if len(fields) == 2:
                    source = fields[0]
                    source_serial = fields[1]

                    if i in [0,1,2,3,4,5,6,7,8,9,20,21,22,23,24,25,26,27,28,29,59]:
                        current_configuration.set_trigger_board_connection(board, channel, source, source_serial, True)
                        configuration_changed = True
                    else:
                        current_configuration.set_digitizer_board_connection(board, channel, source, source_serial, True)
                        configuration_changed = True

                else:
                    print("*** Invalid input")
        else:
            print("*** Invalid index number")

def patch_table(indices, tdbc):
    global current_configuration
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m"])
    table.add_row(["Index", "Source", "Source Serial", "Source Short Name"])
    for i in indices:
        source = tdbc[str(i)]["source"]
        source_serial = tdbc[str(i)]["source_serial"]
        source_short_name = "-"
        if source == "lemo" and source_serial in current_configuration.configuration["output_lemo_assignments"]:
            source_short_name = current_configuration.configuration["output_lemo_assignments"][source_serial]["short_name"]
        table.add_row([str(i), source, source_serial, source_short_name])
    return table

def patch_panel(prompt: bool = True):
    global current_configuration, configuration_changed
    print("Current patch panel connections:")
    panel_connections = current_configuration.configuration["patch_panel_connections"]
    indices = []
    for i in range(60): # CURRENTLY 8 -> will go to 16
        if str(i) in panel_connections:
            indices.append(i)
    table = patch_table(indices, panel_connections)
    print(table.draw())

    # prompt the user to select an index to modify
    while prompt:
        index = input("Enter patch panel connection index to add/modify: [cancel] ")
        if index == "":
            return
        if index.isdigit() and 0 <= int(index) < 16:
            i = int(index)
            indices = [i]
            if index in panel_connections:
                print('Patch panel connection:')
                table = patch_table(indices, panel_connections)
                print(table.draw())
            else:
                # add the new patch panel connection
                current_configuration.set_patch_panel_connection(index,"other", "0", True)
                configuration_changed = True

            while True:
                command = input("Enter source, source_serial: [cancel] ")
                if command == "":
                    break
                fields = [c.strip() for c in command.split(',')]
                if len(fields) == 2:
                    source = fields[0]
                    source_serial = fields[1]

                    current_configuration.set_patch_panel_connection(index, source, source_serial, True)
                    configuration_changed = True

                else:
                    print("*** Invalid input")
        else:
            print("*** Invalid index number")


def show_all():
    global current_configuration
    print("")
    print("Current configuration:", current_configuration.configuration["short_name"], "("+current_configuration.configuration["description"]+")")
    print("")
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
    print()
    connections(False)
    print()
    patch_panel(False)

def save():
    global current_configuration, configuration_changed
    while True:
        command = input("Enter new short name (10 characters max): [cancel] ")
        if command == "":
            return
        if len(command) <= 10:
            current_configuration.configuration["short_name"] = command
            break
        else:
            print("*** Short name too long")
    while True:
        command = input("Enter new description (60 characters max): [cancel] ")
        if command == "":
            return
        if len(command) <= 60:
            current_configuration.configuration["description"] = command
            break
        else:
            print("*** Description too long")
    while True:
        command = input("Enter filename prefix (do not include _config.json): [cancel] ")
        if command == "":
            return
        success = current_configuration.save(command)
        if success:
            configuration_changed = False
        return

def update():
    global current_configuration
    current_configuration.update()

def exit_check():
    if configuration_changed:
        command = input("Current configuration has been modified. Save those changes now? [y] ")
        if command.strip() not in ["n", "N", "no", "No"]:
            save()
            return
    exit()

def help():
    print("Available commands:")
    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["l", "l"])
    table.set_cols_valign(["m", "m"])
    table.add_row(["Command", "Action"])

    table.add_row(["help", "Display this help message"])
    table.add_row(["load", "Load a trigger configuration"])
    table.add_row(["channels", "Show the input signal channels in compact form"])
    table.add_row(["inputs", "Show/modify the input signal properties"])
    table.add_row(["level1", "Show/modify the level 1 logic properties"])
    table.add_row(["level2", "Show/modify the level 2 logic properties"])
    table.add_row(["outputs", "Show/modify the output lemo assignments"])
    table.add_row(["prescalers", "Show/modify the prescaler properties"])
    table.add_row(["spills", "Show/modify the spill signal assignments"])
    table.add_row(["deadtime", "Show/modify the deadtime properties"])
    table.add_row(["connections", "Show/modify the connections to the trigger/digitizer boards"])
    table.add_row(["patches", "Show/modify the connections to the patch panel"])
    table.add_row(["show", "Show all elements of the current configuration"])
    table.add_row(["save", "Save the current configuration (config and register settings)"])
    table.add_row(["update", "Write the current register settings to current_registers.json"])
    table.add_row(["exit", "Exit the program"])
    print(table.draw())

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
        "connections": connections,
        "patches": patch_panel,
        "show": show_all,
        "save": save,
        "update": update,
        "exit": exit_check
    }

    print()
    print("Welcome to the WCTE trigger configuration console. Version", Configuration.get_version())
    print("The default action is shown in square brackets. Press enter to execute the default action.")
    print()
    while True:
        command = input("Enter command: [help] ")
        if command == "":
            command = "help"
        if command in commands:
            commands[command]()
        else:
            print("*** Invalid command. Type 'help' for a list of available commands.")

if __name__ == "__main__":
    main()