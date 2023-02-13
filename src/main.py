"""!
@file main.py
    This file contains a program that uses tasks to run motors for a set
    number of encoder ticks using the ClosedLoopController, EncoderReader,
    and MotorDriver classes. 


@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date   2023-Feb-07
"""

import gc
import pyb
import cotask
import task_share
import ClosedLoopController
import EncoderReader
import MotorDriver



def init_flywheel_one():
    '''!
    This function initializes a motor driver on pins B4,B5, and PA10
    and initializes an encoder on pins C6 and C7. 
    @param NA
    @returns intialized encoder motor and controller objects
    '''
     #Set up pins and timer channel.
    in1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    en = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer(3,freq=20000)
    
    #Create motor driver object
    motorA = MotorDriver.MotorDriver(en,in1,in2,timer,False)

    #Set the GPIO pins and timer channel to pass into the encoder class
    ch1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    ch2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    tim8 = pyb.Timer(8,period=0xffff,prescaler = 0)
    
    #Create encoder driver object
    encoder = EncoderReader.EncoderReader(ch1,ch2,tim8)
    #run the contoller
    controller = ClosedLoopController.PController(.029,1050.0)
    return (encoder,motorA,controller)

def init_flywheel_two():
    '''!
    This function initializes a motor driver on pins A0,A1, and C1
    and initializes an encoder on pins B6 ans B7. 
    @param NA
    @returns intialized encoder motor and controller objects
    '''
     #Set up pins and timer channel.
    in1 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    in2 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    en = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    timer = pyb.Timer(2,freq=20000)
    
    #Create motor driver object
    motorB = MotorDriver.MotorDriver(en,in1,in2,timer,True)

    #Set the GPIO pins and timer channel to pass into the encoder class
    ch1 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
    ch2 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
    tim8 = pyb.Timer(4,period=0xffff,prescaler = 0)
    
    #Create encoder driver object
    encoder = EncoderReader.EncoderReader(ch1,ch2,tim8)
    #run the contoller
    controller = ClosedLoopController.PController(.025,3000.0)
    return (encoder,motorB,controller)


def control_loop_one(encoder: EncoderReader.EncoderReader,
                     motorA: MotorDriver.MotorDriver,
                     controller: ClosedLoopController.PController):
    """!
    This function contains a motor control loop which reads encoder ticks,
    claculates the desired duty cycle, and runs the motor at that duty cycle.
    @param encoder motor and controller class objects
    @returns NA
    """
    #Read encoder value
    encoder.read()
    actual = encoder.ticks
    #Calculate new duty cycle
    output = controller.run(actual)
    #Set new duty cyctle
    motorA.set_duty_cycle(output)
    #Stop motor after step response test        

def task1_fun(shares):
    """!
    Task which initializes encoder, motor, and controller objects,
    and then feeds those to the close loop function.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares
    n = 0
    (encoder,motorA,controller) = init_flywheel_one()

    while True:
        control_loop_one(encoder,motorA,controller)
        yield 0
        


def task2_fun(shares):
    """!
    Task which initializes encoder, motor, and controller objects
    for a second motor and then feeds those to the close loop function.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares
    
    (encoder,motorB,controller) = init_flywheel_two()

    while True:
        control_loop_one(encoder,motorB,controller)
        yield 0



# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=10,
                        profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=50,
                        profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task2.get_trace())
    print('')
