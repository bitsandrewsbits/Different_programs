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

# Also show process stages and their results.

import platform
import psutil
import os

class Music_Dir_on_Local_Disk:
	def __init__(self):
		self.operation_system_type = platform.system()
		self.disk_partitions_mountpoints = []
		self.directories_with_nonzero_amount_of_MP3_files = {}
		self.target_system_path = ''
		self.current_login_user = self.define_log_in_user_to_Linux_system()
		self.dir_level_number = 0

	def get_operation_system_type(self):
		# print('OS type:', self.operation_system_type)
		return self.operation_system_type

	def get_all_partitions_mountpoints_on_local_disk(self):
		for disk_partition in psutil.disk_partitions():
			print('Root dir for partition:', disk_partition.mountpoint)
			self.disk_partitions_mountpoints.append(disk_partition.mountpoint)

	def find_directory_with_majority_MP3_files(self):
		# this method - algorithm of finding music directory

	# TODO: need refactoring
	def set_dirnames_with_MP3_files_amount(self, certain_dir):
		# need to develop method for gathering info about all dir with non-zero amount of MP3 files.
		# it's search in depth and in width. maybe combination.

	# this method level by level dir checking for nonzero MP3 dirs, and set dirname and amount of MP3 files.
	def set_dir_and_nonzero_amount_of_MP3_files_search_from_target_dir(self, root_dir):
		# first step - get dirs list on first level
		current_level_dirs = self.get_only_directories_in_dir(root_dir)
		if self.mp3_files_exist_in_dir(root_dir):
			self.directories_with_nonzero_amount_of_MP3_files[root_dir] = self.get_amount_of_MP3_files_in_dir(root_dir)
		next_level_dirs = current_level_dirs

		# executing while in next level dirs is nothing, but files.
		while next_level_dirs != []:
			next_level_dirs = []
			for current_level_dir in current_level_dirs:
				if self.directories_exists_on_dir(current_level_dir):
					next_level_dirs_for_current_level_dir = self.get_only_directories_in_dir(current_level_dir)
					next_level_dirs.append(next_level_dirs_for_current_level_dir)



	def mp3_files_exist_in_dir(self, certain_dir):
		files_in_dir = self.get_only_files_in_dir(certain_dir)
		for file in files_in_dir:
			if filename[-3:] == 'mp3':
				return True

		return False

	def directories_exists_on_dir(self, certain_dir):
		dirnames = self.get_only_directories_in_dir(certain_dir)

		if dirnames != []:
			return True
		else:
			return False

	def get_amount_of_MP3_files_in_dir(self, certain_dir):
		files_in_dir = self.get_only_files_in_dir(certain_dir)
		amount_of_MP3_files_in_dir = 0

		for file in files_in_dir:
			if file[-3:] == 'mp3':
				amount_of_MP3_files_in_dir += 1

		return amount_of_MP3_files_in_dir

	def get_only_files_in_dir(self, certain_dir):
		all_filenames_in_dir = os.listdir(certain_dir)
		only_files_in_dir = []
		for filename in all_filenames_in_dir:
			if not os.path.isdir(filename):
				only_files_in_dir.append(filename)

		return only_files_in_dir

	def get_only_directories_in_dir(self, certain_dir):
		dirs_in_certain_dir = []
		all_filenames_in_dir = self.get_filenames_in_dir(certain_dir)
		for filename in all_filenames_in_dir:
			if os.path.isdir(filename):
				dirs_in_certain_dir.append(filename)

		return dirs_in_certain_dir

	def get_target_system_path_for_searching_music_folder(self):
		if self.get_operation_system_type() == 'Linux':
			self.target_system_path = '/media/'
			self.target_system_path += self.current_login_user

		return self.target_system_path

	def get_filenames_in_dir(self, abs_path_to_dir):
		return os.listdir(abs_path_to_dir)

	def filename_is_directory(self, filename):
		if os.path.isdir(filename):
			return True
		else:
			return False

	def define_log_in_user_to_Linux_system(self):
		return os.getlogin()

	def get_log_in_user_to_Linux_system(self):
		print('current login user:', self.current_login_user)
		return self.current_login_user

	# def define_music_folder_on_local_disk(self):
		# if self.get_operation_system_type() == 'Linux':
		# 	self.get_not_empty_directories_with_MP3_files() # it will develop in future commits


test_obj = Music_Dir_on_Local_Disk()
# test_obj.get_operation_system_type()
# test_obj.get_all_partitions_mountpoints_on_local_disk()
# test_obj.get_log_in_user_to_Linux_system()
# files_in_certain_dir = test_obj.get_filenames_in_dir('/media/')
# print(files_in_certain_dir)


