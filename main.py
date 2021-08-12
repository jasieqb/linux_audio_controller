import serial


def read_from_serial():
    ser = serial.Serial(port='/dev/ttyUSB0')
    ser.readline()
    while True:
        line = ser.readline()
        # except serial.serialutil.SerialException:
        split_line = line.decode()[:len(line)-2].split('|')
        # print(line)
        print(split_line)


read_from_serial()
