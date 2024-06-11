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
		self.not_empty_directories_with_MP3_files = {}
		self.target_system_path = ''
		self.current_login_user = self.define_log_in_user_to_Linux_system()

	def get_operation_system_type(self):
		# print('OS type:', self.operation_system_type)
		return self.operation_system_type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

	def get_all_partitions_mountpoints_on_local_disk(self):
		for disk_partition in psutil.disk_partitions():
			print('Root dir for partition:', disk_partition.mountpoint)
			self.disk_partitions_mountpoints.append(disk_partition.mountpoint)

	def find_directory_with_majority_MP3_files(self):
		# this method - algorithm of finding music directory

	def get_amount_of_MP3_in_dir(self, certain_dir):
		# TODO: need refactoring
		all_filenames_in_dir = os.listdir(certain_dir)
		self.not_empty_directories_with_MP3_files[certain_dir]
		for filename in all_filenames_in_dir:
			if not os.path.isdir(filename) and filename[-3:] == 'mp3':
				self.not_empty_directories_with_MP3_files[certain_dir]

	def mp3_files_not_exist_in_dir(self, certain_dir):
		files_in_dir = self.get_only_files_in_dir(certain_dir)
		for file in files_in_dir:
			if filename[-3:] == 'mp3':
				return False

		return True

	def get_only_files_in_dir(self, certain_dir):
		all_filenames_in_dir = os.listdir(certain_dir)
		only_files_in_dir = []
		for filename in all_filenames_in_dir:
			if not os.path.isdir(filename):
				only_files_in_dir.append(filename)

		return only_files_in_dir

	def get_directories_in_dir(self, certain_dir):
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

	def define_music_folder_on_local_disk(self):
		if self.get_operation_system_type() == 'Linux':
			self.get_not_empty_directories_with_MP3_files() # it will develop in future commits


test_obj = Music_Dir_on_Local_Disk()
# test_obj.get_operation_system_type()
# test_obj.get_all_partitions_mountpoints_on_local_disk()
# test_obj.get_log_in_user_to_Linux_system()
# files_in_certain_dir = test_obj.get_filenames_in_dir('/media/')
# print(files_in_certain_dir)


