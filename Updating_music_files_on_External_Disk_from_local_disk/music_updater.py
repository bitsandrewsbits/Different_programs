# main class that implements all music updating steps

import disk_partition_music_dir_searcher as music_dir_srchr
import external_device_searcher as usb_srchr
import external_usb_storage_partitions_searcher as usb_prt_srchr
import usb_devices_partitions_displayer as usb_dev_prt_dsplr

class External_Device_Music_Updater:
	def __init__(self):
		self.menu_buttons = {'e': 'exit from program', 's': 'select connected usb storage'} # I will finish it in future commits
		self.music_dir_searcher = music_dir_srchr.Partition_Music_Dir_Searcher()
		self.external_usb_device_searcher = usb_srchr.External_Connected_USB_Disk_Devices_Linux_Searcher()
		self.external_usb_storage_partitions_searcher = usb_prt_srchr.External_USB_Storage_Partitions_Searcher()
		self.selected_connected_usb_storage_partition = ''
		self.found_music_dir_on_selected_local_disk_partition = ''
		self.found_music_dir_on_selected_usb_storage_partition = ''

	def main(self):
		pass

	def update_music_on_selected_usb_storage_device(self):
		self.define_music_dir_abs_path_on_selected_local_partition()
		self.select_connected_external_USB_storage_device_partition()
		self.define_music_dir_abs_path_on_selected_usb_storage_partition(selected_connected_usb_storage_partition)

		# TODO: think how to create further process: defining absent music files in usb storage partition, 
		# but they exist in local disk partition.

	def define_music_dir_abs_path_on_selected_local_partition(self):
		if self.music_dir_searcher.main():
			self.found_music_dir_on_selected_local_disk_partition = self.music_dir_searcher.get_partition_music_dir_abs_path()
			return True
		else:
			return False

	def select_connected_external_USB_storage_device_partition(self):
		if self.external_usb_device_searcher.main():
			self.external_usb_storage_partitions_searcher.find_usb_storages_mountpoints_by_disks()

			while True:
				self.show_connected_usb_storage_devs_and_partitions()
				user_input = input('Select connected USB Storage Partition Mountpoint\n[press leftside number]:')
				if user_input.isdigit():
					user_input_number = int(user_input)
					if user_input_number in self.external_usb_storage_partitions_searcher.all_partitions_numbers:
						self.selected_connected_usb_storage_partition = self.get_selected_partition_mountpoint(user_input_number)
						print(f'You selected partition with mountpoint: {self.selected_connected_usb_storage_partition}')
						user_answer = input('Are you agree with it[y/n]?: ')
						if user_answer == 'y':
							print('OK.')
							return True
					else:
						print('Wrong partition number! Try again.')

	def define_music_dir_abs_path_on_selected_usb_storage_partition(self, selected_usb_partition: str):
		if self.music_dir_searcher.main(selected_usb_partition):
			self.found_music_dir_on_selected_usb_storage_partition = self.music_dir_searcher.get_partition_music_dir_abs_path()
			return True
		else:
			return False

	def get_selected_partition_mountpoint(self, partition_number: int):
		partitions_by_numbers = self.get_partitions_by_numbers()
		print(partitions_by_numbers)

		for number_and_partition in partitions_by_numbers:
			if number_and_partition['number'] == partition_number:
				return number_and_partition['mountpoint']
		return False
	
	def get_partitions_by_numbers(self):
		usb_storage_partitions_by_disks = self.external_usb_storage_partitions_searcher.get_usb_storage_partition_mountpoints_by_disks()
		partitions_by_numbers = []
		for usb_storage_disk in usb_storage_partitions_by_disks:
			disk_partitions_by_numbers = list(usb_storage_disk.values())[0]
			partitions_by_numbers += disk_partitions_by_numbers

		return partitions_by_numbers

	def show_connected_usb_storage_devs_and_partitions(self):
		connected_usb_storage_devices = self.external_usb_device_searcher.get_connected_usb_storage_devices()
		connected_usb_storages_partitions = self.external_usb_storage_partitions_searcher.get_usb_storage_partition_mountpoints_by_disks()
		
		usb_devices_partitions_displayer = usb_dev_prt_dsplr.USB_Devices_Partitions_Displayer(
			connected_usb_storage_devices, connected_usb_storages_partitions
		)
		usb_devices_partitions_displayer.compose_usb_storage_devices_with_partitions()
		
		usb_devices_partitions_displayer.show_info_about_usb_storages_partitions()

	def show_menu(self):
		pass

if __name__ == '__main__':
	music_updater = External_Device_Music_Updater()

	music_updater.select_connected_external_USB_storage_device_partition()