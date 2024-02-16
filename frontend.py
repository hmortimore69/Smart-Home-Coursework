from backend import *
from tkinter import *
from tkinter import ttk


class SmartHomeSystem:
    def __init__(self, home):
        self.home = home
        self.editWin = None
        self.devices = home.getDevices()

        self.win = Tk()
        self.win.title("Smart Home System")

        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(column=0, row=0, padx=10, pady=10)

    def run(self):
        self.createWidgets()
        self.win.mainloop()

    def updateWidgets(self):
        # Clear the mainFrame
        for child in self.mainFrame.winfo_children():
            child.destroy()

        self.createWidgets()

    def createWidgets(self):
        self.devices = self.home.getDevices()

        turnOnAllButton = ttk.Button(
            self.mainFrame,
            text="Turn On All",
            command=lambda: self.turnOnAllButtonClicked()
        )
        turnOnAllButton.grid(column=0, row=0, padx=(10, 100), pady=(0, 10))

        turnOffAllButton = ttk.Button(
            self.mainFrame,
            text="Turn Off All",
            command=lambda: self.turnOffAllButtonClicked()

        )
        turnOffAllButton.grid(column=0, row=0, padx=(100, 10), pady=(0, 10))

        # Initialise the 5 devices
        for i, device in enumerate(self.devices):
            deviceStatus = "On" if device.getSwitchedOn() else "Off"

            if isinstance(device, SmartPlug):
                deviceLabel = ttk.Label(
                    self.mainFrame,
                    text=f"Smart Plug: {deviceStatus}, Consumption Rate: {device.getConsumptionRate()}"
                )
                deviceLabel.grid(column=0, row=i+1, sticky="w")

            else:
                deviceOption = "On" if device.getOption() else "Off"

                deviceLabel = ttk.Label(
                    self.mainFrame,
                    text=f"Smart Doorbell: {deviceStatus}, Sleep Mode: {deviceOption}"
                )
                deviceLabel.grid(column=0, row=i+1, sticky="w")

            togglePower = ttk.Button(
                self.mainFrame,
                text="Toggle Power",
                command=lambda n=i: self.toggleSwitchButtonClicked(n)
            )
            togglePower.grid(column=1, row=i+1, padx=(10, 0))

            editOption = ttk.Button(
                self.mainFrame,
                text="Edit Device",
                command=lambda n=i: self.editDeviceButtonClicked(n)
            )
            editOption.grid(column=2, row=i+1, padx=(10, 0))

            removeDevice = ttk.Button(
                self.mainFrame,
                text="Delete Device",
                command=lambda n=i: self.deleteDeviceButtonClicked(n)
            )
            removeDevice.grid(column=3, row=i+1, padx=(10, 0))

        addDevice = ttk.Button(
            self.mainFrame,
            text="Add Device",
            command=self.addDeviceButtonClicked
        )
        addDevice.grid(column=0, row=len(self.devices)+1)

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

        if isinstance(self.devices[i], SmartPlug):
            consumptionRateVar = StringVar()
            consumptionRateVar.set(str(self.devices[i].getConsumptionRate()))

            editLabel = ttk.Label(
                self.editWin,
                text="Set Consumption Rate"
            )
            editLabel.grid(column=0, row=0)

            consumptionRateSpinbox = ttk.Spinbox(
                self.editWin,
                from_=0,
                to=150,
                increment=1,
                width=3,
                textvariable=consumptionRateVar,
                validate="key",
                validatecommand=(self.editWin.register(validateEntry), "%P")
            )
            consumptionRateSpinbox.grid(column=0, row=2)

            consumptionRateConfirmButton = ttk.Button(
                self.editWin,
                text="Confirm",
                command=lambda n=i: self.setPlugConsumption(i, consumptionRateSpinbox.get())
            )
            consumptionRateConfirmButton.grid(column=0, row=6, padx=60, pady=(10, 10))

        else:
            optionValue = BooleanVar()
            optionValue.set(self.home.devices[i].getOption())

            editLabel = ttk.Label(
                self.editWin,
                text="Sleep Mode"
            )
            editLabel.grid(column=0, row=0, padx=60, pady=(10, 10))

            trueButton = ttk.Radiobutton(
                self.editWin,
                text="On",
                variable=optionValue,
                value=True
            )
            trueButton.grid(column=0, row=2)

            falseButton = ttk.Radiobutton(
                self.editWin,
                text="Off",
                variable=optionValue,
                value=False
            )
            falseButton.grid(column=0, row=3)

            editConfirmButton = ttk.Button(
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
        pass


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
