# decoding QR-code version-1

example_of_QR_code = [[1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1], 
					  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
  					  [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1], 
  					  [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1], 
					  [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1], 
					  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1], 
					  [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1], 
					  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
					  [0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], 
					  [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1], 
					  [0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1], 
					  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], 
					  [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], 
					  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0], 
					  [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1], 
					  [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 
					  [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1], 
					  [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0], 
					  [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1], 
					  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0], 
					  [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1]
]

mask = 0

def decode_QR_code_version_1():
	# for right vertical code design
	pass


def get_content_part_from_QR_code(QR_as_2D_array = [[1, 1], [0, 1]]):
	rows_amount = 8
	columns_amount = 12

	start_content_column = 13
	start_content_row = 9

	result_QR_code_content_part = []
	current_writing_row = -1
	for i in range(len(QR_as_2D_array)):
		if i >= start_content_row:
			result_QR_code_content_part.append([])
			current_writing_row += 1
		for j in range(len(QR_as_2D_array[i])):
			if i >= 11 and (j == 13 or j == 14):
				result_QR_code_content_part[current_writing_row].append('n')
			elif i >= start_content_row and j >= start_content_column:
				result_QR_code_content_part[current_writing_row].append(QR_as_2D_array[i][j])

	return result_QR_code_content_part

def show_matrix_in_pretty_format(arr_2d = [[0, 0],[1, 1]]):
	for i in range(len(arr_2d)):
		print(arr_2d[i])


content_part_of_QR_code = get_content_part_from_QR_code(example_of_QR_code)
show_matrix_in_pretty_format(content_part_of_QR_code)
















