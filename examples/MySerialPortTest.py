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

data1 = int.from_bytes(buffer[4:5], 'big')
data2 = int.from_bytes(buffer[6:7], 'big')
print(data1)
print(data2)