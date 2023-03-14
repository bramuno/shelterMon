This project uses an ESP32 wifi development board connected to a DS18B20 temperature sensor to constantly send temperature readings to a syslog server on the wireless network.  The syslog server runs a cron script to monitor the termperature and send alerts if sensors have been exceeded the temperature threshold for too long a time period as defined by the user. <br>
<br>
This project is designed to help animal shelters monitor the temperature of various kennels they have to ensure the animals are safe.  You can use this for other reasons but you may need to make some additional adjustments not mentioned here.  There are commerical products that can accomplish the same objective, but none are as affordable as they need to be, especially for animal shelters that have very little money to spare.  <br>
<br>
For example, the best temperature monitor I could find on amazon that could do everything in this project was ~$80 for one unit.  Our shelter has 9 locations to monitor, so already that's several hundred dollars for a non-profit, low-budget animal shelter.  This project reduces costs to ~$20 per location plus the cost of a raspberry pi, or you could use free tier on AWS to skip the raspberry pi.  
<br>
Usage and build instructions are below.  I have written these instructions for people that are not tech savvy.  If you know a tech person, I would recommend getting assistance from that person.  worst case, you can google "hackerspace" or "makerspace" and your city name to locate any possible nearby hackerspace/makerspace.  you can reach out to them to locate someone that can help you with this project.  The hardest part in this project is soldering, so if you can handle that you should be fine.  There are lots of tutorials on youtube to help you learn.<br>
<br>
I welcome others to assist me with this project to improve wherever possible, so if you would like to collboarte and contribute, please drop me a line.  <br>

<h2>Obligatory Disclaimer</h2>
All the advice and instruction given is for EDUCATIONAL PURPOSES ONLY.  While I shouldn't have to say this, I am not responsible for anything you do or destroy or anything else that happens as a result of your efforts.  Nothing is fool-proof so do not trust this or anything as a perfect solution for monitoring temperatures.   If you want a guaranteed solution, you should buy one. I am making this project because I have zero solutions that will do the same thing at an affordable price which is what this project accomplishes.  <br> <br>
ALSO, this project involves some soldering which is recommended to install a physical switch.  I am not responsible for you hurting anyone or burning something to the ground or worse.  If you are not comfortable soldering, you can reach out to your local hackerspace/makerspace for help. <br><br>
Ultimately it is YOUR RESPONSIBILITY to do all the proper research of all the subjects discussed here before attempting anything yourself. <br>
ALSO, this project requires Wi-Fi is available at all of the locations you need to monitor.  So that is something else you will need to ensure is ready before you attempt to start this project. 

