import PySimpleGUI as gui
import os
#This is a rough draft of the user interface code, I will make some edits later!
#Please give me feed back especially if some of the text could be worded better
def enter_date():
    layout = [[gui.Text("Enter the date")], [gui.Input(key="Input")], [gui.OK()]]
    window = gui.Window("Title", layout)
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == "OK":
            break
    window.close()
    return values["Input"]
def enter_info():
    layout = [[gui.Text("* means that this field is required")], [gui.Text("Input File *"), gui.Input(key="Infile")], [gui.Text("Output File"), gui.Input(key="Ouput")],
              [gui.Text("File Type"), gui.Input(key="Filetype")], [gui.Text("Output Format"), gui.Input(key="Outputformat")], 
              [gui.Text("Latitude"), gui.Input(key="Lat")], [gui.Text("Longitude"), gui.Input(key="Long")], [gui.Text("Week"), gui.Input(key="Week")],
              [gui.Text("Overlap"), gui.Input(key="Overlap")], [gui.Text("SPP"), gui.Input(key="SPP")], [gui.Text("Sensitivity"), gui.Input(key="Sensitivity")], 
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
    if values["Lat"]:
        lat = float(values["Lat"])
        if lat < -90.0 or lat > 90.0:
            gui.popup("Error", range_error.format("Latitude", "decimal", -90.0, 90.0))
            #To do: Return to the beginning of this function or special function to handel error
        else:
            command += "--lat {} ".format(lat)
    if values["Long"]:
        lon = float(values["Long"])
        if lon < -180.0 or lon > 180.0:
            gui.popup("Error", range_error.format("Longitude", "decimal", -180.0, 180.0))
            #To do: Return to the beginning of this function or special function to handel error
        else:
            command += "--lon {} ".format(lon)
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
command = enter_info()
print(command)
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

