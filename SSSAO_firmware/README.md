# SSSAO CH32V003 Firmware Flashing Guide

Here is code to turn your Hackaday Berlin Proto Petal into a Satisfying Senseless Sonic Add On (SSSAO)

This guide is adapted from the original proto petal tutorial [here](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge/blob/main/i2c_proto_petal_tutorial/README.md)

## Flashing a CH32V003 via the Badge

The proto-petal includes a CH32V003 RISC-V microcontroller. You can flash a compiled binary to the chip using the 2024 Hackaday badge. 

### Setup 
To flash firmware onto the device from the badge, you will need to do a few things:

#### 1. Bridge the programming pin
 
On the back of your Proto-petal, there are a pair of holes for mounting a header with the words "Jump to program". This is necessary to program the chip. You can either solder a header to this and use a jumper, or you can simply bridge it with solder. If you want to use the CH32V003's programming pin (PD1) for other purposes, you may want to leave it as a jumper.

Now connect your SSSAO proto petal to Slot 1 of your Conference Badge.

#### 2. Download the flashing software

The software to flash via the badge can be found in the same directory as this README. The original files are taken from the [pico_ch32v003_prog](https://github.com/hexagon5un/pico_ch32v003_prog/tree/b27aed77272f5a6784cd8eae403d3d86f6571f0e) repository.

#### 3. Load the software onto your badge.

The software files you need are: 
 - `constants.py`
 - `flash_ch32v003.py`
 - `singlewire_pio.py`
 - `SSSAO_firmware.bin`

Copy these files to your badge via either Thonny, VSCode (using the Micropython extension), or mpremote. A description for how to upload files to Thonny is provided in the [sequencer README](./main/tree/badge_sequencer/README.md)

Please note that this is not referring to mounting the disk as you do when flashing the Pico's image.

#### 4. Start up the REPL

Micropython offers an interactive mode when you plug the badge into a computer. You are provided with a command line (again in Thonny or VSCode). This is how we'll interact with the flashing software. This usually becomes active when you connect to the Pico. If not, manually start it up.

#### 5. Flash the firmware to the Proto-petal

In the REPL command line, type the following commands (do not type the '>>>'): 

```
>>> from flash_ch32v003 import CH32_Flash
>>> flasher = CH32_Flash(1)
>>> flasher.flash_binary("SSSAO_firmware.bin")
```
These commands respectively:
- import the CH32_Flash class into your current environment
- This instantiates the object for the GPIO on the i2c port 1.
- This will flash the firmware on the Petal.

#### 6. Celebrate

Provided you already did the associated soldering, your proto petal SAO is now a Satisfying Senseless Sonic Add On (SSSAO) :)

### Troubleshooting

A few folks have experienced trouble with the existing image on the badge. If you experience difficulty, it may be worth flashing the badge's image. The image can be found in the [repo here](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge/blob/main/software/micropython/RPI_PICO_W-20240602-v1.23.0.uf2).

#### Acknowledgments

Many thanks to [davedarkpo](https://github.com/davedarko/), [Spork](https://github.com/conniest),and [Aaron](https://github.com/aaroneiche/) for figuring out how to get code on there. Many many thanks to [Charles](https://github.com/cnlohr) and [Elliot](https://github.com/hexagon5un) for making the whole thing possible.
  
