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


def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    print(plug.getSwitchedOn())
    print(plug.getConsumptionRate())
    print(plug)


testSmartPlug()
