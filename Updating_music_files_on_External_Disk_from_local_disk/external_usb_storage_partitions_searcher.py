# Class that searching on selected usb storage device all partitions
# and show it
import re

class External_USB_Storage_Partitions_Searcher:
	def __init__(self, all_connected_usb_storage_devices: list, selected_usb_storage_device: dict):
		self.all_connected_usb_storage_devices = all_connected_usb_storage_devices
		self.selected_usb_storage_device = selected_usb_storage_device
		self.usb_partitions_searching_cmd = 'lsblk | grep "sd[b-z]"'
		self.all_partitions_of_all_connected_usb_storage_devs = []
		self.all_partitions_of_selected_usb_dev = []

	# bash command - lsblk | grep "sd[b-z]".
	# Task: parse output from this command and define
	# and attach right partitions to the right usb storage devices
	def find_all_partitions_of_selected_usb_device(self):
		pass

	def parse_lsblk_cmd(self):
		pass
	