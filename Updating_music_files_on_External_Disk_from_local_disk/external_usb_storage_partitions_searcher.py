# Class that searching all partitions of connected usb storage devices
import re
import subprocess as sp

class External_USB_Storage_Partitions_Searcher:
	def __init__(self, all_connected_usb_storage_devices = [], selected_usb_storage_device = {}):
		self.lsblk_cmd = ["lsblk"]
		self.usb_storage_devs_lsblk_start_str = 'sdb'

		# data structure - [{'disk-1': [{'number': partition_number-1, 'mountpoint': 'abs_path_part-1'}, {}, ...]}, ...]}, {'disk-2': [...]}, ...]
		self.all_partitions_of_all_connected_usb_storage_devs_by_disks = []

	def find_usb_storages_mountpoints_by_disks(self):
		target_lsblk_strings = self.get_usb_storage_partitions_lsblk_output_strings()

		partition_number = 1
		for lsblk_str in target_lsblk_strings:
			if self.lsblk_string_contain_usb_disk_Linux_name(lsblk_str):
				print('Found external usb disk:', lsblk_str)
				current_usb_disk_dev = {}
				usb_disk_dev_name = self.get_usb_disk_from_lsblk_string(lsblk_str)
				current_usb_disk_dev[usb_disk_dev_name] = []
				self.all_partitions_of_all_connected_usb_storage_devs_by_disks.append(
					current_usb_disk_dev)

			elif self.lsblk_string_contain_usb_partition_Linux_name(lsblk_str):
				usb_disk_mountpoint = self.get_usb_disk_mountpoint_from_lsblk_string(lsblk_str)
				print('Found external usb disk mountpoint:', usb_disk_mountpoint)
				current_usb_disk_partition = {}
				current_usb_disk_partition['number'] = partition_number
				current_usb_disk_partition['mountpoint'] = usb_disk_mountpoint
				current_usb_disk_dev[usb_disk_dev_name].append(current_usb_disk_partition)
				partition_number += 1

		print(self.all_partitions_of_all_connected_usb_storage_devs_by_disks)
		return True

	def get_usb_storage_partition_mountpoints_by_disks(self):
		return self.all_partitions_of_all_connected_usb_storage_devs_by_disks

	def lsblk_string_contain_usb_disk_Linux_name(self, lsblk_str: str):
		str_elements = lsblk_str.split(' ')
		return str_elements[0].isalpha()

	def lsblk_string_contain_usb_partition_Linux_name(self, lsblk_str: str):
		str_elements = lsblk_str.split(' ')
		target_partition_str_elem = str_elements[0][2:]  # without vector line
		return target_partition_str_elem.isalnum()

	def get_usb_disk_from_lsblk_string(self, lsblk_str: str):
		str_elements = lsblk_str.split(' ')
		return str_elements[0]

	def get_usb_disk_mountpoint_from_lsblk_string(self, lsblk_str: str):
		str_elements = lsblk_str.split(' ')
		return str_elements[-1]
		
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

	external_usb_storage_partitions_seacher.find_usb_storages_mountpoints_by_disks()




