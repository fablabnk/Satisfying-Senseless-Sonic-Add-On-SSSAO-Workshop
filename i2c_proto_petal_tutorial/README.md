# I2C Proto Petal Demo

Here is code to turn your I2C Proto Petal into an I2C-blinkable LED, a tiny memory, and an input device all at once.  (You provide the button.)


## Flashing a CH32V003 via the Badge

The Proto-petal includes a CH32V003 RISC-V microcontroller. You can flash a compiled binary to the chip using the 2024 Supercon badge. 

### Setup 
To flash firmware onto the device from the badge, you will need a few things:

#### 1. Bridge the programming pin
 
On the back of your Proto-petal, there is a pair of holes for mounting a header with the words "Jump to program". This is necessary to program the chip. You can either solder a header to this and use a jumper, or you can simply bridge it with solder. If you want to use the CH32V003's programming pin (PD1) for other purposes, you may want to leave it as a jumper.

#### 2. Download the flashing software

The software to flash via the badge can be found in the [pico_ch32v003_prog](https://github.com/hexagon5un/pico_ch32v003_prog/tree/b27aed77272f5a6784cd8eae403d3d86f6571f0e) repository. This repo is linked to the badge repo as a submodule, which is a whole thing on its own. If you don't want to worry about submodule stuff, you can simply download the repo on its own. It will work just fine either way. 

#### 3. Load the software onto your badge.

The software files you need are: 
 - `constants.py`
 - `flash_ch32v003.py`
 - `singlewire_pio.py`
 - `blink.bin`

For the Europe loadout, these are already on the badge.  If you have a Supercon version, copy these files to your badge via either Thonny, VSCode (using the Micropython extension), or mpremote. Please note that this is not referring to mounting the disk as you do when flashing the Pico's image.

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
- Try "blink2.bin" for an inverse blinking experience!

#### 6. Celebrate

You should now see successful blinking on your proto petal.


### Troubleshooting

A few folks have experienced trouble with the existing image on the badge. If you experience difficulty, it may be worth flashing the badge's image. The image can be found in the [repo, here](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge/blob/main/software/micropython/RPI_PICO_W-20240602-v1.23.0.uf2).


#### Acknowledgments

Many thanks to [davedarkpo](https://github.com/davedarko/), [Spork](https://github.com/conniest),and [Aaron](https://github.com/aaroneiche/) for figuring out how to get code on there. Many many thanks to [Charles](https://github.com/cnlohr) and [Elliot](https://github.com/hexagon5un) for making the whole thing possible.
