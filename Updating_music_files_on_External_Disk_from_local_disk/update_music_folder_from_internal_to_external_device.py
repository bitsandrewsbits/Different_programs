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
		self.dirs_by_levels_and_checked_status = {}  # {'dir_abs_path': [1, 'Unchecked']} - [dir_level_int, str]
		self.target_system_path = ''
		self.current_login_user = self.define_log_in_user_to_Linux_system()
		self.current_search_dir_level = 0
		self.excluded_dirnames_for_search = ['SOFT']  # list can be extended
		self.current_search_abs_dir_path = ''
		self.search_to_bottom = True
		self.search_to_up = False

	def get_operation_system_type(self):
		# print('OS type:', self.operation_system_type)
		return self.operation_system_type

	def get_all_partitions_mountpoints_on_local_disk(self):
		for disk_partition in psutil.disk_partitions():
			print('Root dir for partition:', disk_partition.mountpoint)
			self.disk_partitions_mountpoints.append(disk_partition.mountpoint)

	# def find_directory_with_majority_MP3_files(self):
		# this method - algorithm of finding music directory

	# search algorithm - search in depth
	def search_nonzero_MP3_dirs_in_partition_filesystem(self, root_abs_dir_path):
		self.dirs_by_levels_and_checked_status[root_abs_dir_path] = [0, 'Unchecked']    # start point for searching

		while not filesystem_tree_for_certain_dir_entire_checked():
			if directories_exists_in_dir(self.current_search_abs_dir_path) and self.search_to_bottom:

				set_search_status_as_checked_for_dir()

				increase_search_dir_level_by_one()
				switch_from_checked_dir_tree_to_unchecked_on_same_level(current_next_abs_dir_pathes)

				add_all_next_level_abs_dirs_pathes_for_next_searching(self.current_search_abs_dir_path)
				current_next_abs_dir_pathes = get_only_directories_in_dir(self.current_search_abs_dir_path)
			else:
				self.search_to_bottom = False
				self.search_to_up = True
				decrease_search_dir_level_by_one()

			# need to do second step - check to up gradually.
			if self.search_to_up:
				current_abs_dir_pathes_for_checking = get_all_dirs_on_same_level_within_one_dir(
					self.current_search_abs_dir_path
				)

				switch_from_checked_dir_tree_to_unchecked_on_same_level(current_abs_dir_pathes_for_checking)
				
				self.search_to_up = False
				self.search_to_bottom = True

				# need to test.
			
			if all_dirs_on_current_level_checked_within_one_certain_dir(current_next_abs_dir_pathes):
				parent_abs_dir_path = get_parent_dir_for_child_dir(current_next_abs_dir_pathes[0])
				# maybe need to up one more level - parent of parent dir.
				self.current_search_abs_dir_path = parent_abs_dir_path


	def get_all_dirs_on_same_level_within_one_dir(certain_abs_dir_path: str):
		# function for getting other dirs on the same level with input dir
		# they all have one parent dir.
		parent_abs_dir_path = get_parent_dir_for_child_dir(certain_abs_dir_path)
		next_level_dirs = get_only_directories_in_dir(parent_abs_dir_path)

		other_next_level_dirs = []

		for abs_dir_path in next_level_dirs:
			if certain_abs_dir_path != certain_abs_dir_path:
				other_next_level_dirs.append(abs_dir_path)

		return other_next_level_dirs

	def get_parent_dir_for_child_dir(certain_abs_dir_path):
		parent_abs_dir_path = ''
		certain_abs_dir_path = list(certain_abs_dir_path)
		for i in range(len(certain_abs_dir_path), 0, -1):
			if certain_abs_dir_path[i] == '/':
				return parent_abs_dir_path
			else:
				certain_abs_dir_path.pop(-1)


	def add_all_next_level_abs_dirs_pathes_for_next_searching(certain_abs_dir_path):
		increase_search_dir_level_by_one()
		next_abs_dir_pathes_for_searching = self.get_only_directories_in_dir(certain_abs_dir_path)

		for next_abs_dir_path in next_abs_dir_pathes_for_searching:
			add_abs_dir_path_for_next_searching(next_abs_dir_path)


	def switch_from_checked_dir_tree_to_unchecked_on_same_level(abs_dir_pathes: list):
		for abs_dir_path in abs_dir_pathes:
			if self.dirs_by_levels_and_checked_status[abs_dir_pathr][1] == 'Unchecked':
				self.current_search_abs_dir_path = abs_dir_path

	def add_abs_dir_path_for_next_searching(certain_abs_dir_path):
		self.dirs_by_levels_and_checked_status[certain_abs_dir_path] = [self.current_search_dir_level,
		 'Unchecked']

	def increase_search_dir_level_by_one():
		self.current_search_dir_level += 1

	def decrease_search_dir_level_by_one():
		self.current_search_dir_level -= 1

	def set_search_dir_level_for_dir(certain_abs_dir_path, dir_level: int):
		self.dirs_by_levels_and_checked_status[certain_abs_dir_path][0] = dir_level

	def set_search_status_as_checked_for_dir(certain_abs_dir_path):
		self.dirs_by_levels_and_checked_status[certain_abs_dir_path][1] = 'Checked'

	def all_dirs_on_current_level_checked_within_one_certain_dir(abs_dir_pathes: list):
		for abs_dir_path in abs_dir_pathes:
			if self.dirs_by_levels_and_checked_status[abs_dir_path][1] != 'Checked':
				return False
		else:
			return True

	def filesystem_tree_for_certain_dir_entire_checked():
		for abs_dir_path in self.dirs_by_levels_and_checked_status:
			if self.dirs_by_levels_and_checked_status[abs_dir_path][1] == 'Unchecked':
				return False

		return True

	# this method level by level dir checking for nonzero MP3 dirs, and set dirname and amount of MP3 files.
	# def set_dir_and_nonzero_amount_of_MP3_files_search_from_target_dir(self, root_abs_dir_path):
	# 	# first step - get dirs list on first level
	# 	current_level_abs_dirs_pathes = [root_abs_dir_path]
	# 	next_level_abs_dirs_pathes = ['not empty']

	# 	# executing while in next level dirs is nothing, but files.
	# 	while next_level_abs_dirs_pathes != []:
	# 		next_level_abs_dirs_pathes = []
	# 		print('Current level abs dir pathes:', current_level_abs_dirs_pathes)
	# 		print('\n\n')
	# 		for current_level_abs_dir_path in current_level_abs_dirs_pathes:
	# 			if self.mp3_files_exist_in_dir(current_level_abs_dir_path):
	# 				self.directories_with_nonzero_amount_of_MP3_files[current_level_abs_dir_path] = \
	# 				self.get_amount_of_MP3_files_in_dir(current_level_abs_dir_path)
	# 			if directories_exists_in_dir(current_level_abs_dir_path):
	# 				next_level_dirnames = self.get_only_directories_in_dir(current_level_abs_dir_path)
	# 				next_level_dirnames_without_excluded_dirs = self.get_dirs_list_without_excluded_dirs(next_level_dirnames)
	# 				# print('Next Level dirs:', next_level_dirnames_without_excluded_dirs)
	# 				next_level_abs_dirs_pathes_from_one_dir = \
	# 				self.get_abs_dir_pathes_from_one_dir(current_level_abs_dir_path, next_level_dirnames_without_excluded_dirs)
	# 			next_level_abs_dirs_pathes += next_level_abs_dirs_pathes_from_one_dir

	# 		current_level_abs_dirs_pathes = next_level_abs_dirs_pathes

	# 	print('Result of MP3 nonzero folders:')
	# 	print(self.directories_with_nonzero_amount_of_MP3_files)

	def get_dirs_list_without_excluded_dirs(self, dirnames):
		result_dirs = []
		for dirname in dirnames:
			if self.dir_is_excluded_from_search(dirname):
				print('Excluded dir:', dirname)
			else:
				result_dirs.append(dirname)

		return result_dirs

	def dir_is_excluded_from_search(self, dirname):
		if dirname in self.excluded_dirnames_for_search:
			return True
		else:
			return False

	def get_abs_dir_pathes_of_all_next_level_dirs(self, abs_current_level_dirs_pathes):
		all_next_level_abs_dir_pathes = []

		for abs_current_level_dir_path in abs_current_level_dirs_pathes:
			dirnames_in_dir = self.get_only_directories_in_dir(abs_current_level_dir_path)
			next_level_abs_dir_pathes_in_current_level_dir = \
			self.get_abs_dir_pathes_from_one_dir(abs_current_level_dir_path, dirnames_in_dir)
			all_next_level_abs_dir_pathes.append(next_level_abs_dir_pathes_in_current_level_dir)

		return all_next_level_abs_dir_pathes

	def get_abs_dir_pathes_from_one_dir(self, target_abs_dir_path, dirnames_in_target_dir):
		result_abs_pathes_for_target_dir = []
		for dirname in dirnames_in_target_dir:
			temp_abs_dir_path = target_abs_dir_path + '/' + dirname
			result_abs_pathes_for_target_dir.append(temp_abs_dir_path)

		return result_abs_pathes_for_target_dir

	def mp3_files_exist_in_dir(self, certain_abs_dir_path):
		files_in_dir = self.get_only_files_in_dir(certain_abs_dir_path)
		for filename in files_in_dir:
			if filename[-3:] == 'mp3':
				return True

		return False

	def directories_exists_in_dir(certain_abs_dir_path):
		dirnames = self.get_only_directories_in_dir(certain_abs_dir_path)

		if dirnames != []:
			return True
		else:
			return False

	def get_amount_of_MP3_files_in_dir(self, certain_abs_dir_path):
		files_in_dir = self.get_only_files_in_dir(certain_abs_dir_path)
		amount_of_MP3_files_in_dir = 0

		for file in files_in_dir:
			if file[-3:] == 'mp3':
				amount_of_MP3_files_in_dir += 1

		return amount_of_MP3_files_in_dir

	def get_only_files_in_dir(self, certain_abs_dir_path):
		all_filenames_in_dir = self.get_filenames_in_dir(certain_abs_dir_path)

		only_files_in_dir = []
		for filename in all_filenames_in_dir:
			temp_abs_filename_path = certain_abs_dir_path + '/' + filename
			if not os.path.isdir(temp_abs_filename_path):
				only_files_in_dir.append(filename)

		return only_files_in_dir

	def get_only_directories_in_dir(self, certain_abs_dir_path):
		dirs_in_certain_dir = []
		all_filenames_in_dir = self.get_filenames_in_dir(certain_abs_dir_path)
		for filename in all_filenames_in_dir:
			temp_abs_filename_path = certain_abs_dir_path + '/' + filename
			if os.path.isdir(temp_abs_filename_path):
				dirs_in_certain_dir.append(filename)

		return dirs_in_certain_dir

	def get_target_system_path_for_searching_music_folder(self):
		if self.get_operation_system_type() == 'Linux':
			self.target_system_path = '/media/'
			self.target_system_path += self.current_login_user

		print('Target dir for searching:', self.target_system_path)
		return self.target_system_path

	def get_filenames_in_dir(self, abs_path_to_dir):
		try:
			return os.listdir(abs_path_to_dir)
		except Exception as error:
			return ['error(permission denied)']

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
# test1 = test_obj.get_filenames_in_dir('/media/kov_andrew')
# print('dirs in dir:', test1)
test_obj.get_log_in_user_to_Linux_system()
target_system_path = test_obj.get_target_system_path_for_searching_music_folder()
# test_obj.set_dir_and_nonzero_amount_of_MP3_files_search_from_target_dir(target_system_path)

# testing search in depth algorithm - (in future commits)