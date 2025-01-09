# Prototyping I2C SAO Petal for Supercon 8.  

Based on the cheap-as-chips CH32V003, this board has almost nothing on it, yet it lets you configure it as an I2C device.  All of the chip's I/O lines are broken out, you just have to wire them up as you want them.  The possibilities are limitless!  

There is an LED attached to Pin PD0 for your pre-wired debugging pleasure.  Demo code shows you how to turn it into an I2C blinkie.

Finally, if you jumper the "Program" pins, it connects GPIO1 to the CH32's SDIO line, allowing you to program the device in situ.  If all goes well, the badge will have bit-bang programming software installed, so you can flash this peripheral from the badge itself without need of a programmer.  If you will be doing this a lot, consider soldering a wire jumper permanently in place.  You lose a GPIO pin on the SAO header, but programming the petal becomes a cinch.


![front](sao_proto_front.png?raw=true)
![back](sao_proto_back.png?raw=true)
