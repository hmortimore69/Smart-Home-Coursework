from backend import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class SmartHomeSystem:
    def __init__(self, home):
        self.home = home

        # Initialise all objects needed for future assignment and manipulation
        self.accessibility_win = None
        self.edit_win = None
        self.add_win = None
        self.clock_label = None
        self.device_schedule = []

        self.win = Tk()
        self.win.title("Smart Home System")

        self.main_frame = Frame(self.win)
        self.main_frame.grid(column=0, row=0, padx=10, pady=10)

        self.create_widget_frame = Frame(self.main_frame)
        self.create_widget_frame.grid(column=0, row=2, columnspan=5)

        # Create all images and resize to appropriate sizes.
        self.plug_image = PhotoImage(file="images/plug.png")
        self.plug_image = self.plug_image.subsample(
            self.plug_image.width() // 100,
            self.plug_image.height() // 100
        )

        self.doorbell_image = PhotoImage(file="images/doorbell.png")
        self.doorbell_image = self.doorbell_image.subsample(
            self.doorbell_image.width() // 100,
            self.doorbell_image.height() // 100
        )

        # Initial colouring and styling
        self.background_colour = "#66b2b2"
        self.widget_background_colour = "#008080"
        self.image_accent_colour = "#b2d8d8"

        # Assign default styling
        self.win.configure(bg=self.background_colour)
        self.main_frame.configure(bg=self.background_colour)
        self.create_widget_frame.configure(bg=self.widget_background_colour)

        self.win.resizable(False, False)

    def run(self):
        self.create_widgets()
        self.create_device_widgets()

        self.win.mainloop()

    def update_device_widgets(self):
        # Clear the create_widget_frame
        for child in self.create_widget_frame.winfo_children():
            child.destroy()

        self.create_device_widgets()

    def update_clock(self):
        time = self.clock_label.cget("text")[6:-3]
        time = f"{('0' if time == '23' else str(int(time) + 1)).zfill(2)}:00"

        self.clock_label.config(text=f"Time: {time}")
        self.win.after(3000, self.update_clock)

    def create_widgets(self):
        turn_on_all_button = Button(
            self.main_frame,
            text="Turn On All",
            command=lambda: self.turn_on_all_button_clicked()
        )
        turn_on_all_button.grid(column=0, row=0, padx=(10, 0), pady=(0, 10))

        turn_off_all_button = Button(
            self.main_frame,
            text="Turn Off All",
            command=lambda: self.turn_off_all_button_clicked()

        )
        turn_off_all_button.grid(column=1, row=0, padx=(20, 0), pady=(0, 10))

        save_devices = Button(
            self.main_frame,
            text="Save Devices",
            command=lambda: self.save_device_list()
        )
        save_devices.grid(column=3, row=0, pady=(0, 10))

        load_devices = Button(
            self.main_frame,
            text="Load Devices",
            command=lambda: self.load_device_list()
        )
        load_devices.grid(column=4, row=0, pady=(0, 10))

        add_device = Button(
            self.main_frame,
            text="Add Device",
            command=self.add_device_button_clicked,
            width=20
        )
        add_device.grid(column=2, row=len(self.home.get_devices()) + 1, pady=(10, 0))

        self.clock_label = Label(
            self.main_frame,
            text="Time: 00:00",
        )
        self.clock_label.grid(column=2, row=0, pady=(0, 10))
        self.clock_label.after(3000, self.update_clock)

        accessibility_label = Button(
            self.main_frame,
            text="Accessibility Settings",
            command=lambda: self.accessibility_settings()
        )
        accessibility_label.grid(column=4, row=len(self.home.get_devices()) + 1, pady=(10, 0))

    def create_device_widgets(self):
        curr_row = 0
        curr_col = 0

        # Create the 5 devices
        for i, device in enumerate(self.home.get_devices()):
            device_status = "On" if device.get_switched_on() else "Off"

            if i % 7 == 0:
                curr_row += 4
                curr_col = 0

            if isinstance(device, SmartPlug):
                plug_label = Button(
                    self.create_widget_frame,
                    image=self.plug_image,
                    width=100,
                    height=100,
                    command=lambda n=i: self.toggle_switch_button_clicked(n)
                )
                plug_label.image = self.plug_image  # Maintain reference to avoid python garbage collection.
                plug_label.grid(column=curr_col, row=curr_row, padx=10, pady=(10, 5))
                plug_label.configure(bg="#4bad6a" if device.get_switched_on() else "#db4d4d")

                device_label = Label(
                    self.create_widget_frame,
                    text=f"Status: {device_status}\n Consumption Rate: {device.get_consumption_rate()}"
                )
                device_label.grid(column=curr_col, row=curr_row + 1, padx=10, pady=(0, 2))
                device_label.configure(bg=self.widget_background_colour)

            else:  # Else enters if the device is a doorbell.
                device_option = "On" if device.get_option() else "Off"

                doorbell_button = Button(
                    self.create_widget_frame,
                    image=self.doorbell_image,
                    width=100,
                    height=100,
                    borderwidth=2,
                    command=lambda n=i: self.toggle_switch_button_clicked(n)
                )
                doorbell_button.image = self.doorbell_image
                doorbell_button.grid(column=curr_col, row=curr_row, padx=10, pady=(10, 2))
                doorbell_button.configure(bg="#4bad6a" if device.get_switched_on() else "#db4d4d")

                device_label = Label(
                    self.create_widget_frame,
                    text=f"Status: {device_status}\n Sleep Mode: {device_option}"
                )
                device_label.grid(column=curr_col, row=curr_row + 1, padx=10, pady=(0, 2))
                device_label.configure(bg=self.widget_background_colour)

            edit_option = Button(
                self.create_widget_frame,
                text="Edit Device",
                command=lambda n=i: self.edit_device_button_clicked(n)
            )
            edit_option.grid(column=curr_col, row=curr_row + 2, padx=10, pady=(0, 2))

            remove_device = Button(
                self.create_widget_frame,
                text="Delete Device",
                command=lambda n=i: self.delete_device_button_clicked(n)
            )
            remove_device.grid(column=curr_col, row=curr_row + 3, padx=10, pady=(0, 10))

            curr_col += 1

    def turn_on_all_button_clicked(self):
        self.home.turn_on_all()
        self.update_device_widgets()

    def turn_off_all_button_clicked(self):
        self.home.turn_off_all()
        self.update_device_widgets()

    def toggle_switch_button_clicked(self, i):
        self.home.toggle_switch_at_index(i)
        self.update_device_widgets()

    def edit_device_button_clicked(self, i):
        self.edit_win = Toplevel(self.win)
        self.edit_win.configure(bg=self.background_colour)
        self.edit_win.resizable(False, False)

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
        self.update_device_widgets()

    def set_plug_consumption(self, i, value):
        self.home.devices[i].set_consumption_rate(value)
        self.edit_win.destroy()
        self.update_device_widgets()

    def delete_device_button_clicked(self, i):
        self.home.remove_device(i)
        self.update_device_widgets()

    def add_device_button_clicked(self):
        self.add_win = Toplevel(self.win)
        self.add_win.configure(bg=self.background_colour, padx=10, pady=10)
        self.add_win.resizable(False, False)

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
            image=self.plug_image,
            width=100,
            height=100,
            command=lambda: self.add_plug_consumption()
        )
        plug_button.image = self.plug_image  # Maintain reference to avoid python garbage collection.
        plug_button.grid(column=1, row=2, padx=20, pady=(5, 0))

        doorbell_button = Button(
            self.add_win,
            image=self.doorbell_image,
            width=100,
            height=100,
            command=lambda: self.add_doorbell()
        )
        doorbell_button.image = self.doorbell_image
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
        self.update_device_widgets()

        consumption_rate_label.destroy()
        consumption_rate_spinbox.destroy()
        consumption_rate_confirm_button.destroy()

    def add_doorbell(self):
        self.home.add_device(SmartDoorBell())
        self.update_device_widgets()

    def save_device_list(self):
        file_save_location = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialdir="/saves",
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
                "Uh Oh! :(",
                "The selected file is currently in use by another application."
            )

    def load_device_list(self):
        file_load_location = filedialog.askopenfilename(
            defaultextension=".csv",
            initialdir="/saves",
            parent=self.win,
            filetypes=[('CSV Files', '*.csv')]
        )

        if not file_load_location:
            return

        with open(file_load_location, "r") as file:
            devices_to_load = [line.strip().split(',') for line in file]

        if devices_to_load == [['']]:
            messagebox.showinfo(
                "Uh Oh! :(",
                "Empty File. Please select a valid device file."
            )

        else:
            temp_new_devices = []
            self.device_schedule = []

            for i, device in enumerate(devices_to_load):
                if len(device) < 3:
                    messagebox.showinfo(
                       "Uh Oh! :(",
                       f"Invalid entry at line {i + 1}. Each record must have 3 columns."
                    )
                    break

                if len(device) > 3:
                    self.device_schedule.append(device[3:])

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
                        "Uh Oh! :(",
                        f"Invalid entry at line {i + 1}. Please check the format of your entries."
                    )
                    break

            else:  # Only entered if the for loop is NOT broken out of.
                self.home.devices = []

                for device in temp_new_devices:
                    self.home.add_device(device)

            self.update_device_widgets()

    def accessibility_settings(self):
        self.accessibility_win = Toplevel(self.win)
        self.accessibility_win.config(bg=self.background_colour)
        self.accessibility_win.resizable(False, False)


def setup_home():
    home = SmartHome()

    print('''Available Device Types:
    [0] - Smart Plug
    [1] - Smart Doorbell
Add 5 devices by referencing their index.''')

    for counter in range(5):
        index = input("Please enter the index of the device you'd like to add: ")

        while index not in ["0", "1"]:
            print("Invalid argument. Please enter a valid catalogue index.")
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
