# Class that searching on selected usb storage device all partitions
# and show it

class External_USB_Storage_Partitions_Searcher:
	def __init__(self, selected_usb_storage_device):
		self.selected_usb_storage_device = selected_usb_storage_device
		self.all_partitions_of_selected_usb_dev = []

	# bash comand - lsblk | grep "sd[b-z]".
	# Task: parse output from this command and define
	# and attach right partitions to the right usb storage devices
	def find_all_partitions_of_usb_device():
		pass

	