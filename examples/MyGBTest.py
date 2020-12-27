from bluepy.btle import UUID, Peripheral

p = Peripheral('a4:c1:38:ee:b6:50')
my_service = p.getServiceByUUID('0000180f-0000-1000-8000-00805f9b34fb')
my_char = my_service.getCharacteristics('00002a19-0000-1000-8000-00805f9b34fb')[0]
batter_raw_value = my_char.read()
batter_value = int.from_bytes(batter_raw_value, 'big')
print(batter_value)