<h2>Hardware:</h2>
links provided here are only examples as you can swap out brands as needed to save money as long as the part does what it required, any by all means if you can find it somewhere else then you don't need amazon :)<br>
1 - <a href="https://a.co/d/iUwvwW4" target="_blank">Raspberry Pi</a> or alternative, (potentially optional) see below for more info and cheaper alternatives<br>(make sure it comes with a PROPER power supply or buy one with it)<br>
?? - <a href="https://www.amazon.com/dp/B013GB27HS?ref_=cm_sw_r_cp_ud_dp_G5QE4ZMDYW0S37ADKY5F" target="_blank">DS18B20 Temperature Sensor</a> (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/4bGYlUr" target="_blank">ESP-32 WiFi Development Board</a> (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/buQ9nun" target="_blank">Breakout board</a> for ESP32 (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/6vf3yfr" target="_blank">USB chargers</a> (one for each area you need to monitor) <br>
??- Low voltage wires (cat5 cable works great)<br>
1 - <a href="https://a.co/d/dl4wDO9" target="_blank">(optional) lighted toggle switch 3-pole</a> any style is ok as long as its an 3-pole<br>
1 - <a href="https://a.co/d/bAP9Ayc" target="_blank">(optional) solderable breadboard hat</a><br>
1 - 200ohm resistor (optional) (have to buy a pack, but you may be able to locate a someone that has a few to spare)<br>
1 - basic LED (optional) <br>
1 - tiny flat head screwdriver <br>
1 - <a href="https://a.co/d/0wVyD20" target="_blank">micro SD card</a> (16gb or larger).  Don't go cheap here.  Recommend you buy SanDisk brand.  16gb is plenty of space, you don't need space for this project. The card should come with an micro to standard size adapter.  If it doesn't you will need to get one.  <br>
1 - Soldering Iron kit (an iron with an iron stand and some solder, <a href="https://a.co/d/d0QlyU0" target="_blank">micro cutters</a>, maybe something <a href="https://a.co/d/caBHZSg" target="_blank">like this</a>)<br>
1 - helping hands see <a href="https://www.amazon.com/s?k=helping+hands&i=tools&crid=38J2ATXAPQ9XL&sprefix=helping+hands%2Ctools%2C137&ref=nb_sb_noss_1" target="_blank">this search</a> for examples.  You will need something to hold your items while soldering.<br>
<br> <br>
<u>Optional hardware</u>:<br>
You may need a <a href="https://a.co/d/4wtLp9Z" target="_blank">USB-SD card adapter</a> so you can read/write to the card.  Some laptops have this already so check before ordering. <br><br>
<u>Optional alternative hardware</u>: <br>
If you've never done a project like this and don't have any of the items listed above, here is a starter kit that has the M-F cables, low-voltage wires, a temporary breadbaoard, LEDs and resistors.  <br>
ELEGOO Electronic Fun Kit for Arduino, Respberry Pi https://a.co/d/bWZt9zZ <br>
<br>
Respberry Pi notes & alternatives:<br>
A pi is optional, you can run this on a desktop or server because everything is handled over the Wi-Fi network.  Just edit <b>shelterMon.py</b> and edit <b>useSwitch = 1</b> to <b>useSwitch = 0</b>.  The pi is very useful to create a physical switch to disable alerts. <br>
Right now, rPi's are more expensive than they used to be.  You DO NOT NEED to get the latest rPi.  We bought a rPi version 2 for cheap while the version 4 (latest) was ~$150.  You need version 2 or greater.  <br><br>there are some alternatives you can try to use instead of an actual Pi.  I recommend googling "Raspberry Pi Alternatives" but here are a few that look like they may wor.  Overall, you must find somethign that has the same set of GPIO pins that the rPi has.  Below are some options found on google but I HAVE NOT TESTED THEM AND CANNOT RECOMMEND THESE.<br>
<li><a href="https://a.co/d/6iG05cZ" target="_blank">Libre Computer Board AML-S905X-CC </a></li>
<li><a href="https://a.co/d/2Vu5FYG" target="_blank">Banana Pi</a> (I was not able to get the rPi libraries to work with this board)</li>
<li><a href="https://a.co/d/5vRDpWE" target="_blank">Odroid</a></li>
<br><br>
<h1>Build & Installation Instructions</h1>

<a href="https://youtu.be/UqLbqoWmh2U" target="_blank">supplemental video guide here</a><br>

<h2>Raspberry Pi</h2>
A pi is optional, you can run this on a desktop or server because everything is handled over the Wi-Fi network.   But this script requires a LINUX operating system with python3 installed.  Just edit <b>shelterMon.py</b> and edit <b>useSwitch = 1</b> to <b>useSwitch = 0</b>.  Otherwise, follow these steps to setup the pi. 
<ul>
<li>go to https://www.raspberrypi.com/software/ and download the latest Raspbery Pi system imager tool. </li>
  <li>run the EXE file and install the tool, then run the tool.</li>
  <li>for operating system, choose Raspberry Pi OS (should be the top option). Click STORAGE and locate your USB drive and make sure it's the correct size.  Dont click WRITE just yet</li>
  <li>Click the cog wheel icon to set additional options.</li>
  <li>Set the hostname if you prefer, enable SSH and use password authenticaiton.</li>
  <li>Scroll down and set the initial username and password</li>
  <li>Set the wireless LAN (wifi) information</li>
  <li>Click SAVE</li>
  <li>Now click WRITE</li>
  <li>After it's finished writing the data, you can eject the card and place it in the Raspberry Pi. Don't power on the pi just yet.</li>
  <li>First go find your router.  If you don't already know the admin password, you can check on the router as most modern routers will have that printed somewhere.  </li>
  <li>you will need to <a href="https://www.howtogeek.com/233952/how-to-find-your-routers-ip-address-on-any-computer-smartphone-or-tablet/">find your router's IP address</a></li>
  <li>Once you have the address, put that IP in a browser window to connect to the router.  Login using the admin password.  If you can't find the router password and can't login, you will need to <a href="https://www.hellotech.com/guide/for/how-to-reset-router-and-modem" target="_blank">reset the router</a>.   This can be problematic and requires a network cable so make sure you know what you're doing first.  </li>
  <li>Once logged in, go to the LOGS section (you may need to click ADVANCED if your router has a basic/advanced option) and you should have a log file to watch as it assigns IP addresses to your devices.  Once you have that, power on the rpi. </li>
  <li>Watch the log and look for the IP address given to the rpi. Write down the IP address <u>AND</a> the MAC address for that device, you will need both (example MAC:  ab:00:ef:01:23:45).</li>
  <li>Now you will need to locate the DHCP area and find where you can reserve the DHCP address for your rpi. Check <a href="https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router" target="_blank">this link</a> for an example using a netgead router but you may have to google "dhcp reservation" and your router name/model to find the right guide.</li>
  <li>Once your router has the IP reserved, you are done with the router.   REMEMBER how to get back here because you will need to reserve the IPs for each ESP32 device as well.  More on that later.</li>
  <li>Now that you have the IP address, you can SSH into the rpi.<br>
  <li>if you dont know how to SSH to a device, you can <a href="https://www.putty.org/" target="_blank">download putty</a>.  Click <a href="https://www.ssh.com/academy/ssh/putty/windows" target="_blank">here</a> for a guide on how to use putty for SSH. </li>
  <li>After logging in run these commands: (you can paste copied text into the putty window clicking the putty window with the right mouse button):<br>
  <b>sudo apt-get -y install rsyslog git && sudo cd /home && sudo git clone https://github.com/bramuno/shelterMon.git && sudo cd shelterMon && sudo cp shelter.conf /etc/rsyslog.d/ && nano /etc/rsyslog.d/shelter.conf</b></li>
  <li>Edit the file and use the provided examples and replicate as needed to have one line for each ESP32 sensor you have.  The first section defines the log file location, and the second section ties the log file to the IP address of the sensors.   Update the IP addresses to match the IPs you got earlier for each ESP32 device.    Each line has to be unique so change the 1's and 2's as needed.  If you dont have that many devices, don't worry about the extra lines.    hit CTRL-O and ENTER to save, then CTRL-X to exit. </li>
  <li>now run this command to edit the rsyslog.conf file<br>
  <b>sudo nano /etc/rsyslog.conf</b><br>
  locate <b>module(load="imudp")</b> and remove the # before it. Do the same for next line.  Then change <b>port="514"</b> to <b>port="3333"</b> and use CTRL-O to save and CTRL-X to exit.</li>
  <li>now run this command to check your conf file is correct:<br>
  rsyslogd -f /etc/rsyslog.conf -N1</b><br>
  <li>now run this command to restart rsyslog:<br>
  <b>sudo systemctl restart syslog.socket</b><br>If the command returns nothing, especially no errors, then you are fine.  Otherwise, go back into the file and try to find where the problem is.  syslog won't run if that file isn't perfect.</li>
  <li>Now that syslog is listening we can setup the sensors. </li>


  
  <h2>ESP32 & sensors</h2>
  <li>Pop the ESP32 boards into the breakout boards. Make sure the pins line up by matching the labels.  </li>
  <li>The sensors should have come with 3 cables with a header that conects to the sensor board.  Connect the white header plugs into the sensor boards. </li>
  <li>Now the other end of the cables go to the breakout baord.   The red cable goes to the 3V3 pin, the black cable goes to the GND pin, and the yellow cable goes to P14.</li>
  <li>To power on, connect a micro-usb cable to the ESP32 and connect the other end to a usb charger port (like a cell phone charger) or for now you can use the USB port on your computer. </li>
  <li>read <a href="https://dronebotworkshop.com/esp32-intro/">this guide</a> on getting to know the basics on the ESP32, follow the instructions to setup arduino IDE and pay attention on how to upload code to the board.  It requires you press the reset button just before the board begins uploading, so it may take some practice. </li>
  <li>Now that you are familiar with the ES32, you can upload the code to the board.  See the project repo and look for the file "ESP32.ino".  Open that file and copy the code into the arduino IDE.  Now look for the areas you need to edit.  Look for the comments "user changes here".  Update the SSIDname and SSIDpassword to your wifi SSID name and password, and update the udpAddress to the IP address of the rpi.  Leave the rest unless you know what you are doing. </li>
  <li>Now you need the additional libraries before you upload. Click SKETCH menu and select INCLUDE LIBRARY and then select MANAGE LIBRARIES.  It should open a window to allow you to search for new libraries.  Search for <b>dallas</b> and install <b>DallasTemp by Miles Burton</b>.  Choose the option to INSTALL ALL DEPENDENCIES (otherwise search for <b>OneWire by Jim Studt</b> and install that as well).  You should be good to upload now. 
  </li>
  <li>Make sure your <a href="https://www.arduino.cc/en/software">Arduino IDE</a> settings are as instructed by the ESP32 guide, then click the UPLOAD button.  remember uploading is not that simple for ESP32 so refer back to the previous ESP32 guide and remember you need to hold the reset button on the ESP32 then wait for the arduino output to say "uploading..." and then release the button.  it may take a few tries to get it right.</li>
  <li>Repeat the upload process as needed if you have more sensors.</li>
  <li>Once all the sensors are have the wifi code uploaded, you need to reserve the IP address for each device.  Go back to the router's DHCP reservation area and then restart the ESP32 devices.  When the devices restart, they should ask the router for an IP address and the router will respond.  Once you have the IP and MAC addresses, go back to the DHCP reservation area in the router to reserve each device.   Then be sure to label each ESP32 (use the bottom side of the breakout board).  </li>


  
<h2>Email user account</h2>
  <li>If you are using your gmail/google account, you can follow <a href="https://support.google.com/accounts/answer/185833?hl=en">this guide</a> to setup your google account information. Don't use your normal gmail password. </li>
  <li>If you are using something else, then you will need to locate your mail server inforamtion.  You can ask your IT person if you have one, or you can google "smtp server" and the name of your mail provider (eg "smtp server yahoo).  But you will have to check their documentation if it doesnt work as you may need to create an app password similar to the gmail procedure. </li>
  <li>save the username, password and server address and server port as you will need that later. </li>


  <h2>Breadboard Hat (optional)</h2>
  The breadboard hat provides a physical switch to enable/disable the monitor and also an LED that indicates the position of the switch.  <br>
  <img src="https://raw.githubusercontent.com/bramuno/shelterMonitor/main/breadboardHatDone.jpg" width="200"><br>
  Please refer to the images for the <a href="https://raw.githubusercontent.com/bramuno/shelterMonitor/main/breadboardHat.jpg">soldering connections</a> and the video for help with the soldering details.  Otherwise, I suggest you locate someone that knows how to solder or you can reach our to your local hackerspace/makerspace.  If this is your only project you plan to make, then it would be better to lean on some help instead of buying a soldering station.<br>Again, this step is optional as you don't NEED a switch to allow this to read temperatures and send alerts.  However, if there is a problem and the tech person isn't available to disable the alerts, then you could end up sending a lot of emails and SMS messages, which as mentioned in the SMS section below could lead to an expensive scenario.  <br>There are also other ways to make this switch that are more simple and less shiny.  It really doesn't matter as long as it works.  The LED design allows for non-techy people to flip the switch and show an indicator that the switch is on the OFF position.<br><br>
  
<h2>Python Script</h2>
  <li>On the rPi, run this command:<br><b>sudo nano /home/shelterMon/config.json</b></li>
  <li>When nano opens the file, use the information below to configure your devices:
 <ul> 
<li>"enable":"1",                     <-- use 1 to enable, 0 to disable checks for this location</li>
<li>"logfileName":"sensor1.log",      <-- Make sure the <b>logfileName</b> matches the file name as mentioned in the syslog.conf file you created earlier </li>
<li>"locationName":"Kennels",  <-- Change this value to the name of the Shelter or the location name where the sensor has been placed </li>
<li>"maxTemp":"95",                   <-- Change this to your maximum allowed temperature </li>
<li>"minTemp":"50",                   <-- Change this to your minimum required temperature  </li>
<li>"maxDuration":"20"                <-- Set this value to the longest time a bad result is tolerable until it should send a notification alert</li>
<li>"tempUnit":"F",                   <-- Change this to either C for Celcius or F for Farenheit</li>
<li>"emailDestination":"dest.email@gmail.com",  <-- Change this to your desired email destination where alerts should be sent.  Use commas to separate multiple email addresses.</li>
<li>"destSMS":"+15551234567"</li>     <-- set this value to the destination phone number to receive SMS alerts.  Use a comma to separate multiple numbers.  If not using SMS alerts, leave the value blank. (empty quotes "" ).  </li>
<li>"throttle":"20"                   <-- set the number of minutes to wait between sending alert notifications</li>
<li>"checkASM":" no"                  <-- enable/disable the use of ASM (see further instructions below)</li>
<li>"locationID":"1"                  <-- set the locatioID as found in ASM</li>
<li>"locationUnit":"nameHere"         <-- set the locationUnit name as found in ASM </li>
<li></li>
 </ul> 
 </li>
 <li>Repeat the above process for all the sensors your have installed.  Name each file to describe it's location and follow with <b>.json</b> (eg.  kennels.json)</li>
 <li>Now edit the <b>email.json</b> file to update your SMTP server settings
  <ul>
<li>"SMTPuser":"SMTPuserNameHere",    <-- Change this to your SMTP username from the email section </li>
<li>"SMTPpass":"SMTPpasswordHere",    <-- Change this to your SMTP password from the email section </li>
<li>"SMTPserver":"smtp.gmail.com",    <-- Chnage this to your SMTP server address from the email section  </li>
<li>"SMTPport":"465",            <-- Change this to your< SMTP server's destination port from the email section  </li></ul>
<li>hit CTRL-O and ENTER to save, then CTRL-X to exit.</li>
<li>The sms.json is remaining but that is optional and will be addressed later in this guide.</li>
  <li>Now test each config by running the command:<br>
  <b>python3 /home/shelterMon/shelterMon.py -C CONFIGFOLDER</b>
  <br>where CONFIGFOLDER is the full path of the folder that contains the json config files you just created.  It should be <b>/home/shelterMon</b><br>
  Example:<br><b>python /home/shelterMon/shelterMon.py -C /home/shelterMon/ -d yes </b></li>
    <li>If the test is successful you will not get any errors.  If the breadboard hat is working correctly, you should get a message that states the switch is OFF and the script will quit.  When in the ON position, the script should finish without errors.  Refer to the video for a demonstration.</li>
<li>Now we need to tell the server to run that command by itself every minute.<br>
Run this command: (if it prompts for an editor, choose NANO) <br>
<b>crontab -e</b></li>
  <li>Now paste the following line into the nano editor:<br>
  <b>* * * * * sudo python /home/shelterMon/shelterMon.py -C /home/shelterMon/ > /dev/null 2>&1</b></li>
  <li>Use CTRL-O & ENTER to save then CTRL-X to quit</li>
  <li>Now you are ready to start testing the system is doing what it should be doing.  Use whatever you can to test the sensor's temperature readings (hairdryer, freezer, etc).  <br>Turn off the sensor's power supply but leave the Raspberry Pi running.  It should notify you the sensor is offline.<br>Keep the ESP32 powered on but disconenct the sensor from the ESP32, you should get a notification the sensor is not reading correctly within 5 minutes. <br> </li>
  <li>Now you just need to place the sensor(s) where they need to go and use a USB charge adapter to power the sensor unit.  the unit needs to be in a place where it can communicate with the WiFi.  Also keep in mind the sensor should not be too high up since warm air rises.  so a more accurate temperature reading that reflects what the animals will be feeling is going to be when the sensor is closer to their level.  </li>
</ul>
<h1>SMS (optional)</h1>
SMS alerts are an optional feature to send alert notifications via SMS to a mobile device.  This can be useful as many people don't check their email all day long. This is one method and requires a subscription that costs money.  It's cheap but a bug in the code could cause too many alerts to be sent and could accidentally rack up charges fast.  So be warned. <br><br>
As an alternative you send text to a specific mobile carrier's desginated domain like "vtext.com".  Here is an <a href='https://www.verizon.com/about/news/vzw/2013/06/computer-to-phone-text-messaging'>example article</a>. HOWEVER be warned as I tested this thoroughly for this project before going with Twilio.   I can only speak for Verizon as thats all i could test since that's ny carrier, so maybe the other carriers are better in some areas.   <br>But Verizon SERIOUSLY THROTTLES the messages sent to vtext.com.   In my testing  on several different days, I sent more than ~10 mesages in a short amount of time, and Verizon stopped delivering those messages. I later got some emails saying the message I sent hours ago has been delayed and not delivered yet.  That was a very reliable problem and it's why I don't recommend using it as a permanent solution.  <br><br>
Use the below steps to create and use a Twilio account. These instructions are likely to get depreacted as their website and protocols mentioned below may change over time.  So you will have to do your best to do what is needed to get the necessary information.  At the time this was written, you can rent a phone number from Twilio for ~$2/month.
<li>Go to https://www.twilio.com/ and register for an account, then login. </li>
<li>Buy a phone number (you get one free if you are doing the free trial)</li>
<li>on the left menu, click MESSAGING and click SERVICES.</li>
<li>Click CREATE MESSAGING SERVICE, give it a quick name and click NEXT</li>
<li>skip the rest by clicking SKIP SETUP</li>
<li>When it loads the list of services, click the service you just created to open it again.</li>
<li>Click SENDER POOL then click ADD SENDERS</li>
<li>Select PHONE NUMBER as the sender type, then search for the number you got earlier.  Select your number from the list and click  ADD PHONE NUMBERS.   Your number should now be found in the SENDER POOL.  </li>
<li>On the left menu, click on PROPERTIES and you shold find you Service ID.  Copy that to notepad for later. </li>
<li>Upper right corner, click ACCOUNT and select API KEYS & TOKENS.  Scroll down to AUTH TOKENS.   Copy your Account ID and your primary token values. </li>
<li>You now have enough info to use the service.  Now edit the sms.json file in your folder. </li>
<ul>
<li>"twilioServiceID":"ABC123"         <-- this is your Service ID</li>
<li>"twilioAcctID":"DEF123"            <-- This is your Account ID</li>
<li>"twilioFromNumber":"+15551234567"  <-- This is your twilio phone number </li>
<li>"twilioToken":"AAABBBCCC"          <-- This is your Auth Token </li></ul>
<li>Save the file and exit the editor.  remember to validate the json code.</li>
<li>Now just ensure you have a destination SMS number specified in each location's .json file.  </li>
<li>You can test the notifications (email and SMS) by running the following command:<br>
<b>python3 /home/shelterMon/shelterMon.py -C /home/shelterMon -t yes</b></li>

<h1>Troubleshooting</h1>
<li><b>Syslog problems</b><br>
to run rsyslog in debug mode, stop the syslog service with:<br>
<b>systemctl stop rsyslog.socket</b><br>
then run the service in the foreground with:<br>
<b>/sbin/rsyslogd -dn</b></li>
<li><b>readTime = chk[0]+" "+chk[1]+" "+chk[2]<br>
  IndexError: list index out of range</b><br>
These two above lines typically indicate a problem loading the log file created by the syslog service.  Check the config.json file(s) to make sure the file name matches the file created by the syslog service.  Also make sure the file exists and the syslog service is writing to the file.<br>
</li>
<li><b>Config.json load failed.</b><br>
this message typically means there is a parsing error on the config.json file, or the json files does not exist.  This will happen if there is an extra comma, or unbalanced quotes, etc.  the JSON format must be perfect , so if you can't figure it out just go back to the default config.json file provided in the github repo and paste it into your file again.  you can also google for an online json validator to help you find the error in the json code.</li>



<h1>EXTRA OPTIONS</h1>

<h2>ASM connectivity</h2>
Since this script is made for animal rescue shelters, I added a feature to incorporate sheltermanager.com with the temperature checks.   In our example, most of our sensor locations are all indoors and 99% of the time they are fully occupied.  So there is no question to monitor those locations.  However, we also have some sheds built outside with A/C meant for quarantining sick animals.   These locations aren't typically occupied so if we need them monitored we would have to manually enable/disable those locations every time they are used or cleared, or we can rely on our shelter management software to do it for us.  There are other shelter manager platforms out there, but ours is ASM so thats what I wrote it for.    If you use something else, you can alsways modify the script if you know what you are doing.  <br>
<br>
So the script contacts ASM and grabs some data that holds the occupancy data for those outdoor locations.  with that, the script can enable/disable the checks on those locations.  Thus if the temperature is too high/low for that location but there is no animal using it, then there is no need to send an alert.  This makes things much easier for us so we don't have to worry about enabling/disabling the checks.<br>
<br>
If you are using ASM, you can follow these steps to use it with the script. <br>
<ul>
<li>In ASM, first create a new USER ROLE.  ONLY give that new role permissions to VIEW REPORTS, nothing else. </li>
<li>Next create a new USER ACCOUNT and grant that user the new role you just created. </li>
<li>Now you need to create a new REPORT.  Go to SETTINGS > REPORTS and creata a new report. Name it whatever you want but place it in a container that you are sure no one will accidently delete or mess with.  I advise not using spaces in the title. <br>
Grant the new role to the new report.  Paste the below text into the SQL box:
 <blockquote>SELECT a.animalName,a.SHELTERLOCATIONUNIT,a.ShelterLocation,
CASE WHEN a.ActiveMovementType = 2 THEN 'Foster' WHEN a.ActiveMovementType = 8 THEN 'Retailer' WHEN a.ActiveMovementType = 1 THEN 'Trial Adoption' 
ELSE i.LocationName END AS LocationName
FROM animal a
LEFT OUTER JOIN animaltype t ON t.ID = a.AnimalTypeID
LEFT OUTER JOIN species s ON s.ID = a.SpeciesID
LEFT OUTER JOIN lksex sx ON sx.ID = a.Sex
LEFT OUTER JOIN internallocation i ON i.ID = a.ShelterLocation
WHERE a.Archived = 0 and a.ShelterLocation = 1111
ORDER BY a.ShelterLocation, SHELTERLOCATIONUNIT</blockquote>
</li>
  <li>Here you need to figure out the numerical location ID of the location found in ASM.  If you click on SHELTER VIEW and then click on that specifc location, it will bring up the animals in that location.  in the URL address bar, you will see the numerical value of that location ID after "shelterlocation".  (eg.  https://us000.sheltermanager.com/animal_find_results?logicallocation=onshelter&shelterlocation=123456) </li>
  <li>Take that number of your location and replace with the number found in the above SQL query <b>a.ShelterLocation = 18</b>.  Replace the "1111" with your number.</li>
<li>If you have more than one location that needs to be included in the report, then you are going to have to figure out how to get the report to include all the locationd and units you require.</li>
<li>Now hit the SQL check button and then hit the button to generate the HTML.  If no errors, click SAVE</li>
<li>Check the report is working using the REPORTS menu.  When the report opens in the browser, look at the URL address bar.  the <b>report ID number</b> will be in the address. You will need that below.  (eg.  https://us000.sheltermanager.com/report?id=1234567890)</li>
<li>Now on your pi or server, run this command:<br><b>nano /home/shelterMon/asm.json</b></li>
<li>Add the information the file is asking for and save then exit.<br>
Account - your ASM account number<br>
Username - the new user account you created above  <br>
Password - the passwrd for the new user account you created above<br>
Title - the title of the report you created above. If the name has any spaces, replace the space character with + (eg "Spaces+are+Fun) <br></li>
<li>Now edit the .json config file for the location(s) you need to check against ASM.<br><b>nano /home/shelterMon/config.json</b></li>
<li>Towards the end of the file you will see these three fields.  Edit them as needed, then save and exit. <br>
checkASM -set this option to "yes" to enable checks against ASM<br>
locationID - this is the numeric report ID of the report you created earlier. <br>
locationUnit - this is the label/name of that unit found within the location in ASM.  This is custom to what your org has labeled it in ASM, so be sure it matches exactly including whitespace characters. We use numbers for our units, but some are words.  <br></li>
<li>Now you can do a test run of the script and check for errors.  As long as the location's config file has the checkASM value enabled and the asm.json file has all the required info, it should run the check against ASM to look for occupancy. </li>
</ul>

<h2>Free AWS server hosting</h2>
I'm not going to go into detail on how to do this, but instead of buying a physical machine or raspberry pi to act as the server, you could actually use AWS or Azure's FREE TIER of servers.  Granted they are SUPER WEAK but that should be ok since the amount of work they have to do is minimal.  So if you create a free account in AWS/Azure you can look for the VM's that are labeled as "free".  They really are free but other things are not so be sure to google how to check for any costs you have accumulated and make adjustments as needed.  <br>
<br>
Once you have that server running you may need to do some additional work on your network but if you're using a basic home router setup you should be fine.  in this case I would recommend getting help from an IT nerd so you do it correctly.  the ESP sensors will just use your local WIFI to send the temperature readings to an internet address instead of a local address. You would also have to open up the firewall to accept traffic from your source IP using the destination port 3333 or whatever you set that port to use.<br>

<h1>Example output</h1>
Below is the example output of what the script does at our location.  Quarantine shed #2 is occupied, but the others are not.  All the sheds are checking against ASM for occupancy but the other locations are not because they are never empty.

<blockquote>root@server# python3 /home/shelterMon/shelterMon.py -C /home/shelterMon/<br>
{"lastSeen":"1678240977","OKstatus":"1","duration":"0","lastTemp":"71.8","minsSinceLastLog":"0.1","locationName":"Cats Area","notifyMin":"0","diffChange":"0" }<br>
{"lastSeen":"1678240980","OKstatus":"1","duration":"0","lastTemp":"70.2","minsSinceLastLog":"0.0","locationName":"Clinic room","notifyMin":"0","diffChange":"0" }<br>
{"lastSeen":"1678240976","OKstatus":"1","duration":"0","lastTemp":"74.1","minsSinceLastLog":"0.1","locationName":"Clean Room","notifyMin":"0","diffChange":"0" }<br>
{"lastSeen":"1678240979","OKstatus":"1","duration":"0","lastTemp":"77.2","minsSinceLastLog":"0.0","locationName":"Foster Room","notifyMin":"0","diffChange":"0" }<br>
{"lastSeen":"1678240976","OKstatus":"1","duration":"0","lastTemp":"74.0","minsSinceLastLog":"0.1","locationName":"Dog Kennels","notifyMin":"0","diffChange":"0" }<br>
Quarantine Room 1 is NOT occupied.  Disabling.<br>
config: /home/shelterMon/quaran1.json is disabled, skipping.<br>
Quarantine Room 2 is occupied.  Enabling.<br>
{"lastSeen":"1678240979","OKstatus":"1","duration":"0","lastTemp":"73.2","minsSinceLastLog":"0.0","locationName":"Quarantine Room 2","notifyMin":"0","diffChange":"0" }<br>
Quarantine Room 3 is NOT occupied.  Disabling.<br>
config: /home/shelterMon/quaran3.json is disabled, skipping.<br>
Quarantine Room 4 is NOT occupied.  Disabling.<br>
config: /home/shelterMon/quaran4.json is disabled, skipping.
</blockquote>
