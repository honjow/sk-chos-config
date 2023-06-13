#!/usr/bin/python

import evdev
import threading
import os
from evdev import UInput, ecodes, InputEvent, AbsInfo, ecodes as e
import time
from ec import EC
CONTROLLER_EVENTS = {
    e.EV_KEY: [
        e.KEY_MUTE,
        e.KEY_VOLUMEDOWN,
        e.KEY_VOLUMEUP,
    ],
}

while True:
	#进入音量键模式
	EC.Write(0xEB,0XEB)
	audiobuttondev = None
	# 创建uinput设备
	ui_device = None
	devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
	at2path=(
				"isa0060/serio0/input0",
			)
	for device in devices:
		if device.name == 'AT Translated Set 2 keyboard' and device.phys in at2path:
			audiobuttondev = device
			# Create the virtual controller.
			ui_device = UInput(
				CONTROLLER_EVENTS)

			#print(device)
			break
		else:
			device.close()

	# 模拟按下并释放按键事件
	def press_key(key_sec,key_usec,key_type,key_code):
		if ui_device:
			event_down = InputEvent(key_sec, key_usec, key_type, key_code, 1)
			ui_device.write_event(event_down)
			ui_device.syn()

	# 模拟按下并释放按键事件
	def release_key(key_sec,key_usec,key_type,key_code):
		if ui_device:
			event_down = InputEvent(key_sec, key_usec, key_type, key_code, 0)
			ui_device.write_event(event_down)
			ui_device.syn()


	# 循环读取按键事件
	if audiobuttondev != None:
		for event in audiobuttondev.read_loop():
			#print(str(event.type)+" "+str(event.code)+" "+str(audiobuttondev.active_keys())+" "+str(event.value))
			#音量键模式
			if event.type == evdev.ecodes.EV_KEY and event.code in [114,115]:
				press_key(event.sec, event.usec,evdev.ecodes.EV_KEY,event.code)
				release_key(event.sec, event.usec,evdev.ecodes.EV_KEY,event.code)
			#功能键模式
			if event.type == evdev.ecodes.EV_KEY and event.value == 1 and audiobuttondev.active_keys() == [32,125]:
				press_key(event.sec, event.usec,evdev.ecodes.EV_KEY,115)
				time.sleep(0.63)
				release_key(event.sec, event.usec,evdev.ecodes.EV_KEY,115)
			if event.type == evdev.ecodes.EV_KEY and event.value == 1 and audiobuttondev.active_keys() == [24, 29, 125]:
				press_key(event.sec, event.usec,evdev.ecodes.EV_KEY,114)
				time.sleep(0.63)
				release_key(event.sec, event.usec,evdev.ecodes.EV_KEY,114)


		audiobuttondev.close()
		# 关闭uinput设备
		ui_device.close()
		exit()
