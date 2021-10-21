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

from starlinkPassPredictor import *
from locations import locations
from writeAcpPlan import *

from skyfield import api
from skyfield import almanac
 
from tkinter import *
from printPlan import *
from tkinter.scrolledtext import ScrolledText
from datetime import datetime



# Start of GUI block
print("Starting GUI")

# create root window
root = Tk()


# root window title and dimensions
root.title("Starlink Pass Predictor")
root.geometry('1450x500')

# adding menu bar in root window
# new item in menu bar labeled as 'New'
# adding more items in menu bar
menu = Menu(root)
item = Menu(menu)
item.add_command(label = 'New')
menu.add_cascade(label = 'File', menu = item)
root.config(menu = menu)


#end of style GUI Block


###########################


#PassPredictor plan GUI output 

#plan header
planX = Label(root, text = "Name                     ID       Rise Time             Rise Azimuth   Peak Time             Peak Alt   Peak Azimuth   Set Time              Set Azimuth   Duration")
planX.place(x=5,y=65)

#textbox output for copy/pasting
planBox = ScrolledText(root, width=120, font=("lucida", 13))
planBox.place(x=5,y=85)


# adding a label to the root window
lbl = Label(root, text = "Location (e.g. \"TSU farm\")")
lbl.place(x=5,y=0)


# adding Entry field
txt = Entry(root, width=10)
txt.place(x=175,y=0)


btn = Button(root, text = "Plan", fg = "purple", command=displayPlan(planBox))
btn.place(x=280,y=0)

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




