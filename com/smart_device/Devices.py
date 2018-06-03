from com.smart_device.database_helper import RaspberryDevices


class RaspberryPi:
    device = ''

    def __init__(self):
        self.device = RaspberryDevices.RaspberryDevices()

    def switch_on(self, device, user):
        self.device.update_device_state(name=device, status=RaspberryDevices.Status.ON, user=user)

    def switch_off(self, device, user):
        self.device.update_device_state(name=device, status=RaspberryDevices.Status.OFF, user=user)

    def toggle(self, device, user):
        self.device.toggle_device_state(name=device, user=user)

    def current_status(self, device):
        return self.device.get_device(name=device)

home = RaspberryPi()

# def switch_on(device, user):
#     RaspberryDevices.update_device_state(device, RaspberryDevices.Status.ON, user)
#
#
# def switch_off(device, user):
#     RaspberryDevices.update_device_state(device, RaspberryDevices.Status.OFF, user)
#
#
# def toggle(device, user):
#     RaspberryDevices.toggle_device_state(device, user)
#
#
# def current_state(device):
#     return RaspberryDevices.get_device(device)
