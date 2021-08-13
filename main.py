import serial
#import pulsectl


def read_from_serial(ser):
    line = ser.readline()
    # except serial.serialutil.SerialException:
    split_line = line.decode()[:len(line)-2].split('|')  # from 0 to 1023
    # print(line)
    return split_line 


def main():
    ser = serial.Serial(port='/dev/ttyUSB0')
    ser.readline()
    while True:
        print(read_from_serial(ser))


if __name__ == "__main__":
    main()
