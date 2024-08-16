# in this file will be created class for defining
# connected external USB devices like flash, external HDD, SSD, or another.
# if nothing external USB disk connected - to tell user about it, and terminating program.
import os

class External_Connected_USB_Disk_Devices_Searcher:
	def __init__(self):
		pass

	def external_USB_devices_connected_to_computer(self):
		# experimental variant to resolve this task(first for Linux systems):
		pass

		# 1) use dmesg command with grep: sudo dmesg | grep 'usb' > usb_detected_strs.txt
	def get_and_write_info_from_dmesg_cmd_about_connected_USB_devs(self):
		os.system("sudo dmesg | grep 'usb' > usb_detected_strs.txt")

		# 2) use dmesg command with grep: sudo dmesg | grep 'usb-storage' > usb_storage_strs.txt
	def get_and_write_info_from_dmesg_cmd_about_connected_USB_storage_devs(self):
		os.system("sudo dmesg | grep 'usb-storage' > usb_storage_strs.txt")

		# 3) Parse created file from (2) - detect words "1-1.2:" or something like that and save it in python list or dict
		# 4) Create strings - 
		#	1)usb-<detected_words_from_(3)> Product: 
		#	2)usb-<detected_words_from_(3)> Manufacturer:
		# 5) Parse created file from (1) - detect string from (4). Write them to separate file.
		# 6) Parse created file from (5) - detect Product and Manufacturer values and save it to list or dict.
		# 7) If list or dict from (6) - is empty -> method returns False
		#    If list or dict from (6) - not empty -> method returns True

		# I think it will be in another class. About detection partitions of connected USB devices.
		# N) Find from output (1) - detect words - sdb, sdc,... - as block devices, mounted to your Linux system.

if __name__ == "__main__":
	external_usb_dev_seacher = External_Connected_USB_Disk_Devices_Searcher()
	external_usb_dev_seacher.get_and_write_info_from_dmesg_cmd_about_connected_USB_devs()
	external_usb_dev_seacher.get_and_write_info_from_dmesg_cmd_about_connected_USB_storage_devs()