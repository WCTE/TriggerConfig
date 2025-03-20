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
    if current_configuration.configuration["short_name"] == "":
        print("")
        print("===================================")
        print("| No trigger configuration loaded |")
        print("===================================")
        print("")
    else:
        print("")
        print("Currently selected trigger configuration:")
        table = texttable.Texttable(max_width=max_table_width)
        table.set_cols_align(["c", "c"])
        table.set_cols_valign(["m", "m"])
        table.add_row(["Short Name", "Description"])
        table.add_row([current_configuration.configuration["short_name"],
                       current_configuration.configuration["description"]])
        print(table.draw())
        print("")

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
    if index == "":
        pass
    elif index.isdigit() and 0 <= int(index) < len(files):
        current_version = Configuration.get_version()
        if current_version != file_versions[int(index)]:
            print("*** Configuration file version mismatch - cannot load")
        else:
            i = int(index)
            save = input(f"Load configuration {short_names[i]} into the trigger module? [no] ")
            if save == "Yes" or save == "yes" or save == "Y" or save == "y" or save == "YES":
                current_configuration.read_configuration(json_files[i])
                print("")
                print("")
                print("Configuration loaded from " + files[i])
                # calculate the register values and store in the update json files:
                current_configuration.update()
                # write the configuration to the trigger module
                os.system("/home/mpmt/write_registers.sh")
                # keep a record of the change
                now = datetime.datetime.now()
                with open("configurations/trigger_configuration.log", "a") as f:
                    f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} {current_configuration.configuration['short_name']}\n")
            else:
                print("")
                print("*** Configuration NOT loaded to trigger module***")
                print("")

    else:
        print("*** Invalid index ***")