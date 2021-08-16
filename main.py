import serial
import yaml
import pulsectl


class Potentiometer():
    def __init__(self, number: int, app_name: str, out: bool):
        self.out = out
        self.app_name = app_name
        self.number = number

    def update_volume(self, new_volume, pulse):
        self.volume = new_volume
        # output
        if self.out:
            for sink in pulse.sink_input_list():
                if sink.proplist.get('application.process.binary').lower() == self.app_name.lower():
                    pulse.volume_set_all_chans(sink, self.volume)
        # input
        else:
            for source in pulse.source_output_list():
                if source.proplist.get('application.process.binary').lower() == self.app_name.lower():
                    pulse.volume_set_all_chans(source, self.volume)


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
                name, out = p.split('|')
                if out == 'out':
                    out = True
                else:
                    out = False
                self.list_of_potentiometers.append(Potentiometer(i, name, out))
                i += 1

    def print_config(self):
        print("=========CONFIG=========")
        print("N\tNAME\t     DIRECTIONS")
        for p in self.list_of_potentiometers:
            if p.out:
                o = "output"
            else:
                o = "input"
            print("{}:\t{:<8}\t{}".format(
                p.number, p.app_name, o))
        print("=========END=========")


def values_into_percent(value, max_val):
    return value/max_val


def read_from_serial(ser):
    try:
        line = ser.readline()
        split_line = line.decode()[:len(line)-2].split('|')  # from 0 to 1023
    except serial.serialutil.SerialException:
        print("Can't read from serial. Maybe something is unplugged")
    return split_line


def update_volumes(config, values, pulse):
    for (p, v) in zip(config.list_of_potentiometers, values):
        if v <= 0.02:
            v = 0
        if v >= 0.98:
            v = 1
        p.update_volume(v, pulse)


def main():
    c = Configuration()
    c.load_configuration('config.yaml')
    c.print_config()
    ser = serial.Serial(port='/dev/ttyUSB0')
    ser.readline()
    pulse = pulsectl.Pulse()

    while True:
        line = read_from_serial(ser)
        values = [round(values_into_percent(int(x), 1023), 2) for x in line]
        update_volumes(c, values, pulse)


if __name__ == "__main__":
    main()
