"""!
@file ClosedLoopController.py
This file contains a class to implement a Closed Loop P Controller

TODO: Create a constructor which sets the proportional gain, initial setpoint, and other necessary parameters.

TODO: Create a method run() which is called repeatedly to run the control algorithm.
      This method should accept as parameters the setpoint and measured output.
      It should return an actuation value which is sent to a motor in this lab but might be sent to another device in another instance, as this is a generic controller.

TODO: The run() method should not contain a loop and should not print the results of its running; those things go in your main code.

TODO: A method set_setpoint() to set the setpoint.

TODO: A method set_Kp() to set the control gain.

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""

import pyb 
import utime

class PController:
    """! 
    This class implements a ClosedLoopController for an ME405 kit. 
    """
    
    def __init__(self, gain, target):
        """!
        @param gain 		Motor gain
        @param setpoint		Target encoder position
        @param times		Encoder reading times
        @param ticks		Encoder reading positions
        @param time_start	Controller start time
        """
        self.gain = gain
        self.target = target
        self.times = []
        self.ticks = []
        self.time_start = None

    def run(self, actual):
        """!
        Calculate a new duty cycle using Kp and positional error.
        @param actual	Encoder tick reading
        """
        #Initialize start time if there is none 
        if self.time_start == None:
            self.time_start = utime.ticks_ms()
            #Generate first encoder reading at time 0
            self.times.append(0)
            self.ticks.append(actual)
        #If controller is running, read time and ricks
        else:
            #Find difference between start time and current time
            self.times.append(utime.ticks_ms()-self.time_start)
            #Store corresponding encoder reading 
            self.ticks.append(actual)
        #Calculate positional error
        err = self.target - actual
        #Return duty cycle calculated as Kp*error, capped at +100/-100
        return max(min(self.gain*err,100),-100)

    def set_setpoint(self, new_target):
        """!
        Set a new target position.
        """
        self.target = new_target

    def set_Kp(self, new_gain):
        """!
        Set a new Kp.
        """
        self.gain = new_gain

    def get_response(self):
        """!
        Print all times and positions.
        """
        for i in range(len(self.times)):
            print(f"{self.times[i]},{self.ticks[i]}")


    def reset_response(self):
        """!
        Reset the controller times, ticks, and start time.
        """
        self.times = []
        self.ticks = []
        self.time_start = None