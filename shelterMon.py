# sudo apt install rsyslog
## version notes:
## this script will look for .json config files stored in the path passed by -C option
## to disable a shelter/location sensor, just rename the .json file to something without .json (eg.  file.save)
## usage: python3 shelterMon.py -C /path/to/folder
## debug usage: python3 shelterMon.py -C /path/to/folder -d yes
## alert test usage: python3 shelterMon.py -C /path/to/folder -t yes
#
# change the 'useSwitch' option to 0 if you are not using a raspberry pi or other device with GPIO pins
useSwitch = 1
# change the 'useASM' option to 1 if you intend to link your script to ASM
useASM = 0
#
debug = 0
test = 0
import os, sys, json, subprocess, smtplib, datetime, time, os.path, pdb, argparse, glob, requests
from email.message import EmailMessage
from os.path import exists
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
if useSwitch == 1:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if int(GPIO.input(17)) == 0:
        ON = 0
    else:
        ON = 1
    if args.test:
        test = str(args.test.lower())
        if test == "1" or test == 1 or test == "true" or test == "yes":
            test = 1
            print("\n\n TESTING NOTIFICATIONS ENABLED\n\n")
else:
    ON = 1  ## default ON when no switch in use

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
tmplist = sorted(tmplist)
list = []

configFolder = str(args.config)
emailFile = configFolder+"/email.json"
emailFile = emailFile.replace("//","/")

try:
    f = open(emailFile, "r")
    get = json.load(f)
    f.close()
    SMTPuser =  get['SMTPuser']
    SMTPpass =  get['SMTPpass']
    SMTPserver =  get['SMTPserver']
    SMTPport =  int(get['SMTPport'])
except:
    sys.exit("failed to load "+str(emailFile)+" \n")


smsFile = configFolder+"/sms.json"
smsFile = smsFile.replace("//","/")
asmFile = configFolder+"/asm.json"
asmFile = asmFile.replace("//","/")
if os.path.exists(smsFile):
    try:
        f = open(smsFile, "r")
        getSMS = json.load(f)
        f.close()
        sid =  str(getSMS['twilioServiceID'])
        twilioToken =  str(getSMS['twilioToken'])
        twilioAcctID =  str(getSMS['twilioAcctID'])
        twilioFromNumber =  str(getSMS['twilioFromNumber'])
    except:
        sys.exit("failed to load values from '"+str(smsFile)+"'.  Check the json syntax is correct.\n")
else:
    sid = ""
    twilioToken = ""
    twilioAcctID = ""
    twilioFromNumber = ""

if os.path.exists(asmFile):
    try:
        f = open(asmFile, "r")
        getASM = json.load(f)
        f.close()
        ASMacct =  str(getASM['account'])
        ASMuser =  str(getASM['username'])
        ASMpass =  str(getASM['password'])
        ASMtitle =  str(getASM['title'])
    except:
        sys.exit("failed to load values from '"+str(asmFile)+"'.  Check the json syntax is correct.\n")
else:
    ASMacct = ""
    ASMuser = ""
    ASMpass = ""
    ASMtitle = ""

reportData = ""
ASMok = 0
if ASMacct != "" and ASMuser != "" and ASMpass != "" and ASMtitle != "":
    ASMok = 1
    URL = 'https://service.sheltermanager.com/asmservice'
    PARAMS = {'username':ASMuser, 'password': ASMpass, 'account':ASMacct, 'title':ASMtitle, 'method':'json_report'}
    if debug == 1:
        print("getting ASM data via API...")
    try:
        req = requests.get(url = URL, params = PARAMS)
        req.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    reportData = req.json()

