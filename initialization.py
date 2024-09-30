# Create a trigger configuration from scratch

# Import the necessary modules
from Configuration import Configuration

# Define the default signal channel assignments
def set_signal_channels(c, verbose = False):

    # Trigger scintillator 0
    c.set_signal("0", "T00", "Upstream trigger scintillator 0 channel 0", verbose)
    c.set_signal("1", "T01", "Upstream trigger scintillator 0 channel 1", verbose)
    c.set_signal("2", "T02", "Upstream trigger scintillator 0 channel 2", verbose)
    c.set_signal("3", "T03", "Upstream trigger scintillator 0 channel 3", verbose)

    c.set_digitizer_board_connection("0","10","input", "0", verbose)
    c.set_digitizer_board_connection("0","11","input", "1", verbose)
    c.set_digitizer_board_connection("0","12","input", "2", verbose)
    c.set_digitizer_board_connection("0","13","input", "3", verbose)

    # Trigger scintillator 1
    c.set_signal("4", "T10", "Downstream trigger scintillator 1 channel 0", verbose)
    c.set_signal("5", "T11", "Downstream trigger scintillator 1 channel 1", verbose)
    c.set_signal("6", "T12", "Downstream trigger scintillator 1 channel 2", verbose)
    c.set_signal("7", "T13", "Downstream trigger scintillator 1 channel 3", verbose)
    c.set_signal("8", "T2", "Small trigger scintillator upstream of magnet", verbose)

    c.set_digitizer_board_connection("0","14","input", "4", verbose)
    c.set_digitizer_board_connection("0","15","input", "5", verbose)
    c.set_digitizer_board_connection("0","16","input", "6", verbose)
    c.set_digitizer_board_connection("0","17","input", "7", verbose)
    c.set_digitizer_board_connection("0","18","input", "8", verbose)

    # Hole counters
    c.set_signal("9", "HC0", "Hole counter 0 upstream of ACT", verbose)
    c.set_signal("10", "HC1", "Hole counter 1 downstream of ACT", verbose)
    c.set_signal("11", "HC2", "Hole counter 2 upstream of magnet", verbose)

    # ACT modules
    c.set_signal("12", "ACT00", "ACT module 0 channel 0", verbose)
    c.set_signal("13", "ACT01", "ACT module 0 channel 1", verbose)
    c.set_signal("14", "ACT10", "ACT module 1 channel 0", verbose)
    c.set_signal("15", "ACT11", "ACT module 1 channel 1", verbose)
    c.set_signal("16", "ACT20", "ACT module 2 channel 0", verbose)
    c.set_signal("17", "ACT21", "ACT module 2 channel 1", verbose)
    c.set_signal("18", "ACT30", "ACT module 3 channel 0", verbose)
    c.set_signal("19", "ACT31", "ACT module 3 channel 1", verbose)
    c.set_signal("20", "ACT40", "ACT module 4 channel 0", verbose)
    c.set_signal("21", "ACT41", "ACT module 4 channel 1", verbose)
    c.set_signal("22", "ACT50", "ACT module 5 channel 0", verbose)
    c.set_signal("23", "ACT51", "ACT module 5 channel 1", verbose)

    c.set_digitizer_board_connection("2", "0", "input", "12", verbose)
    c.set_digitizer_board_connection("2", "1", "input", "13", verbose)
    c.set_digitizer_board_connection("2", "2", "input", "14", verbose)
    c.set_digitizer_board_connection("2", "3", "input", "15", verbose)
    c.set_digitizer_board_connection("2", "4", "input", "16", verbose)
    c.set_digitizer_board_connection("2", "5", "input", "17", verbose)
    c.set_digitizer_board_connection("2", "6", "input", "18", verbose)
    c.set_digitizer_board_connection("2", "7", "input", "19", verbose)
    c.set_digitizer_board_connection("2", "8", "input", "20", verbose)
    c.set_digitizer_board_connection("2", "9", "input", "21", verbose)
    c.set_digitizer_board_connection("2", "10", "input", "22", verbose)
    c.set_digitizer_board_connection("2", "11", "input", "23", verbose)

    # Muon tagger
    c.set_signal("24", "MUT0", "Muon tagger channel 0", verbose)
    c.set_signal("25", "MUT1", "Muon tagger channel 1", verbose)

    c.set_digitizer_board_connection("2", "12", "input", "24", verbose)
    c.set_digitizer_board_connection("2", "13", "input", "25", verbose)

    # spill information
    c.set_signal("26", "BSW", "Beam spill warning", verbose)
    c.set_signal("27", "BSE", "Beam spill end", verbose)
    c.set_spill_channel("26", "27", "False", verbose)
    c.set_output_lemo_assignment("3", "BSWarn", "Beam spill warning", "input", "26", "True", verbose=True)
    c.set_trigger_board_connection("0", "3", "lemo", "3", verbose=True)
    c.set_output_lemo_assignment("4", "BSEnd", "Beam spill end", "input", "27", "True", verbose=True)
    c.set_trigger_board_connection("0", "4", "lemo", "4", verbose=True)

    # other trigger inputs - to activate TDCT0, these would need to be directed to lemo 0 (see laser trigger configuration)
    c.set_signal("28", "LASER", "Laser signal", verbose)
    c.set_output_lemo_assignment("5", "LASER", "Laser signal", "input", "28", "True", verbose=True)
    c.set_trigger_board_connection("0", "5", "lemo", "5", verbose=True)
    c.set_signal("29", "XTRIG", "Other trigger", verbose)
    c.set_output_lemo_assignment("6", "XTRIG", "Other trigger", "input", "29", "True", verbose=True)
    c.set_trigger_board_connection("0", "6", "lemo", "6", verbose=True)

    # 1 TOF channel left over
    c.set_signal("30", "TOF0F", "TOF module 0 channel 15", verbose)
    c.set_signal("31", "TDCT0", "TDC stop signal for TDC0", verbose)

    # Hodoscope modules: 15 channels labelled as hexidecimal
    c.set_signal("32", "HODO0", "Hodoscope channel 0", verbose)
    c.set_signal("33", "HODO1", "Hodoscope channel 1", verbose)
    c.set_signal("34", "HODO2", "Hodoscope channel 2", verbose)
    c.set_signal("35", "HODO3", "Hodoscope channel 3", verbose)
    c.set_signal("36", "HODO4", "Hodoscope channel 4", verbose)
    c.set_signal("37", "HODO5", "Hodoscope channel 5", verbose)
    c.set_signal("38", "HODO6", "Hodoscope channel 6", verbose)
    c.set_signal("39", "HODO7", "Hodoscope channel 7", verbose)
    c.set_signal("40", "HODO8", "Hodoscope channel 8", verbose)
    c.set_signal("41", "HODO9", "Hodoscope channel 9", verbose)
    c.set_signal("42", "HODOA", "Hodoscope channel 10", verbose)
    c.set_signal("43", "HODOB", "Hodoscope channel 11", verbose)
    c.set_signal("44", "HODOC", "Hodoscope channel 12", verbose)
    c.set_signal("45", "HODOD", "Hodoscope channel 13", verbose)
    c.set_signal("46", "HODOE", "Hodoscope channel 14", verbose)
    c.set_signal("47", "TDCT0", "TDC stop signal for TDC1", verbose)

    c.set_digitizer_board_connection("1", "10", "input", "32", verbose)
    c.set_digitizer_board_connection("1", "11", "input", "33", verbose)
    c.set_digitizer_board_connection("1", "12", "input", "34", verbose)
    c.set_digitizer_board_connection("1", "13", "input", "35", verbose)
    c.set_digitizer_board_connection("1", "14", "input", "36", verbose)
    c.set_digitizer_board_connection("1", "15", "input", "37", verbose)
    c.set_digitizer_board_connection("1", "16", "input", "38", verbose)
    c.set_digitizer_board_connection("1", "17", "input", "39", verbose)
    c.set_digitizer_board_connection("1", "18", "input", "40", verbose)
    c.set_digitizer_board_connection("1", "19", "input", "41", verbose)

    c.set_digitizer_board_connection("2", "14", "input", "42", verbose)
    c.set_digitizer_board_connection("2", "15", "input", "43", verbose)
    c.set_digitizer_board_connection("2", "16", "input", "44", verbose)
    c.set_digitizer_board_connection("2", "17", "input", "45", verbose)
    c.set_digitizer_board_connection("2", "18", "input", "46", verbose)

