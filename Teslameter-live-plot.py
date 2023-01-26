from lakeshore import Teslameter
import matplotlib.pyplot as plt
import numpy as np
from time import time

plt.style.use('ggplot')  # sets the style of the plot to 'ggplot'

com_port_number = input("Enter the number of your Teslameter com_port: ")
my_teslameter = Teslameter(com_port='COM' + str(
    com_port_number))  # creates an instance of the Teslameter class using the input com_port number


def setup_plot(x_vec, B_x, B_y, B_z, B):
    """
    This function sets up the live plot with the given x-axis values, B_x, B_y, B_z and B values.
    It returns the line objects for each of the B values so that they can be updated
    in the live_plotter function.
    """
    plt.ion()  # this is the call to matplotlib that allows dynamic plotting
    fig = plt.figure('Teslameter live plot', figsize=(13, 6))
    ax = fig.add_subplot(111)
    # create a variable for the line so we can later update it
    line_x, = ax.plot(x_vec, B_x, '-o', alpha=0.8, label='B_x')
    line_y, = ax.plot(x_vec, B_y, '-o', alpha=0.8, label='B_y')
    line_z, = ax.plot(x_vec, B_z, '-o', alpha=0.8, label='B_z')
    line_B, = ax.plot(x_vec, B, '-o', alpha=0.8, label='|B|')
    # update plot label/title
    plt.ylabel('B (mT)')
    plt.legend(loc='upper right')
    plt.show()
    return line_x, line_y, line_z, line_B


# code was taken from here https://makersportal.com/blog/2018/8/14/real-time-graphing-in-python
def live_plotter(x_vec, B_x, B_y, B_z, B, line_x, line_y, line_z, line_B, pause_time=0.01):
    """
    This function updates the live plot with the latest B values,
    and pauses the plot for a specified time
    (default 0.01 seconds) before updating it again.
    """
    # check if line objects are empty, if so call setup_plot to create them
    if line_x == []:
        line_x, line_y, line_z, line_B = setup_plot(x_vec, B_x, B_y, B_z, B)

    # after the figure, axis, and line are created, we only need to update the y-data
    line_x.set_ydata(B_x)
    line_y.set_ydata(B_y)
    line_z.set_ydata(B_z)
    line_B.set_ydata(B)
    # adjust limits if new data goes beyond bounds
    y_min = min(np.min(B_x), np.min(B_y), np.min(B_z))
    y_max = np.max(B)
    plt.ylim([y_min - np.std([B_x, B_y, B_z]), y_max + np.std(B)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    # return line, so we can update it again in the next iteration
    return line_x, line_y, line_z, line_B


def do_live():
    # create generator that contains values from Teslameter
    generator = my_teslameter.stream_buffered_data(300, 200)

    line_x, line_y, line_z, line_B = [], [], [], []
    size = 100
    x_vec = np.linspace(0, 1, size + 1)[0:-1]
    B_x = np.zeros(len(x_vec))
    B_y = np.zeros(len(x_vec))
    B_z = np.zeros(len(x_vec))
    B = np.zeros(len(x_vec))

    # initialize counter and start time for time tracking
    i = 0
    t0 = time()

    # loop through data points in generator
    for point in generator:
        now = time() - t0
        print(str(i) + " - " + str(now) + ' s')
        i += 1
        # update y-data with new data point
        B_x[-1] = point[3] * 1000
        B_y[-1] = point[4] * 1000
        B_z[-1] = point[5] * 1000
        B[-1] = point[2] * 1000
        line_x, line_y, line_z, line_B = live_plotter(x_vec, B_x, B_y, B_z, B, line_x, line_y, line_z, line_B)

        # shift data in y-vectors to make room for new data
        B_x = np.append(B_x[1:], 0.0)
        B_y = np.append(B_y[1:], 0.0)
        B_z = np.append(B_z[1:], 0.0)
        B = np.append(B[1:], 0.0)
    plt.show()


if __name__ == '__main__':
    do_live()

'''This is a common pattern in Python scripts to allow 
the script to be both imported as a module into another 
script and run as the main program.
__name__ is a special variable in Python that holds 
the name of the current module. When the script is run 
directly, __name__ is set to "__main__". When the script 
is imported as a module into another script, __name__ is 
set to the name of the module. So the if __name__ == '__main__': 
statement checks if the script is being run directly or imported 
as a module into another script.If the script is run directly, the 
code block following the if statement is executed, in this case 
the do_live() function is called which will start the live streaming 
and plotting of the Teslameter data. If the script is imported as 
a module into another script, the code block following the if 
statement is skipped, so the do_live() function is not executed.'''
