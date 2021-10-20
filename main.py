# main.py
# 
# This script utilizes the functions in the other files to calculate
# ephemerides for Starlink, determine which are visible, and create
# an ACP observing plan for the Pomenis telescope
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# Copyright May 2020
#
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

#plan header
planX = Label(root, text = "STARLINK-2192            47769C   2021-10-20 00:23:57   313.709        2021-10-20 00:30:01   27.9096    26.4055        2021-10-20 00:36:04   99.0810       0:12:07")
planX.place(x=5,y=65)

#textbox output for copy/pasting
planBox = ScrolledText(root, width=120, font=("lucida", 13))
planBox.place(x=5,y=85)


#end of style GUI Block


##########################
#  Parameters
##########################

exposureTime = 3
exposureRepeat = 1
filterLetter = "v"
binning = 1

offset = 9 #offset the requested time to allow for slewing etc. 6 sec for starting at center of FOV. increase to trigger sooner
timePer = dt.timedelta(seconds=90) #minimum number of sec to wait before next target

minAlt = 20
sunUp = False
moonUp = None #any
eclipsed = False

params = [sunUp, moonUp, eclipsed, minAlt]

start = dt.datetime.utcnow().replace(hour=0, minute=00, second=00)
stop = dt.datetime.utcnow().replace(hour=4, minute=00, second=00)

#start = dt.datetime(2020,5,28,0,00,00)
#stop = dt.datetime(2020,5,28,5,00,00)

loc = locations["TSU farm"]

#imagePath = "F:\\++__2020.5__++\\Sats\\%s_Starlink" % (start.strftime('%Y-%m-%d'))
imagePath = "%s_Starlink" % (start.strftime('%Y-%m-%d'))

#staticPath = "C:\\Users\\Pomenis\\Documents\\ACP Astronomy\\Plans"
staticPath = imagePath

###########################


#Make a new directory for todays data
#path = start.strftime('%Y-%m-%d')
path = imagePath

if os.path.isdir(path):
	print("%s already exists, opening it..." % path)
else:
	try:
	    os.mkdir(path)
	except OSError:
	    print ("Creation of the directory %s failed" % path)
	else:
	    print ("Successfully created the directory %s " % path)


###########################


ts = api.load.timescale()
e = api.load('de421.bsp')


### Evening ###
print("\n\n ### EVENING ### \n\n")


#Determine when is sunset and twilight
t, y = almanac.find_discrete(ts.utc(start.replace(tzinfo=api.utc)), ts.utc(stop.replace(tzinfo=api.utc)), almanac.dark_twilight_day(e, loc))

for ti, yi in zip(t,y):
	if yi == 3:
		sunset = ti
	if yi == 1:
		twilight = ti

twilight = twilight.utc_datetime()

print("Astronomical Twilght is " + twilight.strftime('%Y-%m-%d %H:%M:%S') )


###########################


#Find all passes
passes = starlinkPassPredictor(twilight, stop, loc, params, path, "allPassesEvening_" + start.strftime('%Y-%m-%d'))


#Select some to observe
passes = selectStarlinkPasses(passes, timePer, path, "selectedPassesEvening_" + start.strftime('%Y-%m-%d'))

#Make an ACP plan
filename = "starlinkPlanEvening.txt"
print("Writing ACP Plan as " + filename)

#Reorganize for ACP plan
obs = []
for p in passes:
	obs.append([p["name"],p["maxTime"],offset,p["maxRA"],p["maxDec"],p["maxAlt"],p["maxAz"]])

#Write ACP plan for Pomenis
writeAcpPlan(obs, exposureTime, exposureRepeat, filterLetter, binning, imagePath, os.path.join(path, filename), False)
writeAcpPlan(obs, exposureTime, exposureRepeat, filterLetter, binning, imagePath, os.path.join(staticPath, filename), False)

##########################


#PassPredictor plan GUI output 

# adding a label to the root window
lbl = Label(root, text = "Location (e.g. \"TSU farm\")")
lbl.place(x=5,y=0)


# adding Entry field
txt = Entry(root, width=10)
txt.place(x=175,y=0)


#function to display user text when button is clicked
def clicked():
    
    res = "Location (e.g. \"TSU farm\")"
    lbl.configure(text = res)
    
    
# Plan button widget
btn = Button(root, text = "Plan", fg = "purple", command  = clicked)
btn.place(x=280,y=0)

#Find .txt file for GUI
#yyyy-mm-dd
thisDay = datetime.utcnow().strftime("%Y-%m-%d")

#find file
searchFile = thisDay + "_Starlink" + "/" + filename

f = open(searchFile, "r")

#configure GUI plan text

# def displayPlan():
#     n = len(passes)
#     elem = ''
#     for i in range(n):
#         return passes[i]

satLabel = Label(root, text=f.readline())
satLabel.place(x=1005,y=0)


###########################


#Execute tkinter
root.mainloop()

###########################

print("Done!")




