# Simple user interface to select a trigger configuration and load it into the WCTE
# This only works on a machine that is connected to the VME crate

# Import the necessary modules

from Configuration import Configuration
import texttable
import os
import datetime

current_configuration = Configuration("","")
max_table_width = 110

while True:
    # Announce the name of this script
    print("")
    print("")
    print("---------------------------------")
    print("WCTE Trigger Configuration Loader")
    print("---------------------------------")
    print("")

    if current_configuration.configuration["short_name"] == "":
        print("")
        print("===================================")
        print("| No trigger configuration loaded |")
        print("===================================")
        print("")
    else:
        print("")
        print("Currently selected trigger configuration:")
        if current_configuration.configuration["short_name"][0:3] == "LEP":  # this is a configuration with prescaled e veto
            treatments = current_configuration.configuration["input_signal_treatments"]
            if "39" in treatments:
                # show the current ACTEVD width (channel 39)
                current_actevd = treatments["39"]["window_length"]
            else:
                current_actevd = '-'

            table = texttable.Texttable(max_width=max_table_width)
            table.set_cols_align(["c", "c", "c", "c"])
            table.set_cols_valign(["m", "m", "m", "m"])
            table.add_row(["Short Name", "Description", "Deadtime", "ACTEVD"])
            table.add_row([current_configuration.configuration["short_name"],
                           current_configuration.configuration["description"],
                           current_configuration.configuration["deadtime"],
                           current_actevd])
        else:
            table = texttable.Texttable(max_width=max_table_width)
            table.set_cols_align(["c", "c", "c"])
            table.set_cols_valign(["m", "m", "m"])
            table.add_row(["Short Name", "Description", "Deadtime"])
            table.add_row([current_configuration.configuration["short_name"],
                           current_configuration.configuration["description"],
                           current_configuration.configuration["deadtime"]])
        print(table.draw())
        print("")
        print("")

    print("List of available trigger configurations (sorted by modification time)")
    # show a list of available configurations in a texttable
    # get a list of .json files in the configurations directory, oldest first

    path = "configurations"
    name_list = os.listdir(path)
    full_list = [os.path.join(path, i) for i in name_list]
    full_list_sorted = sorted(full_list, key=os.path.getmtime)
    json_files = [i for i in full_list_sorted if i.endswith(".json") and
                  os.path.basename(i) not in ["current_config.json","written_config.json"]]
    files = [os.path.basename(i) for i in json_files]
    file_versions = []

    table = texttable.Texttable(max_width=max_table_width)
    table.set_cols_align(["c", "c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m", "m"])
    table.add_row(["Index", "Filename", "TC Version", "Short Name", "Description"])
    short_names = []
    for i, config_file in enumerate(files):
        config = Configuration("","")
        config.read_configuration(json_files[i])
        short_name = config.configuration["short_name"]
        short_names.append(short_name)
        description = config.configuration["description"]
        configuration_version = config.configuration["config_version"]
        file_versions.append(configuration_version)
        table.add_row([str(i), config_file, configuration_version, short_name, description])
    print(table.draw())

    #prompt the user to select a configuration

    index = input("Select index of file to load: [cancel] ")
    if index !="" and index.isdigit() and 0 <= int(index) < len(files):
        current_version = Configuration.get_version()
        if current_version != file_versions[int(index)]:
            print("")
            print("*** Configuration file version mismatch - cannot load")
            print("")
            dummy = input("Press enter to continue")
        else:
            i = int(index)
            temp_configuration = Configuration("", "")
            temp_configuration.read_configuration(json_files[i])
            temp_short_name = temp_configuration.configuration["short_name"]
            temp_description = temp_configuration.configuration["description"]
            print("")
            print("Configuration selected:")
            table = texttable.Texttable(max_width=max_table_width)
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.add_row(["Short Name", "Description"])
            table.add_row([temp_short_name, temp_description])
            print(table.draw())
            print("")

    #show the current deadtime
            print("Current deadtime value:")
            temp_configuration = Configuration("", "")
            temp_configuration.read_configuration(json_files[i])
            deadtime = temp_configuration.configuration["deadtime"]
            if deadtime is None:
                deadtime = "None"

            table = texttable.Texttable(max_width=max_table_width)
            table.set_cols_align(["c"])
            table.set_cols_valign(["m"])
            table.add_row(["Deadtime"])
            table.add_row([deadtime])
            print(table.draw())

            # prompt the user to modify the deadtime value
            while True:
                command = input(f"Enter deadtime: [{deadtime}] ")
                if command == "":
                    break
                if command.isdigit():
                    deadtime_value = command
                    if int(deadtime_value) < 1:
                        print("*** Invalid deadtime value: must be greater than 0")
                    else:
                        deadtime = deadtime_value
                        break
                else:
                    print("*** Invalid input")

            actevd_changed = False
            if temp_short_name[0:3] == "LEP":   # this is a configuration with prescaled e veto
                temp_treatments = temp_configuration.configuration["input_signal_treatments"]
                if "39" in temp_treatments:
                    # show the current ACTEVD width (channel 39)
                    print("Current ACTEVD width:")
                    actevd = temp_treatments["39"]["window_length"]
                    if actevd is None:
                        actevd = "None"

                    table = texttable.Texttable(max_width=max_table_width)
                    table.set_cols_align(["c"])
                    table.set_cols_valign(["m"])
                    table.add_row(["ACTEVD width"])
                    table.add_row([actevd])
                    print(table.draw())

                    # prompt the user to modify the actevd value
                    while True:
                        command = input(f"Enter ACTEVD width: [{actevd}] ")
                        if command == "":
                            break
                        if command.isdigit():
                            actevd_value = command
                            if int(actevd_value) < 1:
                                print("*** Invalid ACTEVD value: must be greater than 0")
                            else:
                                actevd = actevd_value
                                actevd_changed = True
                                break
                        else:
                            print("*** Invalid input")

            if temp_short_name[0:3] == "LEP":
                save = input(
                    f"Load configuration {short_names[i]} with deadtime {deadtime} and ACTEVD {actevd} into the trigger module? [no] ")
            else:
                save = input(f"Load configuration {short_names[i]} with deadtime {deadtime} into the trigger module? [no] ")
            if save == "Yes" or save == "yes" or save == "Y" or save == "y" or save == "YES":
                current_configuration.read_configuration(json_files[i])
                print("")
                print("")
                print("Configuration loaded from " + files[i])
                # set the deadtime
                current_configuration.set_deadtime_veto(deadtime, True)
                # calculate the register values and store in the update json files:
                if actevd_changed:
                    delay = temp_treatments["39"]["delay"]
                    current_configuration.set_treatment("39", delay, actevd, True)
                # update the configuration
                current_configuration.update()
                # write the configuration to the trigger module
                os.system("/home/mpmt/write_registers.sh")
                # keep a record of the change
                now = datetime.datetime.now()
                with open("configurations/trigger_configuration.log", "a") as f:
                    f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} {current_configuration.configuration['short_name']}\n")
                # write the current short name to a file that will be used for saving in the database
                with open("configurations/trigger_configuration_current.txt", "w") as f:
                    if temp_short_name[0:3] == "LEP":
                        f.write(f'{short_names[i]} deadtime={deadtime} ACTEVD={actevd}')
                    else:
                        f.write(f'{short_names[i]} deadtime={deadtime}')
                print("")
                dummy = input("Press enter to continue")
            else:
                print("")
                print("*** Configuration NOT loaded to trigger module***")
                print("")
                dummy = input("Press enter to continue")

    else:
        print("")
        print("*** Invalid index ***")
        print("")
        dummy = input("Press enter to continue")