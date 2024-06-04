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

class Music_Dir_on_Local_Disk:
	def __init__(self):
		self.operation_system_type = platform.system()
		self.disk_partitions_and_partitions_abs_path = {}
		self.directories_with_MP3_files_amount = {}

	def get_operation_system_type(self):
		# print('OS type:', self.operation_system_type)
		return self.operation_system_type

	def define_all_partitions_on_local_disk(self):
		for disk_partition in psutil.disk_partitions():
			if disk_partition.fstype:
				print('Root dir for partition:', disk_partition.mountpoint)


test_obj = Music_Dir_on_Local_Disk()
# test_obj.get_operation_system_type()
test_obj.define_all_partitions_on_local_disk()