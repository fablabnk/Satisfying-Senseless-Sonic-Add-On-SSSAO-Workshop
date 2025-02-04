# I2C Proto Petal Demo

Here is code to turn your I2C Proto Petal into an I2C-blinkable LED, a tiny memory, and an input device all at once.  (You provide the button.)


## Flashing a CH32V003 via the Badge

The Proto-petal includes a CH32V003 RISC-V microcontroller. You can flash a compiled binary to the chip using the 2024 Supercon badge. 

### Setup 
To flash firmware onto the device from the badge, you will need a few things:

#### 1. Bridge the programming pin
 
On the back of your Proto-petal, there is a pair of holes for mounting a header with the words "Jump to program". This is necessary to program the chip. You can either solder a header to this and use a jumper, or you can simply bridge it with solder. If you want to use the CH32V003's programming pin (PD1) for other purposes, you may want to leave it as a jumper.


#### 1.2 Connect ProtoPetal to RaspberryPi Pico

For purposes of prototyping we need to connect the ThroughHole-Protopetal, as if it was connected to Port 1 on the supercon badge. That means:

 - `P1 (programming pin)` to `GP7 / 10`
 - `P2` to `GP6 / 9`
 - `SDA` to `I2C0 SDA / 1`
 - `SCL` to `I2C0 SCL / 2`
 - `GND` to `any GND`
 - `+V` to `3V3 out`

#### 2. Download the flashing software

