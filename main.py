import serial
import yaml

import pulsectl


class Potentiometer():
    def __init__(self, number, app_name):
        self.app_name = app_name
        self.number = number

    def update_volume(self, new_volume):
        self.volume = new_volume
        # pulsectl


class Configuration():
    def __init__(self):
        pass

    def load_configuration(self, conf_file):
        self.list_of_potentiometers = []
        with open(conf_file, 'r') as f:
            self.config = yaml.load(f)
            self.number_of_sliders = self.config['number_of_sliders']
            i = 0
            for p in self.config['slider_mapping']:
                self.list_of_potentiometers.append(Potentiometer(i, p))
                i += 1


def values_into_percent(value, max_val):
    return value/max_val


def read_from_serial(ser):
    line = ser.readline()
    # except serial.serialutil.SerialException:
    split_line = line.decode()[:len(line)-2].split('|')  # from 0 to 1023
    # print(line)
    return split_line


def update_volumes(config, values):
    for (p, v) in config.list_of_potentiometers, values:
        p.update_volume(v)


def main():
    c = Configuration()
    c.load_configuration('config.yaml')
    ser = serial.Serial(port='/dev/ttyUSB0')
    ser.readline()
    #pulse = pulsectl.Pulse()

    while True:
        line = read_from_serial(ser)
        values = [round(values_into_percent(int(x), 1023), 2) for x in line]
        update_volumes(c, values)


if __name__ == "__main__":
    main()