# Channels 49-63 are not used since we have only 5 discriminator modules (80 channels)

    # TOF modules - 16 channels, labelled as hexidecimal
    c.set_signal("64", "TOF00", "TOF module 0 channel 0", verbose)
    c.set_signal("65", "TOF01", "TOF module 0 channel 1", verbose)
    c.set_signal("66", "TOF02", "TOF module 0 channel 2", verbose)
    c.set_signal("67", "TOF03", "TOF module 0 channel 3", verbose)
    c.set_signal("68", "TOF04", "TOF module 0 channel 4", verbose)
    c.set_signal("69", "TOF05", "TOF module 0 channel 5", verbose)
    c.set_signal("70", "TOF06", "TOF module 0 channel 6", verbose)
    c.set_signal("71", "TOF07", "TOF module 0 channel 7", verbose)
    c.set_signal("72", "TOF08", "TOF module 0 channel 8", verbose)
    c.set_signal("73", "TOF09", "TOF module 0 channel 9", verbose)
    c.set_signal("74", "TOF0A", "TOF module 0 channel 10", verbose)
    c.set_signal("75", "TOF0B", "TOF module 0 channel 11", verbose)
    c.set_signal("76", "TOF0C", "TOF module 0 channel 12", verbose)
    c.set_signal("77", "TOF0D", "TOF module 0 channel 13", verbose)
    c.set_signal("78", "TOF0E", "TOF module 0 channel 14", verbose)
    c.set_signal("79", "TOF0F", "TOF module 0 channel 15", verbose)

    c.set_signal("80", "TOF10", "TOF module 1 channel 0", verbose)
    c.set_signal("81", "TOF11", "TOF module 1 channel 1", verbose)
    c.set_signal("82", "TOF12", "TOF module 1 channel 2", verbose)
    c.set_signal("83", "TOF13", "TOF module 1 channel 3", verbose)
    c.set_signal("84", "TOF14", "TOF module 1 channel 4", verbose)
    c.set_signal("85", "TOF15", "TOF module 1 channel 5", verbose)
    c.set_signal("86", "TOF16", "TOF module 1 channel 6", verbose)
    c.set_signal("87", "TOF17", "TOF module 1 channel 7", verbose)
    c.set_signal("88", "TOF18", "TOF module 1 channel 8", verbose)
    c.set_signal("89", "TOF19", "TOF module 1 channel 9", verbose)
    c.set_signal("90", "TOF1A", "TOF module 1 channel 10", verbose)
    c.set_signal("91", "TOF1B", "TOF module 1 channel 11", verbose)
    c.set_signal("92", "TOF1C", "TOF module 1 channel 12", verbose)
    c.set_signal("93", "TOF1D", "TOF module 1 channel 13", verbose)
    c.set_signal("94", "TOF1E", "TOF module 1 channel 14", verbose)
    c.set_signal("95", "TDCT0", "TDC stop signal for TDC2", verbose)

