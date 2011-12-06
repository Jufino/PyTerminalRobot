from graphics import *
from appuifw import *
from sensor import *
import math
import e32
import key_codes
import time
import camera
import btsocket

#obrazky-----------------------------
rONw =Image.open('e:\\rONw.gif')
rOFFw=Image.open('e:\\rOFFw.jpg')
rONs =Image.open('e:\\rONs.gif')
rOFFs=Image.open('e:\\rOFFs.jpg')
robot=Image.open('e:\\robot.jpg')
robot = robot.resize((320,320))
#-------------------------------------
#-----------------------------------------------------------  
#socket funkcie
def vybernet():
  apid = btsocket.select_access_point()
  apo = btsocket.access_point(apid)
  btsocket.set_default_access_point(apo)
def pripoj():
  global s
  s = btsocket.socket(btsocket.AF_INET, btsocket.SOCK_STREAM)
  #ip = query(u"Vloz ip adresu", "text")
  ip = "192.168.1.109"
  s.connect((ip,1213))
  note(u"pripojene","info")
def uzavri():
  s.close()
  apo.stop()
#-----------------------------------------------------------    
#data0-data7 = senzory IR hodnota
#data8-data9 = kompas16bit
#data10-data11 = ultrazvuky
#data12 = maxhodnota
#data13 = kicker senzor
#data14 = kompas8bit   
def prijmi_senzory():
  global data
  s.send("data")
  data = s.recv(1500)
#-----------------------------------------------------------  
#motory smer 1,rychlost 255 = motory("01","255") 
#motory smer 1,predosla rychlost = motory("01","-1")  
def motory(smer,rychlost):
  s.send("smer")
  s.send(smer) 
  if rychlost!="-1":
    s.send("rych")
    s.send(rychlost)
#----------------------------------------------------------- 
data_smer= "00"
#--------------------------------------
class accelerometer():
  def __init__(self):
    self.accelerometer = AccelerometerXYZAxisData(data_filter=LowPassFilter())
    self.accelerometer.set_callback(data_callback=self.my_callback)
    self.counter = 0
  def my_callback(self):
    rozlisenie = 10
    vyp_rozlisenie = 20
    global data_smer
    if self.counter % 2 == 0:
      if self.accelerometer.z > 30:
        if (self.accelerometer.x > -vyp_rozlisenie) & (self.accelerometer.x < vyp_rozlisenie) & (self.accelerometer.y > -vyp_rozlisenie) & (self.accelerometer.y < vyp_rozlisenie):
          data_smer = "00"
        else:
          if (self.accelerometer.x > -rozlisenie) & (self.accelerometer.x < rozlisenie) & (self.accelerometer.y < rozlisenie):
            data_smer = "07"
          else:
            if (self.accelerometer.x > -rozlisenie) & (self.accelerometer.x < rozlisenie) & (self.accelerometer.y > -rozlisenie):
              data_smer = "03"
            else:
              if (self.accelerometer.x < rozlisenie) & (self.accelerometer.y > -rozlisenie) & (self.accelerometer.y < rozlisenie):
                data_smer = "01"
              else:
                if (self.accelerometer.x > -rozlisenie) & (self.accelerometer.y > -rozlisenie) & (self.accelerometer.y < rozlisenie):         
                  data_smer = "05"
                else:
                  if (self.accelerometer.x < rozlisenie) & (self.accelerometer.y > -rozlisenie):
                    data_smer = "02"
                  else:
                    if (self.accelerometer.x > -rozlisenie) & (self.accelerometer.y > -rozlisenie):
                      data_smer = "04"
                    else:
                      if (self.accelerometer.x > -rozlisenie) & (self.accelerometer.y < rozlisenie):
                        data_smer = "06"
                      else:
                        data_smer = "08"
      else:
        data_smer = "00"
    self.counter = self.counter + 1
  def run(self):
    self.accelerometer.start_listening()
  def stop(self):
    self.accelerometer.stop_listening()
#-------------------------------------------------------
d = accelerometer()
def quit():
  global running
  d.stop()
  uzavri()
  running=0
def start_acc():
  note(u"Accelerometer start", "info")
  d.run()
  app.menu = [(u"Vypni accelerometer", stop_acc)]  
def stop_acc():
  note(u"Accelerometer stop", "info")
  d.stop()
  app.menu = [(u"Spusti accelerometer", start_acc)] 
app.menu = [(u"Spusti accelerometer", start_acc)]   
#-------------------------------------------------------
def radio_button(position,enabled,farba):
  global photo
  if farba == 's':
    if enabled == 0:
      photo.blit(rOFFs,(0,0),position)
    else:
      photo.blit(rONs,(0,0),position)  
  else:
    if enabled == 0:
      photo.blit(rOFFw,(0,0),position)
    else:
      photo.blit(rONw,(0,0),position) 

