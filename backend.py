class SmartDevice:
    def __init__(self):
        self.switchedOn = False

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self) -> bool:
        return self.switchedOn


class SmartPlug(SmartDevice):
    def __init__(self, consumptionRate):
        super().__init__()
        self.consumptionRate = consumptionRate

    def getConsumptionRate(self) -> int:
        return self.consumptionRate

    def setConsumptionRate(self, rate):
        self.consumptionRate = rate

    def __str__(self) -> str:
        return f'''------
        Smart Plug
        ------
        Switched On: {self.switchedOn}
        Consumption Rate: {self.consumptionRate}
        '''


class SmartDoorBell(SmartDevice):
    def __init__(self):
        super().__init__()
        self.sleepMode = False

    def getOption(self) -> bool:
        return self.sleepMode

    def setOption(self, option):
        self.sleepMode = bool(option)

    def __str__(self) -> str:
        return f'''------
        Smart Doorbell
        ------
        Switched On: {self.switchedOn}
        Sleep Mode: {self.sleepMode}
        '''


class SmartHome:
    def __init__(self):
        self.devices = []

    def getDevices(self) -> list:
        return self.devices

    def getDevicesAt(self, i) -> object:
        return self.devices[i]

    def addDevice(self, device):
        self.devices.append(device)

    def removeDevice(self, i):
        self.devices.pop(i)

    def toggleSwitch(self, i):
        self.devices[i].toggleSwitch()

    def turnOnAll(self):
        for device in self.devices:
            device.switchedOn = True

    def turnOffAll(self):
        for device in self.devices:
            device.switchedOn = False

    def __str__(self):
        returnString = ""
        for device in self.devices:
            returnString += str(device)

        return returnString


def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    print(plug.getSwitchedOn())
    print(plug.getConsumptionRate())
    print(plug)


def testSmartDoorBell():
    doorbell = SmartDoorBell()
    doorbell.toggleSwitch()
    doorbell.setOption(input("Do you want sleep mode? (True or False): "))
    print(doorbell)


def testSmartHome():
    home = SmartHome()

    plugOne = SmartPlug(45)
    plugTwo = SmartPlug(45)
    doorbell = SmartDoorBell()

    plugOne.toggleSwitch()

    plugOne.setConsumptionRate("test")
    plugOne.setConsumptionRate(True)
    plugOne.setConsumptionRate(150)
    plugTwo.setConsumptionRate(25)

    doorbell.setOption(2)
    doorbell.setOption(True)

    home.addDevice("true")
    home.addDevice(plugOne)
    home.addDevice(plugTwo)
    home.addDevice(doorbell)

    home.toggleSwitch(1)
    print(home)

    home.turnOnAll()
    print("!!TURNED ON ALL DEVICES!!")
    print(home)
