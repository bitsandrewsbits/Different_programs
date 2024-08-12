# in this file will be created class for searching and defining
# connected external devices like flash, external HDD, SSD, or another.
# if nothing external connected - to tell user about it, and terminating program.

class External_Device_Searcher:
	def __init__(self):
		pass

	def external_device_connected_to_computer(self):
		# question: how exactly to determine which mounted partitions to computer - is external USB hard disk, USB-flash partitions?