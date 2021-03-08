import PySimpleGUI as sg
import os
from datetime import date
#This is a rough draft of the user interface code, I will make some edits later!
#Please give me feed back especially if some of the text could be worded better
#To Do: make buttons bigger, Delete languge, power and network settings, Add loopback, Add Documentation, Why are scdeduling and parameters unde seperate buttons,
#delete output format
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
window_size = (800, 480)
class Settings():
    def __init__(self):
        self.lat = 41.9
        self.long = -87.6
        self.overlap = 1.0
        self.sensitivity = 1.0
        self.min_conf = 0.1
device_settings = Settings()
sg.theme("DarkGreen")
command_base = "python analyze.py --i {} --results raven --lat {} --lon {} --overlap {} --sensitivity {} --min_conf {}"
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
def enter_lat():
    button_size = (10, 3)
    lat_string = ""
    layout = [ [sg.InputText("Latitude: ", font=("Helvetica", 24), key = "Lat")],
               [sg.Button("7", key = "7", size = button_size), sg.Button("8", key = "8", size = button_size), sg.Button("9", key = "9", size = button_size)],
               [sg.Button("4", key = "4", size = button_size), sg.Button("5", key = "5", size = button_size), sg.Button("6", key = "6", size = button_size)],
               [sg.Button("1", key = "1", size = button_size), sg.Button("2", key = "2", size = button_size), sg.Button("3", key = "3", size = button_size)],
               [sg.Button(".", key = ".", size = button_size), sg.Button("0", key = "0", size = button_size), sg.Button("<-", key = "Back", size = button_size)],
               [sg.Radio("North", "HEMISPHERE", size = (10, 1), default = True), sg.Radio("South", "HEMISPHERE", size = (10, 1), default = False, key = "-SOUTH-")],
               [sg.OK()]    ]
    window = sg.Window("Enter the Latitude", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == "OK":
            lat_val = float(lat_string)
            if lat_val > 90:
                sg.popup("Error!", "The latitude cannot be greater than 90°")
                lat_string = ""
            else:
                break
        elif event != "Back":
            lat_string += str(event)
        if event == "Back":
            lat_string = lat_string[:-1]
        window["Lat"].update("Latitude: {}".format(lat_string))
    window.close()
    if values["-SOUTH-"] == True:
        lat_val = lat_val * -1
    device_settings.lat = lat_val
def enter_lon():
    button_size = (10, 3)
    lon_string = ""
    layout = [  [sg.InputText("Longitude: ", font=("Helvetica", 24), key = "Lon")],
                [sg.Button("7", key = "7", size = button_size), sg.Button("8", key = "8", size = button_size), sg.Button("9", key = "9", size = button_size)],
                [sg.Button("4", key = "4", size = button_size), sg.Button("5", key = "5", size = button_size), sg.Button("6", key = "6", size = button_size)],
                [sg.Button("1", key = "1", size = button_size), sg.Button("2", key = "2", size = button_size), sg.Button("3", key = "3", size = button_size)],
                [sg.Button(".", key = ".", size = button_size), sg.Button("0", key = "0", size = button_size), sg.Button("<-", key = "Back", size = button_size)],
                [sg.Radio("East", "HEMISPHERE", size = (10, 1), default = True), sg.Radio("West", "HEMISPHERE", size = (10, 1), default = False, key = "-WEST-")],
                [sg.OK()]    ]
    window = sg.Window("Enter the Longitude", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == "OK":
            lon_val = float(lon_string)
            if lon_val > 180:
                sg.popup("Error!", "The longitude cannot be greater than 180°")
                lon_string = ""
            else:
                break
        elif event != "Back":
            lon_string += str(event)
        if event == "Back":
            lon_string = lat_string[:-1]
        window["Lon"].update("Latitude: {}".format(lon_string))
    window.close()
    #To do implement python version of goto statement for this function 
    if values["-WEST-"] == True:
        lon_val = lon_val * -1
    device_settings.long = lon_val
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
def settings_menu():
    button_size = (12, 1)
    layout = [  [sg.Button("Location", size = button_size)],
                [sg.Button("Scheduling", size = button_size)],
                [sg.Button("Parameters", size = button_size)],
                [sg.Button("Back", size = button_size)]  ]
    window = sg.Window("Settings", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Back":
            break
        if event == "Location":
            enter_lat()
            enter_lon()
        if event == "Parameters":
            enter_parameters()
    window.close()
    return values
def run_command(filename):
    cmd = command_base.format(filename, device_settings.lat, device_settings.long, device_settings.overlap, device_settings.sensitivity, device_settings.min_conf)
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
def run_analysis():
    filename = None
    while filename == None:
        filename = sg.popup_get_file("Select file")
    run_command(filename)
def main():
    layout = [  [sg.Button("Start", size = (12, 1))], [sg.Button("Settings", size = (12, 1))], [sg.Button("Documentation", size = (12, 1))], [sg.Button("Analyze Data", size = (12, 1))]]
    window = sg.Window("Opening Screen", layout, size = window_size)
    #print("mkdir birdup")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Settings":
            settings_menu()
        if event == "Analyze Data":
            run_analysis()
if __name__ == "__main__":
    main()
