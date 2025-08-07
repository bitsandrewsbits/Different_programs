# this will be experimental program for updating music files from local disk to external disk device
# Idea is to 
# 1)define music folder on your computer disks by the most MP3 folder by size
# 1.1 - define OS type - Windows, Linux.
# 1.2 - create diff algorithms for finding music folder in Windows, Linux. 
# 2)find external disk device, 
# 3)define what folder on external disk contains music files, or
# if this folder doesn't exist, create it.
# 4)If music folder was found on external disk, find only absent music files from local music folder.
# 5) copy new music files to your external disk.

#==============================================
#(1) - class, which in this file - Partition_Music_Dir_Searcher
# (2, 3) - separated class
# (4, 5) - main class in music_updater.py
#==============================================

# Also show process stages and their results(optional, maybe)

import platform
import psutil
import os
import re
from additional_functions import *

class Partition_Music_Dir_Searcher:
	def __init__(self):
		self.operation_system_type = platform.system()
		self.excluded_moutpoints = ['/snap', '/var']
		self.selected_partition_root_dir_abs_pathes_by_numbers = {}
		self.excluded_partition_root_dirs_abs_pathes_from_searching = []
		self.disk_partitions_regex = r"/dev/sda[1-9]" # so I think it works if local HDD is only one.
		self.all_disk_devices_mountpoints = {}
		self.user_data_disk_devices_mountpoints = {}
		self.dirs_with_nonzero_amount_of_MP3_files = {}    # {'dir_abs_path': number_of_MP3_files}
		self.dirs_by_levels_and_checked_status = {}    # {'dir_abs_path': [1, 'Unchecked']} - [dir_level_int, str]
		self.selected_partition_abs_path = ''
		self.current_login_user = self.define_log_in_user_to_Linux_system()
		self.current_search_dir_level = 0
		self.current_search_abs_dir_path = ''
		self.search_to_bottom = True
		self.search_to_up = False
		self.abs_dir_path_with_biggest_amount_of_MP3_files = ()

	def main(self, target_partition_abs_path = ''):
		self.reset_all_paramaters_for_new_search()

		self.selected_partition_abs_path = target_partition_abs_path
		self.show_operation_system_type()
		self.get_log_in_user_to_Linux_system()
		self.find_all_local_disk_devices_mountpoints()
		self.define_user_data_disk_devices_moutpoints()
		self.show_partitions_info_for_user()
		if target_partition_abs_path == '':
			if self.choose_local_disk_partition_for_searching() == False:
				return False
			self.selected_partition_abs_path = self.get_selected_partition_abs_path_for_searching_music_folder()
			print(self.selected_partition_abs_path)

		while True:
			self.show_selected_partition_root_dirnames_by_numbers()
			if self.define_user_excluded_dirs_abs_pathes():
				break
		return True # only interrupt for testing!
		
		# searching algorithm
		self.search_nonzero_MP3_dirs_in_partition_filesystem(self.selected_partition_abs_path)
		
		if self.dirs_with_nonzero_amount_of_MP3_files != {}:
			self.define_dir_with_biggest_amount_of_MP3_files()
			self.show_dir_with_biggest_amount_of_MP3_files()
		else:
			print('[INFO] Dirs with MP3 files was not found on selected usb storage partition.')
			print('[INFO] It will be created in the next stages.')
			return False
		return True

	def reset_all_paramaters_for_new_search(self):
		self.all_disk_devices_mountpoints = {}
		self.user_data_disk_devices_mountpoints = {}
		self.dirs_with_nonzero_amount_of_MP3_files = {}    # {'dir_abs_path': number_of_MP3_files}
		self.dirs_by_levels_and_checked_status = {}    # {'dir_abs_path': [1, 'Unchecked']} - [dir_level_int, str]
		self.selected_partition_abs_path = ''
		self.current_search_dir_level = 0
		self.current_search_abs_dir_path = ''
		self.search_to_bottom = True
		self.search_to_up = False
		self.abs_dir_path_with_biggest_amount_of_MP3_files = ()

	def get_partition_music_dir_abs_path(self):
		return self.abs_dir_path_with_biggest_amount_of_MP3_files[0]

	def show_operation_system_type(self):
		print('OS type:', self.operation_system_type)

	def find_all_local_disk_devices_mountpoints(self):
		for disk_partition in psutil.disk_partitions():
			self.all_disk_devices_mountpoints[disk_partition.device] = disk_partition.mountpoint
		return True

	def define_user_data_disk_devices_moutpoints(self):
		correct_mountpoint = True
		for disk_device in self.all_disk_devices_mountpoints:
			partition_mountpoint = self.all_disk_devices_mountpoints[disk_device]
			for excluded_mountpoint in self.excluded_moutpoints:
				if excluded_mountpoint in partition_mountpoint:
					correct_mountpoint = False
					break
			if correct_mountpoint:
				self.user_data_disk_devices_mountpoints[disk_device] = partition_mountpoint
			correct_mountpoint = True
		return True

	def choose_local_disk_partition_for_searching(self):
		input_message = "Select one disk partition for searching [enter number from left column of list above]\n[e - for exit]:"
		while True:
			user_input = input(input_message)
			if user_input.isdigit():
				user_input_number = int(user_input)
				if user_input_number >= 0 and user_input_number < len(self.user_data_disk_devices_mountpoints):
					disk_partitions_mountpoints = list(self.user_data_disk_devices_mountpoints.values())
					self.selected_partition_abs_path = disk_partitions_mountpoints[user_input_number]
					self.define_selected_partition_root_dir_abs_pathes_by_numbers()
					break
				else:
					print('Input value out of range! Try again.')
			elif user_input == 'e':
				return False
			else:
				print('Wrong type of input value! Try again.')

	def define_selected_partition_root_dir_abs_pathes_by_numbers(self):
		partition_root_dirs = get_only_directories_in_dir(self.selected_partition_abs_path)
		for (i, root_dir) in enumerate(partition_root_dirs, 1):
			self.selected_partition_root_dir_abs_pathes_by_numbers[i] = root_dir

	def show_selected_partition_root_dirnames_by_numbers(self):
		print("Choose Partition Root Dirs for Excluding from Searching:")
		for root_dir_number in self.selected_partition_root_dir_abs_pathes_by_numbers:
			dirname = get_last_dir_file_name_from_abs_path(
				self.selected_partition_root_dir_abs_pathes_by_numbers[root_dir_number]
			)
			print(f"({root_dir_number}) - {dirname}")

	def define_user_excluded_dirs_abs_pathes(self):
		while True:
			user_selected_dirs_numbers = input(
				"Select number of dir for excluding from searching\nFor multiple choise, numbers via whitespace:"
			)
			if user_selected_dirs_numbers == 'e':
				return False
			user_answer_elements = get_string_elements_splitting_by_whitespace(user_selected_dirs_numbers)
			if ''.join(user_answer_elements).isdigit():
				user_dirs_numbers = set([int(number) for number in user_answer_elements])
				if self.user_input_dirs_numbers_correct(user_dirs_numbers):
					for number in user_dirs_numbers:
						self.excluded_partition_root_dirs_abs_pathes_from_searching.append(
							self.selected_partition_root_dir_abs_pathes_by_numbers[number]
						)
					while True:
						print('Your selected excluded root dirs:')
						for dir_abs_path in self.excluded_partition_root_dirs_abs_pathes_from_searching:
							dirname = get_last_dir_file_name_from_abs_path(dir_abs_path)
							print(dirname)
						print('-' * 30)
						user_acceptance = input("Are you agree with selected excluded dirs?[y/n]: ")
						if user_acceptance == 'y':
							return True
						elif user_acceptance == 'n':
							self.excluded_partition_root_dirs_abs_pathes_from_searching = []
							break
						else:
							print('Wrong acceptence answer option! Input again.')
				else:
					print('Wrong or no-exist dir(s) number(s)! Input again.')
			else:
				print('Wrong input data! Try again.')

	def user_input_dirs_numbers_correct(self, user_input_dirs_numbers: set):
		for user_dir_number in user_input_dirs_numbers:
			if user_dir_number in self.selected_partition_root_dir_abs_pathes_by_numbers.keys():
				continue
			else:
				return False
		return True

	def show_partitions_info_for_user(self):
		print(f'[INFO] Found {len(self.user_data_disk_devices_mountpoints)} disk partitions.')
		print('Partitions:')
		partition_number = 0
		for disk_device in self.user_data_disk_devices_mountpoints:
			if self.device_is_disk_partition(disk_device):
				print(f'({partition_number}) - {self.user_data_disk_devices_mountpoints[disk_device]}')
			else:
				print(f'({partition_number})(USB Device Partition) - {self.user_data_disk_devices_mountpoints[disk_device]}')
			partition_number += 1
		print()

	def device_is_disk_partition(self, partition_str: str):
		return bool(re.match(self.disk_partitions_regex, partition_str))

	def get_selected_partition_abs_path_for_searching_music_folder(self):
		return self.selected_partition_abs_path

	def define_log_in_user_to_Linux_system(self):
		return os.getlogin()

	def get_log_in_user_to_Linux_system(self):
		return self.current_login_user
	
	def define_dir_with_biggest_amount_of_MP3_files(self):
		biggest_amount_of_MP3_files = 0
		for abs_dir_path in self.dirs_with_nonzero_amount_of_MP3_files:
			current_amount_of_MP3_files = self.dirs_with_nonzero_amount_of_MP3_files[abs_dir_path]
			if biggest_amount_of_MP3_files < current_amount_of_MP3_files:
				biggest_amount_of_MP3_files = current_amount_of_MP3_files
				self.abs_dir_path_with_biggest_amount_of_MP3_files = \
				(abs_dir_path, biggest_amount_of_MP3_files)

	def show_dir_with_biggest_amount_of_MP3_files(self):
		print(f'[INFO] Defined music directory on partition mountpoint - {self.selected_partition_abs_path}:')
		print(f'{self.abs_dir_path_with_biggest_amount_of_MP3_files[0]} - ', end = '')
		print(f'{self.abs_dir_path_with_biggest_amount_of_MP3_files[1]} file(s)\n')

	# search algorithm - search in depth + in width(combination)
	def search_nonzero_MP3_dirs_in_partition_filesystem(self, root_abs_dir_path):
		self.dirs_by_levels_and_checked_status[root_abs_dir_path] = [0, 'Unchecked']    # start point for searching
		self.current_search_abs_dir_path = root_abs_dir_path  # maybe for now. [WARNING]

		while not filesystem_tree_from_certain_dir_entire_checked(self.dirs_by_levels_and_checked_status):
			# TODO: add condition for excluded dirs - as checked status.
			if directories_exists_in_dir(self.current_search_abs_dir_path) and self.search_to_bottom:

				self.set_search_status_as_checked_for_dir(self.current_search_abs_dir_path)

				self.increase_search_dir_level_by_one()

				current_next_abs_dir_pathes = get_only_directories_in_dir(self.current_search_abs_dir_path)
				if self.abs_dir_pathes_not_exist_in_dirs_pathes_dict(current_next_abs_dir_pathes):
					self.add_all_next_level_abs_dirs_pathes_for_next_searching(current_next_abs_dir_pathes)
				
				# print(f'Child dirs for {self.current_search_abs_dir_path}:')
				# print(current_next_abs_dir_pathes)

				self.switch_from_checked_dir_tree_to_unchecked_on_same_level(current_next_abs_dir_pathes)
			else:
				self.set_search_status_as_checked_for_dir(self.current_search_abs_dir_path)
				self.search_to_bottom = False
				self.search_to_up = True
				self.decrease_search_dir_level_by_one()


			# need to do second step - check to up gradually.
			if self.search_to_up:
				current_abs_dir_pathes_for_checking = get_all_dirs_on_same_level_within_one_dir(
					self.current_search_abs_dir_path
				)
				print(current_abs_dir_pathes_for_checking)

				self.switch_from_checked_dir_tree_to_unchecked_on_same_level(current_abs_dir_pathes_for_checking)
				
				self.search_to_up = False
				self.search_to_bottom = True
			
			if self.all_dirs_on_current_level_checked_within_one_certain_dir(current_next_abs_dir_pathes):
				parent_abs_dir_path = get_parent_dir_for_child_dir(current_next_abs_dir_pathes[0])
				self.current_search_abs_dir_path = get_parent_dir_for_child_dir(parent_abs_dir_path)
				print('ALL subdirs was checked! Switching search dir...')

			print(f'[INFO] Current search dir path: {self.current_search_abs_dir_path}')
			
			if mp3_files_exist_in_dir(self.current_search_abs_dir_path):
				self.dirs_with_nonzero_amount_of_MP3_files[self.current_search_abs_dir_path] = \
				get_amount_of_MP3_files_in_dir(self.current_search_abs_dir_path)
		print('\n[INFO] Searching process - finished!')

	def add_all_next_level_abs_dirs_pathes_for_next_searching(self, abs_dir_pathes):
		for next_abs_dir_path in abs_dir_pathes:
			self.add_abs_dir_path_for_next_searching(next_abs_dir_path)

	def abs_dir_pathes_not_exist_in_dirs_pathes_dict(self, abs_dir_pathes):
		all_abs_dir_pathes = self.dirs_by_levels_and_checked_status.keys()
		for abs_dir_path in abs_dir_pathes:
			if abs_dir_path in all_abs_dir_pathes:
				return False

		return True

	def switch_from_checked_dir_tree_to_unchecked_on_same_level(self, abs_dir_pathes: list):
		for abs_dir_path in abs_dir_pathes:
			if self.dirs_by_levels_and_checked_status[abs_dir_path][1] == 'Unchecked':
				self.current_search_abs_dir_path = abs_dir_path
				break

	def add_abs_dir_path_for_next_searching(self, certain_abs_dir_path):
		self.dirs_by_levels_and_checked_status[certain_abs_dir_path] = [self.current_search_dir_level,
		 'Unchecked']

	def increase_search_dir_level_by_one(self):
		self.current_search_dir_level += 1

	def decrease_search_dir_level_by_one(self):
		self.current_search_dir_level -= 1

	def set_search_dir_level_for_dir(self, certain_abs_dir_path, dir_level: int):
		self.dirs_by_levels_and_checked_status[certain_abs_dir_path][0] = dir_level

	def set_search_status_as_checked_for_dir(self, certain_abs_dir_path):
		self.dirs_by_levels_and_checked_status[certain_abs_dir_path][1] = 'Checked'

	def all_dirs_on_current_level_checked_within_one_certain_dir(self, abs_dir_pathes: list):
		for abs_dir_path in abs_dir_pathes:
			if self.dirs_by_levels_and_checked_status[abs_dir_path][1] != 'Checked':
				return False
		else:
			return True

	def show_search_nonzero_MP3_dirs_result(self):
		print(f'[INFO] Found nonzero-MP3 dirs in disk partition - {self.selected_partition_abs_path}:')
		for abs_mp3_dir_path in self.dirs_with_nonzero_amount_of_MP3_files:
			number_of_MP3_files_in_dir = self.dirs_with_nonzero_amount_of_MP3_files[abs_mp3_dir_path]
			print(f'{abs_mp3_dir_path}: {number_of_MP3_files_in_dir} file/s')
		print()


if __name__ == '__main__':
	music_dir_searcher = Partition_Music_Dir_Searcher()
	music_dir_searcher.main()