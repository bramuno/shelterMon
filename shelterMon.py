#!/bin/python3
# sudo apt install rsyslog
## version notes:
## this script will look for .json config files stored in the path passed by -C option
## usage: python3 shelterMon.py -C /path/to/folder
## 
debug = 0
import os, sys, json, subprocess, smtplib, datetime, time, os.path, pdb, argparse, glob
from email.message import EmailMessage
from os.path import exists
import RPi.GPIO as GPIO
parser = argparse.ArgumentParser()
parser.add_argument("-C", "--config", help = "config")
parser.add_argument("-d", "--debug", help = "debug")
args = parser.parse_args()
if args.debug == "yes" or args.debug == "on" or str(args.debug) == "1":
    debug = 1
    print("Diplaying debug as: %s" % args.debug)
if args.debug == "":
    debug = 0
if args.config:
    if debug == 1:
        print("Diplaying config file as: % s" % args.config)

def msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, message):
    server = smtplib.SMTP_SSL(SMTPserver, SMTPport)
    server.connect(SMTPserver,SMTPport)
    server.ehlo()
    server.login(SMTPuser, SMTPpass)
    server.send_message(message)
    server.quit()

configFolder = str(args.config)
if len(configFolder)-1 != "/":
    configFolder = str(configFolder)+"/"

cfg = str(configFolder)
configFolder = str(configFolder)+"*.json"
tmplist = glob.glob(configFolder)
alertFile = ""
list = []
g = 0

configFolder = str(args.config)
try:
    f = open(configFolder+"/email.json", "r")
    get = json.load(f)
    f.close()
except:
    sys.exit("failed to load "+configFolder+"/email.json \n")

SMTPuser =  get['SMTPuser']
SMTPpass =  get['SMTPpass']
SMTPserver =  get['SMTPserver']
SMTPport =  int(get['SMTPport'])

