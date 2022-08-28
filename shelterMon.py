#!/bin/python
# sudo apt install rsyslog
debug = ""
import os, sys, json, subprocess, smtplib, datetime, time, os.path, pdb, argparse
from email.message import EmailMessage
import RPi.GPIO as GPIO
parser = argparse.ArgumentParser()
parser.add_argument("-C", "--config", help = "config")
parser.add_argument("-d", "--debug", help = "debug")
args = parser.parse_args()
if args.debug == "yes" or args.debug == "on" or str(args.debug) == "1":
    debug = 1
    print("Diplaying debug as: %s" % args.debug)
if args.config:
    if debug == 1:
        print("Diplaying config file as: % s" % args.config)

try:
    f = open(args.config, "r")
    get = json.load(f)
except:
    sys.exit("Config.json load failed.\n")

def msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, message):
    server = smtplib.SMTP_SSL(SMTPserver, SMTPport)
    server.connect(SMTPserver,SMTPport)
    server.ehlo()
    server.login(SMTPuser, SMTPpass)
    server.send_message(message)
    server.quit()


f.close()
shelterName = get['shelterName']
folderName =  get['folderName']
logfileName =  str(get['logfileName'])
statusFileName =  logfileName+"-status.txt"
maxTemp =  float(get['maxTemp'])
minTemp =  float(get['minTemp'])
tempUnit =  str(get['tempUnit'])
maxDuration =  int(get['maxDuration'])
emailDestination =  get['emailDestination']
SMTPuser =  get['SMTPuser']
SMTPpass =  get['SMTPpass']
SMTPserver =  get['SMTPserver']
SMTPport =  int(get['SMTPport'])
SMS = get['SMS']
SMScarrier =  int(get['SMScarrier'])

newfile = 0
car=["@vtext.com","@txt.att.net","@sms.myboostmobile.com","@tmomail.net","@sms.cricketwireless.net","@messaging.sprintpcs.com" ]
smsEmailDest = SMS+car[SMScarrier]
logfile = folderName+"/"+logfileName
statusFile = folderName+"/"+statusFileName
lastSeen = 0

if not os.path.exists(logfile):
    sample = '{"lastSeen":"1659588285","state":"1","duration":"0","lastTemp":"80.88","minsSinceLastLog":"0.0" }'
    cmd = "mkdir -p "+str(folderName)
    subprocess.check_output(cmd, shell=True)
    cmd = "touch "+str(logfile)
    subprocess.check_output(cmd, shell=True)
    cmd = "echo '"+str(sample)+"' > "+str(statusFile)
    subprocess.check_output(cmd, shell=True)

try:
    f = open(statusFile, "r")
    get = json.load(f)
    oldStatus = f.read()
    f.close()
    try:
        oldState =  int(get['state'])
        oldDur = float(get['duration'])
        lastSeen = int(get['lastSeen'])
        newfile = 0
    except:
        print("nope")
except:
    get = ""
    oldStatus = 0
    oldState =  0
    oldDur = 0
    lastSeen = 0
    dur = 0
    if debug == 1:
        print(str(statusFile)+" JSON load failed.\n")
    f.close()

if oldDur < 0:
    oldDur = 0

if oldStatus == "" and oldState == "" and oldDur == "":
    newfile = 1

# open data log
f = open(logfile, "r")
empty=0
read = f.read()
f.close()
#
state = 1
data = read.split("\n")
lines = len(data)
now = datetime.datetime.now()
if lines-2 < 0:
    tgt=0
else:
    tgt=lines-2

lastEvent = data[tgt]
nowEpoch = int(datetime.datetime.now().timestamp())
lastEvent = lastEvent.replace("  "," ")
chk = lastEvent.split(" ")
readTime = chk[0]+" "+chk[1]+" "+chk[2]
mo=str(chk[0])
months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
a = mo.strip()[:3].lower()
year = now.year
minute = now.strftime('%M')
month = months[a]
day=int(chk[1])
splTime = chk[2].split(":")
hour=int(splTime[0])
min=int(splTime[1])
sec=int(splTime[2])
logEpoch = int(datetime.datetime(year, month,day, hour, min, sec).timestamp())
diffEpoch = nowEpoch - lastSeen
secSinceLastLog = nowEpoch - logEpoch
minsSinceLastLog = round((secSinceLastLog/60),1)
if diffEpoch < 0:
    diffEpoch = 0