def setup_le_trigger_logic(c: Configuration, verbose = False):

    # level 1 logics
    c.set_level_1_logic("0", "T0 L1", "T0 coincidence", "[0,1,2,3]", "[]", "AND", verbose)
    c.set_level_1_logic("1", "T1 L1", "T1 coincidence", "[4,5,6,7]", "[]", "AND", verbose)
    c.set_level_1_logic("2", "ATCe", "ATC electron", "[12,13]", "[]", "OR", verbose)
    c.set_level_1_logic("3", "ATCeps", "ATC electron prescaled", "[12,13]", "[]", "OR", verbose)
    c.set_level_1_logic("4","HC L1", "Hole counter", "[9,10]", "[]", "OR", verbose)
    c.set_level_1_logic("5","MUON", "Muon tagger", "[24,25]", "[]", "AND", verbose)

    # pre-scale electron veto
    c.set_prescaler("3", "16", "False", verbose)

    # adjust timing for example
    c.set_level_1_treatment("2","3", "7", verbose=verbose)

    # level 2 logics
    c.set_level_2_logic("0", "LE psV", "Low Energy Trigger prescaled eVeto", "[]", "[]", "[0,1]","[3,4]","AND", verbose)
    c.set_level_2_logic("1", "LE nV", "Low Energy Trigger without eVeto", "[]", "[]", "[0,1]","[4]","AND", verbose)
    c.set_level_2_logic("2", "LE e", "Low Energy Trigger with electron", "[]", "[]", "[0,1,2]", "[4]", "AND", verbose)
    c.set_level_2_logic("3", "LE mu", "Low Energy Trigger with muon", "[]", "[]", "[0,1,5]", "[2,4]", "AND", verbose)

