# main class that implements all music updating steps

import disk_partition_music_dir_searcher as music_dir_srchr
import external_device_searcher as usb_srchr
import external_usb_storage_partitions_searcher as usb_prt_srchr
import usb_devices_partitions_displayer as usb_dev_prt_dsplr
import additional_functions as add_fns
import os

class External_Device_Music_Updater:
	def __init__(self):
		self.menu_buttons = {'e': 'exit from program', 's': 'select connected usb storage'} # I will finish it in future commits
		self.music_dir_searcher = music_dir_srchr.Partition_Music_Dir_Searcher()
		self.external_usb_device_searcher = usb_srchr.External_Connected_USB_Disk_Devices_Linux_Searcher()
		self.external_usb_storage_partitions_searcher = usb_prt_srchr.External_USB_Storage_Partitions_Searcher()
		self.spec_symbols_for_cmd = [' ', '(', ')', '\'', '&']
		self.selected_connected_usb_storage_partition_mountpoint = ''
		self.found_music_dir_on_selected_local_disk_partition = ''
		self.found_music_dir_on_selected_usb_storage_partition = ''
		self.mp3_filenames_in_local_partition_music_dir = []
		self.mp3_filenames_in_selected_usb_partition_music_dir = []
		self.new_mp3_files_for_copying_to_usb_storage_music_dir = []

	def update_music_on_selected_usb_storage_device(self):
		self.program_welcome_and_discription()
		user_answer = ''
		# TODO: finish this method
		while user_answer != 'e' and user_answer != 'E':
			self.define_music_dir_abs_path_on_selected_local_partition()
			self.select_connected_external_USB_storage_device_partition()
			self.define_music_dir_abs_path_on_selected_usb_storage_partition(self.selected_connected_usb_storage_partition_mountpoint)
			self.define_filenames_in_local_partition_music_dir()

			if self.music_dir_is_absent_on_selected_usb_partition() and \
			not self.created_usb_partition_music_dir_by_program_is_exist():
				print('[INFO] Music Dir was not found on selected usb storage partition.')
				print('Creating Music Dir...')
				self.create_music_dir_on_selected_usb_partition()
			if self.found_music_dir_on_selected_usb_storage_partition == '':
				print('[INFO] Music_Dir already created by program. But empty.')
				self.set_new_usb_partition_music_dir(
					self.selected_connected_usb_storage_partition_mountpoint + '/Music_Dir'
				)
			self.define_filenames_in_selected_usb_partition_music_dir()
			self.define_new_mp3_files_for_copying_into_usb_music_dir()
			self.show_new_mp3_files_for_usb_storage_music_dir()

		user_answer = input('Copy new MP3 files into selected usb partition?[y/n]:')
		if user_answer == 'y':
			if self.copy_new_mp3_files_to_selected_usb_partition_music_dir():
				print('[INFO] All new MP3 music files was successful copied into')
				print('selected usb partition!')
			else:
				print('[INFO] Something wrong during copying process.')

	def program_welcome_and_discription(self):
		print(f"{'=' * 30}SemiAutoMP3-Updater{'=' * 30}")
		print('Welcome to AutoUpdater of MP3 files!')
		print('It give ability to copy only new MP3 files from local disk dir')
		print('to your connected USB storage device into your music directory')
		print("If you don't have it, don't worry, it will be created during process.")
		print('Enjoy it! And Wish your favourite music be always with you.')

	def show_application_menu(self):
		pass

	def copy_new_mp3_files_to_selected_usb_partition_music_dir(self):
		print('Copying progess:')
		for new_mp3_file in self.new_mp3_files_for_copying_to_usb_storage_music_dir:
			if self.mp3_filename_has_spec_symbols(new_mp3_file):
				new_mp3_file = self.get_transformed_filename_with_spec_symbols_for_terminal(new_mp3_file)
			os.system(f"cp {self.found_music_dir_on_selected_local_disk_partition}/{new_mp3_file} \
						   {self.found_music_dir_on_selected_usb_storage_partition}")
			print('#', end = '')
		print()
		return True

	def mp3_filename_has_spec_symbols(self, mp3_filename: str):
		for spec_symbol in self.spec_symbols_for_cmd:
			if spec_symbol in mp3_filename:
				return True
		return False

	def get_transformed_filename_with_spec_symbols_for_terminal(self, filename: str):
		transformed_filename_for_terminal_cmd = ''

		for i in range(len(filename)):
			if filename[i] in self.spec_symbols_for_cmd:
				transformed_filename_for_terminal_cmd += f"\\{filename[i]}"
			else:
				transformed_filename_for_terminal_cmd += filename[i]

		print(transformed_filename_for_terminal_cmd)
		return transformed_filename_for_terminal_cmd

	def music_dir_is_absent_on_selected_usb_partition(self):
		if self.found_music_dir_on_selected_usb_storage_partition == '':
			return True
		else:
			return False

	def create_music_dir_on_selected_usb_partition(self):
		self.found_music_dir_on_selected_usb_storage_partition = \
		self.selected_connected_usb_storage_partition_mountpoint + '/Music_Dir'
		os.mkdir(
			self.found_music_dir_on_selected_usb_storage_partition
		)

	def created_usb_partition_music_dir_by_program_is_exist(self):
		partition_dirs_list = add_fns.get_filenames_in_dir(
			self.selected_connected_usb_storage_partition_mountpoint
		)
		print(partition_dirs_list)
		return 'Music_Dir' in partition_dirs_list

	def set_new_usb_partition_music_dir(self, new_usb_part_mp3_dir_path: str):
		self.found_music_dir_on_selected_usb_storage_partition = new_usb_part_mp3_dir_path

	def show_new_mp3_files_for_usb_storage_music_dir(self):
		print('[INFO] Found new MP3 files for selected USB storage partition:')
		for i in range(len(self.new_mp3_files_for_copying_to_usb_storage_music_dir)):
			print(f'#{i + 1} - {self.new_mp3_files_for_copying_to_usb_storage_music_dir[i]}')
		print()
		return True

	def define_new_mp3_files_for_copying_into_usb_music_dir(self):
		for local_music_dir_mp3_file in self.mp3_filenames_in_local_partition_music_dir:
			if local_music_dir_mp3_file not in self.mp3_filenames_in_selected_usb_partition_music_dir:
				self.new_mp3_files_for_copying_to_usb_storage_music_dir.append(local_music_dir_mp3_file)
		return True

	def define_filenames_in_local_partition_music_dir(self):
		self.mp3_filenames_in_local_partition_music_dir = os.listdir(
			self.found_music_dir_on_selected_local_disk_partition
		)

	def define_filenames_in_selected_usb_partition_music_dir(self):
		self.mp3_filenames_in_selected_usb_partition_music_dir = os.listdir(
			self.found_music_dir_on_selected_usb_storage_partition
		)

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
						self.selected_connected_usb_storage_partition_mountpoint = self.get_selected_partition_mountpoint(user_input_number)
						print(f'You selected partition with mountpoint: {self.selected_connected_usb_storage_partition_mountpoint}')
						user_answer = input('Are you agree with it[y/n]?: ')
						if user_answer == 'y':
							print('OK.')
							return True
					else:
						print('Wrong partition number! Try again.')

	def define_music_dir_abs_path_on_selected_usb_storage_partition(self, selected_usb_partition: str):
		if self.music_dir_searcher.main(selected_usb_partition):
			self.found_music_dir_on_selected_usb_storage_partition = self.music_dir_searcher.get_partition_music_dir_abs_path()
			if self.found_music_dir_on_selected_usb_storage_partition != '':
				print(f'[INFO] Found music dir on selected usb partition: {self.found_music_dir_on_selected_usb_storage_partition}')
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

	music_updater.update_music_on_selected_usb_storage_device()