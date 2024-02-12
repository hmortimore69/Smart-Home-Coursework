class SmartPlug:
    def __init__(self, consumptionRate: int):
        self.switchedOn = False
        self.consumptionRate = consumptionRate

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self) -> bool:
        return self.switchedOn

    def getConsumptionRate(self) -> int:
        return self.consumptionRate

    def setConsumptionRate(self, rate: int):
        self.consumptionRate = rate

    def __str__(self) -> str:
        return f"------\nSmart Plug\n------\nSwitched On: {self.switchedOn}\nConsumption Rate: {self.consumptionRate}"


class SmartDoorBell:
    def __init__(self):
        self.switchedOn = False
        self.streaming = "Amazon"

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def setStreaming(self, service: str):
        while service.lower() not in ["amazon", "apple", "spotify"]:
            print("Invalid streaming service. Please choose from:\n- Amazon\n- Apple\n- Spotify")
            service = input("Enter your choice of streaming service: ")

        self.streaming = service.lower().capitalize()

    def __str__(self):
        return f"------\nSmart Doorbell\n------\nSwitched On: {self.switchedOn}\nStreaming Service: {self.streaming}"


def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    print(plug.getSwitchedOn())
    print(plug.getConsumptionRate())
    print(plug)


def testSmartDoorBell():
    doorbell = SmartDoorBell()
    doorbell.toggleSwitch()
    doorbell.setStreaming(input("Enter a streaming service: "))
    print(doorbell)


testSmartDoorBell()
