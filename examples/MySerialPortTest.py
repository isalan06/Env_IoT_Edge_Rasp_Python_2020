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

while res != '':
    print(res)
    buffer.append(res)
    res = ser.read()

print(buffer)