# in this file will be created class for defining
# connected external USB devices like flash, external HDD, SSD, or another.
# if nothing external USB disk connected - to tell user about it, and terminating program.
import os
import subprocess as sp
import re

# experimental variant to resolve this task(first for Linux systems):
class External_Connected_USB_Disk_Devices_Linux_Searcher:
	def __init__(self):
		self.usb_number_regex_for_dmesg_txt = re.compile('.*[1-9]-[1-9][.:][1-9 ].*')
		# self.usb_strings = []
		# self.usb_storage_strings = []

		# data structure - [{'usb_dev_number': 'usb-number', 'connected_status_timestamp': 'dmesg_time'}]
		self.connected_usb_storages_number_strs = []
		
		# data structure - [{'usb_dev_number': [usb-dev_Product_regex_obj, usb-dev_Manufacturer_regex_obj]}, {...}]
		self.connected_usb_storage_devs_Manufacturer_Product_regex = []
		
		# data structure - [{'usb_dmesg_number': 'usb-number-1', 'Product': '', 'Manufacturer': '', 'status': 'Connected/Disconnected'}, {},..]
		self.connected_usb_storage_devs_by_Manufacturer_Product = []
		
		# data structure - {'usb-number-1': 'regex-1', ...}
		self.disconnected_usb_storage_devs_regex = {}
		
		# data structure - [{'usb_number': 'usb-number', 'disconnected_status_timestamp': 'dmesg_time'}]
		self.disconnected_usb_dev_numbers = []

		# data structure - [{'usb_dev_number': 'usb-number', 'Product': 'USB-Product-1', 'Manufacturer': Manufacturer-1},...]
		self.disconnected_usb_storage_devs = []

		self.program_start_exec_time_in_seconds = 0

	def external_USB_devices_connected_to_computer(self):
		print(self.connected_usb_storage_devs_by_Manufacturer_Product)
		return len(self.connected_usb_storage_devs_by_Manufacturer_Product) > 0

	def external_usb_storage_devs_disconnected(self):
		return len(self.disconnected_usb_storage_devs) > 0

	def remove_usb_storage_devs_from_connected_devices(self):
		while len(self.get_all_usb_storage_disconnected_statuses()) != 0:
			for usb_storage_dev in self.connected_usb_storage_devs_by_Manufacturer_Product:
				if usb_storage_dev['status'] == 'Disconnected':
					self.connected_usb_storage_devs_by_Manufacturer_Product.pop(0)

		return True
	
	def get_and_write_info_from_dmesg_cmd_about_connected_USB_devs(self):
		os.system("sudo dmesg | grep 'usb' > usb_detected_strs.txt")

	def get_and_write_info_from_dmesg_cmd_about_connected_USB_storage_devs(self):
		os.system("sudo dmesg | grep 'usb-storage' > usb_storage_strs.txt")

	def define_usb_strings_from_file(self):
		self.usb_strings = self.get_strings_from_txt_file('usb_detected_strs.txt')

	def define_usb_storage_strings_from_file(self):
		self.usb_storage_strings = self.get_strings_from_txt_file('usb_storage_strs.txt')

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

	def show_connected_USB_storage_devices(self):
		print('[INFO] Found connected USB-storage devices:')
		print(self.connected_usb_storage_devs_by_Manufacturer_Product)
		for usb_storage in self.connected_usb_storage_devs_by_Manufacturer_Product:
			print(f"\tProduct: {usb_storage['Product']}, Manufacturer: {usb_storage['Manufacturer']}")

	def find_connected_USB_storage_devs_Manufacturer_Product_values(self, target_strs: list[str]):
		added_usb_storage_numbers = []
		for i in range(len(target_strs) - 2, 0, -2):	
			for usb_storage_dev_regex in self.connected_usb_storage_devs_Manufacturer_Product_regex:
				usb_storage_dev_number = list(usb_storage_dev_regex.keys())[0]
				usb_storage_dev_Product_regex = usb_storage_dev_regex[usb_storage_dev_number][0]
				usb_storage_dev_Manufacturer_regex = usb_storage_dev_regex[usb_storage_dev_number][1]

				if usb_storage_dev_Product_regex.match(target_strs[i]) and \
				usb_storage_dev_Manufacturer_regex.match(target_strs[i + 1]):
					if self.usb_storage_is_connected(usb_storage_dev_number):
						usb_storage_dev = {}
						usb_storage_dev['usb_dmesg_number'] = usb_storage_dev_number
						usb_storage_dev['Product'] = self.get_connected_USB_storage_dev_Product_or_Manufacturer_value(target_strs[i])
						usb_storage_dev['Manufacturer'] = self.get_connected_USB_storage_dev_Product_or_Manufacturer_value(target_strs[i + 1])
						usb_storage_dev['status'] = 'Connected'
				
						# current_connected_usb_storage_numbers = self.get_connected_usb_storage_numbers()
						if usb_storage_dev_number not in added_usb_storage_numbers:
							self.connected_usb_storage_devs_by_Manufacturer_Product.append(usb_storage_dev)
							added_usb_storage_numbers.append(usb_storage_dev_number)
		return True

	def create_connected_USB_storage_Manufacturer_Product_regex_strs(self):
		for usb_storage_num_timestamp in self.connected_usb_storages_number_strs:
			dev_Manufacturer_regex = re.compile(self.get_USB_storage_Manufacturer_regex_string(
				usb_storage_num_timestamp['usb_dev_number']))
			dev_Product_regex = re.compile(self.get_USB_storage_Product_regex_string(
				usb_storage_num_timestamp['usb_dev_number']))
			
			self.connected_usb_storage_devs_Manufacturer_Product_regex.append(
				{usb_storage_num_timestamp['usb_dev_number']: [dev_Product_regex, dev_Manufacturer_regex]}
			)

		# print('Define regex for searching USB Storage devs:')
		return True

	# TODO: refactor - add timestamp of each usb dev number from dmesg cmd lines(from brackets)
	# In testing...
	def find_connected_USB_storage_dev_numbers_from_target_strs(self, target_strs: list[str]):
		for i in range(len(target_strs) - 1, 0, -1):
			str_elements = target_strs[i].split(' ')
			for j in range(len(str_elements)):
				if self.usb_number_regex_for_dmesg_txt.match(str_elements[j]) and j != len(str_elements) - 1:
					connected_USB_dev_number = self.get_clean_USB_dev_number_without_suffix(str_elements[j])
					usb_storage_dev_number_timestamp = {}
					usb_storage_dev_number_timestamp['usb_dev_number'] = connected_USB_dev_number
					usb_storage_dev_number_timestamp['connected_status_timestamp'] = self.get_timestamp_value_from_dmesg_cmd_line(target_strs[i])	

					current_connected_usb_storage_numbers = self.get_connected_usb_storage_numbers()
					if connected_USB_dev_number not in current_connected_usb_storage_numbers:
						self.connected_usb_storages_number_strs.append(usb_storage_dev_number_timestamp)

		print('Connected usb numbers: ', self.connected_usb_storages_number_strs)
		return True

	def get_connected_USB_storage_dev_Product_or_Manufacturer_value(self, target_str: str):
		str_elems = target_str.split(':')
		return str_elems[-1][1:] # it's last element without whitespace(in dmesg cmd string format) 

	def get_clean_USB_dev_number_without_suffix(self, usb_num_str: str):
		return usb_num_str.split(':')[0] # return only x-x.x or x-x number

	def get_USB_storage_Product_regex_string(self, usb_number_str: str):
		return f".*usb {usb_number_str}: Product.*"
	
	def get_USB_storage_Manufacturer_regex_string(self, usb_number_str: str):
		return f".*usb {usb_number_str}: Manufacturer.*"

	def get_connected_usb_storage_numbers(self):
		usb_numbers = [list(usb_number_str.values())[0] for usb_number_str in self.connected_usb_storages_number_strs]
		return usb_numbers

	#======================================
	def show_disconnected_USB_storage_devices(self):
		for disconnected_usb_storage_dev in self.disconnected_usb_storage_devs:
			print('[INFO] USB storage device with:')
			print(f"\tProduct: {disconnected_usb_storage_dev['Product']}, " 
					 f"Manufacturer: {disconnected_usb_storage_dev['Manufacturer']}"
			)
			print('was disconnected.\n')

	def define_disconnected_USB_storage_devs(self):
		for connected_usb_dev in self.connected_usb_storage_devs_by_Manufacturer_Product:
			connected_usb_storage_number = connected_usb_dev['usb_dmesg_number']
			if self.usb_storage_is_disconnected(connected_usb_storage_number):
				if len(self.get_all_disconnected_timestamps_for_usb_storage_dev(
					connected_usb_storage_number)) > 0 and \
				   max(self.get_all_disconnected_timestamps_for_usb_storage_dev(
						connected_usb_storage_number)) > self.program_start_exec_time_in_seconds:
					
					disconnected_dev = {'usb_dev_number': connected_usb_storage_number, 
										'Product': connected_usb_dev['Product'], 
							 			'Manufacturer': connected_usb_dev['Manufacturer']
							 			}
					if disconnected_dev not in self.disconnected_usb_storage_devs:
						self.disconnected_usb_storage_devs.append(disconnected_dev)
		
		return True

	# TODO: Refactoring and fixing process...
	def find_disconnected_USB_storage_devs_numbers(self, target_strs: list[str]):
		for i in range(len(target_strs) - 1, 0, -1):
			for usb_dev_number in self.disconnected_usb_storage_devs_regex:
				if self.disconnected_usb_storage_devs_regex[usb_dev_number].match(target_strs[i]):
					disconnected_usb_storage_dev_timestamp = self.get_timestamp_value_from_dmesg_cmd_line(target_strs[i])
					disconnected_usb_storage_dev_number_timestamp = {}
					disconnected_usb_storage_dev_number_timestamp['usb_dev_number'] = usb_dev_number
					disconnected_usb_storage_dev_number_timestamp['disconnected_status_timestamp'] = \
					disconnected_usb_storage_dev_timestamp
					
					all_disconnected_usb_storage_numbers_from_dmesg = self.get_disconnected_usb_storage_numbers()
					if usb_dev_number not in all_disconnected_usb_storage_numbers_from_dmesg:
						self.disconnected_usb_dev_numbers.append(disconnected_usb_storage_dev_number_timestamp)
		return True

	def create_USB_storage_devs_disconnected_regexs(self):
		for usb_dev_number_timestamp in self.connected_usb_storages_number_strs:
			usb_dev_number = usb_dev_number_timestamp['usb_dev_number']
			dev_regex = re.compile(f'.*{usb_dev_number}: USB disconnect.*')
			self.disconnected_usb_storage_devs_regex[f'{usb_dev_number}'] = dev_regex
		return True

	def usb_storage_is_disconnected(self, usb_dev_number: str):
		if len(self.get_all_disconnected_timestamps_for_usb_storage_dev(usb_dev_number)) == 0:
			return False

		connected_max_timestamp = max(self.get_all_connected_timestamps_for_usb_storage_dev(usb_dev_number))
		disconnected_max_timestamp = max(self.get_all_disconnected_timestamps_for_usb_storage_dev(usb_dev_number))
		return connected_max_timestamp < disconnected_max_timestamp

	def usb_storage_is_connected(self, usb_dev_number: str):
		if len(self.get_all_connected_timestamps_for_usb_storage_dev(usb_dev_number)) == 0:
			return False

		connected_max_timestamp = max(self.get_all_connected_timestamps_for_usb_storage_dev(usb_dev_number))
		disconnected_max_timestamp = max(self.get_all_disconnected_timestamps_for_usb_storage_dev(usb_dev_number))
		
		if connected_max_timestamp > disconnected_max_timestamp	or \
		connected_max_timestamp >= self.program_start_exec_time_in_seconds:
			return True
		else:
			return False

	def connected_usb_storage_was_disconnected(self, usb_dev_number: str):
		for usb_storage_dev_number in self.disconnected_usb_dev_numbers:
			if usb_storage_dev_number['usb_dev_number'] == usb_dev_number and \
			usb_storage_dev_number['disconnected_status_timestamp'] > self.program_start_exec_time_in_seconds:
				return True
		return False

	def get_disconnected_usb_storage_numbers(self):
		usb_numbers = [list(usb_number_str.values())[0] for usb_number_str in self.disconnected_usb_dev_numbers]
		return usb_numbers

	def get_all_connected_timestamps_for_usb_storage_dev(self, usb_dev_number):
		all_usb_storage_connected_timestamps = []
		for usb_dev_number_timestamp in self.connected_usb_storages_number_strs:
			if usb_dev_number_timestamp['usb_dev_number'] == usb_dev_number:
				all_usb_storage_connected_timestamps.append(
					usb_dev_number_timestamp['connected_status_timestamp']
				)
		return all_usb_storage_connected_timestamps

	def get_all_disconnected_timestamps_for_usb_storage_dev(self, usb_dev_number):
		all_usb_storage_disconnected_timestamps = []
		for usb_dev_number_timestamp in self.disconnected_usb_dev_numbers:
			if usb_dev_number_timestamp['usb_dev_number'] == usb_dev_number:
				all_usb_storage_disconnected_timestamps.append(
					usb_dev_number_timestamp['disconnected_status_timestamp']
				)
		if all_usb_storage_disconnected_timestamps == []:
			return [0]

		return all_usb_storage_disconnected_timestamps

	def get_all_usb_storage_disconnected_statuses(self):
		all_usb_storages_statuses = []
		for usb_storage_dev in self.connected_usb_storage_devs_by_Manufacturer_Product:
			if usb_storage_dev['status'] == 'Disconnected':
				all_usb_storages_statuses.append('Disconnected')

		return all_usb_storages_statuses

	def get_usb_storage_dev_status(self, usb_dev_number: str):
		for usb_storage_dev in self.connected_usb_storage_devs_by_Manufacturer_Product:
			if usb_storage_dev['usb_dmesg_number'] == usb_dev_number:
				return usb_storage_dev['status']

	def set_usb_storage_dev_status_as_connected(self, usb_dev_number: str):
		for usb_storage_dev in self.connected_usb_storage_devs_by_Manufacturer_Product:
			if usb_storage_dev['usb_dmesg_number'] == usb_dev_number:
				usb_storage_dev['status'] = 'Connected'

		return True

	def set_usb_storage_dev_status_as_disconnected(self, usb_dev_number: str):
		for usb_storage_dev in self.connected_usb_storage_devs_by_Manufacturer_Product:
			if usb_storage_dev['usb_dmesg_number'] == usb_dev_number:
				usb_storage_dev['status'] = 'Disconnected'

		return True

	def get_timestamp_value_from_dmesg_cmd_line(self, dmesg_str_line: str):
		search_timestamp_value = re.search('[0-9]+.[0-9]+', dmesg_str_line)
		return float(search_timestamp_value.group(0))

	def set_program_start_executing_time_in_seconds(self):
		bash_cmd = ["cat", "/proc/uptime"]
		bash_command_output = sp.run(bash_cmd, capture_output = True, text = True)
		bash_command_result_str = bash_command_output.stdout.strip()
		self.program_start_exec_time_in_seconds = float(bash_command_result_str.split(' ')[0])

		return True
		

