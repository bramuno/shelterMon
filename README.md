This project is designed to help animal shelters monitor the temperature of various kennels they have to ensure the animals are safe.  You can use this for other reasons but you may need to make some additional adjustments not mentioned here. 

This project uses an ESP32 wifi development board connected to two DS18B20 temperature sensors to constantly send temperature readings to a syslog server on the user's home network.  The syslog server runs a cron script to monitor the termperature and alert the user if both sensors have been exceeded the temperature threshold for too long a time period.   

Usage and build instructions are below.  I have written these instructions for people that are not tech savvy.  If you know a tech person, I would recommend getting assistance from that person.  worst case, you can google "hackerspace" or "makerspace" and your city name to locate any possible nearby hackerspace/makerspace.  you can reach out to them to locate someone that can help you with this project.  The hardest part in this project is soldering, so if you can handle that you should be fine.  There are lots of tutorials on youtube to help you learn.

I welcome others to assist me with this project to improve wherever possible, so if you would like to collboarte and contribute, please drop me a line.  

<h2>Obligatory Disclaimer</h2>
All the advice and instruction given is for EDUCATIONAL PURPOSES ONLY.  I am not responsible for anything you do or destroy or anything else that happens as a result of your efforts.  Nothing is fool-proof so do not trust this or anything as a perfect solution for monitoring temperatures.   If you want a guaranteed solution, you should buy one. I am making this project because I have not found many solutions that will do the same thing at an affordable price which is what this project accomplishes.   <br>
ALSO, this project involves some soldering which is recommended to install a physical switch.  I am not responsible for hurting yourself or burning something to the ground.  If you are not comfortable soldering, you can reach out to your local hackerspace/makerspace for help. <br>
Ultimately it is YOUR RESPONSIBILITY to do all the proper research of all the subjects discussed here before attempting anything yourself.  

