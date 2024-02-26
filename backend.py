class SmartDevice:
    def __init__(self):
        self.switched_on = False

    def toggle_switch(self):
        self.switched_on = not self.switched_on

    def get_switched_on(self) -> bool:
        return self.switched_on


class SmartPlug(SmartDevice):
    def __init__(self, consumption_rate):
        super().__init__()
        self.consumption_rate = consumption_rate

    def get_consumption_rate(self) -> int:
        return self.consumption_rate

    def set_consumption_rate(self, rate):
        self.consumption_rate = rate

    def __str__(self) -> str:
        return f'''------
        Smart Plug
        ------
        Switched On: {self.switched_on}
        Consumption Rate: {self.consumption_rate}'''


class SmartDoorBell(SmartDevice):
    def __init__(self):
        super().__init__()
        self.sleepMode = False

    def get_option(self) -> bool:
        return self.sleepMode

    def set_option(self, option):
        self.sleepMode = bool(option)

    def __str__(self) -> str:
        return f'''------
        Smart Doorbell
        ------
        Switched On: {self.switched_on}
        Sleep Mode: {self.sleepMode}
        '''


class SmartHome:
    def __init__(self):
        self.devices = []

    def get_devices(self) -> list:
        return self.devices

    def get_devices_at(self, i) -> object:
        return self.devices[i]

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, i):
        self.devices.pop(i)

    def toggle_switch_at_index(self, i):
        self.devices[i].toggle_switch()

    def turn_on_all(self):
        for device in self.devices:
            device.switched_on = True

    def turn_off_all(self):
        for device in self.devices:
            device.switched_on = False

    def __str__(self):
        return_string = ""
        for device in self.devices:
            return_string += str(device)

        return return_string


def test_smart_plug():
    plug = SmartPlug(45)
    plug.toggle_switch()
    print(plug.get_switched_on())
    print(plug.get_consumption_rate())
    print(plug)


def test_smart_doorbell():
    doorbell = SmartDoorBell()
    doorbell.toggle_switch()
    doorbell.set_option(input("Do you want sleep mode? (True or False): "))
    print(doorbell)


def test_smart_home():
    home = SmartHome()

    plug_one = SmartPlug(45)
    plug_two = SmartPlug(45)
    doorbell = SmartDoorBell()

    plug_one.toggle_switch()

    plug_one.set_consumption_rate("test")
    plug_one.set_consumption_rate(True)
    plug_one.set_consumption_rate(150)
    plug_two.set_consumption_rate(25)

    doorbell.set_option(2)
    doorbell.set_option(True)

    home.add_device("true")
    home.add_device(plug_one)
    home.add_device(plug_two)
    home.add_device(doorbell)

    home.toggle_switch(1)
    print(home)

    home.turn_on_all()
    print("!!TURNED ON ALL DEVICES!!")
    print(home)
