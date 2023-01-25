# Liveplotter-Lakeshore-F71Teslameter

Teslameter-live-plot.py imports the Teslameter class from the lakeshore module, as well as the matplotlib, numpy, and time modules. It uses the matplotlib library to create a live plot of magnetic field data from the Teslameter device, which can be connected to a computer via a specified com port. The user is prompted to input the com port number for their Teslameter device. The code defines several functions: setup_plot, which sets up the initial plot with labeled axes and lines for each component of the magnetic field; live_plotter, which updates the plot with new data; and do_live, which uses the Teslameter's stream_buffered_data method to collect data and plots it in real-time. The code also includes print statements for debugging and tracking the number of data points collected and the elapsed time. 

(by Chat GPT)
