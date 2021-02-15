import PySimpleGUI as gui
import os
from datetime import date
#This is a rough draft of the user interface code, I will make some edits later!
#Please give me feed back especially if some of the text could be worded better
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
formats 
supported_langs = ["English"]
layout_dictionary = dict()
window_size = (800, 480)
layout_dictionary["opening"] =  [   [gui.Button("Start")], [gui.Button("Settings")], [gui.Button("Continue")]   ]
layout_dictionary["settings"] = [   [gui.Button("Location"), gui.Button("Scheduling")], [gui.Button("Parameters"), gui.Button("Output")],
                                    [gui.Button("Language"), gui.Button("Network")], [gui.Button("Power"), gui.Button("Back")]  ]
layout_dictionary["location"] = [   [gui.Text("Latitude: from 90°S to 90°N")],
                                    [gui.Slider(key = "Lat", range = (-90,90),  default_value = 42, size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                                    [gui.Text("Longitude: from 180°W to 180°E")],
                                    [gui.Slider(key = "Long", range = (-180, 180), default_value = -88, size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                                    [gui.OK()]  ]
layout_dictionary["parameters"] =[  [gui.Text("Overlap")],
                                    [gui.Slider(key = "Overlap", range(0, 2.9, 0.1), default_value = 1, size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                                    [gui.SPP("Sensitivity")],
                                    [gui.Slider(key = "Sensitivity", range(0.25, 2.0, 0.05), default_value = 1, size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                                    [gui.OK()] ]
layout_dictionary["format"] =   [   [gui.Spin(key="Format", values = ["Raven", "Audacity"])], [gui.OK()]]

def enter_date():
    year_layout = [gui.Text("Year", size = (6,1)), gui.Spin(key = "Year", values = ["2021", "2022", "2023", "2024"])]
    month_layout = [gui.Text("Month", size = (6,1)), gui.Spin(key = "Month", values = months)] 
    layout = [year_layout, month_layout, [gui.OK()]]
    window = gui.Window("Enter the date", layout)
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == "OK":
            break
    window.close()
    return values["Year"], values["Month"]
def enter_lat_long():
    window = gui.Window("Enter the Latitude and Longitude", layout_dictionary["location"])
    while True:
        event, values = window.read()
        print(event, values)
        if event == gui.WIN_CLOSED or event == "OK":
            window.close()
            return values["Lat"], values["Long"]
            #To do: Return to the beginning of this function
def enter_info():
    layout = [[gui.Text("* means that this field is required")], [gui.Text("Input File *", size=(14,1)), gui.Input(key="Infile")], 
              [gui.Text("Output File", size=(14,1)), gui.Input(key="Ouput")], [gui.Text("File Type", size=(14,1)), gui.Input(key="Filetype")], 
              [gui.Text("Output Format", size=(14,1)), gui.Input(key="Outputformat")], 
              [gui.Text("Week", size=(14,1)), gui.Input(key="Week")], [gui.Text("Overlap", size=(14,1)), gui.Input(key="Overlap")], 
              [gui.Text("SPP", size=(14,1)), gui.Input(key="SPP")], [gui.Text("Sensitivity", size=(14,1)), gui.Input(key="Sensitivity")], 
              [gui.OK()]]
    window = gui.Window("Title", layout)
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == "OK":
            break
    window.close()
    if values["Infile"] == None:
        window2 = gui.Window("Error Message", [[gui.Text("You need to specify which file or directory to analyse")]], [[gui.OK()]])
        #To do: Return to the beginning of this function
        #To do: Check if the input file is valid
    #This builds the command line argument piece by piece
    range_error = "{} should be a {} between {} and {}"
    command = "python analyze.py --i {} ".format(values["Infile"])
    if values["Outputformat"]:
        temp1 = values["Outputformat"]
        if temp1 != "audacity" and temp1 != "raven":
            gui.popup("Error", "Output format should be raven or audacity")
            #To do: Return to the beginning of this function or special function to handel error
        else:
            command += "--result {} ".format(temp1)
    if values["Week"]:
        temp2 = int(values["Week"])
        if temp2 < 1 or temp2 > 48:
            window2 =  gui.Window("Error Message", [[gui.Text(range_error.format("Week", "Integer", 1, 48))]], [[gui.OK()]])
            #To do: Return to the beginning of this function or special function to handel error
        else:
            command += "--week {} ".format(temp2)
    if values["Overlap"]:
        temp3 = float(values["Overlap"])
        if temp3 < 0.0 or temp3 > 2.9:
            window2 =  gui.Window("Error Message", [[gui.Text(range_error.format("Overlap", "Decimal", 0.0, 2.9))]], [[gui.OK()]])
            #To do: Return to the beginning of this function or special function to handel error
        else:
            command += "--overlap {} ".format(temp3)
    if values["Sensitivity"]:
        temp4 = float(values["Sensitivity"])
        if temp4 < 0.25 or temp4 > 2.0:
            window2 =  gui.Window("Error Message", [[gui.Text(range_error.format("Sensitivity", "Decimal", 0.25, 2.0))]], [[gui.OK()]])
            #To do: Return to the beginning of this function or special function to handel error
        else:
            command += "--sensitivity {} "
    return command
#print(enter_date())
print(date.today())
print(enter_lat_long())
#command = enter_info()
#print(command)
def start_command(filename):
    cmd = "python analyze.py --i {}".format(filename)
    failure = os.system(cmd)
    if failure:
        window = gui.Window("Error Window", [[gui.Text("There was an error")]], [gui.Button("OK")])
        while True:
            event, values = window.read()
            if event == gui.WIN_CLOSED or event == "OK":
                break
        window.close()
        return -1
    else:
        window = gui.Window("Success Window", [[gui.Text("The analysis was succesful")]], [gui.Button("OK")])
        while True:
            event, values = window.read()
            if event == gui.WIN_CLOSED or event == "OK":
                break
        window.close()
        return 0

