# main.py

# This script utilizes the functions in the other files to calculate
# ephemerides for Starlink, determine which are visible, and create
# an ACP observing plan for the Pomenis telescope
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# Copyright May 2020
#
# This original script has been modified for developing a user-friendly
# interface for planning Starlink satellite observations.
# This is intended for students and amateur astronomers.

# @author modifications: Ian Snider
# Truman State University

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime as dt
import os
import pandas as pd

from starlinkPassPredictor import *
from locations import *
from writeAcpPlan import *
from printPlan import *

from skyfield import api
from skyfield import almanac
 
from tkinter import *
from tkinter import filedialog, messagebox, ttk

from datetime import datetime



# csv file display functions

def openFile():
    filePath = filedialog.askopenfilename(initialdir="/StarlinkPassPredictorUI-main", title="Select a file", filetypes=(("csv files", "*.csv"),("all files","*.*")))
    
    # open file
    os.system('"%s"' % filePath)


# Start of GUI block
print("Starting GUI")


# create root window
root = Tk()


# root window title and dimensions
root.title("Starlink Pass Predictor")

root.geometry('500x700')

# adding menu bar in root window
# new item in menu bar labeled as 'New'
# adding more items in menu bar
# menu = Menu(root)
# item = Menu(menu)
# item.add_command(label = 'New')
# menu.add_cascade(label = 'File', menu = item)
# root.config(menu = menu)

# frame for treeview
display_frame = LabelFrame(root, text="CSV Data")
display_frame.place(height=250,width=500)

#frame for file dialog
file_frame = LabelFrame(root, text="Open File")
file_frame.place(height=100, width=400, rely=0.4, relx=0)

#fram for plan calculation
calc_frame = LabelFrame(root, text="Calculate Observation Plan")
calc_frame.place(height=175, width=500, rely=0.6, relx=0)


#end of style GUI Block


##############################

#Browse observation plan files
selectFileBtn = Button(file_frame, text="Select File", fg = "purple",command=openFile) #TODO fix command
selectFileBtn.place(rely=0.65, relx=0.5)

#Load observation plan files
loadFileBtn = Button(file_frame, text="Load File", fg = "purple") #TODO command
loadFileBtn.place(rely=0.65, relx=0.25)

# label file
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)


##############################

#PassPredictor plan GUI output 

# #plan header
# planX = Label(root, text = "Name                     ID       Rise Time             Rise Azimuth   Peak Time             Peak Alt   Peak Azimuth   Set Time              Set Azimuth   Duration")
# planX.place(x=5,y=65)

# #textbox output for copy/pasting
# planBox = ScrolledText(root, width=120, font=("lucida", 13))
# planBox.place(x=5,y=85)


##############################

# treeview widget
tv1 = ttk.Treeview(display_frame)
tv1.place(relheight=1, relwidth=1)

treescrolly = Scrollbar(display_frame, orient="vertical", command=tv1.yview)
treescrollx = Scrollbar(display_frame, orient="horizontal", command=tv1.xview)

tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")


##############################

# adding a label to the root window
locLbl = Label(calc_frame, text = "Input location (Latitude, Longitude, Elevation)")
locLbl.place(rely=0.05, relx=0.05)


# adding Entry field

#Latitude
latEntry = Entry(calc_frame, width=15)
latEntry.place(rely=0.25, relx=0.05)

#Logitude
lonEntry = Entry(calc_frame, width=15)
lonEntry.place(rely=0.25, relx=0.35)

#Elevation
elevationEntry = Entry(calc_frame, width=15)
elevationEntry.place(rely=0.25, relx=0.65)

###############################

# run printPlan button
btn = Button(calc_frame, text = "Calculate Plan", fg = "purple", command=calculatePlan(latEntry, lonEntry, elevationEntry))
btn.place(rely=0.5, relx=0.05)

calcLbl = Label(calc_frame, text = "*Takes 1-2 mins*")
calcLbl.place(rely=0.7, relx=0.05)

###############################

# #Find .txt file for GUI
# #yyyy-mm-dd
# thisDay = datetime.utcnow().strftime("%Y-%m-%d")

# #find file
# searchFile = thisDay + "_Starlink" + "/" + filename

# f = open(searchFile, "r")

# #configure GUI plan details text

# satLabel = Label(root, text=f.readline())
# satLabel.place(x=1005,y=0)

###########################


#Execute tkinter
root.mainloop()

###########################

print("Done!")




