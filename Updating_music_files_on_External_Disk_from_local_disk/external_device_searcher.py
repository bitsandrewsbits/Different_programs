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
	def get_target_strings_from_strs(self, strings: list[str], regex_str: str):
		found_target_strs = []
		regex_obj = re.compile(regex_str)
		
		for string in strings:
			found_target_str = regex_obj.match(string)
			if found_target_str:
				found_target_strs.append(string)

		return found_target_strs

	def get_connected_USB_storage_devs_regex_strs(self, target_strs: list[str]):
		connected_USB_storage_dev_nums = self.get_connected_USB_dev_numbers_from_target_strs(target_strs)
		connected_USB_storage_devs_regex_strs = []

		for usb_storage_num in connected_USB_storage_dev_nums:
			connected_USB_storage_devs_regex_strs.append(f'.*usb {usb_storage_num}.*')

		return connected_USB_storage_devs_regex_strs

	def get_connected_USB_dev_numbers_from_target_strs(self, target_strs: list[str]):
		connected_USB_dev_numbers = []
		regex_obj = re.compile('.*[1-9]-[1-9][.:][1-9 ].*')

		for str_with_USB_number in target_strs:
			str_elements = str_with_USB_number.split(' ')
			for elem in str_elements:
				if regex_obj.match(elem):
					USB_dev_number = elem
					connected_USB_dev_numbers.append(USB_dev_number)
					break

		connected_USB_dev_numbers_without_suffix = set(self.get_clean_USB_dev_numbers_without_suffix(connected_USB_dev_numbers))
		print('Found connected USB devices with numbers:', connected_USB_dev_numbers_without_suffix)

		return connected_USB_dev_numbers_without_suffix

	def get_clean_USB_dev_numbers_without_suffix(self, usb_num_strs: list[str]):
		clean_USB_dev_numbers = []
		for usb_num_str in usb_num_strs:
			clean_USB_dev_numbers.append(usb_num_str.split(':')[0]) # add only x-x.x or x-x numbers

		return clean_USB_dev_numbers

	# 4) Create strings - 
	#	1)usb-<detected_words_from_(3)> Product:
	def get_USB_storage_Product_regex_string(self, usb_number_str: str):
		return f".*usb-{usb_number_str} Product:"
	
	#	2)usb-<detected_words_from_(3)> Manufacturer:
	def get_USB_storage_Manufacturer_regex_string(self, usb_number_str: str):
		return f"usb-{usb_number_str} Manufacturer:"
		
		# 5) Parse created file from (1) - detect string from (4). Write them to separate file.
	def get_USB_storage_devs_Product_values(self):
		pass

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

	target_usb_storage_strs = external_usb_dev_seacher.get_target_strings_from_strs(usb_storage_strs, '.*[1-9]-[1-9][.:][1-9 ].*')
	
	connected_USB_storage_devs_regex_strs = external_usb_dev_seacher.get_connected_USB_storage_devs_regex_strs(target_usb_storage_strs)
	print(connected_USB_storage_devs_regex_strs)
