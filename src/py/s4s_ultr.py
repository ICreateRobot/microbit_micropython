import iic_base
from microbit import *
import time
class s4s_ultr(iic_base.iic_base):
    def __init__(self, port=0, addr=0x57):
        super().__init__(port, addr)
        self.last_distance = 0
        self.get_distance_last_tick = 0
        self.set_color_last_tick = 0
    
    '''
    unit : 0厘米，1米 1英寸
    '''
    def unit_conversion(self, distance_cm, unit=0):
        if 0 == unit:
            return distance_cm
        elif 1 == unit:
            return distance_cm / 100
        else:
            return distance_cm * 0.393701
        

    '''
    unit : 0厘米，1米 1英寸
    '''
    def get_distance(self, unit=0):
        if (time.ticks_ms() - self.get_distance_last_tick < 50):
            return self.unit_conversion(self.last_distance, unit)
        self.get_distance_last_tick = time.ticks_ms()
        ret = self.read_reg(0x01, 3)
        dis = ret[0]<<16 | ret[1]<<8 | ret[2]
        self.last_distance = dis//10000
        return self.unit_conversion(self.last_distance, unit)

    def set_color(self, light, r, g, b):
        if (time.ticks_ms() - self.set_color_last_tick < 50):
            return
        self.set_color_last_tick = time.ticks_ms()
        self.write_reg(0x02, [light, r, g, b])
