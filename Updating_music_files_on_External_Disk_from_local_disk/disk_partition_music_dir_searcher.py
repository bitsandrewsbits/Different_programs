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
from additional_functions import *

class Partition_Music_Dir_Searcher:
	def __init__(self):
		self.operation_system_type = platform.system()
		self.disk_partitions_mountpoints = []
		self.dirs_with_nonzero_amount_of_MP3_files = {}    # {'dir_abs_path': number_of_MP3_files}
		self.dirs_by_levels_and_checked_status = {}    # {'dir_abs_path': [1, 'Unchecked']} - [dir_level_int, str]
		self.target_system_path = ''
		self.current_login_user = self.define_log_in_user_to_Linux_system()
		self.current_search_dir_level = 0
		self.current_search_abs_dir_path = ''
		self.search_to_bottom = True
		self.search_to_up = False
		self.abs_dir_path_with_biggest_amount_of_MP3_files = ()

	def main(self, target_partition_abs_path = ''):
		self.show_operation_system_type()
		self.find_all_partitions_mountpoints_on_local_disk()
		self.get_log_in_user_to_Linux_system()
		self.show_partitions_info_for_user()
		if target_partition_abs_path == '':
			self.choose_local_disk_partition_for_searching()
			target_system_path = self.get_target_system_path_for_searching_music_folder()
			print(target_system_path)

		# searching algorithm
		self.search_nonzero_MP3_dirs_in_partition_filesystem(target_system_path)
		
		self.define_dir_with_biggest_amount_of_MP3_files()
		self.show_dir_with_biggest_amount_of_MP3_files()
		return True

	def get_partition_music_dir_abs_path(self):
		return self.abs_dir_path_with_biggest_amount_of_MP3_files[0]

	def show_operation_system_type(self):
		print('OS type:', self.operation_system_type)

	def find_all_partitions_mountpoints_on_local_disk(self):
		for disk_partition in psutil.disk_partitions():
			# print('Root dir for partition:', disk_partition.mountpoint)
			self.disk_partitions_mountpoints.append(disk_partition.mountpoint)

	def choose_local_disk_partition_for_searching(self):
		input_message = "Select one disk partition for searching [enter number from left column of list above]:"
		while True:
			user_input = input(input_message)
			if user_input.isdigit():
				user_input_number = int(user_input)
				if user_input_number >= 0 and user_input_number < len(self.disk_partitions_mountpoints):
					self.target_system_path = self.disk_partitions_mountpoints[user_input_number]
					break
				else:
					print('Input value out of range! Try again.')
			else:
				print('Wrong type of input value! Try again.')

	def show_partitions_info_for_user(self):
		print(f'[INFO] Found {len(self.disk_partitions_mountpoints)} disk partitions.')
		print('Partitions:')
		for i in range(len(self.disk_partitions_mountpoints)):
			print(f'({i}) - {self.disk_partitions_mountpoints[i]}')

		print()

	def get_target_system_path_for_searching_music_folder(self):
		return self.target_system_path

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
		print(f'[INFO] Defined music directory on partition mountpoint - {self.target_system_path}:')
		print(f'{self.abs_dir_path_with_biggest_amount_of_MP3_files[0]} - ', end = '')
		print(f'{self.abs_dir_path_with_biggest_amount_of_MP3_files[1]} file(s)\n')

	# search algorithm - search in depth + in width(combination)
	def search_nonzero_MP3_dirs_in_partition_filesystem(self, root_abs_dir_path):
		self.dirs_by_levels_and_checked_status[root_abs_dir_path] = [0, 'Unchecked']    # start point for searching
		self.current_search_abs_dir_path = root_abs_dir_path  # maybe for now. [WARNING]

		while not filesystem_tree_from_certain_dir_entire_checked(self.dirs_by_levels_and_checked_status):
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
		print(f'[INFO] Found nonzero-MP3 dirs in disk partition - {self.target_system_path}:')
		for abs_mp3_dir_path in self.dirs_with_nonzero_amount_of_MP3_files:
			number_of_MP3_files_in_dir = self.dirs_with_nonzero_amount_of_MP3_files[abs_mp3_dir_path]
			print(f'{abs_mp3_dir_path}: {number_of_MP3_files_in_dir} file/s')
		print()


if __name__ == '__main__':
	music_dir_searcher = Partition_Music_Dir_Searcher()
	music_dir_searcher.main()