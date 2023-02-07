"""!
@file EncoderReader.py
This file contains code which uses uses timer channels for encoder measurements.

TODO: Create a class called EncoderReader which allows a user 
      to inialize board pins for use with a motor_encoder, as well 
      as read the encoder counter and handle underflow and overflow.

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""
import pyb

class EncoderReader:
    """! 
    This class implements an EncoderReader for an ME405 kit. 
    """

    def __init__ (self,enc_A,enc_B,timer):
        """! 
        Creates an EncoderReader by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_A     Pin for encoder channel A
        @param en_A     Pin for encoder channel B
        @param timer    Timer used for counting 
        """

        print ("Creating an EncoderReader")

        #Set interal pins and timer
        self.en_A = enc_A
        self.en_B = enc_B
        self.timer = timer

        #Set up channels.
        self.tim4_ch1 = timer.channel(1,mode = pyb.Timer.ENC_AB,pin = self.en_A)
        self.tim4_ch2 = timer.channel(2,mode = pyb.Timer.ENC_AB,pin = self.en_B)

        #Init other EncoderReader members
        self.prev=0
        self.cur=0
        self.ticks=0
        self.timer.counter(0)
   
    def read(self):
        """!
        Reads the counter and calculates the number of ticks.
        Also accounts for underflow and overflow
        """
        #get current encoder count
        self.cur = self.timer.counter()
        #calculate delta
        delta = self.cur-self.prev
        #calculate over/underflow limit
        max_change = (2**16 + 1) / 2
        #print(f"Cur: {self.cur} Delta: {delta} Max: {max_change}")
        #Underflow case
        if(delta > max_change):
            delta -= (2**16 +1)
        #Overflow case
        elif(delta < -1*max_change):
            delta += (2**16 +1)

        #add delta to number of ticks
        self.ticks+=delta
        #store current in previous    
        self.prev = self.cur
        

    def zero(self):
        """!
        Sets ticks to zero
        """
        self.ticks = 0
        self.prev = 0
        self.cur = 0
        self.timer.counter(0)
