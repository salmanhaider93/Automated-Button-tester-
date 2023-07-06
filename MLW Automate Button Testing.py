import tkinter as tk
import u3
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.stopped = False

        # Connect to the LabJack U3-HV
        self.d = u3.U3()

        # Define the digital output lines for the Fill and Vent switches
        # Replace the pin numbers with the correct pin numbers for your switching board
        self.FILL_SWITCH = 8
     


        self.fill_time_var = tk.DoubleVar()
        self.fill_time_var.set(1) # set default value
        self.vent_time_var = tk.DoubleVar()
        self.vent_time_var.set(1) # set default value
       

    def create_widgets(self):

        # Initialize the fill_time_var and vent_time_var StringVars
        self.fill_time_var = tk.StringVar()
        self.vent_time_var = tk.StringVar()

        # Create a label and entry widget for fill time
        self.fill_time_label = tk.Label(self, text="Fill time (s)")
        self.fill_time_label.grid(row=0, column=0, sticky="W")
        self.fill_time_entry = tk.Entry(self, textvariable=self.fill_time_var)
        self.fill_time_entry.grid(row=0, column=1)

                # Create a label and entry widget for vent time
        self.vent_time_label = tk.Label(self, text="Vent time (s)")
        self.vent_time_label.grid(row=1, column=0, sticky="W")
        self.vent_time_entry = tk.Entry(self, textvariable=self.vent_time_var)
        self.vent_time_entry.grid(row=1, column=1)



        # Create a label to display the current cycle number
        self.cycle_number_label = tk.Label(self, text="Cycle number")
        self.cycle_number_label.grid(row=2, column=0, sticky="W")

        self.entry = tk.Entry(self)
        self.entry.grid(row=2, column=1)
        
        self.cycle_number = tk.StringVar()
        self.cycle_number_label = tk.Label(self, textvariable=self.cycle_number)
        self.cycle_number_label.grid(row=3, column=1)

        

        self.run_button = tk.Button(self, text="Start Testing", command=self.run)
        self.run_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.quit = tk.Button(self, text="Stop Testing", command=self.stop)
        self.quit.grid(row=5, column=0, columnspan=2, pady=10)

        self.output = tk.Text(self, height=10, width=30)
        self.output.grid(row=0, column=2, rowspan=5, padx=10)

        # Create the fill light
        self.fill_light = tk.Canvas(self, width=50, height=50)
        self.fill_light.grid(row=6, column=0, padx=10, pady=10)
        self.fill_light_shape = self.fill_light.create_oval(10, 10, 40, 40, fill="grey")
        self.fill_light_label = tk.Label(self, text="On/OFF")
        self.fill_light_label.grid(row=7, column=0)


        
    def stop(self):
        self.stopped = True

    def run(self):
        self.stopped = False

        fill_time = float(self.fill_time_entry.get())
        vent_time = float(self.vent_time_entry.get())

        # Get the number of cycles from the Entry widget
        num_cycles_input = self.entry.get()
        if num_cycles_input == "":
            self.output.insert(tk.END, "Please enter a valid number of cycles\n")
            return

        # Convert the input to an integer
        num_cycles = int(num_cycles_input)

        try:
            # Loop for the specified number of cycles
            for i in range(num_cycles):

                if self.stopped:
                    break
                
                # Turn on the Fill switch
                self.d.setDOState(ioNum=self.FILL_SWITCH, state=1)
                self.fill_light.itemconfig(self.fill_light_shape, fill='green')
                self.master.update()
                time.sleep(fill_time)

                # Turn off the Fill switch
                self.d.setDOState(ioNum=self.FILL_SWITCH, state=0)
                self.fill_light.itemconfig(self.fill_light_shape, fill='Red')
                self.master.update()
                time.sleep(vent_time)
                

                # Update the current cycle number display
                self.cycle_number.set("Current cycle completed: " + str(i+1) + "\n")
                self.master.update()

            # Display a message indicating that the loop is complete
            self.output.insert(tk.END,str(i+1) + "  Cycle complted"+ "\n")

        except Exception as e:
            # If an error occurs, stop the loop and display an error message
            self.output.insert(tk.END, "An error occurred: " + str(e) + "\n")

    def withdraw(self):
        self.master.withdraw()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
