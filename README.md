# linux_audio_controller
[deej](https://github.com/omriharel/deej) for linux in Python  
## Requiments 
* [pulsectl](https://pypi.org/project/pulsectl/)
* [pyserial](https://github.com/pyserial/pyserial)
## TODO
* add groups
* add main(master) in/out device
* add physical audio devices binding by name
* GUI and system tray widget
* docs

## example config file:
```yaml
    number_of_sliders: 7
    baud: 115200 #baudrate for serial communication 
    invert: True #invert all sliders
    slider_mapping: 
    #case INsensitive
    # template (-)|<name>|in/out, separated by '|'
    # - -> invert slider, optional
    # <name> -> app's binary 
    # in/out -> input(stream to app(e.g. from mic)) or output(from app)
    - -|spotify|out 
    - chrome|out
    - discord|out
    - discord|in
    - other|out
    - other|in
    - teams|in
    # skipped streams IN 
    insensitiveIN:
    - obs
    - python3.9
    # skipped streams IN 
    insensitiveOUT: [] #empty array
```    
