"""!
@file MotorDriver.py
This file contains code which uses PWM output
with varying duty cycle to control a DC motor.

TODO: Create a class called MotorDriver which allows a user
      to initialize enabable, in1, in2, and timer pins to control
      a motor with. As well as set the duty cycle of the initialized
      motor to control speed. 

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""
import pyb

class MotorDriver:
    """! 
    This class implements a MotorDriver for an ME405 kit. 
    """

    def __init__ (self, en_pin: pyb.Pin, in1pin: pyb.Pin, in2pin: pyb.Pin, timer: pyb.Timer, polarity: bool):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin Set the enable pin for the motor
        @param in1pin Set the in1 pin for the motor
        @param in2pin Set the in2 pin for the motor
        @param timer  Sets the timer for the motor
        @param polarity Switch polarity if necessary
        """
        #Asign this drivers pins and timer
        self.en_pin = en_pin
        self.in1pin = in1pin
        self.in2pin = in2pin
        self.timer = timer
        self.polarity = polarity

        #Disable the motor to begin
        self.en_pin.value(0)

        #Asign the timer channels
        self.in1ch = self.timer.channel(1,pyb.Timer.PWM,pin = self.in1pin)
        self.in2ch = self.timer.channel(2,pyb.Timer.PWM,pin = self.in2pin)
        

        print ("Creating a motor driver")

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        #Set motor output for valid positive 'level's
        out = level if self.polarity else level*-1
        if(out > 0 and out <=100):
            self.in1ch.pulse_width_percent(abs(out))
            self.in2ch.pulse_width_percent(0)
            self.en_pin(1)
        #Set motor output for valid negative 'level's
        elif(out < 0 and out >= -100):
            self.in2ch.pulse_width_percent(abs(out))
            self.in1ch.pulse_width_percent(0)
            self.en_pin(1)
        #Disable the motor on all other values
        else:
            self.en_pin(0)

        #print(f"Setting duty cycle to {level}")