diffChange = 5
g = 0
# begin loop
while g < len(tmplist):
    occupied = 0
    notifyMin = -1
    alert = 0
    lastSeen = 0
    if tmplist[g] != str(emailFile) and tmplist[g] != str(smsFile) and tmplist[g] != str(asmFile):
        if debug == 1:
            print("\nstarting: "+str(tmplist[g]))
        try:
            f = open(tmplist[g], "r")
            get = json.load(f)
            f.close()
            enabled = str(get['enabled']).lower()
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
            sendSMS = destSMS.split(",")
            throttle =  str(get['throttle'])
            checkASM =  str(get['checkASM']).lower()
            locationID =  str(get['locationID'])
            locationUnit =  str(get['locationUnit'])
        except Exception as e:
            print(e)
            sys.exit("\njson config  load fail.  --> "+str(tmplist[g])+"\n")

        #
        newfile = 0
        logfile = folderName+"/"+logfileName
        statusFile = folderName+"/"+statusFileName

        ## check ASM for current occupancy and update json conifg file
        if ASMok == 1 and checkASM == "yes":
            d = 0
            while d<len(reportData):
                locID = str(reportData[d]['SHELTERLOCATION'])
                locUnit = str(reportData[d]['SHELTERLOCATIONUNIT'])
                if locID == locationID and locUnit == locationUnit:
                    if debug == 1:
                        print("matched "+str(tmplist[g])+" with locationID: '"+str(locationID)+"', Unit: '"+str(locationUnit)+"'")
                    occupied = 1
                    break
                d=d+1
            if occupied == 1:
                ## update config file to enable the sensor checks
                get['enabled']="yes"
                print(str(location)+" is occupied.  Enabling.")
            else:
                get['enabled']="no"
                print(str(location)+" is NOT occupied.  Disabling.")
            try:
                ff = open(tmplist[g], "w")
                ff.write(json.dumps(get, indent=1))
                ff.close()
            except Exception as e:
                print(e)
                print("\nFailed to update "+str(tmplist[g]))
        else:
            if debug == 1:
                print("Check of ASM is disabled or asm.json file is missing/incomplete. skipping...")
        #
        enabled = get['enabled']
        if enabled == "no":
            print("config: "+tmplist[g]+" is disabled, skipping.")
        else:
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
                    lastTemp = float(get['lastTemp'])
                    newfile = 0
                    notifyMin = int(get['notifyMin'])
                    diffChange = int(get['diffChange'])
                except:
                    print("status file load fail")
            except:
                get = ""
                oldOKstatus =  ""
                oldDur = ""
                lastSeen = 0
                lastTemp = 0
                dur = 0
                diffChange = 0
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
            if tempUnit == "C" or tempUnit == "c":
                finalTemp = tempC
            else:
                finalTemp = str(round(float(finalTemp),1))
            if ( float(finalTemp) > float(maxTemp) ) or ( float(finalTemp) < float(minTemp) )  :
                OKstatus = 0

            ## check for a frozen sensor
            if lastTemp == finalTemp:
                diffChange = diffChange + 1
            else:
                diffChange = 0

            if int(OKstatus) == 1:
                newDur = round(diffMins, 1)
            else:
                newDur = round((oldDur + diffMins), 1)

            if debug == 1:
                print("oldOKstatus = "+str(oldOKstatus))
                print("oldDur = "+str(oldDur))
                print("maxTemp = "+str(maxTemp)+str(tempUnit))
                print("minTemp = "+str(minTemp)+str(tempUnit))
                print("new reading = ",str(finalTemp))
                print("lastTemp = ",str(lastTemp))
                print("maxDuration = ",str(maxDuration))
                print("statusFile = ",str(statusFile))
                print("newfile = ",str(newfile))
                print("enabled = ",str(enabled))
                print("test = ",str(test))

            ########## offline sensor alert (every 5m on the 5th minute)
            if round(minsSinceLastLog,0) > 5 or round(minsSinceLastLog,0) < 0:
                body = "No contact from temperature '"+str(location)+"' sensor in "+str(minsSinceLastLog)+" minutes.\nPlease verify it is online and power cycle if needed.\n"
                subject = "Temperature sensor offline"
                alert = 1
            ########## critical temperature alert begin
            if ( int(OKstatus) == 0 and float(oldDur) > float(maxDuration) ) :
                alert = 1
                body = str(location)+" is reading '"+str(finalTemp)+str(tempUnit)+"' degree temperature.  This location has been below the max temperature of "+str(maxTemp)+" for at least "+str(oldDur)+" minutes!\n"
                subject = str(location)+" sensor at '"+str(finalTemp)+str(tempUnit)+"'"
            ########## alert sensor online but reading incorrectly
            if ( float(finalTemp) < -40.0 ) :
                alert = 1
                body = "\nSensor "+str(location)+" is not reading correctly:\n\nLatest reading at: "+str(float(finalTemp))+"\n\nThis typically happens when one of the three wires connecting to the ESP device is disconnected or loose. \nPlease check the connection or power cycle the device.\n"
                subject = str(location)+" Sensor problem"
            ######### sensor is frozen (for at least 24h)
            if ( int(diffChange) > 1440 ) :
                alert = 1
                OKstatus = 0
                body = "\nSensor "+str(location)+" has stopped reading.  Temeperature has not changed from "+str(float(finalTemp))+str(tempUnit)+" in over "+str(diffChange)+" minutes.\nPlease reboot the ESP device\n"
                subject = str(location)+" sensor problem"
            ########## end alerts
            if int(notifyMin) % int(throttle) == 0 :
                go = " - should send alert "
            else:
                go = " - should not send alert"
            if debug == 1:
                print("OKstatus = ",str(OKstatus))
                print("nowEpoch = ",str(nowEpoch))
                print("oldLastSeen = ",str(lastSeen))
                print("logEpoch = ",str(logEpoch))
                print("diffEpoch = ",str(diffEpoch))
                print("diffMins = ",str(diffMins))
                print("newDur = ",str(newDur))
                print("minsSinceLastLog = ",str(minsSinceLastLog))
                print("diffChange = ",str(diffChange))
                print("thisMinute = ",str(minute))
                print("switchCheck = ",str(GPIO.input(17)))
                print("alert = ",str(alert))
                print("logfile = ",str(logfile))
                print("ON = ",str(ON))
                print("test = ",str(test))
                print("notifyMin = ",str(notifyMin))
                print("notify = "+str(notifyMin)+"%"+str(throttle)+str(go)  )
                print("sid = ",str(sid))
                print("twilioAcctID = ",str(twilioAcctID))
                print("twilioFromNumber = ",str(twilioFromNumber))
                print("twilioToken = ",str(twilioToken))
                print("sendSMS = ",str(sendSMS))
                print("\n")

            if alert == 1 and debug == 1:
                print("body = ",str(body))
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
                
            output = '{"lastSeen":"'+str(lastSeen)+'","OKstatus":"'+str(OKstatus)+'","duration":"'+str(newDur)+'","lastTemp":"'+str(finalTemp)+'","minsSinceLastLog":"'+str(minsSinceLastLog)+'","locationName":"'+str(location)+'","notifyMin":"'+str(notifyMin)+'","diffChange":"'+str(diffChange)+'" }'
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

        if (alert == 1 and enabled == "yes" and ON == 1 and test == 0):
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
                    aa = 0
                    while aa < len(sendSMS):
                        url='https://api.twilio.com/2010-04-01/Accounts/'+str(twilioAcctID)+'/Messages.json'
                        cmd='curl -X POST "'+str(url)+'" --data-urlencode "Body='+str(body)+'" --data-urlencode "From='+str(twilioFromNumber)+'" --data-urlencode "To='+str(sendSMS[aa])+'" -u '+str(twilioAcctID)+':'+str(twilioToken)
                        try:
                            response = str(os.system(cmd))
                            if debug == 1:
                                print("SMS response: \n",response)
                        except Exception as e: 
                            print(e)
                        aa = aa + 1
                now = datetime.datetime.now()
                alertFile = "/home/shelterMon/alerts.txt"
                if os.path.exists(alertFile):
                    j = open(alertFile, "a")
                else:
                    j = open(alertFile, "x")
                j.write(str(now)+",DestEmail='"+str(dests)+"',Message='"+str(thisMsg)+"'\n"+str(now)+",DestSMS='"+str(destSMS)+",SMSResponse='"+str(response)+"'\n")
                j.close()
            else:
                print("throttling notifications to every "+str(throttle)+" minutes")

        if test == 1 and enabled == "yes" and ON == 1 :
            if os.path.exists(alertFile):
                j = open(alertFile, "a")
            else:
                j = open(alertFile, "x")
            body = "This is a forced test of the notifications."
            subject = "Test message from temperaure monitor "+str(location)
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
                x=0
                smslist=destSMS.split(",")
                while x < len(smslist):
                    destSMS = str(smslist[x])
                    url='https://api.twilio.com/2010-04-01/Accounts/'+str(twilioAcctID)+'/Messages.json'
                    cmd='curl -s -X POST "'+str(url)+'" --data-urlencode "Body='+str(body)+'" --data-urlencode "From='+str(twilioFromNumber)+'" --data-urlencode "To='+str(destSMS)+'" -u '+str(twilioAcctID)+':'+str(twilioToken)
                    try:
                        response = str(subprocess.check_output(cmd, shell=True))
                        if debug == 1:
                            print("SMS response: \n",response)
                        print("Send SMS to "+destSMS+"")
                    except Exception as e: 
                        print(e)
                    x=x+1
                    time.sleep(2)
            now = datetime.datetime.now()
            j.write(str(now)+",DestEmail='"+str(dests)+"',Message='"+str(thisMsg)+"'\n"+str(now)+",DestSMS='"+str(destSMS)+",SMSResponse='"+str(response)+"'\n")
            j.close()
        if test == 1 and enabled == "yes" and ON == 0:
            print("The Switch is OFF.  You need to turn the witch to ON to enable notifications.")
    g = g + 1

if ON == 0:
    sys.exit("\n\n!!!!!!!!!!!!!!!\nDetected OFF switch position.  All notifications are disabled.\n!!!!!!!!!!!!!!!\n")
else:
    sys.exit()
