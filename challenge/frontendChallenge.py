from backendChallenge import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import ttk


class SmartHomeSystem:
    def __init__(self, home):
        self.home = home

        # Initialise all objects needed for future assignment and manipulation
        self.main_frame = None
        self.create_widget_frame = None
        self.accessibility_win = None
        self.device_schedular_win = None
        self.add_win = None
        self.clock_callback = None
        self.theme = "light"

        self.win = Tk()
        self.win.title("Smart Home System")

        # Create all images and resize to appropriate sizes.
        self.plug_image = resize_image("images/plug.png", 6, 6)
        self.doorbell_image = resize_image("images/doorbell.png", 3, 3)
        self.delete_image = resize_image("images/cross.png", 26, 26)

        # Initial colouring and styling
        self.background_colour = "#D3D3D3"
        self.widget_background_colour = "#b6b6b6"
        self.button_colour = "#ffffff"
        self.text_colour = "black"

        self.font_final = ("Ariel", 9)

        style = ttk.Style()  # Change combobox styling for later on to prevent duplicate themes.
        style.theme_create("custom_style", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": self.widget_background_colour,
                    "selectforeground": self.text_colour,
                    "fieldbackground": self.widget_background_colour,
                    "foreground": self.button_colour,
                    "readonlybackground": self.widget_background_colour
                }
            }
        })
        style.theme_use("custom_style")

        self.win.configure(bg=self.background_colour)

        self.win.resizable(False, False)

    def run(self):
        self.create_interface_widgets()
        self.create_device_widgets()

        self.win.mainloop()

    def update_all_widgets(self):  # Updates every widget in the window
        for child in self.win.winfo_children():
            child.destroy()

        self.create_interface_widgets()
        self.create_device_widgets()

    def update_device_widgets(self):  # Updates all device objects
        # Clear the create_widget_frame
        for child in self.create_widget_frame.winfo_children():
            child.destroy()

        self.create_device_widgets()

    def update_single_device(self, i, row, col):  # Updates only one device label
        device = self.home.get_devices()[i]
        device_status = "On" if self.home.get_devices()[i].get_switched_on() else "Off"

        device_label = self.create_widget_frame.grid_slaves(row=row + 1, column=col)[0]
        device_image_colour = "#4bad6a" if device.get_switched_on() else "#db4d4d"
        icon_background = self.create_widget_frame.grid_slaves(row=row, column=col)[0]
        delete_icon_background = self.create_widget_frame.grid_slaves(row=row, column=col)[1]

        icon_background["bg"] = device_image_colour
        delete_icon_background["bg"] = device_image_colour

        if isinstance(device, SmartDoorBell):
            device_option_status = "On" if self.home.get_devices()[i].get_option() else "Off"
            device_label["text"] = f"Status: {device_status}\n Sleep Mode: {device_option_status}"
        else:
            device_label["text"] = f"Status: {device_status}\n Consumption: {device.get_consumption_rate()}"

    def update_clock(self, clock):
        if not clock.winfo_exists():
            return

        time = clock.cget("text")[6:-3]
        time = f"{('0' if time == '23' else str(int(time) + 1)).zfill(2)}:00"

        clock.config(text=f"Time: {time}")
        self.win.after(3000, lambda: self.update_clock(clock))

    def create_interface_widgets(self):
        self.main_frame = Frame(self.win)
        self.main_frame.grid(column=0, row=0, padx=10, pady=10)
        self.main_frame.configure(bg=self.background_colour)

        self.create_widget_frame = Frame(self.main_frame)
        self.create_widget_frame.grid(column=0, row=2, columnspan=5)
        self.create_widget_frame.configure(bg=self.widget_background_colour)

        if self.clock_callback is not None:
            self.win.after_cancel(self.clock_callback)
            self.clock_callback = None

        turn_on_all_button = Button(
            self.main_frame,
            text="Turn On All Devices",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=lambda: self.turn_on_all_button_clicked()
        )
        turn_on_all_button.grid(column=0, row=0, padx=10, pady=(0, 10))

        turn_off_all_button = Button(
            self.main_frame,
            text="Turn Off All Devices",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=lambda: self.turn_off_all_button_clicked()
        )
        turn_off_all_button.grid(column=1, row=0, padx=10, pady=(0, 10))

        save_devices = Button(
            self.main_frame,
            text="Save Devices",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=lambda: self.save_device_list()
        )
        save_devices.grid(column=3, row=0, padx=10, pady=(0, 10), sticky="ew")

        load_devices = Button(
            self.main_frame,
            text="Load Devices",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=lambda: self.load_device_list()
        )
        load_devices.grid(column=4, row=0, padx=10, pady=(0, 10), sticky="ew")

        add_device = Button(
            self.main_frame,
            text="Add Device",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=self.add_device_button_clicked,
            width=20
        )
        add_device.grid(column=2, row=len(self.home.get_devices()) + 1, pady=(10, 0))

        clock_label = Label(
            self.main_frame,
            text="Time: 00:00",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final
        )
        clock_label.grid(column=2, row=0, pady=(0, 10))
        self.clock_callback = self.win.after(3000, lambda: self.update_clock(clock_label))

        open_schedule_win = Button(
            self.main_frame,
            text="Device Scheduler",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=lambda: self.device_scheduler(),
        )
        open_schedule_win.grid(column=0, row=len(self.home.get_devices()) + 1, pady=(10, 0))

        open_accessibility_win = Button(
            self.main_frame,
            text="Accessibility Settings",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=lambda: self.accessibility_settings()
        )
        open_accessibility_win.grid(column=4, row=len(self.home.get_devices()) + 1, pady=(10, 0))

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
                rate_var = IntVar()
                rate_var.set(device.get_consumption_rate())

                plug_label = Button(
                    self.create_widget_frame,
                    image=self.plug_image,
                    width=100,
                    height=100,
                    command=lambda n=i, row=curr_row, col=curr_col: self.toggle_switch_button_clicked(n, row, col)
                )
                plug_label.image = self.plug_image  # Maintain reference to avoid python garbage collection.
                plug_label.grid(column=curr_col, row=curr_row, padx=10, pady=(10, 5))
                plug_label.configure(bg="#4bad6a" if device.get_switched_on() else "#db4d4d")

                device_label = Label(
                    self.create_widget_frame,
                    text=f"Status: {device_status}\n Consumption: {device.get_consumption_rate()}",
                    fg=self.text_colour,
                    font=self.font_final
                )
                device_label.grid(column=curr_col, row=curr_row + 1, padx=10, pady=(0, 2))
                device_label.configure(bg=self.widget_background_colour)

                consumption_rate_edit = Spinbox(
                    self.create_widget_frame,
                    bg=self.button_colour,
                    fg=self.text_colour,
                    font=self.font_final,
                    buttonbackground=self.button_colour,
                    from_=0,
                    to=150,
                    increment=1,
                    width=4,
                    textvariable=rate_var,
                    validate="key",
                    validatecommand=(self.create_widget_frame.register(validate_consumption_rate_entry), "%P"),
                    command=lambda n=i, row=curr_row, col=curr_col: self.set_plug_consumption(
                        n,
                        consumption_rate_edit.get(),
                        row,
                        col
                    ),
                )
                consumption_rate_edit.grid(column=curr_col, row=curr_row + 2, padx=10, pady=(0, 10))

            else:  # Else enters if the device is a doorbell.
                device_option_status = "On" if device.get_option() else "Off"

                doorbell_button = Button(
                    self.create_widget_frame,
                    image=self.doorbell_image,
                    width=100,
                    height=100,
                    borderwidth=2,
                    command=lambda n=i, row=curr_row, col=curr_col: self.toggle_switch_button_clicked(n, row, col)
                )
                doorbell_button.image = self.doorbell_image
                doorbell_button.grid(column=curr_col, row=curr_row, padx=10, pady=(10, 5))
                doorbell_button.configure(bg="#4bad6a" if device.get_switched_on() else "#db4d4d")

                device_label = Label(
                    self.create_widget_frame,
                    text=f"Status: {device_status}\n Sleep Mode: {device_option_status}",
                    fg=self.text_colour,
                    font=self.font_final
                )
                device_label.grid(column=curr_col, row=curr_row + 1, padx=10)
                device_label.configure(bg=self.widget_background_colour)

                sleep_mode_edit = Button(
                    self.create_widget_frame,
                    text=f"Toggle Sleep Mode",
                    bg=self.button_colour,
                    font=self.font_final,
                    fg=self.text_colour,
                    command=lambda n=i, row=curr_row, col=curr_col: self.toggle_sleep_mode_button_clicked(n, row, col)
                )
                sleep_mode_edit.grid(column=curr_col, row=curr_row + 2, padx=10, pady=(0, 10))

            remove_device = Button(
                self.create_widget_frame,
                image=self.delete_image,
                width=10,
                height=10,
                relief="flat",
                command=lambda n=i: self.delete_device_button_clicked(n)
            )
            remove_device.image = self.delete_image
            remove_device.grid(column=curr_col, row=curr_row, padx=(85, 0), pady=(12, 0), sticky="N")
            remove_device.configure(bg="#4bad6a" if device.get_switched_on() else "#db4d4d")

            curr_col += 1

    def turn_on_all_button_clicked(self):
        self.home.turn_on_all()
        self.update_device_widgets()

    def turn_off_all_button_clicked(self):
        self.home.turn_off_all()
        self.update_device_widgets()

    def toggle_switch_button_clicked(self, i, row, col):
        self.home.toggle_switch_at_index(i)
        self.update_single_device(i, row, col)

    def toggle_sleep_mode_button_clicked(self, i, row, col):
        self.home.get_devices()[i].toggle_option()
        self.update_single_device(i, row, col)

    def set_plug_consumption(self, i, value, row, col):
        self.home.devices[i].set_consumption_rate(value)
        self.update_single_device(i, row, col)

    def delete_device_button_clicked(self, i):
        self.home.remove_device(i)
        self.update_device_widgets()

    def add_device_button_clicked(self):
        self.add_win = Toplevel(self.win)
        self.add_win.configure(bg=self.background_colour, padx=10, pady=10)
        self.add_win.resizable(False, False)

        add_question_label = Label(
            self.add_win,
            text="Would you like to add a Smart Doorbell or a Smart Plug?",
            bg=self.background_colour,
            fg=self.text_colour,
            font=self.font_final
        )
        add_question_label.grid(row=0, column=1, columnspan=2)

        add_smart_plug = Label(
            self.add_win,
            text="Smart Plug",
            bg=self.background_colour,
            fg=self.text_colour,
            font=self.font_final
        )
        add_smart_plug.grid(column=1, row=1, pady=(10, 5), padx=10)

        add_smart_doorbell = Label(
            self.add_win,
            text="Smart Doorbell",
            bg=self.background_colour,
            fg=self.text_colour,
            font=self.font_final
        )
        add_smart_doorbell.grid(column=2, row=1, pady=(10, 5), padx=10)

        plug_button = Button(
            self.add_win,
            image=self.plug_image,
            bg=self.button_colour,
            width=100,
            height=100,
            command=lambda: self.add_plug_consumption()
        )
        plug_button.image = self.plug_image  # Maintain reference to avoid python garbage collection.
        plug_button.grid(column=1, row=2, padx=20, pady=(5, 0))

        doorbell_button = Button(
            self.add_win,
            image=self.doorbell_image,
            bg=self.button_colour,
            width=100,
            height=100,
            command=lambda: self.add_doorbell()
        )
        doorbell_button.image = self.doorbell_image
        doorbell_button.grid(column=2, row=2, padx=20, pady=(5, 0))

    def add_plug_consumption(self):
        rate_label = Label(
            self.add_win,
            text="Set Consumption Rate",
            bg=self.background_colour,
            fg=self.text_colour,
            font=self.font_final
        )
        rate_label.grid(column=1, row=3, pady=(10, 0))

        add_rate_spinbox = Spinbox(
            self.add_win,
            font=self.font_final,
            bg=self.button_colour,
            buttonbackground=self.button_colour,
            fg=self.text_colour,
            from_=0,
            to=150,
            increment=1,
            width=4,
            validate="key",
            validatecommand=(self.add_win.register(validate_consumption_rate_entry), "%P")
        )
        add_rate_spinbox.grid(column=1, row=5, pady=(10, 0))

        rate_confirm_button = Button(
            self.add_win,
            text="Confirm",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            command=lambda: self.confirm_new_plug(
                add_rate_spinbox,
                rate_label,
                rate_confirm_button
            )
        )
        rate_confirm_button.grid(column=1, row=6, pady=(10, 0))

    def confirm_new_plug(self, rate_spinbox, rate_label, rate_confirm_button):
        rate = rate_spinbox.get()
        self.home.add_device(SmartPlug(rate))
        self.update_device_widgets()

        rate_label.destroy()
        rate_spinbox.destroy()
        rate_confirm_button.destroy()

    def add_doorbell(self):
        self.home.add_device(SmartDoorBell())
        self.update_device_widgets()

    def save_device_list(self):
        file_save_location = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialdir="./saves",
            parent=self.win,
            filetypes=[("CSV Files", "*.csv")]
        )

        if not file_save_location:
            return

        # Used try and except on saving as when already open, you will get an error if you overwrite.
        try:
            with open(file_save_location, "w") as file:
                devices_to_save = []

                for device in self.home.get_devices():
                    if isinstance(device, SmartPlug):
                        devices_to_save.append([
                            "Plug",
                            device.get_switched_on(),
                            device.get_consumption_rate()
                        ])

                    else:
                        devices_to_save.append([
                            "Doorbell",
                            device.get_switched_on(),
                            device.get_option()
                        ])

                for row in devices_to_save:
                    row_device = ",".join(map(str, row))
                    file.write(row_device + "\n")

        except PermissionError:
            messagebox.showinfo(
                "Uh Oh! :(",
                "You do not have the appropriate permissions to save this file."
            )

    def load_device_list(self):
        file_load_location = filedialog.askopenfilename(
            defaultextension=".csv",
            initialdir="./saves",
            parent=self.win,
            filetypes=[("CSV Files", "*.csv")]
        )

        if not file_load_location:
            return

        with open(file_load_location, "r") as file:
            devices_to_load = [line.strip().split(",") for line in file]

        if devices_to_load == [[""]]:
            messagebox.showinfo(
                "Uh Oh! :(",
                "Empty File. Please select a valid device file."
            )

        else:
            temp_new_devices = []

            for i, device in enumerate(devices_to_load):
                if len(device) < 3:
                    messagebox.showinfo(
                        "Uh Oh! :(",
                        f"Invalid entry at line {i + 1}. Each record must have 3 columns."
                    )
                    break

                device_class = device[0].strip()
                option1 = device[1].strip().lower()
                option2 = device[2].strip().lower()

                if device_class == "Plug" and option1 in ["true", "false"] and 0 <= int(option2) <= 150:
                    new_device = SmartPlug(option2)
                    temp_new_devices.append(new_device)

                    if option1 == "true":
                        new_device.toggle_switch()

                elif device_class == "Doorbell" and option1 == option2 and option1 in ["true", "false"]:
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

        light_mode_image = resize_image("images/light_mode.png", 2, 2)
        dark_mode_image = resize_image("images/dark_mode.png", 2, 2)
        slider_image = resize_image("images/slider.png", 2, 2)

        custom_bg_colour = StringVar()
        custom_accent_colour = StringVar()
        custom_font_size = IntVar()
        custom_text_colour = StringVar()
        theme_value = StringVar()

        custom_bg_colour.set(self.background_colour)
        custom_accent_colour.set(self.widget_background_colour)
        custom_font_size.set(self.font_final[1])
        custom_text_colour.set(self.text_colour)
        theme_value.set(self.theme)

        light_mode_button = Radiobutton(
            self.accessibility_win,
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
            selectcolor=self.widget_background_colour,
            image=light_mode_image,
            compound="top",
            text="Light Mode",
            value="light",
            variable=theme_value
        )
        light_mode_button.image = light_mode_image
        light_mode_button.grid(column=1, row=1, pady=10, padx=10)

        dark_mode_button = Radiobutton(
            self.accessibility_win,
            bg=self.button_colour,
            fg=self.text_colour,
            selectcolor=self.widget_background_colour,
            font=self.font_final,
            image=dark_mode_image,
            compound="top",
            text="Dark Mode",
            value="dark",
            variable=theme_value
        )
        dark_mode_button.image = dark_mode_image
        dark_mode_button.grid(column=2, row=1, pady=10, padx=10)

        custom_mode_button = Radiobutton(
            self.accessibility_win,
            bg=self.button_colour,
            fg=self.text_colour,
            selectcolor=self.widget_background_colour,
            font=self.font_final,
            image=slider_image,
            compound="top",
            text="Custom",
            value="custom",
            variable=theme_value
        )
        custom_mode_button.image = slider_image
        custom_mode_button.grid(column=3, row=1, pady=10, padx=10)

        custom_background_label = Label(
            self.accessibility_win,
            text="Custom Background Colour:",
            bg=self.background_colour,
            font=self.font_final,
            fg=self.text_colour
        )
        custom_background_label.grid(column=4, row=1, pady=10, padx=(10, 5), sticky="NE")

        custom_background_button = Button(
            self.accessibility_win,
            width=2,
            bg=custom_bg_colour.get(),
            command=lambda: ask_colour(custom_bg_colour, custom_background_button)
        )
        custom_background_button.grid(column=5, row=1, pady=10, padx=(0, 10), sticky="NW")

        custom_accent_label = Label(
            self.accessibility_win,
            text="Custom Accent Colour:",
            font=self.font_final,
            bg=self.background_colour,
            fg=self.text_colour
        )
        custom_accent_label.grid(column=4, row=1, pady=10, padx=(10, 5), sticky="E")

        custom_accent_button = Button(
            self.accessibility_win,
            width=2,
            bg=custom_accent_colour.get(),
            command=lambda: ask_colour(custom_accent_colour, custom_accent_button)
        )
        custom_accent_button.grid(column=5, row=1, pady=10, padx=(0, 10), sticky="W")

        custom_text_colour_label = Label(
            self.accessibility_win,
            bg=self.background_colour,
            font=self.font_final,
            fg=self.text_colour,
            text="Custom Text Colour:"
        )
        custom_text_colour_label.grid(column=4, row=1, pady=10, padx=(10, 5), sticky="SE")

        custom_text_colour_button = Button(
            self.accessibility_win,
            bg=self.text_colour,
            width=2,
            command=lambda: ask_colour(custom_text_colour, custom_text_colour_button)
        )
        custom_text_colour_button.grid(column=5, row=1, pady=10, padx=(0, 10), sticky="SW")

        custom_font_size_button = Scale(
            self.accessibility_win,
            font=self.font_final,
            fg=self.text_colour,
            label="Font Size:",
            bd=0,
            bg=self.widget_background_colour,
            from_=5,
            to=15,
            length=300,
            orient=HORIZONTAL,
            variable=custom_font_size
        )
        custom_font_size_button.grid(column=1, row=2, pady=10, padx=10, sticky="S", columnspan=3)

        apply_changes_button = Button(
            self.accessibility_win,
            fg=self.text_colour,
            text="Apply Changes",
            bg=self.button_colour,
            font=self.font_final,

            #  IDE screamed at me if I didn't do it like this for PEP8. D:
            command=lambda theme=theme_value,
            bg_colour=custom_bg_colour,
            bg_accent=custom_accent_colour,
            font_size=custom_font_size,
            font_colour=custom_text_colour: self.update_styling(
                theme,
                bg_colour,
                bg_accent,
                font_size,
                font_colour
            )
        )
        apply_changes_button.grid(column=2, row=3, pady=10, padx=10)

    def update_styling(self, theme, bg_colour, bg_accent, font_size, font_colour):
        self.theme = theme.get()
        font_size = font_size.get()
        self.font_final = ("Ariel", font_size)

        if self.theme == "light":
            self.background_colour = "#D3D3D3"
            self.widget_background_colour = "#b6b6b6"
            self.button_colour = "#ffffff"
            self.text_colour = "#000000"

        elif self.theme == "dark":
            self.background_colour = "#292E32"
            self.widget_background_colour = "#40474F"
            self.button_colour = "#5a636b"
            self.text_colour = "#ffffff"

        elif self.theme == "custom":
            self.background_colour = bg_colour.get()
            self.widget_background_colour = bg_accent.get()
            self.button_colour = "#ffffff"
            self.text_colour = font_colour.get()

        self.accessibility_win.destroy()
        self.win.configure(bg=self.background_colour)
        self.update_all_widgets()

    def device_scheduler(self):
        def update_add_event_button():
            add_event_to_schedule.configure(state="disabled" if option_menu.get() else "normal")

        self.device_schedular_win = Toplevel(self.win)
        self.device_schedular_win.config(bg=self.background_colour)
        self.device_schedular_win.resizable(False, False)

        current_schedule_frame = Frame(self.device_schedular_win)
        current_schedule_frame.grid(column=3, row=1, padx=10, sticky="N")
        current_schedule_frame.configure(background=self.widget_background_colour)

        option_choices = [f"Device #{i + 1}: {device.name}" for i, device in enumerate(self.home.get_devices())]

        choose_option = Label(
            self.device_schedular_win,
            text="Choose A Device:",
            font=self.font_final,
            fg=self.text_colour,
            bg=self.background_colour
        )
        choose_option.grid(column=1, row=0, padx=10, pady=(10, 2), sticky="SW")

        option_menu = ttk.Combobox(
            self.device_schedular_win,
            values=option_choices,
            width=23,
            state="readonly",
            font=self.font_final,
            validate="all",
            validatecommand=update_add_event_button,
            style="TCombobox"  # Use the custom style for the combobox
        )
        option_menu.grid(column=1, row=1, padx=10, pady=(0, 10))
        option_menu.bind(
            "<<ComboboxSelected>>",
            lambda event: self.load_device_schedule(current_schedule_frame, option_menu.get())
        )

        add_event_to_schedule = Button(
            self.device_schedular_win,
            text="Add Event",
            font=self.font_final,
            fg=self.text_colour,
            bg=self.background_colour,
            state="disabled",
            command=lambda: self.add_event_to_schedule(option_menu.get())
        )
        add_event_to_schedule.grid(column=1, row=3, padx=10, pady=(0, 10))

    def get_device_from_combobox(self, option):
        start_index = option.find("#") + 1
        end_index = option.find(":", start_index)
        device_index = int(option[start_index:end_index]) - 1
        device = self.home.get_devices()[device_index]

        return device

    def load_device_schedule(self, frame, option):
        chosen_device = self.get_device_from_combobox(option)
        device_schedule = chosen_device.get_schedule()

        curr_row = 0
        curr_col = 0

        if not device_schedule:
            empty_schedule = Label(
                frame,
                text="The Device's Schedule Is Empty.",
                font=self.font_final,
                fg=self.text_colour,
                background=self.background_colour
            )
            empty_schedule.grid(column=1, row=1)

        for i, device in enumerate(device_schedule):
            if i % 7 == 0:
                curr_row += 4
                curr_col = 0

    def add_event_to_schedule(self, option):
        add_event_win = Toplevel(self.device_schedular_win)
        add_event_win.configure(bg=self.background_colour)
        add_event_win.resizable(width=False, height=False)

        add_event_frame = Frame(add_event_win)
        add_event_frame.configure(background=self.widget_background_colour)
        add_event_frame.grid(column=1, row=1, padx=10, pady=10)

        set_power_var = BooleanVar()
        chosen_device = self.get_device_from_combobox(option)

        set_power_var.set(False)

        hours_label = Label(
            add_event_frame,
            text="Select the time for the event:",
            font=self.font_final,
            fg=self.text_colour,
            background=self.widget_background_colour
        )
        hours_label.grid(column=1, row=2, padx=10, pady=(10, 0))

        hours_combobox = ttk.Combobox(
            add_event_frame,
            values=[f"{str(i).zfill(2)}:00" for i in range(0, 24)],
            state="readonly"
        )
        hours_combobox.grid(column=1, row=3, padx=10, pady=10)
        hours_combobox.current(0)

        set_power_label = Label(
            add_event_frame,
            text="Device Power:",
            font=self.font_final,
            fg=self.text_colour,
            background=self.widget_background_colour
        )
        set_power_label.grid(column=3, row=2, padx=10, pady=(10, 0))

        set_power_on = Radiobutton(
            add_event_frame,
            text="On",
            variable=set_power_var,
            value=True,
            font=self.font_final,
            fg=self.text_colour,
            bg=self.button_colour,
            selectcolor=self.widget_background_colour,

        )
        set_power_on.grid(column=3, row=3, padx=(0, 50))

        set_power_off = Radiobutton(
            add_event_frame,
            text="Off",
            variable=set_power_var,
            value=False,
            font=self.font_final,
            fg=self.text_colour,
            bg=self.button_colour,
            selectcolor=self.widget_background_colour,
        )
        set_power_off.grid(column=3, row=3, padx=(50, 0))

        if isinstance(chosen_device, SmartPlug):
            set_event_rate_label = Label(
                add_event_frame,
                text="Set Consumption Rate",
                bg=self.widget_background_colour,
                fg=self.text_colour,
                font=self.font_final
            )
            set_event_rate_label.grid(column=5, row=2, padx=10, pady=(10, 0))

            set_event_rate_spinbox = Spinbox(
                add_event_frame,
                font=self.font_final,
                bg=self.button_colour,
                buttonbackground=self.button_colour,
                fg=self.text_colour,
                from_=0,
                to=150,
                increment=1,
                width=4,
                validate="key",
                validatecommand=(add_event_win.register(validate_consumption_rate_entry), "%P")
            )
            set_event_rate_spinbox.grid(column=5, row=3, padx=10)

        else:
            sleep_mode_var = BooleanVar()
            sleep_mode_var.set(False)

            set_event_sleep_mode_label = Label(
                add_event_frame,
                text="Set Sleep Mode Value:",
                bg=self.widget_background_colour,
                fg=self.text_colour,
                font=self.font_final
            )
            set_event_sleep_mode_label.grid(column=5, row=2, padx=10, pady=(10, 0))

            set_event_sleep_mode_on = Radiobutton(
                add_event_frame,
                text="On",
                variable=sleep_mode_var,
                value=True,
                font=self.font_final,
                fg=self.text_colour,
                bg=self.button_colour,
                selectcolor=self.widget_background_colour,

            )
            set_event_sleep_mode_on.grid(column=5, row=3, padx=(0, 50))

            set_event_sleep_mode_off = Radiobutton(
                add_event_frame,
                text="Off",
                variable=sleep_mode_var,
                value=False,
                font=self.font_final,
                fg=self.text_colour,
                bg=self.button_colour,
                selectcolor=self.widget_background_colour,
            )
            set_event_sleep_mode_off.grid(column=5, row=3, padx=(50, 0))

        event_confirm_button = Button(
            add_event_frame,
            text="Confirm",
            bg=self.button_colour,
            fg=self.text_colour,
            font=self.font_final,
        )
        event_confirm_button.grid(column=1, row=6, padx=10, pady=10)


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


def validate_consumption_rate_entry(text):
    if text.isdigit() or not text:
        if text and int(text) > 150:
            return False
        return True
    else:
        return False


def resize_image(image_path, width, height):
    image = PhotoImage(file=image_path)
    image = image.subsample(width, height)
    return image


def ask_colour(colour, button):
    colour_tuple = colorchooser.askcolor()

    colour.set(colour_tuple[1] if colour_tuple[1] else colour.get())
    button.configure(bg=colour.get(), fg="white" if colour.get() == "#000000" else "black")

    return


def main():
    home = setup_home()
    system = SmartHomeSystem(home)

    system.run()


main()
