from backend import *
from tkinter import *


class SmartHomeSystem:
    def __init__(self, home):
        self.home = home
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
        turnOnAllButton = Button(
            self.mainFrame,
            text="Turn On All"
        )
        turnOnAllButton.grid(column=0, row=0, pady=(0, 10))

        turnOffAllButton = Button(
            self.mainFrame,
            text="Turn Off All"
        )
        turnOffAllButton.grid(column=1, row=0, pady=(0, 10), columnspan=2)

        # Initialise the 5 devices
        for i, device in enumerate(self.devices):
            deviceStatus = "On" if device.getSwitchedOn() else "Off"

            if isinstance(device, SmartPlug):
                deviceLabel = Label(
                    self.mainFrame,
                    text=f"Smart Plug: {deviceStatus}, Consumption Rate: {device.getConsumptionRate()}"
                )
                deviceLabel.grid(column=0, row=i+1, sticky="w")

            else:
                deviceOption = "On" if device.getOption() else "Off"

                deviceLabel = Label(
                    self.mainFrame,
                    text=f"Smart Doorbell: {deviceStatus}, Sleep Mode: {deviceOption}"
                )
                deviceLabel.grid(column=0, row=i+1, sticky="w")

            togglePower = Button(
                self.mainFrame,
                text="Toggle Power",
                command=lambda n=i: self.toggleSwitchButtonClicked(n)
            )
            togglePower.grid(column=1, row=i+1, padx=(10, 0))

            editOption = Button(
                self.mainFrame,
                text="Edit Device"
            )
            editOption.grid(column=2, row=i+1, padx=(10, 0))

            removeDevice = Button(
                self.mainFrame,
                text="Delete Device",
                command=lambda n=i: self.deleteDeviceButtonClicked(n)
            )
            removeDevice.grid(column=3, row=i+1, padx=(10, 0))

        addDevice = Button(
            self.mainFrame,
            text="Add Device",
            command=self.addDeviceButtonClicked
        )
        addDevice.grid(column=0, row=len(self.devices)+1)

    def addDeviceButtonClicked(self):
        pass

    def toggleSwitchButtonClicked(self, i):
        self.home.toggleSwitch(i)
        self.updateWidgets()

    def deleteDeviceButtonClicked(self, i):
        self.home.removeDevice(i)
        self.updateWidgets()


def setUpHome():
    home = SmartHome()
    deviceChoices = [SmartPlug, SmartDoorBell]

    print("Available Device Types:\n[0] - Smart Plug\n[1] - Smart Doorbell\nAdd 5 devices by referencing their index.")

    for counter in range(5):
        index = input("Please enter the index of the device you'd like to add: ")

        while index not in ["0", "1"]:
            print("Invalid argument. Please enter a valid catalog index.")
            index = input("Please enter the index of the device you'd like to add: ")

        if index == "0":
            rate = input("Please enter the consumption rate of your smart plug: ")

            while not rate.isnumeric():
                print("Invalid argument. Please enter a valid number.")
                rate = input("Please enter the consumption rate of your smart plug: ")

            print(f"Added a Smart Plug device with a consumption rate of {rate}.")
            home.addDevice(SmartPlug(int(rate)))

        else:
            print("Added a Smart Doorbell device.")
            home.addDevice(SmartDoorBell())

    return home


def main():
    home = setUpHome()
    system = SmartHomeSystem(home)

    system.run()


main()