def camera_max(robot_y,senzor):
  if senzor == 1:
    radio_button((47,robot_y),1,'w')
  else:
    radio_button((47,robot_y),0,'w')
  if senzor == 2:
    radio_button((94,robot_y),1,'w')
  else:
    radio_button((94,robot_y),0,'w')
  if senzor == 3:
    radio_button((141,robot_y),1,'w')
  else:
    radio_button((141,robot_y),0,'w')
  if senzor == 4:
    radio_button((188,robot_y),1,'w')
  else:
    radio_button((188,robot_y),0,'w')
  if senzor == 5:
    radio_button((235,robot_y),1,'w')
  else:
    radio_button((235,robot_y),0,'w')
  if senzor == 6:
    radio_button((282,robot_y),1,'w')
  else:
    radio_button((282,robot_y),0,'w')
  if senzor == 7:
    radio_button((329,robot_y),1,'w')
  else:
    radio_button((329,robot_y),0,'w')
  if senzor == 8:
    radio_button((376,robot_y),1,'w')
  else:
    radio_button((376,robot_y),0,'w')
  if senzor == 9:
    radio_button((423,robot_y),1,'w')
  else:
    radio_button((423,robot_y),0,'w')
 
def robot_max(robot_x,robot_y,senzor):
  photo.blit(robot,(0,0),(robot_x,robot_y))     
  if senzor == 1:
    radio_button((152+robot_x,45+robot_y),1,'s')
  else:
    radio_button((152+robot_x,45+robot_y),0,'s')
  if senzor == 2:
    radio_button((215+robot_x,15+robot_y),1,'s')
  else:
    radio_button((215+robot_x,15+robot_y),0,'s')
  if senzor == 3:
    radio_button((247+robot_x,47+robot_y),1,'w')
  else:
    radio_button((247+robot_x,47+robot_y),0,'w')
  if senzor == 4:
    radio_button((280+robot_x,80+robot_y),1,'s')
  else:
    radio_button((280+robot_x,80+robot_y),0,'s')
  if senzor == 5:
    radio_button((295+robot_x,147+robot_y),1,'s')
  else:
    radio_button((295+robot_x,147+robot_y),0,'s')
  if senzor == 6:
    radio_button((280+robot_x,215+robot_y),1,'s')
  else:
    radio_button((280+robot_x,215+robot_y),0,'s')
  if senzor == 7:
    radio_button((247+robot_x,247+robot_y),1,'w')
  else:
    radio_button((247+robot_x,247+robot_y),0,'w')
  if senzor == 8:
    radio_button((215+robot_x,280+robot_y),1,'s')
  else:
    radio_button((215+robot_x,280+robot_y),0,'s')
  if senzor == 9:
    radio_button((152+robot_x,295+robot_y),1,'s')
  else:
    radio_button((152+robot_x,295+robot_y),0,'s')
  if senzor == 10:
    radio_button((90+robot_x,280+robot_y),1,'s')
  else:
    radio_button((90+robot_x,280+robot_y),0,'s')
  if senzor == 11:
    radio_button((57+robot_x,247+robot_y),1,'w')
  else:
    radio_button((57+robot_x,247+robot_y),0,'w')
  if senzor == 12:
    radio_button((25+robot_x,215+robot_y),1,'s') 
  else:
    radio_button((25+robot_x,215+robot_y),0,'s') 
  if senzor == 13:
    radio_button((15+robot_x,147+robot_y),1,'s')
  else:
    radio_button((15+robot_x,147+robot_y),0,'s')
  if senzor == 14:
    radio_button((25+robot_x,80+robot_y),1,'s')
  else:
    radio_button((25+robot_x,80+robot_y),0,'s') 
  if senzor == 15:
    radio_button((57+robot_x,47+robot_y),1,'w')
  else:
    radio_button((57+robot_x,47+robot_y),0,'w')
  if senzor == 16:
    radio_button((90+robot_x,15+robot_y),1,'s')
  else:
    radio_button((90+robot_x,15+robot_y),0,'s')  

def refresh(rect):
  global photo
  c.blit(photo)
  

#inicializacia
a=0
app.screen = 'full'
app.orientation = 'landscape'
app.title = u'Tlacitka test' 
photo=Image.new((480,360))
photo.clear(0xFFFFFF)

robot_max(75,30,0)

c=Canvas(redraw_callback=refresh)
app.body=c 
app.exit_key_handler=quit
running=1 
   
vybernet()
pripoj()
motory("00","255")
predosle = "00"
while running:
  photo.clear(0xFFFFFF)
  prijmi_senzory()
  robot_max(75,30,ord(data[12])-32)
  if predosle != data_smer:
    motory(data_smer,"-1")
  predosle = data_smer
  refresh(())  