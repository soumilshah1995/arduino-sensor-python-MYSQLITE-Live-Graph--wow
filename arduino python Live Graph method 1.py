import serial
import sqlite3
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg ,NavigationToolbar2Tk
import urllib
import geocoder
import threading
import _thread
import urllib.request
import json


from drawnow import *

style.use('ggplot')
fig=plt.figure()
ax1=fig.add_subplot(111)

global y_axis_t

x_axis=[]               # comtains time inn xaxis
y_axis_t=[]             # contains live data from sensor
y_axis_h=[]             #contains live data from hunidity sensor
m=[]
global counter
counter=0


def get_geolocations():
    try:
        g = geocoder.ip('me')
        my_string=g.latlng
        longitude=my_string[0]
        latitude=my_string[1]
        return longitude,latitude
    except:
        print('Could Not Get the  Co-ordinates!')


def get_date_time():
    try:
        mytime = datetime.datetime.now()
        tm= '{}:{}:{}'.format(mytime.hour,mytime.minute,mytime.second)
        dt= '{}/{}/{}'.format(mytime.month,mytime.day,mytime.year)
        return tm,dt
    except:
        print('Error Cannot get Date and Time ')


def add_db(time, t, h, dt, longitude, latitude):
    try:
        conn=sqlite3.connect('Temperature.db')
        c=conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS data 
        (Time TEXT,Temperature TEXT,Humidity TEXT,Date TEXT,longitude TEXT,latitude TEXT)""")

        c.execute(""" INSERT INTO data
        (Time, Temperature, Humidity, Date,longitude, latitude)
        VALUES (?, ?, ?, ?, ?, ?)""", (time, t, h, dt,longitude,latitude))

        conn.commit()
        c.close()
        conn.close()
    except:
        print('Cannot add to Datbase!')



def read_data():
    try:
        arduinodata =serial.Serial('COM8',9600,timeout=0.1)
        while arduinodata.inWaiting:
            val=arduinodata.readline().decode('ascii')
            if len(val) == 13 :
                return val
    except:
        print('Cannot read daata !')


def process():
    try:
        global counter
        counter = counter + 1

        # call all functon and get their respective value !
        h,t=read_data().split(',')

        tm,dt=get_date_time()
        longitude,latitude=get_geolocations()

        # append to the list for plotiing value
        x_axis.append(tm)
        y_axis_t.append(t)
        y_axis_h.append(h)

        if counter == 5: # represent rate at which you cant to add data to database
            # 2 indicate upload data to database after  4 sec
            add_db(tm,t,h,dt,longitude,latitude)
            counter=0

        return tm,str(t),str(h),str(dt)
    except:
        print('Failed to Execute Process ! ')


def animate(i):

    ax1.clear()
    tm,t,h,dt=process()

    #Plot Temperature versus Time on X axis
    ax1.plot(y_axis_t,label='Temperature',color='r')
    ax1.fill_between(x_axis, y_axis_t, color='r', alpha=0.2)

    # Plot Humidity Versus Time
    ax1.plot(x_axis,y_axis_h, label='Humidity',color='b')
    ax1.fill_between(x_axis, y_axis_h, color='b', alpha=0.2)

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.set_xlim(left=max(0, i-10),right=i+1 )
    plt.xlabel('Time ')
    plt.ylabel('Temperature in C and Humidity in %')
    plt.title('Live Sensor Data\nDHT-11 Sensor Graph ')
    plt.legend()




if __name__ == '__main__':
    ani= animation.FuncAnimation(fig, animate, interval=2000)
    plt.show()


