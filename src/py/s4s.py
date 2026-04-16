from microbit import *
import s4s_gray
import s4s_mainBoard
import s4s_ultr
import music
import speech
mainBoard = s4s_mainBoard.s4s_mainBoard()
gray = s4s_gray.s4s_gray()
ultr = s4s_ultr.s4s_ultr()
import time

def uartReadLine():
    ic_uart_read = uart.readline()
    if not ic_uart_read:
        return ""
    return ic_uart_read.strip()

def toggle(x,y):
  if display.get_pixel(x,y) > 0:
      display.set_pixel(x,y,0)
  else:
      display.set_pixel(x,y,9)

'''
电机【】以【】运行【0-...】【】
dir : 0 正转；1反转
data:
state: 0秒，1圈，2厘米, 3角度
timeout: -1无限等待，>=0 最长等待时间 （单位：秒）
'''
def encoder_motor_run_3state(motor, dir, data, state, timeout=-1):
    last_time = time.ticks_ms()
    if state == 0:
        mainBoard.encoder_motor_set_time(motor, data)
        mainBoard.encoder_motor_set_action(motor, dir+11)
    elif state == 1:
        mainBoard.encoder_motor_set_ring(motor, data)
        mainBoard.encoder_motor_set_action(motor, dir+7)
    elif state == 2:
        mainBoard.encoder_motor_set_centimeter(motor, data)
        mainBoard.encoder_motor_set_action(motor, dir+13)
    elif state == 3:
        mainBoard.encoder_motor_set_relative_angle(motor, data)
        mainBoard.encoder_motor_set_action(motor, dir+9)
    time.sleep_ms(100)
    while True:
        if 0 == mainBoard.encoder_motor_get_action_runing(motor):
            break
        if timeout >= 0 and time.ticks_diff(time.ticks_ms(), last_time) > timeout*1000:
            break
'''
电机【】以【】启动电机 （动态速度）
dir : 0 正转；1反转
'''
def encoder_motor_run(motor, dir):
    mainBoard.encoder_motor_set_action(motor, dir+3)

'''
电机【】停止 （电机会失能）
'''
def encoder_motor_stop(motor):
    mainBoard.encoder_motor_set_action(motor, 0)

'''
电机【】设置速度【0-100】 
'''
def encoder_motor_set_dynamic_speed(motor, speed):
    mainBoard.encoder_motor_set_dynamic_speed(motor, speed)

'''
电机【】位置
'''
def encoder_motor_get_angle(motor):
    return mainBoard.encoder_motor_get_angle(motor)

'''
电机【】速度 （动态速度）
'''
def encoder_motor_get_dynamic_speed(motor):
    return mainBoard.encoder_motor_get_dynamic_speed(motor)

'''
电机【】设置当前位置为0
'''
def encoder_motor_reset_angle(motor):
    mainBoard.encoder_motor_reset_angle(motor)

'''
内部电源在-100 ~ 100；外部电源在-180 ~ 180
电机【】动力【-180 ~ 180】启动
'''
def encoder_motor_start_rpm_speed(motor, power):
    mainBoard.encoder_motor_set_rpm_speed(motor, abs(power))
    mainBoard.encoder_motor_set_action(motor, (power<0)+1)

'''
电机【】动力
'''
def encoder_motor_get_rpm_speed(motor):
    return mainBoard.encoder_motor_get_rpm_speed(motor)


''''
设置运动电机端口【】和【】
'''
def encoder_motor_pair_set_group(l_motor, r_motor):
    mainBoard.encoder_motor_pair_set_group(l_motor, r_motor)

'''
开始运动【state】
state : 0前进；1后退；2左转；3右转
'''
def encoder_motor_pair_run(state):
    mainBoard.encoder_motor_pair_set_action(state+1)

'''
移动【state】以 【data】【for】
state : 0前进；1后退；2左转；3右转
for   ：0秒，1圈，2厘米
timeout: -1无限等待，>=0 最长等待时间 （单位：秒）
'''
def encoder_motor_pair_run_for(state, data, _for, timeout=-1):
    last_time = time.ticks_ms()
    if _for  == 0:
        mainBoard.encoder_motor_pair_set_time(data)
        mainBoard.encoder_motor_pair_set_action(state + 5)
    elif _for == 1:
        mainBoard.encoder_motor_pair_set_ring(data)
        mainBoard.encoder_motor_pair_set_action(state + 9)
    elif _for == 2:
        mainBoard.encoder_motor_pair_set_centimeter(data)
        mainBoard.encoder_motor_pair_set_action(state + 13)
    time.sleep_ms(100)
    while True:
        if 0 == mainBoard.encoder_motor_pair_get_action_runing():
            break
        if timeout >= 0 and time.ticks_diff(time.ticks_ms(), last_time) > timeout*1000:
            break
'''
移动【】【】速度%
'''
def encoder_motor_pair_run_dynamic_speed(l_speed, r_speed):
    mainBoard.encoder_motor_pair_set_dynamic_speed(abs(l_speed), abs(r_speed))
    if l_speed >= 0 and r_speed >= 0:
        mainBoard.encoder_motor_pair_set_action(1)
    elif l_speed <= 0 and r_speed <= 0:
        mainBoard.encoder_motor_pair_set_action(2)
    elif l_speed <= 0 and r_speed >= 0:
        mainBoard.encoder_motor_pair_set_action(3)
    elif l_speed >= 0 and r_speed <= 0:
        mainBoard.encoder_motor_pair_set_action(4)

'''
停止运动
'''
def encoder_motor_pair_stop():
    mainBoard.encoder_motor_pair_set_action(0)

'''
设置移动速度在【】%
'''
def encoder_motor_pair_set_dynamic_speed(speed):
    mainBoard.encoder_motor_pair_set_dynamic_speed(abs(speed), abs(speed))
