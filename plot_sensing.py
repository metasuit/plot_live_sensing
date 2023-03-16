import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import threading
import time

stop_event = threading.Event()
BUFFER_SIZE = 20
buffer = [[] for _ in range(8)]

# Define a function to read all 8 sine waves from the file
def read_data():
    with open('sine_waves.txt', 'r') as f:
        wave_data = f.readline().strip().split(',')
    return [float(d) for d in wave_data]


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
                #if len(lines) > i:
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

# Create a matplotlib figure and embed it inside the Tkinter window
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

start_button = Button(root, text="Start", command=start_plot)
start_button.pack()

stop_button = Button(root, text="Stop", command=stop_plot)
stop_button.pack()

save_button = Checkbutton(root, text="Save", command=toggle_save)
save_button.pack()

# Initialize the save flag
save_flag = False

# Add labels to the x and y axes
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_xticks([])

# Start the GUI
root.mainloop()