# Alpha Petal

Displays a string on the SAO petal, one char at a time. the font is hand drawn and hard coded, crafted with love in the alley. The class needs to be initialized then can be passed a string consisting of [a-z] or space. There is no exception handling.


# Usage
### Initialization:
Initialize the class:
`ap = alpha_petal(petal_bus, PETAL_ADDRESS, time)`

### Functions
`set_slot(slot:int[1-6])` This wraps the `set_rotation` function allowing you to specify a slot on the badge. 1,2,5,6 are recommended.
`set_rotation(rotation:int[0-7])` This allows you to natively set the rotation, [0-7], 45* incriments
`rotate_string(string:string)` This displays a string, rotating 45* between each char
`disp_string(string:string)` This displays a string, should be called after `set_rotation` or `set_slot`
`petal_letter_reset()` This is used internally to wipe letters
`petal_char(char:char)` This is used internally to display a single char and then wipe it away

### Usage
To just display text:
`set_rotation(0) #not strictly needed, but it's best to clean up`
`disp_string('your string ') #the trailing space is important to delinate between the trailing 'g' and leading 'y'`