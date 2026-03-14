# s4s_mainBoard.py
from microbit import *
import iic_base
import struct

class s4s_mainBoard(iic_base.iic_base):
    CHARGING_REG           = 0x00
    AMBIENT_LIGHT_REG      = 0x0A
    RTC_REG                = 0x14
    SERVO_REG              = 0x1E
    VOICE_REG              = 0x28
    ENCODER_MOTOR_REG      = [0x50, 0x6E, 0x8C, 0xAA]
    ENCODER_MOTOR_PAIR_REG = 0xC8

    def __init__(self, port=0, addr=0x0F):
        super().__init__(port, addr)
    
    def _ret_data_(self, data, port):
        if port is None:
            return data
        else:
            return data[port]
        
    # ---------------- 充电管理 ----------------
    def power_get_internal_battery_level(self):
        '''返回内部电池电量的百分比'''
        charging_voltage = self.read_reg(self.CHARGING_REG+0, 1)[0]
        return charging_voltage

    def power_get_external_battery_voltage(self):
        '''返回外部电池电量原始电压值'''
        charging_voltage = self.read_reg(self.CHARGING_REG+1, 1)[0]
        return charging_voltage/10

    def power_is_charging(self):
        '''返回是否正在充电'''
        charging_state = self.read_reg(self.CHARGING_REG+2, 1)[0]
        return charging_state
    
    def power_is_fully_charged(self):
        '''返回是否已充满电'''
        charging_state = self.read_reg(self.CHARGING_REG+3, 1)[0]
        return charging_state

    # ---------------- 氛围灯 ----------------
    def ambient_light_set_state(self, light=None, color=None):
        """
        light : 0~255 , None 表示保持
        color : (r,g,b) 或 None 表示保持
        """
        if light is not None:
            light = max(0, min(255, int(light)))
            self.write_reg(self.AMBIENT_LIGHT_REG, [light])
        if color is not None:
            if len(color) != 3:
                raise ValueError("color must be (r,g,b)")
            self.write_reg(self.AMBIENT_LIGHT_REG + 1, list(color))

    # ---------------- RTC ----------------
    def rtc_set_date(self, year, month, day):
        """year 0~99 , month 1~12 , day 1~31"""
        self.write_reg(self.RTC_REG+1, [0, month, day, year])

    def rtc_set_time(self, hour, minute, second):
        self.write_reg(self.RTC_REG, [hour, minute, second])

    def rtc_get_date(self, sel=None):
        buf = self.read_reg(self.RTC_REG+1, 4)
        return self._ret_data_( [buf[3], buf[1], buf[2], buf[0]], sel )   # year, month, day, week

    def rtc_get_time(self, sel=None):
        buf = self.read_reg(self.RTC_REG, 3)
        return self._ret_data_( [buf[0], buf[1], buf[2]], sel )           # hour, minute, second

    # ---------------- 舵机 ----------------
    def servo_set_angle(self, servo_id, angle):
        """servo_id 0/1 , angle 0~180"""
        if servo_id > 1:
            raise ValueError("servo_id only 0 or 1")
        self.write_reg(self.SERVO_REG + servo_id, [angle])

    # --------------- 连续舵机 ---------------
    def continuous_servo_set_speed(self, servo_id, speed):
        """speed -100~100"""
        if servo_id > 1:
            raise ValueError("servo_id only 0 or 1")
        self.write_reg(self.SERVO_REG + servo_id + 2, [struct.unpack('B', struct.pack('b', speed))[0]])

    # ---------------- 编码电机 ----------------
    def _motor_reg(self, motor_id):
        if motor_id > 3:
            raise ValueError("motor_id only 0~3")
        return self.ENCODER_MOTOR_REG[motor_id]

    def encoder_motor_get_angle(self, motor_id):
        buf = self.read_reg(self._motor_reg(motor_id) + 0, 4)
        return struct.unpack('>i', buf)[0]

    def encoder_motor_get_rpm_speed(self, motor_id):
        buf = self.read_reg(self._motor_reg(motor_id) + 1, 2)
        return struct.unpack('>h', buf)[0]
    
    def encoder_motor_get_dynamic_speed(self, motor_id):
        buf = self.read_reg(self._motor_reg(motor_id) + 2, 2)
        return struct.unpack('>h', buf)[0]
    
    def encoder_motor_get_power(self, motor_id):
        buf = self.read_reg(self._motor_reg(motor_id) + 3, 2)
        return struct.unpack('>h', buf)[0]
    
    def encoder_motor_reset_angle(self, motor_id):
        self.write_reg(self._motor_reg(motor_id) + 0, [0, 0, 0, 0])
    
    def encoder_motor_set_action(self, motor_id, action):
        self.write_reg(self._motor_reg(motor_id) + 4, [action])

    def encoder_motor_set_rpm_speed(self, motor_id, speed):
        """speed 0 ~ (100 ~ 180)"""
        speed = max(0, min(180, speed))
        data = list(struct.unpack('BB', struct.pack('>h', int(speed))))
        self.write_reg(self._motor_reg(motor_id) + 5, data)

    def encoder_motor_set_dynamic_speed(self, motor_id, speed):
        """speed 0 ~ 100"""
        speed = max(0, min(100, speed))
        data = list(struct.unpack('BB', struct.pack('>h', int(speed))))
        self.write_reg(self._motor_reg(motor_id) + 6, data)

    def encoder_motor_set_power(self, motor_id, power):
        """power 0~100"""
        power = max(0, min(100, power))
        self.write_reg(self._motor_reg(motor_id) + 7, [int(power)])

    def encoder_motor_set_ring(self, motor_id, ring):
        """ring 0~65535"""
        ring = max(0, min(100, 65535))
        data = list(struct.unpack('BB', struct.pack('>h', int(ring))))
        self.write_reg(self._motor_reg(motor_id) + 8, data)

    def encoder_motor_set_relative_angle(self, motor_id, angle):
        """angle 0~65535"""
        angle = max(0, min(65535, angle))
        data = list(struct.unpack('BB', struct.pack('>h', int(angle))))
        self.write_reg(self._motor_reg(motor_id) + 9, data)

    def encoder_motor_set_time(self, motor_id, time):
        """time 0~65535"""
        time = max(0, min(65535, time))
        data = list(struct.unpack('BB', struct.pack('>h', int(time))))
        self.write_reg(self._motor_reg(motor_id) + 10, data)
    
    def encoder_motor_set_centimeters(self, motor_id, centimeters):
        """centimeters 0~1000"""
        centimeters = max(0, min(1000, centimeters))
        data = list(struct.unpack('BB', struct.pack('>h', int(centimeters))))
        self.write_reg(self._motor_reg(motor_id) + 11, data)


    # ---------------- 电机组 ----------------
    def encoder_motor_pair_set_action(self, action):
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+0, [action])
    
    def encoder_motor_pair_set_group(self, l_motor, r_motor):
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+1, [l_motor, r_motor])

    def encoder_motor_pair_set_dynamic_speed(self, l_speed, r_speed):
        l_speed = max(0, min(100, l_speed))
        r_speed = max(0, min(100, r_speed))
        data1 = list(struct.unpack('BB', struct.pack('>h', int(l_speed))))
        data2 = list(struct.unpack('BB', struct.pack('>h', int(r_speed))))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+2, data1+data2)

    def encoder_motor_pair_set_time(self, time):
        time = max(0, min(65535, time))
        data = list(struct.unpack('BB', struct.pack('>h', int(time))))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+3, data)

    def encoder_motor_pair_set_ring(self, l_ring, r_ring):
        l_ring = max(0, min(65535, l_ring))
        data1 = list(struct.unpack('BB', struct.pack('>h', int(l_ring))))
        data2 = list(struct.unpack('BB', struct.pack('>h', int(r_ring))))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+4, data1+data2)
    
    def encoder_motor_pair_set_centimeters(self, l_centimeters, r_centimeters):
        l_centimeters = max(0, min(1000, l_centimeters))
        r_centimeters = max(0, min(1000, r_centimeters))
        data1 = list(struct.unpack('BB', struct.pack('>h', int(l_centimeters))))
        data2 = list(struct.unpack('BB', struct.pack('>h', int(r_centimeters))))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+5, data1+data2)

    # ------------------ 语音模块 -------------------------
    def voice_get_state(self):
        sleep(10)
        return self.read_reg(self.VOICE_REG, 1)[0]
