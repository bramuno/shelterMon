This project is designed to help animal shelters monitor the temperature of various kennels they have to ensure the animals are safe.  You can use this for other reasons but you may need to make some additional adjustments not mentioned here. 

This project uses an ESP32 wifi development board connected to a DS18B20 temperature sensor to constantly send temperature readings to a syslog server on the wireless network.  The syslog server runs a cron script to monitor the termperature and alert the user if both sensors have been exceeded the temperature threshold for too long a time period.   

Usage and build instructions are below.  I have written these instructions for people that are not tech savvy.  If you know a tech person, I would recommend getting assistance from that person.  worst case, you can google "hackerspace" or "makerspace" and your city name to locate any possible nearby hackerspace/makerspace.  you can reach out to them to locate someone that can help you with this project.  The hardest part in this project is soldering, so if you can handle that you should be fine.  There are lots of tutorials on youtube to help you learn.

I welcome others to assist me with this project to improve wherever possible, so if you would like to collboarte and contribute, please drop me a line.  

<h2>Obligatory Disclaimer</h2>
All the advice and instruction given is for EDUCATIONAL PURPOSES ONLY.  I am not responsible for anything you do or destroy or anything else that happens as a result of your efforts.  Nothing is fool-proof so do not trust this or anything as a perfect solution for monitoring temperatures.   If you want a guaranteed solution, you should buy one. I am making this project because I have zero solutions that will do the same thing at an affordable price which is what this project accomplishes.   <br>
ALSO, this project involves some soldering which is recommended to install a physical switch.  I am not responsible for hurting yourself or burning something to the ground.  If you are not comfortable soldering, you can reach out to your local hackerspace/makerspace for help. <br>
Ultimately it is YOUR RESPONSIBILITY to do all the proper research of all the subjects discussed here before attempting anything yourself. <br>
ALSO, this projct requires Wi-Fi is available at all of the locations you need to monitor.  So that is something else you will need to ensure is ready before you attempt to start this project. 

