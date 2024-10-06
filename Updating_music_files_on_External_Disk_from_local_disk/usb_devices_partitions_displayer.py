# this class helps to combine usb storage devices names and their 
# partitions respectively

class USB_Devices_Partitions_Displayer:
	def __init__(self, all_connected_usb_storage_devs, all_usb_storages_partitions):
		self.all_connected_usb_storage_devices = all_connected_usb_storage_devs
		self.all_connected_usb_storages_partitions = all_usb_storages_partitions

		# data structure - [{'Product': 'USB-Product-1', 'Manufacturer': Manufacturer-1, 
		# 'partitions_mountpoints': ['abs_path_part-1', 'abs_path_part-2', ...]}, ...]
		self.all_connected_usb_storage_devs_with_partitions = []

	def compose_usb_storage_devices_with_partitions(self):
		pass
		
	def show_info_about_usb_storages_partitions(self):
		pass

