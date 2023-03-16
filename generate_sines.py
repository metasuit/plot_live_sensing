import math
import time

# Define the number of sine waves and the sampling frequency
num_waves = 8
sampling_freq = 30

# Define the output file name
filename = 'sine_waves.txt'

# Define the function to write the sine wave data to the file
def write_sine_data(file):
    # Calculate the time interval between samples
    time_interval = 1 / sampling_freq

    # Initialize the time and angle variables
    t = 0
    angle_incr = 2 * math.pi / num_waves

    while True:
        # Calculate the values of the sine waves
        values = [2*math.sin(i * angle_incr + t) for i in range(num_waves)]

        # Write the values to the file
        file.seek(0) # Move the file pointer to the beginning of the file
        file.write(','.join([str(v) for v in values]) + '\n')
        file.flush()  # Flush the buffer to ensure the data is written to disk immediately

        # Wait for the next sample time
        t += time_interval
        time.sleep(time_interval)

# Open the output file for writing
with open(filename, 'w') as f:
    # Write the initial values of the sine waves to the file
    write_sine_data(f)