def search_external_usb_storages(external_usb_storage_seacher):
	external_usb_storage_seacher.get_and_write_info_from_dmesg_cmd_about_connected_USB_devs()
	external_usb_storage_seacher.get_and_write_info_from_dmesg_cmd_about_connected_USB_storage_devs()

	usb_strs = external_usb_storage_seacher.get_strings_from_txt_file('usb_detected_strs.txt')
	usb_storage_strs = external_usb_storage_seacher.get_strings_from_txt_file('usb_storage_strs.txt')
	target_usb_storage_strs = external_usb_storage_seacher.get_target_strings_from_strs(usb_storage_strs, '.*[1-9]-[1-9][.:][1-9 ].*')

	external_usb_storage_seacher.find_connected_USB_storage_dev_numbers_from_target_strs(target_usb_storage_strs)
	external_usb_storage_seacher.create_connected_USB_storage_Manufacturer_Product_regex_strs()
	# external_usb_storage_seacher.create_USB_storage_devs_disconnected_regexs()
	# external_usb_storage_seacher.find_disconnected_USB_storage_devs_numbers(usb_strs)
	external_usb_storage_seacher.find_connected_USB_storage_devs_Manufacturer_Product_values(usb_strs)
	# external_usb_storage_seacher.define_disconnected_USB_storage_devs()
	
	if external_usb_storage_seacher.external_USB_devices_connected_to_computer():
		external_usb_storage_seacher.show_connected_USB_storage_devices()
	else:
		print('External USB storage devices was not found.')

	# if external_usb_storage_seacher.connected_usb_storage_was_disconnected()
	# 	external_usb_storage_seacher.show_disconnected_USB_storage_devices()

	# print(external_usb_storage_seacher.disconnected_usb_storage_devs)
	# external_usb_storage_seacher.define_usb_strings_from_file()
	# external_usb_storage_seacher.define_usb_storage_strings_from_file()


# def usb_strs_changed(current_usb_strs: list[str], new_usb_strs: list[str]):
# 	return len(current_usb_strs) < len(new_usb_strs)

# def usb_storage_strs_changed(current_storage_strs: list[str], new_storage_strs: list[str]):
# 	return len(current_storage_strs) < len(new_storage_strs)



if __name__ == "__main__":
	external_usb_dev_seacher = External_Connected_USB_Disk_Devices_Linux_Searcher()
	external_usb_dev_seacher.set_program_start_executing_time_in_seconds()
	print('Uptime:', external_usb_dev_seacher.program_start_exec_time_in_seconds)

	while True:
		user_answer = input('Search external USB storage devices?[y/n]: ')
		if user_answer == 'y':
			search_external_usb_storages(external_usb_dev_seacher)
		else:
			print('Exiting from searching USB storages.')
			break
