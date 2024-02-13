from backend import *
from tkinter import *


class SmartHomeSystem:
    def __init__(self):
        self.win = Tk()
        self.win.title("Smart Home System")
        self.win.geometry("")
        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(column=0, row=0)

    def run(self):
        self.createWidgets()
        self.win.mainloop()

    def createWidgets(self):
        turnOnAllButton = Button(
            self.mainFrame,
            text="Turn On All"
        )
        turnOnAllButton.grid(column=0, row=0)

        turnOffAllButton = Button(
            self.mainFrame,
            text="Turn Off All"
        )
        turnOffAllButton.grid(column=1, row=0)


def setUpHome():
    home = SmartHome()
    deviceChoices = [SmartPlug, SmartDoorBell]

    print("Available Device Types:\n[0] - Smart Plug\n[1] - Smart Doorbell\nAdd 5 devices by referencing their index.")

    for counter in range(5):
        while True:
            try:
                index = int(input("Enter the catalog index of the device you'd like to add: "))

                if index == 0:  # Smart Plug
                    # Ensure a value is entered inside the consumption rate w/o needing to re-enter an index.
                    while True:
                        try:
                            consumption_rate = int(input("Enter the consumption rate of the Smart Plug: "))
                            device = deviceChoices[index](consumption_rate)
                            break

                        except ValueError:
                            print("Invalid consumption rate. Please enter a number.")

                elif index == 1:  # Smart Doorbell
                    device = deviceChoices[index]()

                else:
                    print("Invalid index. Please enter an appropriate value (0 or 1).")
                    continue

                home.addDevice(device)
                break

            except ValueError:
                print("Invalid input. Please enter a number.")

    return home


def main():
    home = setUpHome()
    system = SmartHomeSystem()

    system.run()


main()
