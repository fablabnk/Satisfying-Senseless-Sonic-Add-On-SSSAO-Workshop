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
        self.sleeper = sleeper
    
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
        self.bus.writeto_mem(self.addr, 0x01, bytes([0x0])) 
        self.bus.writeto_mem(self.addr, 0x02, bytes([0x0])) 
        self.bus.writeto_mem(self.addr, 0x03, bytes([0x0]))
        self.bus.writeto_mem(self.addr, 0x04, bytes([0x0])) 
        self.bus.writeto_mem(self.addr, 0x05, bytes([0x0])) 
        self.bus.writeto_mem(self.addr, 0x06, bytes([0x0])) 
        self.bus.writeto_mem(self.addr, 0x07, bytes([0x0]))
        self.bus.writeto_mem(self.addr, 0x08, bytes([0x0]))

    def petal_string(self,disp_str):
        """
        This is the meat of the class, a monstrosity of ifs because micropython doesnt 
        have match. it loops through the string and displays each char, resets the 
        display and moves on to the next char. there is also some print statements to 
        help with debug that are vestigial.
        
        Args:
            disp_str: the string you want to display, [a-z] only. spaces are a 2 second 
            pause.
        
        returns:
            nothing
        """
        for chr in disp_str:
            if chr == 'a':
                print("char was a")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2])) 
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4])) 
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0xE])) 
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x3])) 
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x5])) 
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x11]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7F]))
                self.petal_letter_reset()
            if chr == 'b':
                print("char was b")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2])) 
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4])) 
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x1F]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x0])) 
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x9]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7F]))
                self.petal_letter_reset()
            if chr == 'c':
                print("char was c")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x70]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7C]))
                self.petal_letter_reset()
            if chr == 'd':
                print("char was d")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x1F]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x1F]))
                self.petal_letter_reset()
            if chr == 'e':
                print("char was e")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x1C]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7F]))
                self.petal_letter_reset()
            if chr == 'f':
                print("char was f")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x11]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7F]))
                self.petal_letter_reset()
            if chr == 'g':
                print("char was g")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x7F]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7E]))
                self.petal_letter_reset()
            if chr == 'h':
                print("char was h")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0xF]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0xF]))
                self.petal_letter_reset()
            if chr == 'i':
                print("char was i")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x41]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x18]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x60]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x31]))
                self.petal_letter_reset()
            if chr == 'j':
                print("char was j")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x41]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x78]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x71]))
                self.petal_letter_reset()
            if chr == 'k':
                print("char was k")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x5]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x12]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x1F]))
                self.petal_letter_reset()
            if chr == 'l':
                print("char was l")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x1C]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0xF]))
                self.petal_letter_reset()
            if chr == 'm':
                print("char was m")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x5]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x40]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x1E]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x7]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0xF]))
                self.petal_letter_reset()
            if chr == 'n':
                print("char was n")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0xF]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x5]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x12]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0xE]))
                self.petal_letter_reset()
            if chr == 'o':
                print("char was o")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x8]))
                self.petal_letter_reset()
            if chr == 'p':
                print("char was p")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x9]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7F]))
                self.petal_letter_reset()
            if chr == 'q':
                print("char was q")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0xE]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x68]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x8]))
                self.petal_letter_reset()
            if chr == 'r':
                print("char was r")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x11]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x20]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x9]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7F]))
                self.petal_letter_reset()
            if chr == 's':
                print("char was s")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x7F]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x7F]))
                self.petal_letter_reset()
            if chr == 't':
                print("char was t")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x21]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x40]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x1F]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x8]))
                self.petal_letter_reset()
            if chr == 'u':
                print("char was u")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x7E]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0xF]))
                self.petal_letter_reset()
            if chr == 'v':
                print("char was v")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0xF]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x41]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x0]))
                self.petal_letter_reset()
            if chr == 'w':
                print("char was w")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x1]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0xD]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x22]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0xE]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x0]))
                self.petal_letter_reset()
            if chr == 'x':
                print("char was x")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x21]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x21]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x21]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x21]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x4]))
                self.petal_letter_reset()
            if chr == 'y':
                print("char was y")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x21]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x2]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x8]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x40]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x0]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x11]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x4]))
                self.petal_letter_reset()
            if chr == 'z':
                print("char was z")
                self.bus.writeto_mem(self.addr, 0x01, bytes([0x12]))
                self.bus.writeto_mem(self.addr, 0x02, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x03, bytes([0x1C]))
                self.bus.writeto_mem(self.addr, 0x04, bytes([0x4]))
                self.bus.writeto_mem(self.addr, 0x05, bytes([0x10]))
                self.bus.writeto_mem(self.addr, 0x06, bytes([0x3]))
                self.bus.writeto_mem(self.addr, 0x07, bytes([0x1C]))
                self.bus.writeto_mem(self.addr, 0x08, bytes([0x9]))
                self.petal_letter_reset()
            if chr == ' ':
                self.petal_letter_reset()
                self.petal_letter_reset()
