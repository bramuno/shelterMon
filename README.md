Under construction...

This project is designed to help animal shelters monitor the temperature of various kennels they have to ensure the animals are safe.  

This project uses an ESP32 wifi development board connected to two DS18B20 temperature sensors to constantly send temperature readings to a syslog server on the user's home network.  The syslog server runs a cron script to monitor the termperature and alert the user if both sensors have been exceeded the temperature threshold for too long a time period.   

Usage and build instructions coming soon...

I welcome others to assist me with this project to improve wherever possible, so if you would like to collboarte and contribute, please drop me a line.  

<h2>Hardware:</h2>
links provided here are only examples as you can swap out brands as needed to save money as long as the part does what it required, any by all means if you can find it somewhere else then you don't need amazon :)<br>
1 - Raspberry Pi/Odroid (make sure it comes with a power supply)<br>
1 - 16GB (or larger) Micro SD card<br>
?? - DS18B20 Temperature Sensor (one for each area you need to monitor)<br>
?? - ESP-WROOM-32 Development Board (one for each area you need to monitor)<br>
?? - <a href="https://a.co/d/buQ9nun">Breakout board</a> for ESP32 (one for each area you need to monitor)<br>
??- Low voltage wires (cat5 cable works great)<br>
1 - <a href="https://a.co/d/dl4wDO9">lighted toggle switch 3-pole</a> any style is ok as long as its an 3-pole<br>
1 - <a href="https://a.co/d/bAP9Ayc">solderable breadboard hat</a><br>
1 - 200ohm resistor (have to buy a pack)<br>
1 - basic LED (optional)<br>
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
<h2>Raspberry Pi</h2>
<ul>
<li>go to https://www.raspberrypi.com/software/ and download the latest Raspbery Pi system imager tool. </li>
  <li></li>
</ul>
