# printPlan.py

# Created on Thu Oct 21 13:15:39 2021

# @author: iqsnider


import datetime as dt
import os

from starlinkPassPredictor import *
from locations import *
from writeAcpPlan import *

from skyfield import api
from skyfield import almanac
 
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from datetime import datetime



#functions to display user text when button is clicked

def calculatePlan(x, y, z):
    return lambda : callback(x, y, z)

#callback function for printing to text box
def callback(x, y, z):
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
    
    #set location
    # loc = locations["TSU farm"]
    
    # input location
    loc = inputLocation(x, y, z)
    
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
    
    print("Astronomical Twilght is " + twilight.strftime('%Y-%m-%d %H:%M:%S'))
    
    
    ###########################
    
    # TODO function that accepts custom start time
    #               will then go here | *maybe* not for certain if this will work (but shall try lol)
    #                                 V
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

    ###########################
    ### Morning ###

    print("\n\n ### MORNING ### \n\n")
    
    start = dt.datetime.utcnow().replace(hour=9, minute=00, second=00)
    stop = dt.datetime.utcnow().replace(hour=15, minute=00, second=00)
    
    #start = dt.datetime(2020,5,28,9,00,00)
    #stop = dt.datetime(2020,5,28,15,00,00)
    
    
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
    passes = starlinkPassPredictor(start, twilight, loc, params, path, "allPassesMorning_" + start.strftime('%Y-%m-%d'))
    
    #Select some to observe
    passes = selectStarlinkPasses(passes, timePer, path, "selectedPassesMorning_" + start.strftime('%Y-%m-%d'))
    
    
    ###########################
    
    
    #Make an ACP plan
    filename = "starlinkPlanMorning.txt"
    print("Writing ACP Plan as " + filename)
    
    #Reorganize for ACP plan
    obs = []
    for p in passes:
    	obs.append([p["name"],p["maxTime"],offset,p["maxRA"],p["maxDec"],p["maxAlt"],p["maxAz"]])
    
    #Write ACP plan for Pomenis
    writeAcpPlan(obs, exposureTime, exposureRepeat, filterLetter, binning, imagePath, os.path.join(path, filename), True)
    writeAcpPlan(obs, exposureTime, exposureRepeat, filterLetter, binning, imagePath, os.path.join(staticPath, filename), True)
    
    
    ###########################

    
    # #insert to text box
    # temp = passes
    # planBox.insert(END, temp)
    # planBox.see(END)    
    
    



















