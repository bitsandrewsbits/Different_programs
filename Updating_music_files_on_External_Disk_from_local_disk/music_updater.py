# main class that implements all music updating steps

import external_device_searcher as usb_srchr
import external_usb_storage_partitions_searcher as usb_prt_srchr
import usb_devices_partitions_displayer as usb_dev_prt_dsplr

class External_Device_Music_Updater:
	def __init__(self):
		self.external_usb_device_searcher = usb_srchr.External_Connected_USB_Disk_Devices_Linux_Searcher()
		self.external_usb_storage_partitions_searcher = usb_prt_srchr.External_USB_Storage_Partitions_Searcher()
		self.selected_connected_usb_storage_partition = ''

	def update_music_on_selected_usb_storage_device(self):
		pass

	def select_connected_external_USB_storage_device_partition(self):		
		if self.external_usb_device_searcher.main():
			self.external_usb_storage_partitions_searcher.find_usb_storages_mountpoints_by_disks()
			self.show_connected_usb_storage_devs_and_partitions()

			user_input = input('Select connected USB Storage Device:')
		
		# TODO: finish this method

	def show_connected_usb_storage_devs_and_partitions(self):
		connected_usb_storage_devices = self.external_usb_device_searcher.get_connected_usb_storage_devices()
		connected_usb_storages_partitions = self.external_usb_storage_partitions_searcher.get_usb_storage_partition_mountpoints_by_disks()
		
		usb_devices_partitions_displayer = usb_dev_prt_dsplr.USB_Devices_Partitions_Displayer(
			connected_usb_storage_devices, connected_usb_storages_partitions
		)
		usb_devices_partitions_displayer.compose_usb_storage_devices_with_partitions()
		usb_devices_partitions_displayer.show_info_about_usb_storages_partitions()

if __name__ == '__main__':
	music_updater = External_Device_Music_Updater()

	music_updater.select_connected_external_USB_storage_device_partition()