# initialize the low energy trigger configuration
def configure_le_trigger(short_name: str, description: str, filename: str, verbose = False):

    # Create a low energy trigger configuration object
    le = Configuration(short_name,description)

    # Set signal inputs (as defined by the inputs to the CFD modules)
    set_signal_channels(le, verbose=verbose)

    # setup the trigger logic
    setup_le_trigger_logic(le, verbose=verbose)

    # this selects the trigger for TDC readout: direct the output of the trigger logic to lemo 0
    le.set_output_lemo_assignment("0", "TDCT0", "Event trigger (TDC_STOP)", "level 2", "0", "True", verbose=True)

    # The TDCT0 signal (lemo 0) will be fanned out to the TDCs, the trigger/digitizer boards, and the patch panel
    le.set_trigger_board_connection("0", "0", "other", "TDCT0", verbose=verbose)
    le.set_trigger_board_connection("1", "0", "other", "TDCT0", verbose=verbose)
    le.set_trigger_board_connection("2", "19", "other", "TDCT0", verbose=verbose)
    le.set_patch_panel_connection("0", "other", "TDCT0", verbose=verbose)

    # custom trigger from control room to input 29
    le.set_patch_panel_connection("1", "other", "XTRIG", verbose=verbose)

    # output electron and muon tags
    le.set_output_lemo_assignment("1", "EL TAG", "Electron tagged", "level 2", "2", "True", verbose=verbose)
    le.set_trigger_board_connection("0", "1", "lemo", "1", verbose=verbose)

    le.set_output_lemo_assignment("2", "MU TAG", "Muon tagged", "level 2", "3", "True", verbose=True)
    le.set_trigger_board_connection("0", "2", "lemo", "2", verbose=True)

    # LE trigger without electron veto patched to control room (for beam tuning)
    le.set_output_lemo_assignment("7", "LE nV", "Low Energy Trigger without eVeto", "level 2", "1", "True", verbose=True)
    le.set_patch_panel_connection("2", "lemo", "7", verbose=True)

    # Reserve 8 patch panel connections connected to LEMO outputs 8-15
    for i in range(8,16):
        le.set_patch_panel_connection(str(i), "lemo", str(i), verbose=True)

    # Set some treatment examples
    le.set_treatment("1","7","3", verbose=verbose)
    le.set_treatment("3","255","3", verbose=verbose)

    # define the deadtime veto: 625 time bins = 5 us
    le.set_deadtime_veto("625", verbose=verbose)

    # Save the low energy trigger configuration and register settings to json files
    le.save(filename)

def setup_tp_trigger_logic(c: Configuration, verbose = False):

    # level 1 logics
    c.set_level_1_logic("0", "T0 L1", "T0 coincidence", "[0,1,2,3]", "[]", "AND", verbose)
    hodoscope_channels = "[32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]"
    c.set_level_1_logic("1","HODO", "Hodoscope signal", hodoscope_channels, "[]", "OR", verbose)

    # level 2 logics
    c.set_level_2_logic("0", "TP", "Tagged Photon Trigger", "[8]", "[12]", "[0,1]","[]","AND", verbose)
    c.set_level_2_logic("1", "TP nH", "Tagged Photon Trigger no HODO requirement", "[8]", "[12]", "[0]","[]","AND", verbose)

