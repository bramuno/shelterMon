#!/bin/python3
# sudo apt install rsyslog
## version notes:
## this script will look for .json config files stored in the path passed by -C option
## to disable a shelter/location sensor, just rename the .json file to something without .json (eg.  file.save)
## usage: python3 shelterMon.py -C /path/to/folder
## debug usage: python3 shelterMon.py -C /path/to/folder -d yes
## alert test usage: python3 shelterMon.py -C /path/to/folder -t yes
## 
debug = 0
test = 0
import os, sys, json, subprocess, smtplib, datetime, time, os.path, pdb, argparse, glob
from email.message import EmailMessage
from os.path import exists
import RPi.GPIO as GPIO
parser = argparse.ArgumentParser()
parser.add_argument("-C", "--config", help = "config")
parser.add_argument("-d", "--debug", help = "debug")
parser.add_argument("-t", "--test", help = "test")
args = parser.parse_args()
if args.debug:
    if args.debug.lower() == "yes" or args.debug.lower() == "on" or str(args.debug.lower()) == "1":
        debug = 1
        print("Diplaying debug as: %s" % args.debug.lower())
    else:
        debug = 0
if args.config:
    if debug == 1:
        print("Diplaying config file as: % s" % args.config)
if args.test:
    if debug == 1:
        print("Diplaying config file as: % s" % args.test)

# detect physical switch position
# off switch disables all notifications
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
if int(GPIO.input(17)) == 0:
    ON = 0
else:
    ON = 1
if args.test:
    test = str(args.test.lower())
    if test == 1 or test == 1 or test == "true" or test == "yes":
        test = 1
        print("\n\n TESTING NOTIFICATIONS ENABLED\n\n")

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

if os.path.exists(configFolder+"/sms.json"):
    try:
        f = open(configFolder+"/sms.json", "r")
        getSMS = json.load(f)
        f.close()
        sid =  str(getSMS['twilioServiceID'])
        twilioToken =  str(getSMS['twilioToken'])
        twilioAcctID =  str(getSMS['twilioAcctID'])
        twilioFromNumber =  str(getSMS['twilioFromNumber'])
    except:
        sys.exit("failed to load values from '"+configFolder+"/sms.json'.  Check the json syntax is correct.\n")
else:
    sid = ""
    twilioToken = ""
    twilioAcctID = ""
    twilioFromNumber = ""



