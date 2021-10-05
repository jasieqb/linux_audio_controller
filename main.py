import serial
import yaml
import pulsectl
from time import sleep


class Potentiometer():
    def __init__(self, number: int, app_name: str, out: bool, invert: bool):
        self.out = out
        self.app_name = app_name
        self.number = number
        self.invert = invert

    def set_out(self, new_out):
        self.out = new_out

    def update_volume(self, new_volume):
        self.volume = new_volume
        #print(new_volume, " ,", end="")


class Configuration():
    def __init__(self):
        self._other_in = {}
        self._other_out = {}
        self._in = {}
        self._out = {}

    def load_configuration(self, conf_file):
        self.invert = False
        self.list_of_potentiometers = []
        with open(conf_file, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
            self.invert = self.config['invert']
            self.number_of_sliders = self.config['number_of_sliders']
            i = 0
            if self.invert:
                for p in self.config['slider_mapping']:
                    if len(p.split('|')) != 2:
                        invert, name, out = p.split('|')
                    else:
                        invert = "+"
                        name, out = p.split('|')
                    name = name.lower()
                    tmp_p = Potentiometer(i, name, out == 'out', invert != "-")
                    if name != 'other':
                        if out == 'out':
                            self._out[name] = tmp_p
                        else:
                            self._in[name] = tmp_p
                    else:
                        if out == 'out':
                            self._other_out[name] = tmp_p
                        else:
                            self._other_in[name] = tmp_p
                    self.list_of_potentiometers.append(tmp_p)
                    i += 1
            else:
                for p in self.config['slider_mapping']:
                    if len(p.split('|')) != 2:
                        invert, name, out = p.split('|')
                    else:
                        invert = "+"
                        name, out = p.split('|')
                    name = name.lower()
                    tmp_p = Potentiometer(
                        i, name, out == 'out', invert == "-")
                    if name != 'other':
                        if out == 'out':
                            self._out[name] = tmp_p
                        else:
                            self._in[name] = tmp_p
                    else:
                        if out == 'out':
                            self._other_out[name] = tmp_p
                        else:
                            self._other_in[name] = tmp_p
                self.list_of_potentiometers.append(tmp_p)
                i += 1

    def print_config(self):
        print("=========CONFIG=========")
        print("N\tNAME\t       DIRECTIONS")
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


def update_volumes(config: Configuration, values: list, pulse: pulsectl.Pulse):
    for (p, v) in zip(config.list_of_potentiometers, values):
        if not p.invert:
            p.update_volume(v)
        else:
            p.update_volume(1 - v)
    # out
    for sink in pulse.sink_input_list():
        tmp_name = sink.proplist.get('application.process.binary').lower()
        if tmp_name in config._out:
            pulse.volume_set_all_chans(sink, config._out[tmp_name].volume)
        elif config._other_out:
            pulse.volume_set_all_chans(
                sink, config._other_out['other'].volume)
    # in
    for source in pulse.source_output_list():
        tmp_name = source.proplist.get('application.process.binary').lower()
        if tmp_name in config._in:
            pulse.volume_set_all_chans(source, config._out[tmp_name].volume)
        elif config._other_in:
            pulse.volume_set_all_chans(
                source, config._other_in['other'].volume)


def main():
    c = Configuration()
    c.load_configuration('config.yaml')
    c.print_config()
    ser = serial.Serial(port='/dev/ttyUSB0')
    ser.readline()
    pulse = pulsectl.Pulse()

    while 1:  # True: podobno szybciej
        line = read_from_serial(ser)
        # print(line)
        values = [round(values_into_percent(int(x), 1023), 3) for x in line]
        # print(values)
        update_volumes(c, values, pulse)
        # sleep(0.001)
        # print()


if __name__ == "__main__":
    main()
