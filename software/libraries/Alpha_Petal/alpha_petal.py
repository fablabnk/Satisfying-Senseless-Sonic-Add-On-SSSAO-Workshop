import time
class alpha_petal:
    """
    Displays a string on the SAO petal, one char at a time. the font is hand drawn
    and hard coded. The class needs to be initialized then can be passed a string
    consisting of [a-z] or space. There is no exception handling.
    """
        
    def __init__(self, bus, addr, sleeper):
        """
        Initializes the class.

        Args:
            bus: which i2c bus the petal is on. shold be passed from the define in main
            addr: the address of the petal. can be passed in as 0x00 or as the define from main
            sleeper: the time import needs to be passed in for some reason, idk I don't write python
        
        returns:
            none
        """
        self.bus = bus
        self.addr = addr
        self.memx = [1,2,3,4,5,6,7,8]
        self.sleeper = sleeper
        self.rot = 0
    
    def touchwheel_read(self, bus):
        """Returns 0 for no touch, 1-255 clockwise around the circle from the south
        
        Args: 
            bus: this is passed in from the calling function and shold be the i2c bus the touch wheel is on

        Returns:
            none
        
        """
        return(bus.readfrom_mem(84, 0, 1)[0])

    def set_slot(self, slot):
        """
        The font is originally designed to be in slot 1. if you're using the SAO in a different slot on the 2024 supercon
        badge, you can call this function and you don't have to figure out rotation yourself. if its on a different badge
        check out the set_rotation function.
        
        Args:
            slot: int 1-6
        
        Returns:
            none
        """
        if slot == 1:
            self.rot = 0
        if slot == 2:
            self.rot = 1
        if slot == 3:
            self.rot = 2
        if slot == 4:
            self.rot = 4
        if slot == 5:
            self.rot = 5
        if slot == 6:
            self.rot = 6
        self.rot %= 8

    def set_rotation(self, rot):
        """
        sets the rotation of the text displayed on the petal. there are 8 possible orientations 0-7.
        each rotation moves 45* anti-clockwise
        
        
        Args:
            rot: int [0-7] this will be mod 8, so really any number can be used.
        
        Returns:
            none
        """
        self.rot = rot
        self.rot %= 8

    def rotate_string(self, disp_str):
        """
        this function takes in a string and rotates 45* after every letter. the rotation is saved across calls and is shared with
        the rest of the class, so a call to set_rotation will affect the starting point of this function
        
        Args:
            disp_str: [a-z] and space. string of lowercase letters to display
        
        Returns:
            none
        """
        for chr in disp_str:
            self.petal_char(chr)
            self.rot += 1
            self.rot %= 8

    def disp_string(self, disp_str):
        """
        displays a string one char at a time. spaces are processed as a double reset to delinate words. 
        
        Args:
            disp_str: [a-z] and space. string of lowercase letters to display
        
        Returns:
            none
        """
        for chr in disp_str:
            self.petal_char(chr)
            
    def touchwheel_string(self, disp_str, touchwheel_bus):
        """
        displays a string one char at a time but each char is rotated based on the touch of the touchwheel.
    
        Args:
            string: [a-z] and space. string of lowercase letters to display
            touchwheel_bus: pass this in from main
        Returns:
            none
        """
        for chr in disp_str:
            tw = self.touchwheel_read(touchwheel_bus) #0 for no touch; 1-255 for touch
            if tw != 0:
                self.rot = tw/32
                self.rot %= 8
            self.petal_char(chr)

    def petal_letter_reset(self):
        """
        mostly shamelessly stolen from the startup animation. used to 'wipe' the letters off and
        as a break where spaces are
        
        args:
            none
        
        returns:
            none
        """
        self.sleeper.sleep_ms(500)
        for j in range(8):
            which_leds = (1 << (j+1)) - 1 
        for i in range(1,9):
            #print(which_leds)
            self.bus.writeto_mem(self.addr, i, bytes([which_leds]))
            self.sleeper.sleep_ms(30)
            self.bus.writeto_mem(self.addr, i, bytes([which_leds]))
        self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x0])) 
        self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x0])) 
        self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x0]))
        self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0])) 
        self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0])) 
        self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0])) 
        self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x0]))
        self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x0]))

    def petal_char(self, chr):
        """
        This is the meat of the class, a monstrosity of ifs because micropython doesnt 
        have match. it displays a char then resets the display. there is also some print statements to 
        help with debug that are vestigial. If you want to use this by itself for some reason, be my
        guest but it is implimented elsewhere to display strings.
        
        Args:
            chr: the char you want to display, [a-z] only. spaces are a 2 second 
            pause.
        
        returns:
            nothing
        """
        self.memx = [1,2,3,4,5,6,7,8]
        self.rot %= 8
        self.rot = int(self.rot)
        self.memx[:] = self.memx[-self.rot:] + self.memx[:-self.rot]
        print(f'rotation after converstion to int... {self.rot}')
        if chr == 'a':
            print("char was a")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2])) 
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4])) 
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0xE])) 
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x3])) 
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x5])) 
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x11]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7F]))
            
        if chr == 'b':
            print("char was b")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2])) 
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4])) 
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x1F]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0])) 
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x9]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7F]))
            
        if chr == 'c':
            print("char was c")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x70]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7C]))
            
        if chr == 'd':
            print("char was d")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x1F]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x1F]))
            
        if chr == 'e':
            print("char was e")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x1C]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7F]))
            
        if chr == 'f':
            print("char was f")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x11]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7F]))
            
        if chr == 'g':
            print("char was g")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x7F]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7E]))
            
        if chr == 'h':
            print("char was h")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0xF]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0xF]))
            
        if chr == 'i':
            print("char was i")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x41]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x18]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x60]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x31]))
            
        if chr == 'j':
            print("char was j")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x41]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x78]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x71]))
            
        if chr == 'k':
            print("char was k")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x5]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x12]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x1F]))
            
        if chr == 'l':
            print("char was l")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x1C]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0xF]))
            
        if chr == 'm':
            print("char was m")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x5]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x40]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x1E]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x7]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0xF]))
            
        if chr == 'n':
            print("char was n")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0xF]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x5]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x12]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0xE]))
            
        if chr == 'o':
            print("char was o")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x8]))
            
        if chr == 'p':
            print("char was p")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x9]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7F]))
            
        if chr == 'q':
            print("char was q")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0xE]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x68]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x8]))
            
        if chr == 'r':
            print("char was r")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x11]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x20]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x9]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7F]))
            
        if chr == 's':
            print("char was s")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x7F]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x7F]))
            
        if chr == 't':
            print("char was t")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x21]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x40]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x1F]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x8]))
            
        if chr == 'u':
            print("char was u")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x7E]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0xF]))
            
        if chr == 'v':
            print("char was v")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0xF]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x41]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x0]))
            
        if chr == 'w':
            print("char was w")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x1]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0xD]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x22]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0xE]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x0]))
            
        if chr == 'x':
            print("char was x")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x21]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x21]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x21]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x21]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x4]))
            
        if chr == 'y':
            print("char was y")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x21]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x2]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x8]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x40]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x0]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x11]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x4]))
            
        if chr == 'z':
            print("char was z")
            self.bus.writeto_mem(self.addr, self.memx[0], bytes([0x12]))
            self.bus.writeto_mem(self.addr, self.memx[1], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[2], bytes([0x1C]))
            self.bus.writeto_mem(self.addr, self.memx[3], bytes([0x4]))
            self.bus.writeto_mem(self.addr, self.memx[4], bytes([0x10]))
            self.bus.writeto_mem(self.addr, self.memx[5], bytes([0x3]))
            self.bus.writeto_mem(self.addr, self.memx[6], bytes([0x1C]))
            self.bus.writeto_mem(self.addr, self.memx[7], bytes([0x9]))
            
        if chr == ' ':
            self.petal_letter_reset()
        self.petal_letter_reset()
