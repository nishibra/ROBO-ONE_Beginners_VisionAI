#!/usr/bin/env micropython
# Kondo KRS servo control program
# 2025.4.6
# by T.Nishimura of AiRRC
#
#from machine import Pin, I2C, UART
import serial
import time
#-------------------------
class KRSdriver():
  def __init__(self):
   #set serial
    self.con = serial.Serial('/dev/ttyAMA0',1250000)
    self.con.bytesize=8
    self.con.parity=serial.PARITY_EVEN
    self.con.stopbits=1
    self.con.timeout=0.1
    self.con.setDTR(False)
    self.con.close()
    time.sleep(1)
    self.con.open()

    #self.con = UART(1, baudrate=1250000, tx=Pin(8), rx=Pin(9))
    #self.con.init(bits=8, parity=0, stop=1,timeout=50)
#
    self.buf2=bytearray(2)
    self.buf3=bytearray(3)
    self.buf4=bytearray(4)
    time.sleep(0.2)
    print("Initialized")
#
  def current_set(self,sid,curr):
    self.buf3[0]=0xC0+sid #cmd+id
    self.buf3[1]=0x03
    self.buf3[2]=curr&0x1F
    self.con.write(self.buf3)
#
    buf_read=self.con.read(2)
    if buf_read is not None:
      if (len(buf_read)==2):
        val=buf_read[1]
        return(val)
      else:
        #print ("ID="+str(sid)+"read few")
        return (9998)
    else:
      #print ("ID="+str(sid)+"read none")
      return(9999)
# set angle
  def set_position_ret(self,sid,t_pos):
    if(t_pos==0): #set free
      t_pos=0
    elif(t_pos>11500):
      t_pos=11500
    elif(t_pos<3500 ):
      t_pos=3500
  #
    self.buf3[0]=0x80+sid #cmd+id
    self.buf3[1]=(t_pos>>7)&0x7f
    self.buf3[2]=t_pos&0x7f
    self.con.write(self.buf3)
    
    buf_read=self.con.read(3)
    if buf_read is not None:
      #print(len(buf_read))
      if (len(buf_read)==3):
        val=buf_read[2]+(buf_read[1]<<7)
        return(val)
      else:
        #print ("ID="+str(sid)+" read few="+str(len(buf_read)))
        return (9998)
    else:
      print ("ID="+str(sid)+" read none")
      return(9999)
#-----------------------------
# set angle by slave mode
  def set_position(self,sid,t_pos):
# 
    if(t_pos==0): #set free
      t_pos=0
    elif(t_pos>11500):
      t_pos=11500
    elif(t_pos<3500 ) :
      t_pos=3500
  #
    self.buf3[0]=0x80+sid #cmd+id
    self.buf3[1]=(t_pos>>7)&0x7f
    self.buf3[2]=t_pos&0x7f
  # write
    self.con.write(self.buf3)
#------------------------
# read angle at free condition
  def read_position_set_free(self,sid):
    position=self.set_position_ret(sid,0)
    return position
#--------------------------
# read any condition
  def read_position(self,sid):  #from ics3.6
    self.buf2[0]=0xA0+sid #cmd+id
    self.buf2[1]=0x05 #angle
    self.con.write(self.buf2)
    #time.sleep(0.001)
    buf_read=self.con.read(4)
    if buf_read is not None:
      if (len(buf_read)==4):
        val=buf_read[3]|(buf_read[2]<<7)
        return(val)
      else:
        #print ("ID="+str(sid)+" read few")
        #print ("ID="+str(sid)+" set few="+str(len(buf_read)))
        return (9998)
    else:
      print ("ID="+str(sid)+" read none")
      return (9999)
# set ID
  def id_read(self):
    self. buf4[0]=0xFF
    self. buf4[1]=0x00
    self.buf4[2]=0x00
    self.buf4[3]=0x00
    self.con.write(self.buf4)
    buf_read=self.con.read(1)
    if (len(buf_read)==1):
      val=(buf_read[0])&0x1f
      return(val)
    else:
      print ("ID read error")
      return(99)
