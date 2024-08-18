# in this file will be created class for defining
# connected external USB devices like flash, external HDD, SSD, or another.
# if nothing external USB disk connected - to tell user about it, and terminating program.
import os
import re

class External_Connected_USB_Disk_Devices_Searcher:
	def __init__(self):
		pass

	# experimental variant to resolve this task(first for Linux systems):
	def external_USB_devices_connected_to_computer(self):
		pass
	
	# 1) use dmesg command with grep: sudo dmesg | grep 'usb' > usb_detected_strs.txt
	def get_and_write_info_from_dmesg_cmd_about_connected_USB_devs(self):
		os.system("sudo dmesg | grep 'usb' > usb_detected_strs.txt")

	# 2) use dmesg command with grep: sudo dmesg | grep 'usb-storage' > usb_storage_strs.txt
	def get_and_write_info_from_dmesg_cmd_about_connected_USB_storage_devs(self):
		os.system("sudo dmesg | grep 'usb-storage' > usb_storage_strs.txt")

	def get_strings_from_txt_file(self, filename: str):
		result_file_strs = []
		with open(filename, 'r') as file_for_reading:
			for string in file_for_reading:
				result_file_strs.append(string[:-1])

		return result_file_strs

	# 3) Parse created file from (2) - detect words "1-1.2:" or something like that and save it in python list or dict
	def get_target_strings_from_file_strs(self, file_strs: list[str], target_str: str):
		found_target_strs = []
		regex_obj = re.compile('.*' + target_str + '.*')
		
		for string in file_strs:
			found_target_str = regex_obj.match(string)
			if found_target_str:
				found_target_strs.append(string)

		return found_target_strs

	def get_USB_dev_number_from_target_strs(self, target_strs: str):
		USB_dev_number = ''
		regex_obj = re.compile('.*usb-storage [1-9]-[1-9][.:][1-9 ].*')
		str_with_USB_number = ''
		for string in target_strs:
			if regex_obj.match(string):
				str_with_USB_number = string
				print('Found target USB number in string:', string)
				break

		str_elements = str_with_USB_number.split(' ')
		regex_obj = re.compile('.*[1-9]-[1-9][.:][1-9 ].*')
		for elem in str_elements:
			if regex_obj.match(elem):
				USB_dev_number = elem

		found_USB_dev_number = USB_dev_number.split(':')[0]
		print('Found connected USB dev with number:', found_USB_dev_number)

		return found_USB_dev_number

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
	usb_strs = external_usb_dev_seacher.get_strings_from_txt_file('usb_detected_strs.txt')
	usb_storage_strs = external_usb_dev_seacher.get_strings_from_txt_file('usb_storage_strs.txt')
	target_usb_storage_strs = external_usb_dev_seacher.get_target_strings_from_file_strs(usb_storage_strs, 'usb-storage')
	print(target_usb_storage_strs)
	external_usb_dev_seacher.get_USB_dev_number_from_target_strs(target_usb_storage_strs)
