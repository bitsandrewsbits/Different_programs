# Class that searching on selected usb storage device all partitions
# and show it
import re
import subprocess as sp

class External_USB_Storage_Partitions_Searcher:
	def __init__(self, all_connected_usb_storage_devices = [], selected_usb_storage_device = {}):
		self.all_connected_usb_storage_devices = all_connected_usb_storage_devices
		self.selected_usb_storage_device = selected_usb_storage_device
		self.lsblk_cmd = ["lsblk"]
		self.usb_storage_devs_lsblk_start_str = 'sdb'

		# data structure - [{'disk-1': ['partition-1_mount-point', 'partition-2_mount-point']}, {'disk-2': [...]}, ...]
		self.all_partitions_of_all_connected_usb_storage_devs_by_disks = []
		
		self.all_partitions_of_selected_usb_dev = []

	# bash command - lsblk
	# Task: parse output from this command and define
	# and attach right partitions to the right usb storage devices
	def find_all_partitions_of_selected_usb_device(self):
		pass

	def get_usb_storages_partitions_by_disks(self):
		target_lsblk_strings = self.get_usb_storage_partitions_lsblk_output_strings()

		for lsblk_str in target_lsblk_strings:
			if self.lsblk_string_contain_usb_disk_Linux_name(lsblk_str):
				print('Found external usb disk:', lsblk_str)

	def lsblk_string_contain_usb_disk_Linux_name(self, lsblk_str: str):
		str_elements = lsblk_str.split(' ')
		return str_elements[0].isalpha()

	def get_usb_storage_partitions_lsblk_output_strings(self):
		usb_storages_partitions_strs = []
		lsblk_output_strings = self.parse_output_lsblk_output_strings()
		for i in range(len(lsblk_output_strings)):
			if self.usb_storage_devs_lsblk_start_str in lsblk_output_strings[i]:
				usb_storages_partitions_strs = lsblk_output_strings[i:]
				break

		print(usb_storages_partitions_strs)
		return usb_storages_partitions_strs

	def parse_output_lsblk_output_strings(self):
		lsblk_output_strings = self.get_output_from_lsblk_cmd().split('\n')
		return lsblk_output_strings

	def get_output_from_lsblk_cmd(self):
		bash_command_output = sp.run(self.lsblk_cmd, capture_output = True, text = True)
		bash_command_result_strs = bash_command_output.stdout.strip()

		return bash_command_result_strs
	

if __name__ == '__main__':
	external_usb_storage_partitions_seacher = External_USB_Storage_Partitions_Searcher()

	external_usb_storage_partitions_seacher.get_usb_storages_partitions_by_disks()