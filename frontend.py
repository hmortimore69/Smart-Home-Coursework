from backend import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class SmartHomeSystem:
    def __init__(self, home):
        self.home = home

        # Initialise all objects needed for future assignment and manipulation
        self.consumption_rate_window = None
        self.edit_win = None
        self.add_win = None
        self.clock_label = None

        self.win = Tk()
        self.win.title("Smart Home System")

        self.main_frame = Frame(self.win)
        self.main_frame.grid(column=0, row=0, padx=10, pady=10)

        # Initial colouring and styling
        self.background_colour = "teal"

        # Assign default styling
        self.win.configure(bg=self.background_colour)
        self.main_frame.configure(bg=self.background_colour)

    def run(self):
        self.create_widgets()

        self.clock_label = Label(
            self.main_frame,
            text="Time: 00:00",
        )
        self.clock_label.grid(column=1, row=0, pady=(0, 10))

        self.clock_label.after(3000, self.update_clock)
        self.win.mainloop()

    def update_widgets(self):
        # Clear the mainFrame
        for child in self.main_frame.winfo_children():
            if child != self.clock_label:
                child.destroy()

        self.create_widgets()

    def update_clock(self):
        time = self.clock_label.cget("text")[6:-3]
        time = f"{"0" if time == "23" else str(int(time) + 1).zfill(2)}:00"

        self.clock_label.config(text=f"Time: {time}")
        self.win.after(3000, self.update_clock)

    def create_widgets(self):
        turn_on_all_button = Button(
            self.main_frame,
            text="Turn On All",
            command=lambda: self.turn_on_all_button_clicked()
        )
        turn_on_all_button.grid(column=0, row=0, padx=(10, 100), pady=(0, 10))

        turn_off_all_button = Button(
            self.main_frame,
            text="Turn Off All",
            command=lambda: self.turn_off_all_button_clicked()

        )
        turn_off_all_button.grid(column=0, row=0, padx=(100, 10), pady=(0, 10))

        save_devices = Button(
            self.main_frame,
            text="Save Devices",
            command=lambda: self.save_device_list()
        )
        save_devices.grid(column=2, row=0, padx=(10, 0), pady=(0, 10))

        load_devices = Button(
            self.main_frame,
            text="Load Devices",
            command=lambda: self.load_device_list()
        )
        load_devices.grid(column=3, row=0, padx=(10, 0), pady=(0, 10))

        # Initialise the 5 devices
        for i, device in enumerate(self.home.get_devices()):
            device_status = "On" if device.get_switched_on() else "Off"

            if isinstance(device, SmartPlug):
                device_label = Label(
                    self.main_frame,
                    text=f"Smart Plug: {device_status}, Consumption Rate: {device.get_consumption_rate()}"
                )
                device_label.grid(column=0, row=i + 1, sticky="w")

            else:
                device_option = "On" if device.get_option() else "Off"

                device_label = Label(
                    self.main_frame,
                    text=f"Smart Doorbell: {device_status}, Sleep Mode: {device_option}"
                )
                device_label.grid(column=0, row=i + 1, sticky="w")

            toggle_power = Button(
                self.main_frame,
                text="Toggle Power",
                command=lambda n=i: self.toggle_switch_button_clicked(n)
            )
            toggle_power.grid(column=1, row=i + 1, padx=(10, 0))

            edit_option = Button(
                self.main_frame,
                text="Edit Device",
                command=lambda n=i: self.edit_device_button_clicked(n)
            )
            edit_option.grid(column=2, row=i + 1, padx=(10, 0))

            remove_device = Button(
                self.main_frame,
                text="Delete Device",
                command=lambda n=i: self.delete_device_button_clicked(n)
            )
            remove_device.grid(column=3, row=i + 1, padx=(10, 0))

        add_device = Button(
            self.main_frame,
            text="Add Device",
            command=self.add_device_button_clicked
        )
        add_device.grid(column=0, row=len(self.home.get_devices()) + 1, pady=(10, 0))

    def turn_on_all_button_clicked(self):
        self.home.turn_on_all()
        self.update_widgets()

    def turn_off_all_button_clicked(self):
        self.home.turn_off_all()
        self.update_widgets()

    def toggle_switch_button_clicked(self, i):
        self.home.toggle_switch_at_index(i)
        self.update_widgets()

    def edit_device_button_clicked(self, i):
        self.edit_win = Toplevel(self.win)
        self.edit_win.configure(bg="teal")

        if isinstance(self.home.get_devices()[i], SmartPlug):
            consumption_rate_var = StringVar()
            consumption_rate_var.set(str(self.home.get_devices()[i].get_consumption_rate()))

            edit_label = Label(
                self.edit_win,
                text="Set Consumption Rate"
            )
            edit_label.grid(column=0, row=0, pady=(10, 0))

            consumption_rate_spinbox = Spinbox(
                self.edit_win,
                from_=0,
                to=150,
                increment=1,
                width=4,
                textvariable=consumption_rate_var,
                validate="key",
                validatecommand=(self.edit_win.register(validate_entry), "%P")
            )
            consumption_rate_spinbox.grid(column=0, row=2, pady=(10, 0))

            consumption_rate_confirm_button = Button(
                self.edit_win,
                text="Confirm",
                command=lambda n=i: self.set_plug_consumption(i, consumption_rate_spinbox.get())
            )
            consumption_rate_confirm_button.grid(column=0, row=6, padx=60, pady=(10, 10))

        else:
            option_value = BooleanVar()
            option_value.set(self.home.devices[i].get_option())

            edit_label = Label(
                self.edit_win,
                text="Sleep Mode"
            )
            edit_label.grid(column=0, row=0, padx=60, pady=(10, 10))

            true_button = Radiobutton(
                self.edit_win,
                text="On",
                variable=option_value,
                value=True
            )
            true_button.grid(column=0, row=2, pady=(0, 5))

            false_button = Radiobutton(
                self.edit_win,
                text="Off",
                variable=option_value,
                value=False
            )
            false_button.grid(column=0, row=3)

            edit_confirm_button = Button(
                self.edit_win,
                text="Confirm",
                command=lambda n=i: self.set_custom_device_option(n, option_value.get())
            )
            edit_confirm_button.grid(column=0, row=6, padx=60, pady=(10, 10))

    def set_custom_device_option(self, i, value):
        self.home.devices[i].set_option(value)
        self.edit_win.destroy()
        self.update_widgets()

    def set_plug_consumption(self, i, value):
        self.home.devices[i].set_consumption_rate(value)
        self.edit_win.destroy()
        self.update_widgets()

    def delete_device_button_clicked(self, i):
        self.home.remove_device(i)
        self.update_widgets()

    def add_device_button_clicked(self):
        self.add_win = Toplevel(self.win)
        self.add_win.configure(bg="teal", padx=10, pady=10)

        # Create light bulb image and resize to button size.
        plug_image = PhotoImage(file="images/plug.png")
        plug_image = plug_image.subsample(plug_image.width() // 100, plug_image.height() // 100)

        doorbell_image = PhotoImage(file="images/doorbell.png")
        doorbell_image = doorbell_image.subsample(doorbell_image.width() // 100, doorbell_image.height() // 100)

        add_question_label = Label(
            self.add_win,
            text="Would you like to add a Smart Doorbell or a Smart Plug?"
        )
        add_question_label.grid(row=0, column=1, columnspan=2)

        add_smart_plug = Label(
            self.add_win,
            text="Smart Plug"
        )
        add_smart_plug.grid(column=1, row=1, pady=(10, 5), padx=10)

        add_smart_doorbell = Label(
            self.add_win,
            text="Smart Doorbell"
        )
        add_smart_doorbell.grid(column=2, row=1, pady=(10, 5), padx=10)

        plug_button = Button(
            self.add_win,
            image=plug_image,
            width=100,
            height=100,
            command=lambda: self.add_plug_consumption()
        )
        plug_button.image = plug_image  # Maintain reference to avoid python garbage collection.
        plug_button.grid(column=1, row=2, padx=20, pady=(5, 0))

        doorbell_button = Button(
            self.add_win,
            image=doorbell_image,
            width=100,
            height=100,
            command=lambda: self.add_doorbell()
        )
        doorbell_button.image = doorbell_image
        doorbell_button.grid(column=2, row=2, padx=20, pady=(5, 0))

    def add_plug_consumption(self):
        consumption_rate_label = Label(
            self.add_win,
            text="Set Consumption Rate"
        )
        consumption_rate_label.grid(column=1, row=3, pady=(10, 0))

        add_consumption_rate_spinbox = Spinbox(
            self.add_win,
            from_=0,
            to=150,
            increment=1,
            width=4,
            validate="key",
            validatecommand=(self.add_win.register(validate_entry), "%P")
        )
        add_consumption_rate_spinbox.grid(column=1, row=5, pady=(10, 0))

        consumption_rate_confirm_button = Button(
            self.add_win,
            text="Confirm",
            command=lambda: self.confirm_new_plug(
                add_consumption_rate_spinbox,
                consumption_rate_label,
                consumption_rate_confirm_button
            )
        )
        consumption_rate_confirm_button.grid(column=1, row=6, pady=(10, 0))

    def confirm_new_plug(self, consumption_rate_spinbox, consumption_rate_label, consumption_rate_confirm_button):
        consumption_rate = consumption_rate_spinbox.get()
        self.home.add_device(SmartPlug(consumption_rate))
        self.update_widgets()

        consumption_rate_label.destroy()
        consumption_rate_spinbox.destroy()
        consumption_rate_confirm_button.destroy()

    def add_doorbell(self):
        self.home.add_device(SmartDoorBell())
        self.update_widgets()

    def save_device_list(self):
        file_save_location = filedialog.asksaveasfilename(
            defaultextension=".csv",
            parent=self.win,
            filetypes=[('CSV Files', '*.csv')]
        )

        if not file_save_location:
            return

        # Used try and except on saving as when already open, you will get an error if you overwrite.
        try:
            with open(file_save_location, "w") as file:
                devices_to_save = []

                for device in self.home.get_devices():
                    if isinstance(device, SmartPlug):
                        devices_to_save.append(["Plug", device.get_switched_on(), device.get_consumption_rate()])
                    else:
                        devices_to_save.append(["Doorbell", device.get_switched_on(), device.get_option()])

                for row in devices_to_save:
                    row_device = ','.join(map(str, row))
                    file.write(row_device + '\n')

        except PermissionError:  # Only appears when trying to overwrite an open file.
            messagebox.showinfo(
                "Uh Oh! D:",
                "The selected file is currently in use by an application."
            )

    def load_device_list(self):
        file_load_location = filedialog.askopenfilename(
            defaultextension=".csv",
            parent=self.win,
            filetypes=[('CSV Files', '*.csv')]
        )

        if not file_load_location:
            return

        with open(file_load_location, "r") as file:
            devices_to_load = [line.strip().split(',') for line in file]

        if devices_to_load == [['']]:
            messagebox.showinfo(
                "Uh Oh! D:",
                "Empty File. Please select a valid device file."
            )

        else:
            temp_new_devices = []

            for i, device in enumerate(devices_to_load):
                if len(device) != 3:
                    messagebox.showinfo(
                       "Uh Oh! D:",
                       f"Invalid entry at line {i + 1}. Each record must have 3 columns."
                    )
                    break
                    
                device_class = device[0].strip()
                option1 = device[1].strip().lower()
                option2 = device[2].strip().lower()

                if device_class == "Plug" and option1 in ["true", "false"] and option2.isdigit() and 0 <= int(
                        option2) <= 150:
                    new_device = SmartPlug(option2)
                    temp_new_devices.append(new_device)

                    if option1 == "true":
                        new_device.toggle_switch()

                elif device_class == "Doorbell" and option1 in ["true", "false"] and option2 in ["true", "false"]:
                    new_device = SmartDoorBell()
                    temp_new_devices.append(new_device)

                    if option1 == "true":
                        new_device.toggle_switch()

                    if option2 == "true":
                        new_device.set_option(True)

                else:
                    messagebox.showinfo(
                        "Uh Oh!",
                        f"Invalid entry at line {i + 1}. Please check the format of your entries."
                    )
                    break

            else:  # Only entered if the for loop is NOT broken out of.
                self.home.devices = []

                for device in temp_new_devices:
                    self.home.add_device(device)

            self.update_widgets()


def setup_home():
    home = SmartHome()

    print('''Available Device Types:
    [0] - Smart Plug
    [1] - Smart Doorbell
Add 5 devices by referencing their index.''')

    for counter in range(5):
        index = input("Please enter the index of the device you'd like to add: ")

        while index not in ["0", "1"]:
            print("Invalid argument. Please enter a valid catalog index.")
            index = input("Please enter the index of the device you'd like to add: ")

        if index == "0":
            rate = input("Please enter the consumption rate of your smart plug: ")

            while not rate.isdigit() or int(rate) < 0 or int(rate) > 150:
                print("Invalid argument. Please enter a valid number.")
                rate = input("Please enter the consumption rate of your smart plug: ")

            print(f"Added a Smart Plug device with a consumption rate of {rate}.")
            home.add_device(SmartPlug(int(rate)))

        else:
            print("Added a Smart Doorbell device.")
            home.add_device(SmartDoorBell())

    return home


def validate_entry(text):
    if text.isdigit() or not text:
        if text and int(text) > 150:
            return False
        return True
    else:
        return False


def main():
    home = setup_home()
    system = SmartHomeSystem(home)

    system.run()


main()
