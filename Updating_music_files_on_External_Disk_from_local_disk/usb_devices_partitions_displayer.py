# this class helps to combine usb storage devices names and their 
# partitions respectively

class USB_Devices_Partitions_Displayer:
	def __init__(self, all_connected_usb_storage_devs, all_usb_storages_partitions):
		self.all_connected_usb_storage_devices = all_connected_usb_storage_devs
		self.all_connected_usb_storages_partitions = all_usb_storages_partitions

		# data structure - [{'Product': 'USB-Product-1', 'Manufacturer': Manufacturer-1, 
		# 'partitions_mountpoints': [{'number': partition_number-1, 'mountpoint': 'abs_path_part-1'}, 
		#  							 {'number': partition_number-2, 'mountpoint': 'abs_path_part-2'}, ...]}, ...]
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
			print('Partitions:')
			for usb_partition_mountpoint in usb_storage_dev['partitions_mountpoints']:
				unique_partition_number_for_selection = usb_partition_mountpoint['unique_number_for_user']
				partition_mountpoint = usb_partition_mountpoint['mountpoint']
				partition_free_space = usb_partition_mountpoint['free_memory']
				print(f'\t({unique_partition_number_for_selection}) Mountpoint_path: {partition_mountpoint}', end = ' ')
				print(f'- {partition_free_space} bytes of Free memory!')
			print('=' * 40)
		return True

