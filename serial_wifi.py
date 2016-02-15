import time
import serial
from  wifi import Cell

ser=serial.Serial(port ="/dev/ttyAMA0",
baudrate=9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1)
cmd=""	
counter=0
inbuff=""
state="run"
newcmdflag=False
outbuff=""
cmdlist=[]

def getcells():
	datast=""
	n=0
	for cll in cellx:
		n+=1
		datast=datast+"***** "+str(n)+"  ******"+"\n"	
		datast=datast+"Channel: "+str(cll.channel)+"\n"
		datast=datast+"Addess: "+str(cll.address)+"\n"
		datast=datast+"Quality: "+str(cll.quality)+"\n"
	
#print cll.bitrates
	#print cll.frequency
	#print cll.quality
	#print cll.mode
	#print cll.adress
	#print cll.encryption_type
	return datast

cellx=Cell.all('wlan0')
try:
	while state=="run":
		data="Counter %d \n"%(counter)
		#ser.write("Hello\n")
		print data
		time.sleep(1)
		counter+=1
		x=ser.readline()
		if len(x) > 0:
			print "lenght ", len(x)
			inbuff=inbuff+x
		for char in inbuff:
			if char == "<": #start of command
				newcmd=""
				newcmdflag=True
				inbuff=inbuff[:-1]
			elif char ==">":
				print newcmd
				cmdlist.append(newcmd)	

				newcmd=""
				newcmdflag=False
				inbuff=inbuff[:-1]
			elif newcmdflag==True:
				newcmd=newcmd+char
				inbuff=inbuff[:-1]
		        #print "inbuff", inbuff
	
		for cmd in cmdlist:
			if cmd == "GET_CELLS":
				print "Sent command GET_CELLS"
				cmdlist.remove("GET_CELLS")
				ser.write(getcells())
			else:
				cmdlist.remove(cmd)
				print "Invalid Command : ", cmd
	#	print cmdlist
#		if "stop" in x:
#			state="stop"

except KeyboardInterrupt:
	print "port closed"
	ser.close()