<h2>Hardware:</h2>
links provided here are only examples as you can swap out brands as needed to save money as long as the part does what it required, any by all means if you can find it somewhere else then you don't need amazon :)<br>
1 - Raspberry Pi or alternative, see below for some alternatives (make sure it comes with a PROPER power supply or buy one with it)<br>
?? - <a href="https://www.amazon.com/dp/B013GB27HS?ref_=cm_sw_r_cp_ud_dp_G5QE4ZMDYW0S37ADKY5F">DS18B20 Temperature Sensor</a> (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/4bGYlUr">ESP-32 WiFi Development Board</a> (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/buQ9nun">Breakout board</a> for ESP32 (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/6vf3yfr">USB chargers</a> (one for each area you need to monitor) <br>
??- Low voltage wires (cat5 cable works great)<br>
1 - <a href="https://a.co/d/dl4wDO9">lighted toggle switch 3-pole</a> any style is ok as long as its an 3-pole<br>
1 - <a href="https://a.co/d/bAP9Ayc">solderable breadboard hat</a><br>
1 - 200ohm resistor (have to buy a pack, but you may be able to locate a someone that has a few to spare)<br>
1 - basic LED (not needed if the toggle switch is lighted)<br>
1 - tiny flat head screwdriver <br>
1 - <a href="https://a.co/d/0wVyD20">micro SD card</a> (16gb or larger).  Don't go cheap here.  Recommend you buy SanDisk brand.  16gb is plenty of space, you don't need space for this project. The card should come with an micro to standard size adapter.  If it doesn't you will need to get one. <br>
1 - Soldering Iron kit (an iron with an iron stand and some solder, something <a href="https://a.co/d/caBHZSg">like this</a>)<br>
1 - helping hands see <a href="https://www.amazon.com/s?k=helping+hands&i=tools&crid=38J2ATXAPQ9XL&sprefix=helping+hands%2Ctools%2C137&ref=nb_sb_noss_1">this search</a> for examples.  You will need something to hold your items while soldering.<br>
<br> <br>
<u>Optional hardware</u>:<br>
You may need a <a href="https://a.co/d/4wtLp9Z">USB-SD card adapter</a> so you can read/write to the card.  Some laptops have this already so check before ordering. <br><br>
<u>Optional alternative hardware</u>: <br>
If you've never done a project like this and don't have any of the items listed above, here is a starter kit that has the M-F cables, low-voltage wires, a temporary breadbaoard, LEDs and resistors.  <br>
ELEGOO Electronic Fun Kit for Arduino, Respberry Pi https://a.co/d/bWZt9zZ <br>
<br>
Respberry Pi alternatives:<br>
Right now, rPi's are more expensive than they used to be.  so there are some alternatives you can try to use instead of an actual Pi.  I recommend googling "Raspberry Pi Alternatives" but here are a few that look like they may wor.  Overall, you must find somethign that has the same set of GPIO pins that the rPi has.:<br>
<li><a href="https://a.co/d/6iG05cZ">Libre Computer Board AML-S905X-CC </a></li>
<li><a href="https://a.co/d/2Vu5FYG">Banana Pi</a></li>
<li><a href="https://a.co/d/5vRDpWE">Odroid</a></li>
<br><br>
<h1>Build & Installation Instructions</h1>

<h2>ESP32 & sensors</h2>
  <li>Pop the ESP32 boards into the breakout boards. Make sure the pins line up.  </li>
  <li>The sensors should have come with 3 cables with a header that conects to the sensor board.  Connect the cables to the boards. </li>
  <li>Now the other end of the cables go to the breakout baord.   The red cable goes to the 3V3 pin, the black cable goes to the GND pin, and the yellow cable goes to P14.</li>
  <li>To power on, connect a micro-usb cable to the ESP32 and connect the other end to a usb charger port (like a cell phone charger) or for now you can use the USB port on your computer. </li>
  <li>read <a href="https://dronebotworkshop.com/esp32-intro/">this guide</a> on getting to know the basics on the ESP32, follow the instructions to setup arduino IDE and pay attention on how to upload code to the board.  It requires you hold the reset button until the board begins uploading, so it may take some practice. </li>
  <li>Now that you are familiar with the ES32, you can upload the code to the board.  See the project repo and look for the file "shelter.ino".  Open that file and copy the code into the arduino IDE.  Now look for the areas you need to edit.  Look for the comments "user changes here".  Update the SSIDname and SSIDpassword to your wifi SSID name and password, and update the udpAddress to the IP address of the rpi.  Leave the rest unless you know what you are doing. </li>
  <li>Make sure your IDE settings are as instructed by the ESP32 guide, then click the UPLOAD button.  remember uploading is not that simple for ESP32 so refer back to the previous ESP32 guide and remember you need to hold the reset button on the ESP32 then wait for the arduino output to say "uploading..." and then release the button.  it may take a few tries to get it right.</li>
  <li>Repeat the upload process as needed if you have more sensors.</li>

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
  <li>Once you have the address, put that IP in a browser window to connect to the router.  Login using the admin password.  If you can't find the router password and can't login, you will need to <a href="https://www.hellotech.com/guide/for/how-to-reset-router-and-modem">reset the router</a>.   This can be problematic and requires a netowrk cable so make sure you know what you're doing first.  </li>
  <li>Once logged in, go to the LOGS section (you may need to click ADVANCED if your router has a basic/advanced option) and you should have a log file to watch as it distributes IP addresses.  Once you have that, power on the rpi. </li>
  <li>Watch the log and look for the IP address given to the rpi. Write down the IP address <u>AND</a> the MAC address for that device, you will need both (example MAC:  ab:cd:ef:01:23:45).</li>
  <li>Now you need to power on each ESP32 running the code provided earlier.  They will attempt to get an IP address like your rpi.   Write down all IPs and MACs for each device.  </li>
  <li>Now you will need to locate the DHCP area and find where you can reserve the DHCP address for your rpi. Check <a href="https://kb.netgear.com/25722/How-do-I-reserve-an-IP-address-on-my-NETGEAR-router">this link</a> for an example using a netgead router but you may have to google "dhcp reservation" and your router name to find the right guide.</li>
  <li>Once your router has the IP reserved, you are done with the router.</li>
  <li>Now that you have the IP address, you can SSH into the rpi.<br>
  <li>if you dont know how to SSH to a device, you can <a href="https://www.putty.org/">download putty</a>.  Click <a href="https://www.ssh.com/academy/ssh/putty/windows">here</a> for a guide on how to use putty for SSH. </li>
  <li>After logging in run these commands: (you can paste copied text into the putty window using the right mouse button)<br>:
  <b>sudo apt-get -y install rsyslog && sudo nano /etc/rsyslog.d/shelter.conf</b>
  </li>
  <li>Nano will open to a blank page, go to the repo and find the file named "syslog.conf", open it and copy the data.  Then paste the data into the nano window. hit CTRL-O and ENTER to save, then CTRL-X to exit. </li>
  <li>Use the provided examples and duplicate as needed to have one line for each sensor you have.  The first section defines the log file location, and the second section ties the log file to the IP address of the sensors.   Update the IP addresses to match the IPs you got earlier for each ESP32 device.    Each line has to be unique so change the 1's and 2's as needed.  If you dont have that many devices, don't worry about the extra lines.    hit CTRL-O and ENTER to save, then CTRL-X to exit. </li>
  <li>now run this command to edit the rsyslog.conf file<br>
  <b>sudo nano /etc/rsyslog.conf</b><br>
  locate "module(load="imudp")" and remove the # before it. Do the same for next line.  Then change 'port="514"' to 'port="3333"' and use CTRL-O to save and CTRL-X to exit.</li>
  <li>now run this command to restart rsyslog and check your conf file is correct<br>
  <b>sudo systemctl restart rsyslog</b><br>If the command returns nothing, especially no errors, then you are fine.  Otherwise, go back into the file and try to find where the problem is.  syslog won't run if that file isn't perfect.</li>
  <li>Now that syslog is listening make sure your sensors are powered on.  </li>
  <li>The sensors should start sending data to the rpi.  Now we can finish with the rpi.</li>

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
  
"folderName":"/home/shelterMon",  <-- leave this as is unless you know what you are doing <br>
"logfileName":"sensor1.log",      <-- Make sure the <b>logfileName</b> matches the file name as mentioned in the syslog.conf file you created earlier <br>
"statusFileName":"status.txt",    <-- leave this as is unless you know what you are doing <br>
"shelterName":"ShelterNameHere",  <-- Change this value to the name of the Shelter or the location name where the sensor has been placed <br>
"maxTemp":"95",                   <-- Change this to your maximum allowed temperature <br>
"minTemp":"50",                   <-- Change this to your minimum required temperature  <br>
"tempUnit":"F",                   <-- Change this to either C for Celcius or F for Farenheit <br>
"emailDestination":"dest.email@gmail.com",  <-- Change this to your desired email destination where alerts should be sent <br>
"SMTPuser":"SMTPuserNameHere",    <-- Change this to your SMTP username from the previous section <br>
"SMTPpass":"SMTPpasswordHere",    <-- Change this to your SMTP password from the previous section <br>
"SMTPserver":"smtp.gmail.com",    <-- Chnage this to your SMTP server address from the previous section  <br>
"SMTPport":"465",                 <-- Change this to your SMTP server's destination port from the previous section  <br>
"SMS":"5551114444",               <-- Change this to your SMS phone number including area code, no hyphens and no country code <br>
"SMScarrier":"0"                  <-- Change this to your SMS carrier code as defined fom the list below  <br>  
 <br> 
 </li>    
<h3>SMS carriers codes</h3>
0 - Verizon<br>
1 - AT&T<br>
2 - Boost<br>
3 - T-Mobile<br>
4 - Cricket<br>
5 - Sprint<br><br>

  <li>hit CTRL-O and ENTER to save, then CTRL-X to exit.</li>
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
  <li>Thanks for reading this. </li>
</ul>
