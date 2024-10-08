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
		all_connected_usb_storage_disks = [list(usb_disk.keys())[0] for usb_disk in self.all_connected_usb_storages_partitions]
		print(all_connected_usb_storage_disks)
		for i in range(len(self.all_connected_usb_storage_devices)):
			total_usb_storage_device_info = self.all_connected_usb_storage_devices[i]
			total_usb_storage_device_info['partitions_mountpoints'] = \
			self.all_connected_usb_storages_partitions[i][all_connected_usb_storage_disks[i]]
			self.all_connected_usb_storage_devs_with_partitions.append(total_usb_storage_device_info)
		return True

	def show_info_about_usb_storages_partitions(self):
		print('Total information about connected USB Storage Devices:')
		for usb_storage_dev in self.all_connected_usb_storage_devs_with_partitions:
			print('USB Storage Product :', usb_storage_dev['Product'])
			print('USB Storage Manufacturer: ', usb_storage_dev['Manufacturer'])
			for usb_partition_mountpoint in usb_storage_dev['partitions_mountpoints']:
				print('Partitions:')
				print('\tMountpoint_path:', usb_partition_mountpoint)
			print('=' * 40)
		return True

