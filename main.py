import serial
import pulsectl
from time import sleep

from configuration import Configuration


def values_into_percent(value, max_val):
    return value/max_val


def read_from_serial(ser):
    try:
        line = ser.readline()
        #print(line)
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
            pulse.volume_set_all_chans(source, config._in[tmp_name].volume)
        elif config._other_in:
            pulse.volume_set_all_chans(
                source, config._other_in['other'].volume)


def main():
    c = Configuration()
    c.load_configuration('config.yaml')
    c.print_config()        #print(values)
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=c.baud)
    ser.readline()
    ser.readline()
    #ser.flushInput()
    pulse = pulsectl.Pulse()
    i = 0
    while 1:  # True: podobno szybciej
        line = read_from_serial(ser)
        #line2 = read_from_serial(ser)
        #ser.flushInput()
        print(i, " :", end="")
        print(line)
        values = [round(values_into_percent(int(x), 999), 3) for x in line]
        #print(values)
        update_volumes(c, values, pulse)
        #sleep(0.001)
        i += 1
        # print(i)


if __name__ == "__main__":
    main()