# begin loop
while g < len(tmplist):
    alert = 0
    lastSeen = 0
    if tmplist[g] != configFolder+"/email.json":
        if debug == 1:
            print("\nstarting: "+str(tmplist[g]))
        try:
            f = open(tmplist[g], "r")
            get = json.load(f)
            f.close()
        except:
            sys.exit("json config  load fail.  --> "+str(tmplist[g])+"\n")

        shelterName = get['shelterName']
        folderName =  get['folderName']
        logfileName =  str(get['logfileName'])
        statusFileName =  logfileName+"-status.txt"
        maxTemp =  float(get['maxTemp'])
        minTemp =  float(get['minTemp'])
        tempUnit =  str(get['tempUnit'])
        maxDuration =  int(get['maxDuration'])
        dests =  get['emailDestination']
        #
        newfile = 0
        logfile = folderName+"/"+logfileName
        statusFile = folderName+"/"+statusFileName

        if not os.path.exists(logfile) or not os.path.exists(statusFile):
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
        read = f.read()
        f.close()
        #
        empty=0
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
        finalTemp = temp[0]
        tempC = round(float(finalTemp)-32*(5/9),2)
        if tempUnit == "C":
            finalTemp = tempC
        else:
            finalTemp = str(round(float(finalTemp),1))
        if ( float(finalTemp) > float(maxTemp) ) or ( float(finalTemp) < float(minTemp) )  :
            state = 0

        if int(state) == 1:
            newDur = round(diffMins, 1)
        else:
            newDur = round((oldDur + diffMins), 1)

        if debug == 1:
            print("oldState = "+str(oldState))
            print("oldDur = "+str(oldDur))
            print("maxTemp = "+str(maxTemp)+str(tempUnit))
            print("minTemp = "+str(minTemp)+str(tempUnit))
            print("temp reading = ",str(finalTemp)+str(tempUnit))
            print("maxDuration = ",str(maxDuration))
            print("statusFile = ",str(statusFile))
            print("newfile = ",str(newfile))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if int(GPIO.input(17)) == 0:
            f = open(logfile, "w")
            f.write(str(lastEvent))
            f.close()
            if debug == 1:
                print("switchCheck = ",str(GPIO.input(17)))
            sys.exit("\nDetected OFF switch position on syslog server. Quitting.\n")
        ###################
        # offline sensor alert (every 5m on the 5th minute)
        if round(minsSinceLastLog,0) > 5:
            body = "No contact from temperature sensor "+str(shelterName)+" in "+str(minsSinceLastLog)+" minutes.\nPlease check it is online and batteries are charged.\nReboot if needed.\n"
            subject = "Temperature sensor offline"
            alert = 1
        ########## critical temperature alert begin
        if ( int(state) == 0 and int(oldState) == 0 and float(oldDur) > float(maxDuration) ) :
            alert = 1
            body = str(shelterName)+" has been reading '"+str(reading)+str(tempUnit)+"' degree temperature for at least "+str(oldDur)+" minutes!\n"
            subject = str(shelterName)+" Sensor temperature problem"
        ########## END critical temperature alert
        ## alert sensor online but reading incorrectly
        if ( float(finalTemp) < -40.0 ) :
            alert = 1
            body = "\nA sensor is not reading correctly:\n\nsensorA="+str(float(finalTemp))+"\n"
            subject = 'Sensor read problem'
        ########## end
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
            print("alert = ",str(alert))
            print("logfile = ",str(logfile))

        if newfile == 1:
            newDur = "0"
            lastSeen = str(nowEpoch)
            if debug == 1:
                print("\nnew status file created\n")
        else:
            lastSeen = str(logEpoch)
            if state == 1:
                newDur = "0"

        output = '{"lastSeen":"'+str(lastSeen)+'","state":"'+str(state)+'","duration":"'+str(newDur)+'","lastTemp":"'+str(finalTemp)+'","minsSinceLastLog":"'+str(minsSinceLastLog)+'","location":"'+str(shelterName)+'" }'
        print(output)

        f = open(statusFile, "w")
        f.write(output)
        f.close()
        # clear data log and add the last event
        f = open(logfile, "w")
        f.write(lastEvent)
        f.close()

        ## create master file
        if alert == 1:
            alertFile = str(args.config)+"/alert.txt"
            if exists(alertFile):
                gg = open(alertFile, 'a')
                if debug == 1:
                    print("deleting alertFile")
            else:
                gg = open(alertFile, 'x')
                if debug == 1:
                        print("creating alertFile")
            alertOut = '{"dests":"'+str(dests)+'", "subject":"'+str(subject)+'", "body":"'+str(body)+'"}\nbreak'
            if debug == 1:
                print(str(alertOut)+" >> "+str(alertFile))
            gg.write(alertOut)
            gg.close()
    g = g + 1

## END LOOP

if exists(alertFile):
    m = open(alertFile, 'r')
    read = m.read().split("\nbreak")
    m.close()
    ##get = json.loads(read[0], strict=False)
    emails = []
    body = ""
    x=0
    while x < len(read):
        if read[x] == "\n" or  read[x] == "":
            read.pop(x)
        else:
            line = json.loads(read[x], strict=False)
            b=0
            tmp = line['dests'].split(',')
            while b < len(tmp):
                tmp[b] = tmp[b].replace(" ","")
                emails.append(tmp[b])
                b=b+1
        x=x+1

    now = datetime.datetime.now()
    minute = now.strftime('%M')
    x=0
    if int(minute)%5 == 0:
        while x < len(emails):
            tgt = emails[x]
            b=0
            mSubject = ""
            thisBody = ""
            while b < len(read):
                if tgt in read[b]:
                    line = json.loads(read[b], strict=False)
                    if line['body'] not in thisBody:
                        thisBody = str(line['body'])+"\n"
                b=b+1
            thisMsg = EmailMessage()
            thisMsg.set_content(thisBody)
            thisMsg['Subject'] = line['subject']
            thisMsg['From'] = "alert@temperatureMon.org"
            thisMsg['To'] = tgt
            try:
                msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, thisMsg)
            except Exception as e: 
                print(e)
            else:
                print("Sent email to :"+str(tgt))
            x=x+1
    else:
        print("not the 5th minute, skipping notification")
    if debug == 0:
        print("deleting "+str(alertFile))
        os.remove(alertFile)
sys.exit()
