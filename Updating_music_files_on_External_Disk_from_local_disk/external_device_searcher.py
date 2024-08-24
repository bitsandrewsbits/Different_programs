# in this file will be created class for defining
# connected external USB devices like flash, external HDD, SSD, or another.
# if nothing external USB disk connected - to tell user about it, and terminating program.
import os
import re

# experimental variant to resolve this task(first for Linux systems):
class External_Connected_USB_Disk_Devices_Linux_Searcher:
	def __init__(self):
		self.usb_number_regex_for_dmesg_txt = re.compile('.*[1-9]-[1-9][.:][1-9 ].*')
		self.connected_usb_storages_number_strs = {}
		self.connected_usb_storages_full_name_regex_strs = []
		self.connected_usb_storage_devs_Manufacturer_Product_regex = [] # data structure - [[usb-dev_Manufacturer_regex_obj, usb-dev_Product_regex_obj], [...]]
		self.connected_usb_storage_devs_by_Manufacturer_Product = [] # data structure - [{'Manufacturer': '', 'Product': ''}, {},..]

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

	def get_target_strings_from_strs(self, strings: list[str], regex_str: str):
		found_target_strs = []
		regex_obj = re.compile(regex_str)
		
		for string in strings:
			found_target_str = regex_obj.match(string)
			if found_target_str:
				found_target_strs.append(string)

		return found_target_strs

	def create_connected_USB_storage_Manufacturer_Product_regex_strs(self):
		for usb_storage_num_str in self.connected_usb_storages_number_strs:
			dev_Manufacturer_regex = re.compile(self.get_USB_storage_Manufacturer_regex_string(usb_storage_num_str))
			dev_Product_regex = re.compile(self.get_USB_storage_Product_regex_string(usb_storage_num_str))
			self.connected_usb_storage_devs_Manufacturer_Product_regex.append(
				[dev_Manufacturer_regex, dev_Product_regex]
			)

		print('Define regex for searching USB Storage devs:')
		print(self.connected_usb_storage_devs_Manufacturer_Product_regex)
		return True

	def find_connected_USB_storage_dev_numbers_from_target_strs(self, target_strs: list[str]):
		connected_USB_dev_numbers = []

		for str_with_USB_number in target_strs:
			str_elements = str_with_USB_number.split(' ')
			for elem in str_elements:
				if self.usb_number_regex_for_dmesg_txt.match(elem):
					USB_dev_number = elem
					connected_USB_dev_numbers.append(USB_dev_number)
					break

		self.connected_usb_storages_number_strs = set(self.get_clean_USB_dev_numbers_without_suffix(connected_USB_dev_numbers))
		print('Found connected USB storage devices with numbers:', self.connected_usb_storages_number_strs)

		return True

	def get_clean_USB_dev_numbers_without_suffix(self, usb_num_strs: list[str]):
		clean_USB_dev_numbers = []
		for usb_num_str in usb_num_strs:
			clean_USB_dev_numbers.append(usb_num_str.split(':')[0]) # add only x-x.x or x-x numbers

		return clean_USB_dev_numbers

	# 4) Create strings - 
	#	1)usb-<detected_words_from_(3)> Product:
	def get_USB_storage_Product_regex_string(self, usb_number_str: str):
		return f".*usb {usb_number_str}: Product.*"
	
	#	2)usb-<detected_words_from_(3)> Manufacturer:
	def get_USB_storage_Manufacturer_regex_string(self, usb_number_str: str):
		return f".*usb {usb_number_str}: Manufacturer.*"
		
		# 5) Parse created file from (1) - detect string from (4). Write them to separate file.
	def get_USB_storage_devs_Manufacturer_Product(self, target_strs: list[str]):
		pass

		# 6) Parse created file from (5) - detect Product and Manufacturer values and save it to list or dict.
		# 7) If list or dict from (6) - is empty -> method returns False
		#    If list or dict from (6) - not empty -> method returns True

		# I think it will be in another class. About detection partitions of connected USB devices.
		# N) Find from output (1) - detect words - sdb, sdc,... - as block devices, mounted to your Linux system.

if __name__ == "__main__":
	external_usb_dev_seacher = External_Connected_USB_Disk_Devices_Linux_Searcher()
	external_usb_dev_seacher.get_and_write_info_from_dmesg_cmd_about_connected_USB_devs()
	external_usb_dev_seacher.get_and_write_info_from_dmesg_cmd_about_connected_USB_storage_devs()
	usb_strs = external_usb_dev_seacher.get_strings_from_txt_file('usb_detected_strs.txt')
	usb_storage_strs = external_usb_dev_seacher.get_strings_from_txt_file('usb_storage_strs.txt')

	target_usb_storage_strs = external_usb_dev_seacher.get_target_strings_from_strs(usb_storage_strs, '.*[1-9]-[1-9][.:][1-9 ].*')
	
	external_usb_dev_seacher.find_connected_USB_storage_dev_numbers_from_target_strs(target_usb_storage_strs)
	external_usb_dev_seacher.create_connected_USB_storage_Manufacturer_Product_regex_strs()
