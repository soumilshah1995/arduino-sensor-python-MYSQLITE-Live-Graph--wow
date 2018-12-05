import serial # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
from matplotlib import style
import json
import urllib.request
import requests
from twilio.rest import Client
import threading
import time


style.use('ggplot')

t= []
h=[]
style.use('ggplot')

fig=plt.figure()
ax1=fig.add_subplot(111)

arduinoData = serial.Serial('COM8',9600,timeout=0.1) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data

cnt=0
global timer
timer=0
start_time = time.time()

def makeFig(): #Create a function that makes our desired plot

    plt.ylim(10,99)                                 #Set y min and max values
    plt.title('DHT-11 Sensor Data ')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temp *C')                            #Set ylabels
    plt.plot(t, 'ro-', label='Degrees F')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend


    plt2=plt.twinx()                                #Create a second y axis
    plt.ylim(10,100)                           #Set limits of second y axis- adjust to readings you are getting
    plt.plot(h, 'b^-', label='Humidity %') #plot pressure data
    plt2.set_ylabel('Humidity %')                    #label second y axis
    plt2.ticklabel_format(useOffset=False)           #Force matplotlib to NOT autoscale y axis
    plt2.legend(loc='upper right')                  #plot the legend



while True: # While loop that loops forever
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing

    arduinoString = arduinoData.readline().decode('ascii') #read the line of text from the serial port
    dataArray = arduinoString.split(',')   #Split it into an array called dataArray
    H = float( dataArray[0])            #Convert first element to floating number and put in temp
    T =    float( dataArray[1])            #Convert second element to floating number and put in P
    t.append(T)                     #Build our tempF array by appending temp readings
    h.append(H)                     #Building our pressure array by appending P readings
    drawnow(makeFig)                       #Call drawnow to update our live graph
    plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
    cnt=cnt+1

    if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
        t.pop(0)                       #This allows us to just see the last 50 data points
        h.pop(0)



""""  
    timer=timer+1

    if timer == 150:
        print("--- %s seconds ---" % (time.time() - start_time))
        post_cloud_humidity(H,T)
        timer=0
"""