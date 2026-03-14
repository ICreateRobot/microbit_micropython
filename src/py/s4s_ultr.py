import iic_base
from microbit import *
import time
class s4s_ultr(iic_base.iic_base):
    def __init__(self, port=0, addr=0x57):
        super().__init__(port, addr)
        self.last_distance = 0
        self.get_distance_last_tick = 0
        self.set_color_last_tick = 0
        
    def get_distance(self):
        if (time.ticks_ms() - self.get_distance_last_tick < 50):
            return self.last_distance
        self.get_distance_last_tick = time.ticks_ms()
        ret = self.read_reg(0x01, 3)
        dis = ret[0]<<16 | ret[1]<<8 | ret[2]
        self.last_distance = dis//10000
        return self.last_distance

    def set_color(self, light, r, g, b):
        if (time.ticks_ms() - self.set_color_last_tick < 50):
            return
        self.set_color_last_tick = time.ticks_ms()
        self.write_reg(0x02, [light, r, g, b])
