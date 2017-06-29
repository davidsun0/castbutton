# castbutton
Chromecast predetermined videos at the touch of a button

## Set up

### Server

The files in the Server folder are to be put on a server that shares a local network with the Chromecast. [youtube-dl](https://github.com/rg3/youtube-dl), [castnow](https://github.com/xat/castnow), and their dependencies need to be installed on the server as well.
This program uses a workaround to pipe Youtube videos into the Chromecast's default media player.
For the serach module, a Youtube API key is needed to get the video id. xinwenquery.py can be changed to play any desired videos. In its current state, it plays the current day's Xin Wen Lian Bo video.

Then, run castserver.py which accepts connection and manages the Chromecast. launcher.sh can be put in a cron job to start the script on boot.

### Client

The client program has been created for a NodeMCU running Arduino. It must be configured to connect to the same network that the server and Chromecast are on.

#### Wiring

D0 is connected to the button. The line is pulled high by a 10K resistor and the button connects to ground.

D1 controls the error LED.

D2 controlls the success LED.
