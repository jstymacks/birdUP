import PySimpleGUI as sg
import os
import datetime as dt
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
               [sg.Text("", key = "-PROMPT-")],
               [sg.OK(size = button_size), sg.Button("Back", key = "Exit", size = button_size)] ]
    window = sg.Window("Enter the Latitude", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == "OK":
            if len(lat_string) != 0:
                lat_val = float(lat_string)
                if lat_val > 90:
                    sg.popup("Error!", "The latitude cannot be greater than 90°")
                    lat_string = ""
                else:
                    break
            else:
                window["-PROMPT-"].update("Enter a value between 0 and 90, and the Hemisphere")
                continue
        if event == "Exit":
            window.close()
            return
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
                [sg.OK(size = button_size), sg.Button("Back", key = "Exit", size = button_size)] ]
    window = sg.Window("Enter the Longitude", layout, size = window_size)
    while True:
        event, values = window.read()
        if event == "OK":
            if len(lon_string) != 0:
                lon_val = float(lon_string)
                if lon_val > 180:
                    sg.popup("Error!", "The longitude cannot be greater than 180°")
                    lon_string = ""
                else:
                    break
            else:
                window["-PROMPT-"].update("Enter a value between 0 and 180, and the Hemisphere")
                continue
        if event == "Exit":
            window.close()
            return
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
def scheduling():
    ''' def days_in_month(y, m):
        m -= 1
        day_counts = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (y % 4 == 0) and (y % 100 != 0) or (y % 400 == 0):
            day_counts[1] += 1
        return day_counts[m] '''
    today = dt.date.today()
    #month_list = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    weekday_list = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    layout = [  [sg.Text("Repeats", size = (8, 1)),
                 sg.Radio("Once", "-PERIOD-", enable_events = True, size = (6, 1), default = True, key = "-O-"),
                 sg.Radio("Daily", "-PERIOD-", enable_events = True, size = (6, 1), key = "-D-"),
                 sg.Radio("Weekly", "-PERIOD-", enable_events = True, size = (7, 1), key = "-W-"),
                 sg.Radio("Monthly", "-PERIOD-", enable_events = True, size = (8, 1), key = "-M-"),
                 sg.Radio("Yearly", "-PERIOD-", enable_events = True, size = (7, 1), key = "-Y-")],
                [sg.Text("Minute", size = (8, 1)), sg.Spin(values = [*range(0, 60)], size = (3, 1), key = "-MIN-", initial_value = 0)],
                [sg.Text("Hour", size = (8, 1)), sg.Spin(values = [*range(0, 24)], size = (3, 1), key = "-HOUR-", initial_value = 0)],
                [sg.Text("Day", size = (8, 1)), sg.Spin(values = [*range(1, 32)], size = (3, 1), key = "-DAY-", initial_value = today.day)],
                [sg.Text("Weekday", size = (8, 1)), sg.Spin(values = weekday_list, size = (5, 1), initial_value = weekday_list[today.weekday()], key = "-WEEKDAY-")],
                [sg.Text("Month", size = (8, 1)), sg.Spin(values = [*range(1, 13)], size = (5, 1), key = "-MON-", initial_value = today.month)],
                [sg.Text("Repeat"), sg.Radio("Until", "-ENDDATE-", enable_events = True, size = (6, 1), default = True, key = "-U-"),
                 sg.Radio("Indefinitely", "-ENDDATE-", enable_events = True, size = (10, 1), key = "-I-")],
                [sg.Text("Day", size = (8, 1)), sg.Spin(values = [*range(1, 31)], size = (3, 1), key = "-DAY2-", initial_value = today.day)],
                [sg.Text("Month", size = (8, 1)), sg.Spin(values = [*range(1, 13)], size = (3, 1), key = "-MON2-", initial_value = today.month)],
                [sg.Text("Year", size = (8, 1)), sg.Spin(values = [*range(today.year, 2100)], key = "-YEAR2-", initial_value = today.year)],
                [sg.OK(), sg.Button("Back", key = "-BACK-")] ]
    window = sg.Window("Set recording time", layout, size = window_size)
    ''' def _show_repeat_(window):
        window["-U-"].update(visible = True)
        window["-I-"].update(visible = True)
        window["-DAY2-"].update(visible == True)
        window["-MON2-"].update(visible == True)
        window["-YEAR2-"].update(visible = True)
    def _func1_(window):
        window["-DAY-"].update(visible = True)
        window["-WEEKDAY-"].update(visible = False)
        window["-MON-"].update(visible = True)
        window["-ENDDATE-"].update(visible = False)
        window["-DAY2-"].update(visible == False)
        window["-MON2-"].update(visible == False)
        window["-YEAR2-"].update(visible = False)
    def _func2_(window):
        window["-DAY-"].update(visible = False)
        window["-WEEKDAY-"].update(visible = False)
        window["-MON-"].update(visible = False)
        _show_repeat_(window)
    def _func3_(window):
        window["-DAY-"].update(visible = False)
        window["-WEEKDAY-"].update(visible = True)
        window["-MON-"].update(visible = False)
        _show_repeat_(window)
    def _func4_(window):
        window["-DAY-"].update(visible = True)
        window["-WEEKDAY-"].update(visible = False)
        window["-MON-"].update(visible = False)
        _show_repeat_(window)
    def _func5_(window):
        window["-DAY-"].update(visible = True)
        window["-WEEKDAY-"].update(visible = False)
        window["-MON-"].update(visible = False)
        _show_repeat_(window) 
    action_dict = {
        "-O-" : _func1_,
        "-D-" : _func2_,
        "-W-" : _func3_,
        "-M-" : _func4_,
        "-Y-" : _func5_
    } '''
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "OK":
            window.close()
            break
        print(event)
        if event == "-BACK-":
            window.close()
            return
        #This is ugly and should be restructured
        if event == "-O-":
            window["-DAY-"].update(visible = True)
            window["-WEEKDAY-"].update(visible = False)
            window["-MON-"].update(visible = True)
            window["-U-"].update(visible = False)
            window["-I-"].update(visible = False)
        elif event == "-D-":
            window["-DAY-"].update(visible = False)
            window["-WEEKDAY-"].update(visible = False)
            window["-MON-"].update(visible = False)
            window["-U-"].update(visible = True)
            window["-I-"].update(visible = True)
        elif event == "-W-":
            window["-DAY-"].update(visible = False)
            window["-WEEKDAY-"].update(visible = True)
            window["-MON-"].update(visible = False)
            window["-U-"].update(visible = True)
            window["-I-"].update(visible = True)
        elif event == "-M-":
            window["-DAY-"].update(visible = True)
            window["-WEEKDAY-"].update(visible = False)
            window["-MON-"].update(visible = False)
            window["-U-"].update(visible = True)
            window["-I-"].update(visible = True)
        elif event == "-Y-": 
            window["-DAY-"].update(visible = True)
            window["-WEEKDAY-"].update(visible = False)
            window["-MON-"].update(visible = True)
            window["-U-"].update(visible = True)
            window["-I-"].update(visible = True)
    (m, h, d, mo) = (values["-MIN-"], values["-HOUR-"], values["-DAY-"], values["-MON-"])
    record_time = dt.datetime(today.year, mo, d, hour = h, minute = m)
    print(record_time)
    #This should also be restructured
    if values["-O-"] == True:
        cron_command = "{:02d} {:02d} {:02d} {:02d} * ".format(m, h, d, mo)
    elif values["-D-"] == True:
        if values["-I-"] == True:
            cron_command = "{:02d} {:02d} * * * ".format(m, d)
        else:
            y2 = values["-YEAR2-"]
            if y2 > today.year:
                cron_command = "{:02d} {:02d} * * * ".format(m, d) #Edit later
            elif y2 < today.year:
                sg.popup("Error: Invalid Interval") #goto statement
            else:
                mo2 = values["-MON2-"]
                if mo2 > mo:
                    cron_command = "{:02d} {:02d} * {:02d}-{:02d} * ".format(m, h, mo, mo2) #edit later #split into 2 commands
                elif mo2 < mo:
                    sg.popup("Error: Invalid Interval") #goto statement
                else:
                    d2 = values["-DAY2-"]
                    if d2 > d:
                        cron_command = "{:02d} {:02d} {0:2d}-{0:2d} {0:2d} * ".format(m, h, d, d2, m) #edit later
                    elif d2 < d:
                        sg.popup("Error: Invalid Interval") #goto statement
                    else:
                        cron_command = "{:02d} {:02d} {:02d} {:02d} * ".format(m, h, d, mo)
    elif values["-W-"] == True:
        w = values["-WEEKDAY-"]
        cron_command = "{:02d} {:02d} * * {} ".format(m, d, w) 
    elif values["-M-"] == True:
        cron_command = "{:02d} {:02d} {:02d} * * ".format(m, h, d)
    cron_command += "python record.py"
    print(cron_command)
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
        if event == "Scheduling":
            scheduling()
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
def run_command2(command, success_window_text):
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
        window = sg.Window("Success Window", [[sg.Text(success_window_text)], [sg.Button("OK")]], size = window_size)
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
def run_analysis2():
    filename = None
    while filename == None:
        filename = sg.popup_get_file("Select file")
    command = "python analyze.py --i {} --results raven --lat {} --lon {} --overlap {} --sensitivity {} --min_conf {}".format(filename,
        device_settings.lat, device_settings.long, device_settings.overlap, device_settings.sensitivity, device_settings.min_conf)
    run_command2(command, "The analysis was sucessful")
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
