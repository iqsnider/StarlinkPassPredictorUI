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
import csv

from starlinkPassPredictor import *
from locations import *
from writeAcpPlan import *
from printPlan import *

from skyfield import api
from skyfield import almanac
 
from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

from datetime import datetime



# Start of GUI block
print("Starting GUI")

def openFile():
    filePath = filedialog.askopenfilename(initialdir="StarlinkPassPredictorUI-main", title="Select a file")
    
    # open file
    os.system('"%s"' % filePath)

# create root window
root = Tk()


# root window title and dimensions
root.title("Starlink Pass Predictor")

root.geometry('400x200')

# adding menu bar in root window
# new item in menu bar labeled as 'New'
# adding more items in menu bar
# menu = Menu(root)
# item = Menu(menu)
# item.add_command(label = 'New')
# menu.add_cascade(label = 'File', menu = item)
# root.config(menu = menu)


#end of style GUI Block


###########################

#Open observation plan files
file_button = Button(root, text="Open Plan File", fg = "purple",command=openFile)
file_button.pack()

#PassPredictor plan GUI output 

# #plan header
# planX = Label(root, text = "Name                     ID       Rise Time             Rise Azimuth   Peak Time             Peak Alt   Peak Azimuth   Set Time              Set Azimuth   Duration")
# planX.place(x=5,y=65)

# #textbox output for copy/pasting
# planBox = ScrolledText(root, width=120, font=("lucida", 13))
# planBox.place(x=5,y=85)


##############################

# adding a label to the root window
locLbl = Label(root, text = "Location (Latitude, Longitude, Elevation)")
locLbl.pack()


# adding Entry field

#Latitude
latEntry = Entry(root, width=15)
latEntry.pack()

#Logitude
lonEntry = Entry(root, width=15)
lonEntry.pack()

#Elevation
elevationEntry = Entry(root, width=15)
elevationEntry.pack()

###############################

# run printPlan button
btn = Button(root, text = "Calculate Plan", fg = "purple", command=calculatePlan(latEntry, lonEntry, elevationEntry))
btn.pack()

calcLbl = Label(root, text = "*Takes 1-2 mins*")
calcLbl.pack()

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