# initialize the tagged photon trigger configuration
def configure_tp_trigger(short_name: str, description: str, filename: str, verbose = False):

    # Create a tagged photon trigger configuration object
    tp = Configuration(short_name,description)

    # Set signal inputs (as defined by the inputs to the CFD modules)
    set_signal_channels(tp, verbose = False)

    # setup the trigger logic
    setup_tp_trigger_logic(tp, verbose=verbose)

    # this selects the trigger for TDC readout: direct the output of the trigger logic to lemo 0
    tp.set_output_lemo_assignment("0", "TDCT0", "Event trigger (TDC_STOP)", "level 2", "0", "True", verbose=True)

    # The TDCT0 signal (lemo 0) will be fanned out to the TDCs, the trigger/digitizer boards, and the patch panel
    tp.set_trigger_board_connection("0", "0", "other", "TDCT0", verbose=verbose)
    tp.set_trigger_board_connection("1", "0", "other", "TDCT0", verbose=verbose)
    tp.set_trigger_board_connection("2", "19", "other", "TDCT0", verbose=verbose)
    tp.set_patch_panel_connection("0", "other", "TDCT0", verbose=verbose)

    # custom trigger from control room to input 29
    tp.set_patch_panel_connection("1", "other", "XTRIG", verbose=True)

    # Tagged photon trigger without hodoscope requirement patched to control room (for beam tuning)
    tp.set_output_lemo_assignment("7", "TP nH", "Tagged Photon Trigger no HODO requirement", "level 2", "1", "True", verbose=True)
    tp.set_patch_panel_connection("2", "lemo", "7", verbose=True)

    # Reserve 8 patch panel connections connected to LEMO outputs 8-15
    for i in range(8,16):
        tp.set_patch_panel_connection(str(i), "lemo", str(i), verbose=True)

    # define the deadtime veto: 625 time bins = 5 us
    tp.set_deadtime_veto("625", verbose=verbose)

    # Save the low energy trigger configuration and register settings to json files
    tp.save(filename)

# initialize the laser trigger configuration
def configure_la_trigger(short_name: str, description: str, filename: str, verbose = False):

    # Create a laser trigger configuration object
    la = Configuration(short_name,description)

    la.set_signal("28", "LASER", "Laser signal", verbose=verbose)
    la.set_output_lemo_assignment("5", "LASER", "Laser signal", "input", "28", "True", verbose=verbose)
    la.set_trigger_board_connection("0", "5", "lemo", "5", verbose=verbose)

    # this selects the trigger for TDC readout (to get laser flash time): direct the output of the trigger logic to lemo 0
    la.set_output_lemo_assignment("0", "TDCT0", "Event trigger (TDC_STOP)", "input", "28", "True", verbose=verbose)

    # The TDCT0 signal (lemo 0) will be fanned out to the TDCs, the trigger/digitizer boards, and the patch panel
    la.set_trigger_board_connection("0", "0", "other", "TDCT0", verbose=verbose)
    la.set_trigger_board_connection("1", "0", "other", "TDCT0", verbose=verbose)
    la.set_trigger_board_connection("2", "19", "other", "TDCT0", verbose=verbose)
    la.set_patch_panel_connection("0", "other", "TDCT0", verbose=verbose)

    # define the deadtime veto: 625 time bins = 5 us
    la.set_deadtime_veto("625", verbose=verbose)

    # Save the low energy trigger configuration and register settings to json files
    la.save(filename)


# Select the trigger configuration to setup:

# trigger = "LE"  # one of "LE" (low energy) "TP" (tagged photon) "LA" (laser) or "TS" (test stand)
verbose = False

for trigger in ["LE", "TP", "LA"]:

    if trigger == "LE":
        configure_le_trigger("LE v14","Low Energy Trigger version 1.4", "le_v14", verbose=verbose)

    elif trigger == "TP":
        configure_tp_trigger("TP v14","Tagged Photon Trigger version 1.4", "tp_v14", verbose=verbose)

    elif trigger == "LA":
        configure_la_trigger("LA v14","Laser Trigger version 1.4", "la_v14", verbose=verbose)