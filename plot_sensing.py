import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import threading
import time
import numpy as np
from scipy.signal import medfilt

stop_event = threading.Event()
BUFFER_SIZE = 20
buffer = [[] for _ in range(8)]
window_size = 5 #default window size

# Define a function to read all 8 sine waves from the file
def read_data():
    with open('sine_waves.txt', 'r') as f:
        wave_data = f.readline().strip().split(',')
    return [float(d) for d in wave_data]

# Define a function to apply the moving average filter to the data
def moving_average_filter(data, windowsize):
    #solution convolution
    """
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    """
    #solution cumsum
    cumsum_data = np.cumsum(np.insert(data, 0, 0))
    return (cumsum_data[windowsize:] - cumsum_data[:-windowsize]) / float(windowsize)


# Define a function to continuously update the plot with new data
def update_plot():
    global canvas, buffer, start_button
    ax.clear() #Clear the plot before starting the update
    #plt.clf()
    # Read the initial data
    data = read_data()

    # Initialize the buffer with the initial data
    if len(data) == 8:
        buffer = [data[:] for _ in range(8)]

    # Plot the initial data
    labels = ["Hasel 1", "Hasel 2", "Hasel 3", "Hasel 4", "Hasel 5", "Hasel 6", "Hasel 7", "Hasel 8"]
    lines = ax.plot(buffer)

    prev_first_value = data[0]

    while not stop_event.is_set():
        # Read the new data
        new_data = read_data()
        #print(new_data)

        if len(new_data) == 8 and new_data[0] != prev_first_value:
            # Add the new data to the buffer, and remove the oldest data point
            for i in range(8):
                buffer[i].append(new_data[i])
                if len(buffer[i]) > BUFFER_SIZE:
                    buffer[i].pop(0)

            # Update the plot with the new data
            for i in range(8):
                if moving_avg_var.get() == 1 and window_size_entry.get().isdigit():
                    window_size1 = int(window_size_entry.get())
                    filtered_data = moving_average_filter(buffer[i], window_size1)
                    lines[i].set_data(list(range(len(filtered_data))), filtered_data)
                else:
                    lines[i].set_data(list(range(len(buffer[i]))), buffer[i])

            # Add labels to the x and y axes
            ax.set_xlabel('Time')
            ax.set_ylabel('Value')
            ax.set_xticks([])

            plt.legend(lines, labels, loc="upper right")
            canvas.draw()

            # Save the data if the save flag is on
            if save_flag:
                with open('saved_data.txt', 'a') as f:
                    f.write(','.join([str(d) for d in new_data]) + '\n')
            prev_first_value = new_data[0]
        # Wait for a short time before checking for changes again
        time.sleep(0.001)
    start_button.config(state=NORMAL)

# Define a function to start the plot update
def start_plot():
    #plt.clf()
    global stop_event, start_button
    start_button.config(state=DISABLED)
    stop_event = threading.Event()
    threading.Thread(target=update_plot).start()


# Define a function to stop the plot update
def stop_plot():
    global stop_event
    stop_event.set()



# Define a function to toggle the save flag
def toggle_save():
    global save_flag
    save_flag = not save_flag


# Create the GUI
root = Tk()

# Create a frame to contain the Start and Stop buttons, and the new checkbox and entry
control_frame = Frame(root)
control_frame.pack(side=TOP, pady=10)

# Create a matplotlib figure and embed it inside the Tkinter window
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

start_button = Button(root, text="Start", command=start_plot)
start_button.pack(side=LEFT, padx=5)

stop_button = Button(root, text="Stop", command=stop_plot)
stop_button.pack(side=LEFT, padx=5)

save_button = Checkbutton(root, text="Save", command=toggle_save)
save_button.pack(side=LEFT, padx=5)

# Initialize the save flag
save_flag = False

#Add checkbox and input field for moving average filter

window_size_entry = Entry(root, width=10)
window_size_entry.pack(side=RIGHT, padx=5)
window_size_entry.insert(END, "5")
window_size_label = Label(root, text="Filter window Size:")
window_size_label.pack(side=RIGHT, padx=5)

moving_avg_var = IntVar()
moving_avg_checkbox = Checkbutton(root, text="Moving Average", variable=moving_avg_var)
moving_avg_checkbox.pack(side=RIGHT, padx=5)

# Add labels to the x and y axes
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_xticks([])

# Start the GUI
root.mainloop()