# set ID 0-31
  def id_set(self,sid):
    cmd1=sid&0x1f 
    cmd=0xE0+cmd1
    self.buf4[0]=cmd    #cmd+id
    self.buf4[1]=0x01
    self.buf4[2]=0x01
    self.buf4[3]=0x01
    self.con.write(self.buf4)
    #time.sleep(0.005)
    buf_read=self.con.read(1)
    if (len(buf_read)==1):
      val=(buf_read[0])&0x1f
      return(val)
    else:
      print ("IDS read error")
      return(99)
#
  def read_memory(self,sid): #2->66
    print("read_memory")
    cmd1=sid&0x1f #sid 0-31
    cmd=0xA0+cmd1
    self.buf2[0]=cmd    #cmd+id
    self.buf2[1]=0x00
    self.con.write(self.buf2)
    #
    buf_read=self.con.read(66) #2-66byte
    #print (len(buf_read))
    if (len(buf_read)==66):
      return(buf_read)
    else:
      print ("memory read error")
      return(99)
    #
  def write_memory(self,sid,write_buf):#3-
    print("write memory ")
    cmd1=sid&0x1f #sid 0-31
    cmd=0xC0+cmd1
    write_buf[0]=cmd    #cmd+id
    write_buf[1]=0x00   #EEPROM
    self.con.write(write_buf)
    
    time.sleep(1)
    #
    buf_read=self.con.read() #2-66byte
    
    #print (len(buf_read))
    if (len(buf_read)==2):
      return(buf_read)
    else:
      print ("memory read error")
      return(99)
      
  #def set_baud(self,baud):
  #    print(" ")
      
# get buttan data of KRS-5FH #id= 31
  def get_5fh(self):
    #print("read button")
    temp=bytearray(4)
    self.buf4[0]=0xbf 
    self.buf4[1]=0x7f
    self.buf4[2]=0x00
    self.buf4[3]=0x02
    self.con.write(self.buf4)
    buf_read=self.con.read(12)
    #print(buf_read)
    if (len(buf_read)==8):
      temp[0]=(buf_read[4])
      temp[1]=(buf_read[5])
      b1=temp[1]|(temp[0]<<8)
      temp[0]=(buf_read[6])
      temp[1]=(buf_read[7])
      b2=temp[1]|(temp[0]<<8)
      return b1,b2
    else:
      print ("5FH read error")
      return 0,0
#---------------------------------    
#
def main1():
  sid=1 # left motor
  print(sid,"=",krs.read_position(sid))
  sid=2 # right motor
  print(sid,"=",krs.read_position(sid))
  sid=3 # pan motor
  print(sid,"=",krs.read_position(sid))
  sid=4 # tilt motor
  print(sid,"=",krs.read_position(sid))
  for i in range(4):
      krs.read_position_set_free(i+1)
        
def main():
  #Arm
  krs.set_position_ret(3,6250)
  krs.set_position_ret(4,7500)
  #直進
  krs.set_position_ret(1,7400)
  krs.set_position_ret(2,7600)
  time.sleep(0.3)
  #回転
  krs.set_position_ret(1,7600)
  krs.set_position_ret(2,7600)
  time.sleep(0.4)
  #stop
  krs.set_position_ret(1,7500)
  krs.set_position_ret(2,7500)
  time.sleep(3)
  #free
  krs.read_position_set_free(1)
  krs.read_position_set_free(2)
  krs.read_position_set_free(3)
  krs.read_position_set_free(4)  
#
#------------------------
if __name__ == '__main__':
  print('Start KRS Test')
  krs=KRSdriver()
  main1()
  #while(1):
  #  a,b=krs.get_5fh()
  #  aa=f'{a:#016b}'
  #  bb=f'{b:#016b}'
  #  print(aa,bb)
    
  #  time.sleep(0.002)
