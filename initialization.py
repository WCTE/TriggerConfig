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

    # Trigger scintillator 1
    c.set_signal("4", "T10", "Downstream trigger scintillator 1 channel 0", verbose)
    c.set_signal("5", "T11", "Downstream trigger scintillator 1 channel 1", verbose)
    c.set_signal("6", "T12", "Downstream trigger scintillator 1 channel 2", verbose)
    c.set_signal("7", "T13", "Downstream trigger scintillator 1 channel 3", verbose)
    c.set_signal("8", "T2", "Small trigger scintillator upstream of magnet", verbose)

    # Hole counters
    c.set_signal("9", "HC0", "Hole counter 0", verbose)
    c.set_signal("10", "HC1", "Hole counter 1", verbose)
    c.set_signal("11", "HC2", "Hole counter 2", verbose)

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

    # Muon tagger
    c.set_signal("24", "MUT0", "Muon tagger channel 0", verbose)
    c.set_signal("25", "MUT1", "Muon tagger channel 1", verbose)

    # spill information
    c.set_signal("26", "BSW", "Beam spill warning", verbose)
    c.set_signal("27", "BSE", "Beam spill end", verbose)
    c.set_spill_channel("26", "27", verbose)

    # other trigger inputs
    c.set_signal("28", "LASER", "Laser signal", verbose)
    c.set_signal("29", "CUSTOM", "Other trigger", verbose)

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
    c.set_signal("47", "HODOF", "Hodoscope channel 15", verbose)
    c.set_signal("48", "TDCT0", "TDC stop signal for TDC1", verbose)

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

def setup_low_e_trigger_logic(c: Configuration, verbose = False):

    c.set_level_1_logic("0", "T0 L1", "T0 coincidence", "[0,1,2,3]", "[]", "AND", verbose)
    c.set_level_1_logic("1", "T1 L1", "T1 coincidence", "[4,5,6,7]", "[]", "AND", verbose)
    c.set_level_1_logic("2", "ATCe", "ATC electron", "[12,13]", "[]", "OR", verbose)
    c.set_level_1_treatment("2","3", "7", verbose=verbose)

    c.set_level_2_logic("0", "LowE", "Low Energy Trigger with eVeto", "[]", "[]", "[0,1]","[2]","AND", verbose)

    return


# Create a low energy trigger configuration object
low_e = Configuration("Low E v1", "Low Energy Trigger - version 0.6")

# Set signal inputs (as defined by the inputs to the CFD modules)
set_signal_channels(low_e, verbose = True)

# setup the trigger logic
setup_low_e_trigger_logic(low_e, verbose = True)

# direct the output of the trigger logic to lemo 0
low_e.set_output_lemo_assignment("0", "TRIGGER", "Event trigger (TDC_STOP)", "level 2", "0","False", verbose = True)
# direct the short trigger output to lemo 1
low_e.set_output_lemo_assignment("1", "SHORT", "Short signal", "level 2", "2","True", verbose = True)

# Set some treatments
low_e.set_treatment("1","7","3", verbose = True)
low_e.set_treatment("3","255","3", verbose = True)

# define some prescale factors
low_e.set_prescaler("0", "8", verbose = True)
low_e.set_prescaler("1", "16", verbose = True)

# define the deadtime: 625 time bins = 5 us
low_e.set_deadtime_veto("625", verbose = True)

# Save the low energy trigger configuration and register settings to json files
low_e.save("low_e_v06")
