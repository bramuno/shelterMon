This project is designed to help animal shelters monitor the temperature of various kennels they have to ensure the animals are safe.  You can use this for other reasons but you may need to make some additional adjustments not mentioned here. 

This project uses an ESP32 wifi development board connected to two DS18B20 temperature sensors to constantly send temperature readings to a syslog server on the user's home network.  The syslog server runs a cron script to monitor the termperature and alert the user if both sensors have been exceeded the temperature threshold for too long a time period.   

Usage and build instructions are below.  I have written these instructions for people that are not tech savvy.  If you know a tech person, I would recommend getting assistance from that person.  worst case, you can google "hackerspace" or "makerspace" and your city name to locate any possible nearby hackerspace/makerspace.  you can reach out to them to locate someone that can help you with this project.  The hardest part in this project is soldering, so if you can handle that you should be fine.  There are lots of tutorials on youtube to help you learn.

I welcome others to assist me with this project to improve wherever possible, so if you would like to collboarte and contribute, please drop me a line.  

<h2>Obligatory Disclaimer</h2>
All the advice and instruction given is for EDUCATIONAL PURPOSES ONLY.  I am not responsible for anything you do or destroy or anything else that happens as a result of your efforts.  Nothing is fool-proof so do not trust this or anything as a perfect solution for monitoring temperatures.   If you want a guaranteed solution, you should buy one. I am making this project because I have not found many solutions that will do the same thing at an affordable price which is what this project accomplishes.   <br>
ALSO, this project involves some soldering which is recommended to install a physical switch.  I am not responsible for hurting yourself or burning something to the ground.  If you are not comfortable soldering, you can reach out to your local hackerspace/makerspace for help. <br>

<h2>Hardware:</h2>
links provided here are only examples as you can swap out brands as needed to save money as long as the part does what it required, any by all means if you can find it somewhere else then you don't need amazon :)<br>
1 - Raspberry Pi/Odroid (make sure it comes with a power supply)<br>
?? - DS18B20 Temperature Sensor (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/4bGYlUr">ESP-32 WiFi Development Board</a> (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/buQ9nun">Breakout board</a> for ESP32 (one for each area you need to monitor)<br>
??- Low voltage wires (cat5 cable works great)<br>
1 - <a href="https://a.co/d/dl4wDO9">lighted toggle switch 3-pole</a> any style is ok as long as its an 3-pole<br>
1 - <a href="https://a.co/d/bAP9Ayc">solderable breadboard hat</a><br>
1 - 200ohm resistor (have to buy a pack)<br>
1 - basic LED (not needed if the toggle switch is lighted)<br>
1 - tiny flat head screwdriver <br>
1 - <a href="https://a.co/d/0wVyD20">micro SD card</a> (16gb or larger).  Don't go cheap here.  Recommend you buy SanDisk brand.  16gb is plenty of space, you don't need space for this project. The card should come with an micro to standard size adapter.  If it doesn't you will need to get one. <br>
1 - <a href="https://a.co/d/brV2cMs">SD card to USB adapter</a><br>
1 - Soldering Iron kit (an iron and an iron stand, something <a href="https://a.co/d/caBHZSg">like this</a><br>
1 - helping hands see <a href="https://www.amazon.com/s?k=helping+hands&i=tools&crid=38J2ATXAPQ9XL&sprefix=helping+hands%2Ctools%2C137&ref=nb_sb_noss_1">this search</a> for examples.  You will need something to hold your items for soldering.<br>
<br> <br>
Optional hardware:<br>
You may need a <a href="https://a.co/d/4wtLp9Z">USB-SD card adapter</a> so you can read/write to the card.  Some laptops have this already so check before ordering. <br>
I do recommend a fan hat for the raspberry pi to keep it cool.  something <a href="https://a.co/d/cjng3cB">like this</a> that raises the GPIO pins so they can still be used. <br>
Optional replacement hardware: <br>
If you've never done a project like this and don't have any of the items listed above, here is a starter kit that has the M-F cables, low-voltage wires, a temporary breadbaoard, LEDs and resistors.  <br>
ELEGOO Electronic Fun Kit for Arduino, Respberry Pi https://a.co/d/bWZt9zZ <br>
TBD<br>
<br>

<h3>SMS carriers codes</h3>
0 - Verizon<br>
1 - AT&T<br>
2 - Boost<br>
3 - T-Mobile<br>
4 - Cricket<br>
5 - Sprint<br><br>

Total Power Consumption:<br>
I've connected the <b>ESP32 and both sensors</b> to a power meter and the most power it has used is 80ma, but the average appears to be 30ma.   This does not include the raspberry pi. 

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

<h2>Python Script</h2>
  <li>Run this command:<br><b>nano /home/shelterMon/shelterMon.py</b></li>
  <li>When nano opens the blank document, go to the repo and look for the "shelterMon.py" file. Open the file and copy the data, then paste it into the nano window.  hit CTRL-O and ENTER to save, then CTRL-X to exit.</li>
  <li>Now run this command:<br><b>nano /home/shelterMon/config1.json</b></li>
  <li>When nano opens the blank document, go to the repo and look for the "config.json" file. Open the file and copy the data, then paste it into the nano window. Now update the information to suit your preferences.  Make sure the <b>logfileName</b> matches the file name as mentioned in the syslog.conf file you created earlier.  Enter the SMTP/email information per the steps performed earlier. hit CTRL-O and ENTER to save, then CTRL-X to exit.</li>
  <li>Repeat the previous step for all the sensors you have, and be sure to name the file with a unique name each time (eg, change config1.json to config2,json)</li>
  <li>Now test each config by running the command:<b>python /home/shelterMon/shelterMon.py -C CONFIGFILE</b> where CONFIGFILE is the full path of the config files you created a couple steps back<br>
  Example:<br><b>python /home/shelterMon/shelterMon.py -C /home/shelterMon/config1.json -d yes </b></li>
  OR <br><b>python /home/shelterMon/shelterMon.py /home/shelterMon/config2.json -d yes </b></li>
  <li>You should get some debug data and a message that states "Detected OFF switch position on syslog server. Quitting."</li>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
</ul>
