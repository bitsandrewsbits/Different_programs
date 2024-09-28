# Class that searching on selected usb storage device all partitions
# and show it
import re
import subprocess as sp

class External_USB_Storage_Partitions_Searcher:
	def __init__(self, all_connected_usb_storage_devices = [], selected_usb_storage_device = {}):
		self.all_connected_usb_storage_devices = all_connected_usb_storage_devices
		self.selected_usb_storage_device = selected_usb_storage_device
		self.lsblk_cmd = ["lsblk"]
		self.all_partitions_of_all_connected_usb_storage_devs = []
		self.all_partitions_of_selected_usb_dev = []

	# bash command - lsblk | grep "sd[b-z]".
	# Task: parse output from this command and define
	# and attach right partitions to the right usb storage devices
	def find_all_partitions_of_selected_usb_device(self):
		pass

	def parse_output_lsblk_output_strings(self):
		pass

	def get_output_strings_from_lsblk_cmd(self):
		bash_command_output = sp.run(self.lsblk_cmd, capture_output = True, text = True)
		bash_command_result_strs = bash_command_output.stdout.strip()

		return bash_command_result_strs
	

if __name__ == '__main__':
	external_usb_storage_partitions_seacher = External_USB_Storage_Partitions_Searcher()

	external_usb_storage_partitions_seacher.execute_target_lsblk_cmd()