import serial
#import pulsectl


def values_into_percent(value, max_val):
    return value/max_val


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
        line = read_from_serial(ser)
        print([round(values_into_percent(int(x), 1023), 2) for x in line])


if __name__ == "__main__":
    main()
