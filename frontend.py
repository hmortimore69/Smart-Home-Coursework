from backend import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class SmartHomeSystem:
    def __init__(self, home):
        self.consumptionRateWindow = None
        self.editWin = None
        self.addWin = None

        self.home = home

        self.backgroundColour = "teal"

        self.win = Tk()
        self.win.title("Smart Home System")

        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(column=0, row=0, padx=10, pady=10)

        self.win.configure(bg=self.backgroundColour)
        self.mainFrame.configure(bg=self.backgroundColour)

    def run(self):
        self.createWidgets()
        self.win.mainloop()

    def updateWidgets(self):
        # Clear the mainFrame
        for child in self.mainFrame.winfo_children():
            child.destroy()

        self.createWidgets()

    def createWidgets(self):
        turnOnAllButton = Button(
            self.mainFrame,
            text="Turn On All",
            command=lambda: self.turnOnAllButtonClicked()
        )
        turnOnAllButton.grid(column=0, row=0, padx=(10, 100), pady=(0, 10))

        turnOffAllButton = Button(
            self.mainFrame,
            text="Turn Off All",
            command=lambda: self.turnOffAllButtonClicked()

        )
        turnOffAllButton.grid(column=0, row=0, padx=(100, 10), pady=(0, 10))

        saveDevices = Button(
            self.mainFrame,
            text="Save Devices",
            command=lambda: self.saveDeviceList()
        )
        saveDevices.grid(column=2, row=0, padx=(10, 0), pady=(0, 10))

        loadDevices = Button(
            self.mainFrame,
            text="Load Devices",
            command=lambda: self.loadDeviceList()
        )
        loadDevices.grid(column=3, row=0, padx=(10, 0), pady=(0, 10))

        # Initialise the 5 devices
        for i, device in enumerate(self.home.getDevices()):
            deviceStatus = "On" if device.getSwitchedOn() else "Off"

            if isinstance(device, SmartPlug):
                deviceLabel = Label(
                    self.mainFrame,
                    text=f"Smart Plug: {deviceStatus}, Consumption Rate: {device.getConsumptionRate()}"
                )
                deviceLabel.grid(column=0, row=i + 1, sticky="w")

            else:
                deviceOption = "On" if device.getOption() else "Off"

                deviceLabel = Label(
                    self.mainFrame,
                    text=f"Smart Doorbell: {deviceStatus}, Sleep Mode: {deviceOption}"
                )
                deviceLabel.grid(column=0, row=i + 1, sticky="w")

            togglePower = Button(
                self.mainFrame,
                text="Toggle Power",
                command=lambda n=i: self.toggleSwitchButtonClicked(n)
            )
            togglePower.grid(column=1, row=i + 1, padx=(10, 0))

            editOption = Button(
                self.mainFrame,
                text="Edit Device",
                command=lambda n=i: self.editDeviceButtonClicked(n)
            )
            editOption.grid(column=2, row=i + 1, padx=(10, 0))

            removeDevice = Button(
                self.mainFrame,
                text="Delete Device",
                command=lambda n=i: self.deleteDeviceButtonClicked(n)
            )
            removeDevice.grid(column=3, row=i + 1, padx=(10, 0))

        addDevice = Button(
            self.mainFrame,
            text="Add Device",
            command=self.addDeviceButtonClicked
        )
        addDevice.grid(column=0, row=len(self.home.getDevices()) + 1, pady=(10, 0))

    def turnOnAllButtonClicked(self):
        self.home.turnOnAll()
        self.updateWidgets()

    def turnOffAllButtonClicked(self):
        self.home.turnOffAll()
        self.updateWidgets()

    def toggleSwitchButtonClicked(self, i):
        self.home.toggleSwitch(i)
        self.updateWidgets()

    def editDeviceButtonClicked(self, i):
        self.editWin = Toplevel(self.win)
        self.editWin.configure(bg="teal")

        if isinstance(self.home.getDevices()[i], SmartPlug):
            consumptionRateVar = StringVar()
            consumptionRateVar.set(str(self.home.getDevices()[i].getConsumptionRate()))

            editLabel = Label(
                self.editWin,
                text="Set Consumption Rate"
            )
            editLabel.grid(column=0, row=0, pady=(10, 0))

            consumptionRateSpinbox = Spinbox(
                self.editWin,
                from_=0,
                to=150,
                increment=1,
                width=3,
                textvariable=consumptionRateVar,
                validate="key",
                validatecommand=(self.editWin.register(validateEntry), "%P")
            )
            consumptionRateSpinbox.grid(column=0, row=2, pady=(10, 0))

            consumptionRateConfirmButton = Button(
                self.editWin,
                text="Confirm",
                command=lambda n=i: self.setPlugConsumption(i, consumptionRateSpinbox.get())
            )
            consumptionRateConfirmButton.grid(column=0, row=6, padx=60, pady=(10, 10))

        else:
            optionValue = BooleanVar()
            optionValue.set(self.home.devices[i].getOption())

            editLabel = Label(
                self.editWin,
                text="Sleep Mode"
            )
            editLabel.grid(column=0, row=0, padx=60, pady=(10, 10))

            trueButton = Radiobutton(
                self.editWin,
                text="On",
                variable=optionValue,
                value=True
            )
            trueButton.grid(column=0, row=2, pady=(0, 5))

            falseButton = Radiobutton(
                self.editWin,
                text="Off",
                variable=optionValue,
                value=False
            )
            falseButton.grid(column=0, row=3)

            editConfirmButton = Button(
                self.editWin,
                text="Confirm",
                command=lambda n=i: self.setCustomDeviceOption(n, optionValue.get())
            )
            editConfirmButton.grid(column=0, row=6, padx=60, pady=(10, 10))

    def setCustomDeviceOption(self, i, value):
        self.home.devices[i].setOption(value)
        self.editWin.destroy()
        self.updateWidgets()

    def setPlugConsumption(self, i, value):
        self.home.devices[i].setConsumptionRate(value)
        self.editWin.destroy()
        self.updateWidgets()

    def deleteDeviceButtonClicked(self, i):
        self.home.removeDevice(i)
        self.updateWidgets()

    def addDeviceButtonClicked(self):
        self.addWin = Toplevel(self.win)
        self.addWin.configure(bg="teal", padx=10, pady=10)

        # Create light bulb image and resize to button size.
        plugImage = PhotoImage(file="images/plug.png")
        plugImage = plugImage.subsample(plugImage.width() // 100, plugImage.height() // 100)

        doorbellImage = PhotoImage(file="images/doorbell.png")
        doorbellImage = doorbellImage.subsample(doorbellImage.width() // 100, doorbellImage.height() // 100)

        addQuestionLabel = Label(
            self.addWin,
            text="Would you like to add a Smart Doorbell or a Smart Plug?"
        )
        addQuestionLabel.grid(row=0, column=1, columnspan=2)

        addSmartPlug = Label(
            self.addWin,
            text="Smart Plug"
        )
        addSmartPlug.grid(column=1, row=1, pady=(10, 5), padx=10)

        addSmartDoorbell = Label(
            self.addWin,
            text="Smart Doorbell"
        )
        addSmartDoorbell.grid(column=2, row=1, pady=(10, 5), padx=10)

        plugButton = Button(
            self.addWin,
            image=plugImage,
            width=100,
            height=100,
            command=lambda: self.addSmartPlugConsumption()
        )
        plugButton.image = plugImage  # Maintain reference to avoid python garbage collection.
        plugButton.grid(column=1, row=2, padx=20, pady=(5, 0))

        doorbellButton = Button(
            self.addWin,
            image=doorbellImage,
            width=100,
            height=100,
            command=lambda: self.addSmartDoorbell()
        )
        doorbellButton.image = doorbellImage
        doorbellButton.grid(column=2, row=2, padx=20, pady=(5, 0))

    def addSmartPlugConsumption(self):
        consumptionRateLabel = Label(
            self.addWin,
            text="Set Consumption Rate"
        )
        consumptionRateLabel.grid(column=1, row=3, pady=(10, 0))

        addConsumptionRateSpinbox = Spinbox(
            self.addWin,
            from_=0,
            to=150,
            increment=1,
            width=3,
            validate="key",
            validatecommand=(self.addWin.register(validateEntry), "%P")
        )
        addConsumptionRateSpinbox.grid(column=1, row=5, pady=(10, 0))

        consumptionRateConfirmButton = Button(
            self.addWin,
            text="Confirm",
            command=lambda: self.confirmNewSmartPlug(
                addConsumptionRateSpinbox,
                consumptionRateLabel,
                consumptionRateConfirmButton
            )
        )
        consumptionRateConfirmButton.grid(column=1, row=6, pady=(10, 0))

    def confirmNewSmartPlug(self, consumptionRateSpinbox, consumptionRateLabel, consumptionRateConfirmButton):
        consumptionRate = consumptionRateSpinbox.get()
        self.home.addDevice(SmartPlug(consumptionRate))
        self.updateWidgets()

        # Destroy the labels and buttons
        consumptionRateLabel.destroy()
        consumptionRateSpinbox.destroy()
        consumptionRateConfirmButton.destroy()

    def addSmartDoorbell(self):
        self.home.addDevice(SmartDoorBell())
        self.updateWidgets()

    def saveDeviceList(self):
        fileSaveLocation = filedialog.asksaveasfilename(
            defaultextension=".csv",
            parent=self.win,
            filetypes=[('CSV Files', '*.csv')]
        )

        # Used try and except on saving due to if the file is open, then you will get an error if you try to overwrite.
        try:
            with open(fileSaveLocation, "w") as file:
                devicesToSave = []

                for device in self.home.getDevices():
                    if isinstance(device, SmartPlug):
                        devicesToSave.append(["Plug", device.getSwitchedOn(), device.getConsumptionRate()])
                    else:
                        devicesToSave.append(["Doorbell", device.getSwitchedOn(), device.getOption()])

                for row in devicesToSave:
                    rowDevice = ','.join(map(str, row))
                    file.write(rowDevice + '\n')

        except PermissionError:  # Only appears when trying to overwrite an open file.
            messagebox.showinfo("Uh Oh!", "The selected file is currently in use by an application.")

        except FileNotFoundError:  # Take a guess
            return

    def loadDeviceList(self):
        fileLoadLocation = filedialog.askopenfilename(
            defaultextension=".csv",
            parent=self.win,
            filetypes=[('CSV Files', '*.csv')]
        )

        if not fileLoadLocation:
            return

        with open(fileLoadLocation, "r") as file:
            devicesToLoad = [line.strip().split(',') for line in file]

        if devicesToLoad == [['']]:
            messagebox.showinfo("Uh Oh!", "Empty File. Please select a valid device file.")

        else:
            tempNewDevices = []

            for i, device in enumerate(devicesToLoad):
                if len(device) != 3:
                    messagebox.showinfo(
                       "Uh Oh!",
                       f"Invalid entry at line {i + 1}. Each record must have 3 columns."
                    )
                    break
                deviceClass = device[0].strip()
                option1 = device[1].strip().lower()
                option2 = device[2].strip().lower()

                if deviceClass == "Plug" and option1 in ["true", "false"] and option2.isdigit():
                    newDevice = SmartPlug(option2)
                    tempNewDevices.append(newDevice)

                    if option1 == "true":
                        newDevice.toggleSwitch()

                elif deviceClass == "Doorbell" and option1 in ["true", "false"] and option2 in ["true", "false"]:
                    newDevice = SmartDoorBell()
                    tempNewDevices.append(newDevice)

                    if option1 == "true":
                        newDevice.toggleSwitch()

                    if option2 == "true":
                        newDevice.setOption(True)

                else:
                    messagebox.showinfo(
                        "Uh Oh!",
                        f"Invalid entry at line {i + 1}. Please check the format of your entries."
                    )
                    break

            else:  # Only entered if the for loop is NOT broken out of.
                self.home.devices = []

                for device in tempNewDevices:
                    self.home.addDevice(device)

            self.updateWidgets()


def setUpHome():
    home = SmartHome()

    print("Available Device Types:\n[0] - Smart Plug\n[1] - Smart Doorbell\nAdd 5 devices by referencing their index.")

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
            home.addDevice(SmartPlug(int(rate)))

        else:
            print("Added a Smart Doorbell device.")
            home.addDevice(SmartDoorBell())

    return home


def validateEntry(text):
    if text.isdigit() or not text:
        if text and int(text) > 150:
            return False
        return True
    else:
        return False


def main():
    home = setUpHome()
    system = SmartHomeSystem(home)

    system.run()


main()