if float(secSinceLastLog) < 0:
    secSinceLastLog = 0

diffMins = float(round(diffEpoch/60,2))
temp=chk[3].split(",")
if ( float(temp[0]) > float(maxTemp) ) or ( float(temp[0]) < float(minTemp) )  :
    state = 0

reading = str(temp[0])
avg = ( float(temp[0]) ) /2
avg = round(avg,1)
if int(state) == 1:
    newDur = round(diffMins, 1)
else:
    newDur = round((oldDur + diffMins), 1)

if debug == 1: 
    print("oldState = "+str(oldState))
    print("oldDur = "+str(oldDur))
    print("maxTemp = ",str(maxTemp))
    print("minTemp = ",str(minTemp))
    print("temp[0] = ",str(temp[0]))
    print("maxDuration = ",str(maxDuration))
    print("newfile = ",str(newfile))

GPIO.setmode(GPIO.BCM)     
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
if int(GPIO.input(17)) == 0:
    f = open(logfile, "w")
    f.write(str(lastEvent))
    f.close()
    if debug == 1:
        print("switchCheck = ",str(GPIO.input(17)))
    print("\nDetected OFF switch position on syslog server. Quitting.\n")
    sys.exit()
#
###################
# offline sensor alert (every 5m on the 5th minute)
if round(minsSinceLastLog,0) > 5 and int(minute)%5 == 0:
    msgMissing = EmailMessage()
    msgMissing.set_content("No contact from temperature sensor harness in "+str(minsSinceLastLog)+" minutes.\nPlease check it is online and batteries are charged.\nReboot if needed.\n\nsent:"+str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(sec)+"\n")
    msgMissing['Subject'] = "No contact from temperature sensor"
    msgMissing['From'] = emailDestination
    msgMissing['To'] = emailDestination+","+smsEmailDest
    msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, msgMissing)
    if debug == 1:
        print(">>>>> email alert sent")  

########## critical temperature alert begin
if ( state != 1 and int(oldState) == 0 and float(oldDur) > float(maxDuration) ) :
    alert = 1
    msgCritical = EmailMessage()
    msgCritical.set_content("\nSensor temperature outside desired threshold for at least "+str(oldDur)+" minutes.\n\n")
    msgCritical['Subject'] = str(shelterName)+" has been in "+str(avg)+str(tempUnit)+" degree temperature for at least "+str(oldDur)+" minutes!"
    msgCritical['From'] = emailDestination
    msgCritical['To'] = emailDestination+","+smsEmailDest
    msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, msgCritical)
    if debug == 1:
        print(">>>>> email alert sent")  
########## critical temperature alert end
## alert sensor online but reading incorrectly
if ( float(temp[0]) < -60.0 ) and int(minute)%5 == 0 :
    glitchMSG = EmailMessage()
    glitchMSG.set_content("\nA harness sensor is not reading correctly:\n\nsensorA="+str(float(temp[0]))+"\n")
    glitchMSG['Subject'] = 'A harness sensor is not reading correctly'
    glitchMSG['From'] = "alert@temperatureMon.org"
    glitchMSG['To'] = emailDestination+","+smsEmailDest
    msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, glitchMSG)
#
if debug == 1:
    print("state = ",str(state))
    print("nowEpoch = ",str(nowEpoch))
    print("lastSeen = ",str(lastSeen))
    print("diffEpoch = ",str(diffEpoch))
    print("diffMins = ",str(diffMins))
    print("newDur = ",str(newDur))
    print("minsSinceLastLog = ",str(minsSinceLastLog))
    print("thisMinute = ",str(minute))
    print("switchCheck = ",str(GPIO.input(17)))
#
if newfile == 1:
    newDur = "0"
    lastSeen = str(nowEpoch)
    if debug == 1:
        print("\nnew status file created\n")
else:
    lastSeen = str(logEpoch)
    if state == 1:
        newDur = "0"

output = '{"lastSeen":"'+str(lastSeen)+'","state":"'+str(state)+'","duration":"'+str(newDur)+'","lastTemp":"'+reading+'","minsSinceLastLog":"'+str(minsSinceLastLog)+'" }'
print(output)
#
f = open(statusFile, "w")
f.write(output)
f.close()
sys.exit()
# clear data log and add the last event
f = open(logfile, "w")
f.write(lastEvent)
f.close()
