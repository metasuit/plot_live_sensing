import math
import time
import random

# Define the number of sine waves and the sampling frequency
num_waves = 7
sampling_freq = 30

# Define the output file name
#filename = 'sine_waves.txt'
filename = 'c:\\tmp\\values_muxes2.txt'

# Define global parameters for adding artificial noise
add_noise = True  # Set to True to add noise, False to disable
noise_amplitude = 0.1  # Amplitude of the noise

# Define the function to write the sine wave data to the file
def write_sine_data(file):
    # Calculate the time interval between samples
    time_interval = 1 / sampling_freq

    # Initialize the time and angle variables
    t = 0
    angle_incr = 2 * math.pi / num_waves
    #angle_incr = 0

    while True:
        # Calculate the values of the sine waves
        values = [2*math.sin(i * angle_incr + t) for i in range(num_waves)]


        # Add artificial noise to the values if required
        if add_noise:
            values = [v + random.uniform(-noise_amplitude, noise_amplitude) for v in values]

        # Write the values to the file
        file.seek(0) # Move the file pointer to the beginning of the file
        file.write(','.join([str(v) for v in values]) + '\n')
        #print(','.join([str(v) for v in values]) + '\n')
        #time.sleep(1)
        file.flush()  # Flush the buffer to ensure the data is written to disk immediately

        # Wait for the next sample time
        t += time_interval
        time.sleep(time_interval)

# Open the output file for writing
with open(filename, 'w') as f:
    # Write the initial values of the sine waves to the file
    write_sine_data(f)