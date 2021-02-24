import PySimpleGUI as sg
import os
from datetime import date
#This is a rough draft of the user interface code, I will make some edits later!
#Please give me feed back especially if some of the text could be worded better
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
supported_langs = ["English"]
window_size = (800, 480)
class Settings():
    def __init__(self):
        self.lat = 41.9
        self.long = -87.6
        self.language = "English"
        self.result_format = "raven"
        self.overlap = 1.0
        self.sensitivity = 1.0
        self.min_conf = 0.1
device_settings = Settings()
sg.theme("DarkGreen")
command_base = "python analyze.py --i {} --results {} --lat {} --lon {} --overlap {} --sensitivity {} --min_conf {}"
def enter_date():
    year_layout = [sg.Text("Year", size = (6,1)), sg.Spin(key = "Year", values = ["2021", "2022", "2023", "2024"])]
    month_layout = [sg.Text("Month", size = (6,1)), sg.Spin(key = "Month", values = months)] 
    layout = [year_layout, month_layout, [sg.OK()]]
    window = sg.Window("Enter the date", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            break
    window.close()
    return values["Year"], values["Month"]
def enter_lat_long():
    layout = [  [sg.Text("Latitude: from 90°S to 90°N")],
                [sg.Slider(key = "Lat", range = (-90,90, 0.1),  default_value = device_settings.lat, size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                [sg.Text("Longitude: from 180°W to 180°E")],
                [sg.Slider(key = "Long", range = (-180, 180, 0.1), default_value = device_settings.long, size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                [sg.OK()]  ]
    window = sg.Window("Enter the Latitude and Longitude", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            window.close()
            break
    if values != None:
        device_settings.lat = values["Lat"]
        device_settings.long = values["Long"]
        return None
def enter_parameters():
    layout = [  [sg.Text("Overlap")],
                [sg.Slider(key = "Overlap", range = (0, 29), default_value = (device_settings.overlap * 10), size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                [sg.Text("Sensitivity")],
                [sg.Slider(key = "Sensitivity", range = (25, 200, 5), default_value = (device_settings.sensitivity * 100), size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                [sg.Text("Minumum Confidence")],
                [sg.Slider(key = "Min_Conf", range = (1, 99), default_value = (device_settings.min_conf * 100), size=(20,15), orientation='horizontal', font=("Helvetica", 12))],
                [sg.OK()] ]
    window = sg.Window("Parameters", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            window.close()
            break
    if values != None:
        device_settings.overlap = values["Overlap"]/10
        device_settings.sensitivity = values["Sensitivity"]/100
        device_settings.min_conf = values["Min_Conf"]/100
def output_format():
    layout = [   [sg.Spin(key="Format", values = ["raven", "audacity"])], [sg.OK()]]
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            window.close()
            break
    device_settings.result_format = values["Format"]
def settings_menu():
    button_size = (12, 1)
    layout = [  [sg.Button("Location", size = button_size), sg.Button("Scheduling", size = button_size)], [sg.Button("Parameters", size = button_size), sg.Button("Output", size = button_size)],
                [sg.Button("Language", size = button_size), sg.Button("Network", size = button_size)], [sg.Button("Power", size = button_size), sg.Button("Back", size = button_size)]  ]
    window = sg.Window("Settings", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Back":
            break
        if event == "Location":
            enter_lat_long()
        if event == "Parameters":
            enter_parameters()
        if event == "Output":
            output_format()
    window.close()
    return values
layout_dictionary["location"] = enter_lat_long
layout_dictionary["parameters"] = enter_parameters
def enter_info():
    layout = [[sg.Text("* means that this field is required")], [sg.Text("Input File *", size=(14,1)), sg.Input(key="Infile")], 
              [sg.Text("Output File", size=(14,1)), sg.Input(key="Ouput")], [sg.Text("File Type", size=(14,1)), sg.Input(key="Filetype")], 
              [sg.Text("Output Format", size=(14,1)), sg.Input(key="Outputformat")], 
              [sg.Text("Week", size=(14,1)), sg.Input(key="Week")],
              [sg.Text("SPP", size=(14,1)), sg.Input(key="SPP")],  
              [sg.OK()]]
    window = sg.Window("Title", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            break
    window.close()
    if values["Infile"] == None:
        window2 = sg.Window("Error Message", [[sg.Text("You need to specify which file or directory to analyse")]], [[sg.OK()]])
        #To do: Return to the beginning of this function
        #To do: Check if the input file is valid
    #This builds the command line argument piece by piece
    range_error = "{} should be a {} between {} and {}"
    command = "python analyze.py --i {} ".format(values["Infile"])
    if values["Week"]:
        temp2 = int(values["Week"])
        if temp2 < 1 or temp2 > 48:
            window2 =  sg.Window("Error Message", [[sg.Text(range_error.format("Week", "Integer", 1, 48))]], [[sg.OK()]])
            #To do: Return to the beginning of this function or special function to handel error
        else:
            command += "--week {} ".format(temp2)
    return command
#print(enter_date())
#print(date.today())
#enter_lat_long()
#layout_dictionary["location"]()
#enter_parameters()
def run_command(filename):
    cmd = command_base.format(filename, device_settings.result_format, device_settings.lat, device_settings.long, device_settings.overlap, device_settings.sensitivity, device_settings.min_conf)
    print(cmd)
    failure = os.system(cmd)
    if failure:
        window = sg.Window("Error Window", [[sg.Text("There was an error")], [sg.Button("OK")]], size = window_size)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "OK":
                break
        window.close()
        return -1
    else:
        window = sg.Window("Success Window", [[sg.Text("The analysis was succesful")], [sg.Button("OK")]], size = window_size)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "OK":
                break
        window.close()
        return 0
def main():
    layout = [  [sg.Button("Start", size = (12, 1))], [sg.Button("Settings", size = (12, 1))], [sg.Button("Documentation", size = (12, 1))]]
    window = sg.Window("Opening Screen", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Settings":
            settings_menu()
        if event == "Start":
            break
    filename = input("Enter the Filename")    
    run_command(filename)
if __name__ == "__main__":
    main()