g = 0
# begin loop
while g < len(tmplist):
    notifyMin = -1
    alert = 0
    lastSeen = 0
    if tmplist[g] != configFolder+"/email.json" and tmplist[g] != configFolder+"/sms.json":
        if debug == 1:
            print("\nstarting: "+str(tmplist[g]))
        try:
            f = open(tmplist[g], "r")
            get = json.load(f)
            f.close()
        except:
            sys.exit("json config  load fail.  --> "+str(tmplist[g])+"\n")

        enabled = get['enabled'].lower()
        location = str(get['locationName'])
        folderName =  str(get['folderName'])
        logfileName =  str(get['logfileName'])
        statusFileName =  str(logfileName)+"-status.txt"
        maxTemp =  float(get['maxTemp'])
        minTemp =  float(get['minTemp'])
        tempUnit =  str(get['tempUnit'])
        maxDuration =  int(get['maxDuration'])
        dests =  str(get['emailDestination'])
        destSMS =  str(get['destSMS'])
        throttle =  str(get['throttle'])
        #
        newfile = 0
        logfile = folderName+"/"+logfileName
        statusFile = folderName+"/"+statusFileName

        if enabled == "yes":
            if not os.path.exists(logfile) or not os.path.exists(statusFile):
                sample = '{"lastSeen":"1659588285","OKstatus":"1","duration":"0","lastTemp":"80.88","minsSinceLastLog":"0.0","notifyMin":"0" }'
                cmd = "mkdir -p "+str(folderName)
                subprocess.check_output(cmd, shell=True)
                cmd = "touch "+str(logfile)
                subprocess.check_output(cmd, shell=True)
                cmd = "echo '"+str(sample)+"' > "+str(statusFile)
                subprocess.check_output(cmd, shell=True)

            try:
                f = open(statusFile, "r")
                get = json.load(f)
                f.close()
                try:
                    oldOKstatus =  int(get['OKstatus'])
                    oldDur = float(get['duration'])
                    lastSeen = int(get['lastSeen'])
                    newfile = 0
                    notifyMin = int(get['notifyMin'])
                except:
                    print("status file load fail")
            except:
                get = ""
                oldOKstatus =  0
                oldDur = 0
                lastSeen = 0
                dur = 0
                if debug == 1:
                    print(str(statusFile)+" JSON load failed.\n")
                f.close()

            if oldDur < 0:
                oldDur = 0

            if oldOKstatus == "" and oldDur == "":
                newfile = 1

            # open data log
            f = open(logfile, "r")
            read = f.read()
            f.close()
            #
            empty=0
            OKstatus = 1
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
            if(secSinceLastLog) < 0:
                secSinceLastLog = 10000000000
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
                OKstatus = 0

            if int(OKstatus) == 1:
                newDur = round(diffMins, 1)
            else:
                newDur = round((oldDur + diffMins), 1)

            if debug == 1:
                print("oldOKstatus = "+str(oldOKstatus))
                print("oldDur = "+str(oldDur))
                print("maxTemp = "+str(maxTemp)+str(tempUnit))
                print("minTemp = "+str(minTemp)+str(tempUnit))
                print("temp reading = ",str(finalTemp)+str(tempUnit))
                print("maxDuration = ",str(maxDuration))
                print("statusFile = ",str(statusFile))
                print("newfile = ",str(newfile))
                print("enabled = ",str(enabled))
                print("test = ",str(test))

            ###################
            # offline sensor alert (every 5m on the 5th minute)
            if round(minsSinceLastLog,0) > 5 or round(minsSinceLastLog,0) < 0:
                body = "No contact from temperature sensor '"+str(location)+"' in "+str(minsSinceLastLog)+" minutes.\nPlease verify it is online and reboot if needed.\n"
                subject = "Temperature sensor offline"
                alert = 1
            ########## critical temperature alert begin
            if ( int(OKstatus) == 0 and int(oldOKstatus) == 0 and float(oldDur) > float(maxDuration) ) :
                alert = 1
                body = str(location)+" has been reading '"+str(finalTemp)+str(tempUnit)+"' degree temperature for at least "+str(oldDur)+" minutes!\n"
                subject = str(location)+" Sensor temperature OKstatus"
            ########## END critical temperature alert
            ## alert sensor online but reading incorrectly
            if ( float(finalTemp) < -40.0 ) :
                alert = 1
                body = "\nSensor "+str(location)+" is not reading correctly:\n\nsensorA="+str(float(finalTemp))+"\nPlease check the connection.\n"
                subject = str(location)+" Sensor problem"
            ########## end
            if debug == 1:
                print("OKstatus = ",str(OKstatus))
                print("nowEpoch = ",str(nowEpoch))
                print("oldLastSeen = ",str(lastSeen))
                print("logEpoch = ",str(logEpoch))
                print("diffEpoch = ",str(diffEpoch))
                print("diffMins = ",str(diffMins))
                print("newDur = ",str(newDur))
                print("minsSinceLastLog = ",str(minsSinceLastLog))
                print("thisMinute = ",str(minute))
                print("switchCheck = ",str(GPIO.input(17)))
                print("alert = ",str(alert))
                print("logfile = ",str(logfile))
                print("notifyMin = ",str(notifyMin))
                print("notify = "+str(notifyMin)+"%"+str(throttle))


            if newfile == 1:
                newDur = "0"
                lastSeen = str(nowEpoch)
                if debug == 1:
                    print("\nnew status file created\n")
            else:
                lastSeen = str(logEpoch)
                if OKstatus == 1:
                    newDur = "0"
            if alert == 1:
                OKstatus = 0
            if alert == 0:
                notifyMin = 0
            else:
                notifyMin = notifyMin + 1
                
            output = '{"lastSeen":"'+str(lastSeen)+'","OKstatus":"'+str(OKstatus)+'","duration":"'+str(newDur)+'","lastTemp":"'+str(finalTemp)+'","minsSinceLastLog":"'+str(minsSinceLastLog)+'","locationName":"'+str(location)+'","notifyMin":"'+str(notifyMin)+'" }'
            if enabled == "yes":
                print(output)
                f = open(statusFile, "w")
                f.write(output)
                f.close()
            else:
                print("Location <"+str(location)+"> disabled in config")
            
            # clear data log and add the last event
            f = open(logfile, "w")
            f.write(lastEvent)
            f.close()
        else:
            print("config: "+tmplist[g]+" is disabled, skipping.")

        if alert == 1 and enabled == "yes" and ON == 1 and test == "0":
            if int(notifyMin) % int(throttle) == 0:
                thisMsg = EmailMessage()
                thisMsg.set_content(body)
                thisMsg['Subject'] = subject
                thisMsg['From'] = "alert@temperatureMon.org"
                thisMsg['To'] = dests
                try:
                    msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, thisMsg)
                except Exception as e: 
                    print(e)
                else:
                    print("Sent email to: "+str(dests))
                # send sms if available
                if sid != "" and twilioToken != "":
                    url='https://api.twilio.com/2010-04-01/Accounts/'+str(twilioAcctID)+'/Messages.json'
                    cmd='curl -X POST "'+str(url)+'" --data-urlencode "Body='+str(body)+'" --data-urlencode "From='+str(twilioFromNumber)+'" --data-urlencode "To='+str(destSMS)+'" -u '+str(twilioAcctID)+':'+str(twilioToken)
                    try:
                        response = str(os.system(cmd))
                        if debug == 1:
                            print("SMS response: \n",response)
                    except Exception as e: 
                        print(e)
            else:
                print("throttling notifications to every "+str(throttle)+" minutes")

        if test == 1 and enabled == "yes" and ON == 1 :
            body = "This is a forced test of the notifications."
            subject = "Test message from temperaure monitor"
            thisMsg = EmailMessage()
            thisMsg.set_content(body)
            thisMsg['Subject'] = subject
            thisMsg['From'] = "alert@temperatureMon.org"
            thisMsg['To'] = dests
            try:
                msg(SMTPserver, SMTPport, SMTPuser, SMTPpass, thisMsg)
            except Exception as e: 
                print(e)
            else:
                print("Sent TEST email to: "+str(dests))
            # send sms if available
            if sid != "" and twilioToken != "":
                url='https://api.twilio.com/2010-04-01/Accounts/'+str(twilioAcctID)+'/Messages.json'
                cmd='curl -s -X POST "'+str(url)+'" --data-urlencode "Body='+str(body)+'" --data-urlencode "From='+str(twilioFromNumber)+'" --data-urlencode "To='+str(destSMS)+'" -u '+str(twilioAcctID)+':'+str(twilioToken)
                try:
                    response = str(subprocess.check_output(cmd, shell=True))
                    if debug == 1:
                        print("SMS response: \n",response)
                    print("Send SMS to "+destSMS+"")
                except Exception as e: 
                    print(e)
        if test == 1 and enabled == "yes" and ON == 0:
            print("The Switch is OFF.  You need to turn the witch to ON to enable notifications.")
    g = g + 1

if ON == 0:
    sys.exit("\n\n!!!!!!!!!!!!!!!\nDetected OFF switch position.  All notifications are disabled.\n!!!!!!!!!!!!!!!\n")
else:
    sys.exit()
