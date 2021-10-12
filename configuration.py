from potentiometr import Potentiometer
import yaml


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
            self.baud = self.config['baud']
            self.number_of_sliders = self.config['number_of_sliders']
            self.insensitiveIN = self.config['insensitiveIN']
            self.insensitiveOUT = self.config['insensitiveOUT']
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
