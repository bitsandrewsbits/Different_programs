# additional functions for classes methods.
import os

def get_all_dirs_on_same_level_within_one_dir(certain_abs_dir_path: str):
	# function for getting other dirs on the same level with input dir
	# they all have one parent dir.
	parent_abs_dir_path = get_parent_dir_for_child_dir(certain_abs_dir_path)
	next_level_dirs = get_only_directories_in_dir(parent_abs_dir_path)

	other_next_level_dirs = []

	for abs_dir_path in next_level_dirs:
		if abs_dir_path != certain_abs_dir_path:
			other_next_level_dirs.append(abs_dir_path)

	return other_next_level_dirs

def get_parent_dir_for_child_dir(certain_abs_dir_path):
	parent_abs_dir_path = ''
	certain_abs_dir_path = list(certain_abs_dir_path)
	for i in range(len(certain_abs_dir_path) - 1, 0, -1):
		if certain_abs_dir_path[i] == '/':
			parent_abs_dir_path = ''.join(certain_abs_dir_path[:-1])    # without last symbol '/'
			return parent_abs_dir_path
		else:
			certain_abs_dir_path.pop(-1)

def filesystem_tree_from_certain_dir_entire_checked(dirs_pathes_statuses: dict):
	for abs_dir_path_status in dirs_pathes_statuses:
		if dirs_pathes_statuses[abs_dir_path_status][1] == 'Unchecked':
			return False

	return True


def get_abs_dir_pathes_of_all_next_level_dirs(abs_current_level_dirs_pathes):
	all_next_level_abs_dir_pathes = []

	for abs_current_level_dir_path in abs_current_level_dirs_pathes:
		dirnames_in_dir = get_only_directories_in_dir(abs_current_level_dir_path)
		
		next_level_abs_dir_pathes_in_current_level_dir = \
		get_abs_dir_pathes_from_one_dir(abs_current_level_dir_path, dirnames_in_dir)
		all_next_level_abs_dir_pathes.append(next_level_abs_dir_pathes_in_current_level_dir)

	return all_next_level_abs_dir_pathes


def get_abs_dir_pathes_from_one_dir(target_abs_dir_path, dirnames_in_target_dir):
	result_abs_pathes_for_target_dir = []
	for dirname in dirnames_in_target_dir:
		temp_abs_dir_path = target_abs_dir_path + '/' + dirname
		result_abs_pathes_for_target_dir.append(temp_abs_dir_path)

	return result_abs_pathes_for_target_dir


def mp3_files_exist_in_dir(certain_abs_dir_path):
	files_in_dir = get_only_files_in_dir(certain_abs_dir_path)
	for filename in files_in_dir:
		if filename[-3:] == 'mp3':
			return True

	return False


def directories_exists_in_dir(certain_abs_dir_path):
	dirnames = get_only_directories_in_dir(certain_abs_dir_path)

	return dirnames != []


def get_amount_of_MP3_files_in_dir(certain_abs_dir_path):
	files_in_dir = get_only_files_in_dir(certain_abs_dir_path)
	amount_of_MP3_files_in_dir = 0

	for file in files_in_dir:
		if file[-3:] == 'mp3':
			amount_of_MP3_files_in_dir += 1

	return amount_of_MP3_files_in_dir


def get_only_files_in_dir(certain_abs_dir_path):
	all_filenames_in_dir = get_filenames_in_dir(certain_abs_dir_path)

	only_files_in_dir = []
	for filename in all_filenames_in_dir:
		temp_abs_filename_path = certain_abs_dir_path + '/' + filename
		if not os.path.isdir(temp_abs_filename_path):
			only_files_in_dir.append(filename)

	return only_files_in_dir


def get_only_directories_in_dir(certain_abs_dir_path):
	dirs_in_certain_dir = []
	all_filenames_in_dir = get_filenames_in_dir(certain_abs_dir_path)
	for filename in all_filenames_in_dir:
		temp_abs_filename_path = certain_abs_dir_path + '/' + filename
		if os.path.isdir(temp_abs_filename_path):
			dirs_in_certain_dir.append(temp_abs_filename_path)

	return dirs_in_certain_dir


def get_filenames_in_dir(abs_path_to_dir):
	try:
		return os.listdir(abs_path_to_dir)
	except Exception:
		return 'error(permission denied)'

def get_string_elements_splitting_by_whitespace(string: str):
	str_elements = string.split(' ')
	result_elements = [result_elem for result_elem in str_elements if result_elem != '']

	return result_elements

def get_last_dir_file_name_from_abs_path(dir_abs_path: str):
	dir_abs_path_parts = dir_abs_path.split('/')
	return dir_abs_path_parts[-1]

def get_file_size_in_bytes(file_abs_path: str):
	file_status = os.stat(file_abs_path)
	file_size_in_bytes = file_status.st_size
	return file_size_in_bytes

if __name__ == '__main__':
	# test_str = "a    b bi c   8 d   =  98/2834"
	# print(get_string_elements_splitting_by_whitespace(test_str))

	test_abs_path = "insert/your/file/abs/path"
	get_file_size_in_bytes(test_abs_path)
