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
