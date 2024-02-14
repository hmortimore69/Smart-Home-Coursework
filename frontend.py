from backend import *
from tkinter import *


class SmartHomeSystem:
    def __init__(self):
        self.win = Tk()
        self.win.title("Smart Home System")
        self.win.geometry("")
        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(column=0, row=0, padx=10, pady=10)

    def run(self, devices):
        self.createWidgets(devices)
        self.win.mainloop()

    def createWidgets(self, devices):
        turnOnAllButton = Button(
            self.mainFrame,
            text="Turn On All"
        )
        turnOnAllButton.grid(column=0, row=0, pady=(0, 10))

        turnOffAllButton = Button(
            self.mainFrame,
            text="Turn Off All"
        )
        turnOffAllButton.grid(column=1, row=0, pady=(0, 10))

        # Initialise the 5 devices
        for i in range(len(devices)):
            device = devices[i]
            deviceStatus = "On" if device.getSwitchedOn() else "Off"

            if isinstance(device, SmartPlug):
                deviceLabel = Label(
                    self.mainFrame,
                    text=f"Smart Plug: {deviceStatus}, Consumption Rate: {device.getConsumptionRate()}"
                )
                deviceLabel.grid(column=0, row=i+1)

            else:
                deviceOption = "On" if device.getOption() else "Off"
                deviceLabel = Label(
                    self.mainFrame,
                    text=f"Smart Doorbell: {deviceStatus}, Sleep Mode: {deviceOption}"
                )
                deviceLabel.grid(column=0, row=i+1)


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
    system = SmartHomeSystem()

    system.run(home.getDevices())


main()
