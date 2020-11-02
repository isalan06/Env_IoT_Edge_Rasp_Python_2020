import gatt

class AnyDeviceManager(gatt.DeviceManager):
    def device_discoverd(self, device):
        print("Discoverd [%s] %s" % (device.mac_address, device.alias()))

print("A")
manager = AnyDeviceManager(adapter_name='hci0')
print("B")
manager.start_discovery()
print("C")
manager.run()
