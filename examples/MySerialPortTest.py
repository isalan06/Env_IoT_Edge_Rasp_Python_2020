import serial

ser=serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1    
)

ser.flushInput()

outputCommand = b'\xA5\x09\xAE'

ser.write(outputCommand)

buffer = []

res = ser.read()

while res != b'':
    print(res)
    buffer.append(res)
    res = ser.read()

print(buffer)

data_byte1 = []
data_byte1.append(buffer[4])
data_byte1.append(buffer[5])
data_byte2 = []
data_byte2.append(buffer[6])
data_byte2.append(buffer[7])
data1 = int.from_bytes(data_byte1, 'big')
data2 = int.from_bytes(data_byte2, 'big')
print(data1)
print(data2)