The software to flash via the badge can be found in the [pico_ch32v003_prog](https://github.com/hexagon5un/pico_ch32v003_prog/tree/b27aed77272f5a6784cd8eae403d3d86f6571f0e) repository. This repo is linked to the badge repo as a submodule, which is a whole thing on its own. If you don't want to worry about submodule stuff, you can simply download the repo on its own. It will work just fine either way. 

#### 3. Load the software onto your badge.

The software files you need are: 
 - `constants.py`
 - `flash_ch32v003.py`
 - `singlewire_pio.py`
 - `blink.bin`

Copy these files to your badge via either Thonny, VSCode (using the Micropython extension), or mpremote. Please note that this is not referring to mounting the disk as you do when flashing the Pico's image.

#### 4. Start up the REPL

Micropython offers an interactive mode when you plug the badge into a computer. You are provided with a command line (again in Thonny or VSCode). This is how we'll interact with the flashing software. This usually becomes active when you connect to the Pico. If not, manually start it up.

#### 5. Flash the firmware to the Proto-petal

In the REPL command line, type the following commands (do not type the '>>>'): 

```
>>> from flash_ch32v003 import CH32_Flash
>>> flasher = CH32_Flash(1)
>>> flasher.flash_binary("blink.bin")
```
These commands respectively:
- import the CH32_Flash class into your current environment
- This instantiates the object for the GPIO on the i2c port 1.
- This will flash the firmware on the Petal.

#### 6. Celebrate

You should now see successful blinking on your proto petal.


### Troubleshooting

A few folks have experienced trouble with the existing image on the badge. If you experience difficulty, it may be worth flashing the badge's image. The image can be found in the [repo, here](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge/blob/main/software/micropython/RPI_PICO_W-20240602-v1.23.0.uf2).


#### Acknowledgments

Many thanks to [davedarkpo](https://github.com/davedarko/), [Spork](https://github.com/conniest),and [Aaron](https://github.com/aaroneiche/) for figuring out how to get code on there. Many many thanks to [Charles](https://github.com/cnlohr) and [Elliot](https://github.com/hexagon5un) for making the whole thing possible.

## Setting up an environment on Windows   to program the CH32V003 on the SAO from the Pico on the Hackaday Badge  

### Steps Mitch took on 2-Feb-2025 to use a Raspberry Pi Pico to program a CH32V003 on the SAO board -- using Windows.  
  
I started by following the tutorial from Raspberry Pi on installing Thonny:  
But, before installing Thonny, your laptop needs Python 3 (see next paragraph).  
https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2  
  
#### Install latest version of Python -- I upgraded from v3.11 to 3.13.1  
https://www.python.org/downloads/windows/  
* "Latest Python 3 Release - Python 3.13.1"  
* "Windows installer (64-bit)"download and double-click to install  
  
#### Install Thonny:
https://thonny.org/  
* At upper-right:  
* * Download version 4.1.7 for Windows  
* * "Installer with 64-bit Python 3.10"  
* * download and double-click to install  
  
#### Get MicroPython running on the Pico:
https://micropython.org/  
* DOWNLOAD tab  
* * search for "Pico Raspberry Pi" (but for Workshop with Hackaday badge:  "Pico W Raspberry Pi")  
* click on "v1.24.1 (2024-11-29).uf2"  
* unplug Pico from laptop's USB  
* hold Pico's BOOTSEL button while plugging it into laptop's USB (to pop up the RPI-RP2 disk volume)  
* on your laptop copy the "RPI_PICO-20241129-v1.24.1.uf2" file:  
* *paste it into the RPI-RP2 disk volume  
&nbsp;&nbsp;&nbsp;&nbsp; MicroPython is now installed on the Pico  
  
#### Run Thonny and set it up  
* View --> Files   --   to view laptop files in upper-right column 
* Lower-left corner Hamburger menu --> MicroPython (Raspberry Pi Pico)   --   to view files from Pico in lower-right column
 	
#### Make the LED blink on the Pico:  
* in Thonny:  
* * Run --> Configure interpreter --> MicroPython (Raspberry Pi Pico)   --   (already chosen when I did this)  
* * File --> New  
* * File --> Save --> Raspberry Pi Pico --> FirstTest.py  
* * type into Thonny upper pane:  
```
print("Hello World")  
```  
* * click the little green _**run**_ icon near the top of Thonny   --   *and Hello World prints in the lower pane*  
* * type into Thonny upper pane:  
```
import machine  
led=machine.Pin(25, machine.Pin.OUT)  
while True:  
  led.toggle()  
  time.sleep(1)  
```  
* Click the little green _**run**_ icon   --   *and the LED on the Pico blinks!*  
  
#### Make the LED blink on the CH32V003 SAO board:  
  
##### Grab files we need for making the LED on the CH32V003 SAO board blink:  
https://github.com/hexagon5un/pico_ch32v003_prog  
* copy to laptop:  
* * constants.py  
* * flash_ch32v003.py  
* * singlewire_pio.py  
* * blink.bin  
* copy the above files from laptop to Pico via Thonny  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; by right-clicking on each file --> Upload to /  
  
##### Hardware connection between CH32V003 SAO board and Pico:  
* short out "Jump to program" pads on CH32V003 SAO board (and leave them shorted)
  
| CH32V003   |     Pico       | color on prototype CH32V003   |  
| :--------: | :------------: | :---------------------------: |  
|    GP1     |   GP7 / 10     |           Yellow              |  
|    GP2     |   GP6 / 9      |           Green               |  
|  		SDA     | I2C0 SDA / 1   |           Orange              |  
|  		SCL     | I2C0 SCL / 2   |           Blue                |  
|  		GND     |   any GND      |           Black               |  
|  		+V      |   3V3 out      |           Red                 |  
		
##### Copy/Paste the following lines into the lower pane of Thonny (Python interpreter):  
```
from flash_ch32v003 import CH32_Flash  
flasher = CH32_Flash(1)  
flasher.flash_binary("blink.bin")
```  
*And the LED on the CH32V003 SAO board blinks !*  
  
  
#### Let's try flashing some other code into the CH32V003 SAO board  
  
* Clone the ch32v003fun Github repository from:  
https://github.com/cnlohr/ch32v003fun		
  
*  From the CH3fun wiki:  
https://github.com/cnlohr/ch32v003fun/wiki/Installation  
  
under the Windows section:  
* Click on the "this copy" link to get GCC10 installed  
* https://gnutoolchains.com/risc-v/  
* * Click "risc-v-gcc10.1.0.exe" in the top line of the table  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(NOTE:  do not click the green DOWNLOAD button at the bottom)  
* * Double-click to install  
  
* Open a cmd prompt window  
* * cd to the example\blink directory  
Type in:  
```
make
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This will compile the blink program with the result of blink.bin in the directory  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NOTE:  the flashing will fail, which is expected and OK  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NOTE: THE ABOVE IS ONLY TO TEST OUR COMMAND LINE DEVELOPMENT ENVIRONMENT  
* * Copy the *blink* directory to create a new *blink-petal* directory  
* * Copy *blink.c* to *blink-petal.c*  
* * Edit the make file to change the TARGET to *blink-petal*  
* * Edit the *blink-petal.c* file to contain only the following text:  
```
#include "ch32v003fun.h"
#include <stdio.h>

// use defines to make more meaningful names for our GPIO pins
#define PIN_1 PD0

int main()
{
  SystemInit();

  // Enable GPIOs
  funGpioInitAll();

  funPinMode( PIN_1, GPIO_Speed_10MHz | GPIO_CNF_OUT_PP );

  while(1)
  {
    funDigitalWrite( PIN_1, FUN_HIGH );
    Delay_Ms( 250 );
    funDigitalWrite( PIN_1, FUN_LOW );
    Delay_Ms( 250 );
  }
}	 
```
  
** Now do a  
```
   make
```  
&nbsp;&nbsp;&nbsp;to create a blink-petal.bin file  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NOTE:  the flashing will fail, which is expected and OK
  
* * delete the *blink.bin* file from the Pico, from the lower pane of Thonny (right-click --> delete)
* * add the new *blink-petal.bin* file from your laptop to the Pico using Thonny (right-click --> Upload to /)
* * Copy/Paste the following lines into the lower pane of Thonny (Python interpreter):
```
   from flash_ch32v003 import CH32_Flash
   flasher = CH32_Flash(1)
   flasher.flash_binary("blink-petal.bin")
```  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*And the LED on the CH32V003 SAO board blinks quickly!*  
  
_**Now you know that you can program the CH32V003 on the SAO board to do whatever you want.**_  
  
  
  
### The following is not used for our Hackaday workshop, but is cool for programming the Pico with C code using Visual Studio:  
  
#### Install Pico SDK for Windows  
https://www.raspberrypi.com/news/raspberry-pi-pico-windows-installer/  
* * click the red "Download Windows Pico Installer" button
* * download and double-click to install (takes a long, long, long time to download and install Visual Studio and other files in the process)  
  
* WindowsKey --> type "Pico"  
* * run "Pico - Visual Studio Code"  
* * * on left, under "PICO-EXAMPLES", click on "C blink.c"  
* * * click on "Build" icon at the bottom of the left pane  
* * * * choose "Pico ARM GCC"  
* * * * click Pico's BOOTSEL button --> it takes a while to compile everything  
* * * click the "Run and Debug (Ctrl+Shift+D)" icon in the left column  
* * * tap "F5" key  
* * unplug Pico from laptop's USB  
* * hold Pico's BOOTSEL button while plugging it into laptop's USB (to pop up the RPI-RP2 disk volume)  
* * copy the "blink.uf2" file from where it compiled on your laptop  
NOTE:  for me it was at:  "C:\Users\maltm\Documents\Pico-v1.5.1\pico-examples\build\blink"  
* * paste it into the RPI-RP2 disk volume  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *The LED on the Pico starts blinking !*  
  