<h2>Hardware:</h2>
links provided here are only examples as you can swap out brands as needed to save money as long as the part does what it required, any by all means if you can find it somewhere else then you don't need amazon :)<br>
1 - <a href="https://a.co/d/iUwvwW4" target="_blank">Raspberry Pi</a> or alternative, see below for some cheaper alternatives<br>(make sure it comes with a PROPER power supply or buy one with it)<br>
?? - <a href="https://www.amazon.com/dp/B013GB27HS?ref_=cm_sw_r_cp_ud_dp_G5QE4ZMDYW0S37ADKY5F" target="_blank">DS18B20 Temperature Sensor</a> (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/4bGYlUr" target="_blank">ESP-32 WiFi Development Board</a> (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/buQ9nun" target="_blank">Breakout board</a> for ESP32 (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/6vf3yfr" target="_blank">USB chargers</a> (one for each area you need to monitor) <br>
??- Low voltage wires (cat5 cable works great)<br>
1 - <a href="https://a.co/d/dl4wDO9" target="_blank">lighted toggle switch 3-pole</a> any style is ok as long as its an 3-pole<br>
1 - <a href="https://a.co/d/bAP9Ayc" target="_blank">solderable breadboard hat</a><br>
1 - 200ohm resistor (have to buy a pack, but you may be able to locate a someone that has a few to spare)<br>
1 - basic LED <br>
1 - tiny flat head screwdriver <br>
1 - <a href="https://a.co/d/0wVyD20" target="_blank">micro SD card</a> (16gb or larger).  Don't go cheap here.  Recommend you buy SanDisk brand.  16gb is plenty of space, you don't need space for this project. The card should come with an micro to standard size adapter.  If it doesn't you will need to get one. <br>
1 - Soldering Iron kit (an iron with an iron stand and some solder, <a href="https://a.co/d/d0QlyU0" target="_blank">micro cutters</a>, maybe something <a href="https://a.co/d/caBHZSg" target="_blank">like this</a>)<br>
1 - helping hands see <a href="https://www.amazon.com/s?k=helping+hands&i=tools&crid=38J2ATXAPQ9XL&sprefix=helping+hands%2Ctools%2C137&ref=nb_sb_noss_1" target="_blank">this search</a> for examples.  You will need something to hold your items while soldering.<br>
<br> <br>
<u>Optional hardware</u>:<br>
You may need a <a href="https://a.co/d/4wtLp9Z" target="_blank">USB-SD card adapter</a> so you can read/write to the card.  Some laptops have this already so check before ordering. <br><br>
<u>Optional alternative hardware</u>: <br>
If you've never done a project like this and don't have any of the items listed above, here is a starter kit that has the M-F cables, low-voltage wires, a temporary breadbaoard, LEDs and resistors.  <br>
ELEGOO Electronic Fun Kit for Arduino, Respberry Pi https://a.co/d/bWZt9zZ <br>
<br>
Respberry Pi alternatives:<br>
Right now, rPi's are more expensive than they used to be.  so there are some alternatives you can try to use instead of an actual Pi.  I recommend googling "Raspberry Pi Alternatives" but here are a few that look like they may wor.  Overall, you must find somethign that has the same set of GPIO pins that the rPi has.:<br>
<li><a href="https://a.co/d/6iG05cZ" target="_blank">Libre Computer Board AML-S905X-CC </a></li>
<li><a href="https://a.co/d/2Vu5FYG" target="_blank">Banana Pi</a></li>
<li><a href="https://a.co/d/5vRDpWE" target="_blank">Odroid</a></li>
<br><br>
<h1>Build & Installation Instructions</h1>

<a href="https://youtu.be/UqLbqoWmh2U" target="_blank">supplemental video guide here</a><br>

<h2>Raspberry Pi</h2>
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
  <li>After it's finished writing the data, you can eject the card and place it in the Raspberry Pi. Don't poower on the spi just yet.</li>
  <li>First go find your router.  If you don't already know the admin password, you can check on the router as most modern routers will have that printed somewhere.  </li>
  <li>you will need to <a href="https://www.howtogeek.com/233952/how-to-find-your-routers-ip-address-on-any-computer-smartphone-or-tablet/">find your router's IP address</a></li>
  <li>Once you have the address, put that IP in a browser window to connect to the router.  Login using the admin password.  If you can't find the router password and can't login, you will need to <a href="https://www.hellotech.com/guide/for/how-to-reset-router-and-modem" target="_blank">reset the router</a>.   This can be problematic and requires a netowrk cable so make sure you know what you're doing first.  </li>
  <li>Once logged in, go to the LOGS section (you may need to click ADVANCED if your router has a basic/advanced option) and you should have a log file to watch as it distributes IP addresses.  Once you have that, power on the rpi. </li>
  <li>Watch the log and look for the IP address given to the rpi. Write down the IP address <u>AND</a> the MAC address for that device, you will need both (example MAC:  ab:00:ef:01:23:45).</li>
  <li>Now you need to power on each ESP32 running the code provided earlier.  They will attempt to get an IP address like your rpi.   Write down all IPs and MACs for each device.  </li>
  <li>Now you will need to locate the DHCP area and find where you can reserve the DHCP address for your rpi. Check <a href="https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router" target="_blank">this link</a> for an example using a netgead router but you may have to google "dhcp reservation" and your router name to find the right guide.</li>
  <li>Once your router has the IP reserved, you are done with the router.   REMEMBER how to get back here because you will need to reserve the IPs for each ESP32 device as well.  More on that later.</li>
  <li>Now that you have the IP address, you can SSH into the rpi.<br>
  <li>if you dont know how to SSH to a device, you can <a href="https://www.putty.org/" target="_blank">download putty</a>.  Click <a href="https://www.ssh.com/academy/ssh/putty/windows" target="_blank">here</a> for a guide on how to use putty for SSH. </li>
  <li>After logging in run these commands: (you can paste copied text into the putty window using the right mouse button):<br>
  <b>sudo apt-get -y install rsyslog git && sudo cd /home && sudo git clone https://github.com/bramuno/shelterMonitor.git && sudo mv shelterMonitor/ shelterMon/ && sudo cd /home/shelterMon && nano /etc/rsyslog.d/shelter.conf</b></li>
  <li>Nano will open to a blank page, go to the repo and find the file named "syslog.conf", open it and copy the data.  Then paste the data into the nano window. hit CTRL-O and ENTER to save, then CTRL-X to exit. </li>
  <li>Use the provided examples and duplicate as needed to have one line for each sensor you have.  The first section defines the log file location, and the second section ties the log file to the IP address of the sensors.   Update the IP addresses to match the IPs you got earlier for each ESP32 device.    Each line has to be unique so change the 1's and 2's as needed.  If you dont have that many devices, don't worry about the extra lines.    hit CTRL-O and ENTER to save, then CTRL-X to exit. </li>
  <li>now run this command to edit the rsyslog.conf file<br>
  <b>sudo nano /etc/rsyslog.conf</b><br>
  locate "module(load="imudp")" and remove the # before it. Do the same for next line.  Then change <b>port="514"</b> to <b>port="3333"</b> and use CTRL-O to save and CTRL-X to exit.</li>
  <li>now run this command to check your conf file is correct:<br>
  <br>rsyslogd -f /etc/rsyslog.conf -N1</b><br>
  <li>now run this command to restart rsyslog:<br>
  <b>sudo systemctl restart syslog.socket</b><br>If the command returns nothing, especially no errors, then you are fine.  Otherwise, go back into the file and try to find where the problem is.  syslog won't run if that file isn't perfect.</li>
  <li>Now that syslog is listening make sure your sensors are powered on.  </li>
  <li>The sensors should start sending data to the rpi.  Now we can finish with the rpi.</li>

  
  <h2>ESP32 & sensors</h2>
  <li>Pop the ESP32 boards into the breakout boards. Make sure the pins line up.  </li>
  <li>The sensors should have come with 3 cables with a header that conects to the sensor board.  Connect the cables to the boards. </li>
  <li>Now the other end of the cables go to the breakout baord.   The red cable goes to the 3V3 pin, the black cable goes to the GND pin, and the yellow cable goes to P14.</li>
  <li>To power on, connect a micro-usb cable to the ESP32 and connect the other end to a usb charger port (like a cell phone charger) or for now you can use the USB port on your computer. </li>
  <li>read <a href="https://dronebotworkshop.com/esp32-intro/">this guide</a> on getting to know the basics on the ESP32, follow the instructions to setup arduino IDE and pay attention on how to upload code to the board.  It requires you hold the reset button until the board begins uploading, so it may take some practice. </li>
  <li>Now that you are familiar with the ES32, you can upload the code to the board.  See the project repo and look for the file "ESP32.ino".  Open that file and copy the code into the arduino IDE.  Now look for the areas you need to edit.  Look for the comments "user changes here".  Update the SSIDname and SSIDpassword to your wifi SSID name and password, and update the udpAddress to the IP address of the rpi.  Leave the rest unless you know what you are doing. </li>
  <li>Now you need the additional libraries before you upload. Click SKETCH menu and select INCLUDE LIBRARY and then select MANAGE LIBRARIES.  It should open a window to allow you to search for new libraries.  Search for <b>dallas</b> and install <b>DallasTemp by Miles Burton</b>.  Choose the option to INSTALL ALL DEPENDENCIES (otherwise search for <b>OneWire by Jim Studt</b> and install that as well).  You should be good to upload now. 
  </li>
  <li>Make sure your <a href="https://www.arduino.cc/en/software">Arduino IDE</a> settings are as instructed by the ESP32 guide, then click the UPLOAD button.  remember uploading is not that simple for ESP32 so refer back to the previous ESP32 guide and remember you need to hold the reset button on the ESP32 then wait for the arduino output to say "uploading..." and then release the button.  it may take a few tries to get it right.</li>
  <li>Repeat the upload process as needed if you have more sensors.</li>
  <li>Once all the sensors are working on the network, you need to reserve the IP address for each device.  Go back to the router's DHCP reservation area and then restart the ESP32 devices.  WHen the devices restart, they should as the router for an IP address and the router will respond.  Reserve each device and be sure to label them.  </li>


  
<h2>Email user account</h2>
  <li>If you are using your gmail/google account, you can follow <a href="https://support.google.com/accounts/answer/185833?hl=en">this guide</a> to setup your google account information. Don't use your normal gmail password. </li>
  <li>If you are using something else, then you will need to locate your mail server inforamtion.  You can ask your IT person if you have one, or you can google "smtp server" and the name of your mail provider (eg "smtp server yahoo).  But you will have to check their documentation if it doesnt work as you may need to create an app password similar to the gmail procedure. </li>
  <li>save the username, password and server info as you will need it later. </li>


  <h2>Breadboard Hat</h2>
  The breadboard hat provides a physical switch to enable/disable the monitor and also an LED that indicates the position of the switch.  <br>
  <img src="https://raw.githubusercontent.com/bramuno/shelterMonitor/main/breadboardHatDone.jpg" width="200"><br>
  Please refer to the images for the <a href="https://raw.githubusercontent.com/bramuno/shelterMonitor/main/breadboardHat.jpg">soldering connections</a> and the video for help with the soldering details.  Otherwise, I suggest you locate someone that knows how to solder or you can reach our to your local hackerspace/makerspace.  If this is your only project you plan to make, then it would be better to lean on some help instead of buying a soldering station.<br><br>
  
<h2>Python Script</h2>
  The python script depends on the breadboard hat, so make sure that's working as expected before proceeding or you will likely get lots of email/SMS alerts.<br>
  <li>Run this command:<br><b>sudo mkdir -p  /home/shelterMon && sudo nano /home/shelterMon/shelterMon.py</b></li>
  <li>When nano opens the blank document, go to the repo and look for the "shelterMon.py" file. Open the file and copy the data, then paste it into the nano window.  hit CTRL-O and ENTER to save, then CTRL-X to exit.</li>
  <li>Now run this command:<br><b>sudo nano /home/shelterMon/config.json</b></li>
  <li>When nano opens the blank document, go to the repo and look for the "config.json" file. Open the file and copy the data, then paste it into the nano window. Now update the information to suit your preferences.<br>
 <ul> 
<li>"enable":"1",                     <-- use 1 to enable, 0 to disable checks for this location</li><br>
<li>"folderName":"/home/shelterMon",  <-- leave this as is unless you know what you are doing </li><br>
<li>"logfileName":"sensor1.log",      <-- Make sure the <b>logfileName</b> matches the file name as mentioned in the syslog.conf file you created earlier </li><br>
<li>"locationName":"LocationNameHere",  <-- Change this value to the name of the Shelter or the location name where the sensor has been placed </li><br>
<li>"maxTemp":"95",                   <-- Change this to your maximum allowed temperature </li><br>
<li>"minTemp":"50",                   <-- Change this to your minimum required temperature  </li><br>
<li>"maxDuration":"20"                <-- Set this value to the longest time a bad result is tolderable until it should send a notification alert</li>
<li>"tempUnit":"F",                   <-- Change this to either C for Celcius or F for Farenheit</li> <br></li>
<li>"emailDestination":"dest.email@gmail.com",  <-- Change this to your desired email destination where alerts should be sent</li> <br> 
<li>"destSMS":"+15551234567"</li>     <-- set this value to the destination phone number to receive SMS alerts.  If none, leave the value blank.</li>
<li>"throttle":"20"                   <-- set the number of minutes to wait between sending alert notifications</li>
 <br></ul> 
 </li>    
 <li>Now edit the <b>email.json</b> file to update your SMTP server settings<br>
  <ul>
<li>"SMTPuser":"SMTPuserNameHere",    <-- Change this to your SMTP username from the previous section </li><br>
<li>"SMTPpass":"SMTPpasswordHere",    <-- Change this to your SMTP password from the previous section </li><br>
<li>"SMTPserver":"smtp.gmail.com",    <-- Chnage this to your SMTP server address from the previous section  </li><br>
<li>"SMTPport":"465",            <-- Change this to your< SMTP server's destination port from the previous section  </li></ul><br>
<li>hit CTRL-O and ENTER to save, then CTRL-X to exit.</li>
<li>The sms.json is remaining but that is optional and will be addressed later in this guide.</li>
<li>Restart rsyslog just incase with this command:<br>
<b>sudo systemctl restart rsyslog</b></li>
  <li>Repeat the previous step for all the sensors you have, and be sure to name the file with a unique name each time (eg, change config1.json to config.json)</li>
  <li>Now test each config by running the command:<br>
  <b>python /home/shelterMon/shelterMon.py -C CONFIGFILE</b>
  <br>where CONFIGFILE is the full path of the config files you created a couple steps back<br>
  Example:<br><b>python /home/shelterMon/shelterMon.py -C /home/shelterMon/config.json -d yes </b></li>
  OR <br><b>python /home/shelterMon/shelterMon.py /home/shelterMon/myConfigFileName.json -d yes </b></li>
    <li>If the test is successful you will not get any errors.  If the breadboard hat is working correctly, you should get a message that states the switch is OFF and the script will quit.  When in the ON position, the script should finish without errors.  Refer to the video for a demonstration.</li>
<li>Now we need to tell the server to run that command by itself every minute.<br>
Run this command: (if it prompts for an editor, choose NANO) <br>
<b>crontab -e</b></li>
  <li>Now paste the following line into the nano editor just like you did for the previous files:<br>
  <b>* * * * * sudo python /home/shelterMon/shelterMon.py -C /home/shelterMon/config.json > /dev/null 2>&1</b></li>
  <li>Use CTRL-O & ENTER to save then CTRL-X to quit</li>
  <li>Now you are ready to start testing the system is doing what it should be doing.  Use whatever you can to test the sensor's temperature readings (hairdryer, etc).  <br>Turn off the sensor's power supply but leave the Raspberry Pi running.  It should notify you the sensor is offline.<br>Keep the ESP32 powered on but disconenct the sensor from the ESP32, you should get a notification the sensor is not reading correctly within 10 minutes. <br> </li>
  <li>Now you just need to place the sensor(s) where they need to go and use a USB charge adapter to power the sensor unit.  the unit needs to be in a place where it can communicate with the WiFi. </li>
</ul>
<h1>SMS (optional)</h1>
SMS alerts are an optional feature to send alert notifications via SMS to a mobile device.  This can be useful as many people don't check their email all day long. This is one method and requires a subscription that costs money.  It's cheap but a bug in the code could cause too many alerts to be sent and could accidentally rack up charges fast.  So be warned. <br><br>
As an alternative you send text to a specific mobile carrier's desginated domain like "vtext.com".  Here is an example article: https://www.verizon.com/about/news/vzw/2013/06/computer-to-phone-text-messaging, HOWEVER be warned as I tested this thoroughly for this project before going with Twilio.   I can onlhy speak for Verizon as thats all i could test since that's ny carrier, so maybe the other carriers are better in some areas.   <br>BUt Verizon SERIOUSLY THROTTLES the messages sent to vtext.com.   In my testing  on several different days, I sent more than ~10 mesages in a short amount of time, and Verizon stopped delivering those messages. I later got som eemails saying the message i sent hours ago has been delayed and not delivered yet.  That was a very reliable problem and it's why I don't recommend using it as a permanent solution.  <br><br>
Use the below steps to create and use a Twilio account. These instructions are likely to get depreacted as their website and protocols mentioned below may change over time.  So you will have to do your best to do what is needed to get the necessary information.  At the time this was written, you can rent a phone number from Twilio for $1.15/month.
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
<li>"twilioServiceID":""  <-- this is your Service ID</li>
<li>"twilioAcctID":""  <-- This is your Account ID</li>
<li>"twilioFromNumber":""  <-- This is your twilio phone number </li>
<li>"twilioToken":""  <-- This is your Auth Token </li>
<li>Save the file and exit the editor.  remember to validate the json code.</li>
<li>Now just ensure you have a destination SMS number specified in each location's .json file.  </li>
<li></li>


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
<li></li>
<li></li>
<li></li>
<li></li>
