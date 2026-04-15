import iic_base
import struct

class mainBoard(iic_base.iic_base):
    CHARGING_REG           = 0x00
    ENCODER_MOTOR_REG      = [0x50, 0x6E]
    ENCODER_MOTOR_PAIR_REG = 0x8C

    def __init__(self, port=0, addr=0x10):
        super().__init__(port, addr)

    def _ret_data_(self, data, port):
        if port is None:
            return data
        else:
            return data[port]

    # ---------------- 充电管理 ----------------
    def power_get_battery_voltage(self):
        '''返回电池电压(0.1v)'''
        charging_voltage = self.read_reg(self.CHARGING_REG+0, 1)[0]
        return charging_voltage
    
    def power_is_charging(self):
        '''返回是否正在充电'''
        charging_state = self.read_reg(self.CHARGING_REG+1, 1)[0]
        return charging_state
    
    def power_is_fully_charged(self):
        '''返回是否已充满电'''
        charging_state = self.read_reg(self.CHARGING_REG+2, 1)[0]
        return charging_state
    
    def version_get(self):
        '''返回版本号'''
        version = self.read_reg(self.CHARGING_REG+3, 3)
        return "%d.%d.%d" % (version[0], version[1], version[2])

    # ---------------- 编码电机 ---------------
    def _motor_reg(self, motor_id):
        if motor_id > 1:
            raise ValueError("motor_id only 0~1")
        return self.ENCODER_MOTOR_REG[motor_id]

    def encoder_motor_get_angle(self, motor_id):
        buf = self.read_reg(self._motor_reg(motor_id) + 0, 4)
        return struct.unpack('>i', buf)[0]

    def encoder_motor_get_speed(self, motor_id):
        buf = self.read_reg(self._motor_reg(motor_id) + 1, 2)
        return struct.unpack('>h', buf)[0]

    def encoder_motor_get_power(self, motor_id):
        buf = self.read_reg(self._motor_reg(motor_id) + 2, 2)
        return struct.unpack('>h', buf)[0]

    def encoder_motor_set_action(self, motor_id, action):
        self.write_reg(self._motor_reg(motor_id) + 3, [action])

    def encoder_motor_set_speed(self, motor_id, speed):
        """speed 0 ~ 100"""
        speed = max(0, min(100, speed))
        data = list(struct.unpack('BB', struct.pack('>h', int(speed))))
        self.write_reg(self._motor_reg(motor_id) + 4, data)
    
    def encoder_motor_set_power(self, motor_id, power):
        """power 0~100"""
        power = max(0, min(100, power))
        self.write_reg(self._motor_reg(motor_id) + 5, [int(power)])
    
    def encoder_motor_set_relative_angle(self, motor_id, angle):
        """angle 0~65535"""
        angle = max(0, min(65535, angle))
        data = list(struct.unpack('BB', struct.pack('>h', int(angle))))
        self.write_reg(self._motor_reg(motor_id) + 6, data)

    def encoder_motor_set_centimeter(self, motor_id, centimeters):
        """centimeters 0~1000"""
        centimeters = max(0, min(1000, centimeters))
        data = list(struct.unpack('BB', struct.pack('>h', int(centimeters))))
        self.write_reg(self._motor_reg(motor_id) + 7, data)

    def encoder_motor_set_absolute_angle(self, motor_id, angle):
        """angle 0~65535"""
        angle = max(0, min(65535, angle))
        data = list(struct.unpack('BB', struct.pack('>h', int(angle))))
        self.write_reg(self._motor_reg(motor_id) + 8, data)

    def encoder_motor_get_action_runing(self, motor_id):
        '''获取电机是否正在执行活动 0空闲 1执行中'''
        return self.read_reg(self._motor_reg(motor_id) + 9, 1)[0]

    # ---------------- 电机组 ----------------
    def encoder_motor_pair_set_action(self, action):
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+0, [action])
    
    def encoder_motor_pair_set_speed(self, l_speed, r_speed):
        '''设置电机的速度 0 ~ 100'''
        l_speed = max(0, min(100, l_speed))
        r_speed = max(0, min(100, r_speed))
        data1 = list(struct.unpack('BB', struct.pack('>h', int(l_speed))))
        data2 = list(struct.unpack('BB', struct.pack('>h', int(r_speed))))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+1, data1+data2)
    
    def encoder_motor_pair_set_centimeter(self, centimeters):
        '''设置电机的距离 0 ~ 1000 (cm)'''
        centimeters = max(0, min(1000, centimeters))
        data = list(struct.unpack('BB', struct.pack('>h', int(centimeters))))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+2, data)
    
    def encoder_motor_pair_set_axle_length(self, length):
        '''设置电机的轴距 0 ~ 255 (mm)'''
        length = max(0, min(255, length))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+3, [length])
    
    def encoder_motor_pair_set_rotation_angle(self, angle):
        '''设置电机的旋转角度(0 ~ 1000)'''
        angle = max(0, min(1000, angle))
        data = list(struct.unpack('BB', struct.pack('>h', int(angle))))
        self.write_reg(self.ENCODER_MOTOR_PAIR_REG+4, data)

    def encoder_motor_pair_get_action_runing(self):
        '''获取电机是否正在执行活动 0空闲 1执行中'''
        return self.read_reg(self.ENCODER_MOTOR_PAIR_REG+5, 1)[0]
