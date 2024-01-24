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


def get_QR_content_coordinates_values(QR_content_part = [[1, 0], [0, 1]]):
	result_bits_sequence_with_coordinates = {}

	rows_index_i = len(QR_content_part) - 1
	columns_index_j = len(QR_content_part[0]) - 1
	movement_vector_for_read_QR_content = 'up'
	QR_content_bit_amount = len(QR_content_part) * len(QR_content_part[0])
	QR_row_max_index = len(QR_content_part) - 1
	for _ in range(0, QR_content_bit_amount):

		result_bits_sequence_with_coordinates[(rows_index_i, columns_index_j)] = QR_content_part[rows_index_i][columns_index_j]
		# result_bits_string += str(QR_content_part[rows_index_i][columns_index_j])

		# first phase - from down to up	
		if rows_index_i > 0 and columns_index_j % 2 != 0 and movement_vector_for_read_QR_content == 'up':
			columns_index_j -= 1
		elif rows_index_i > 0 and columns_index_j % 2 == 0 and movement_vector_for_read_QR_content == 'up':
			columns_index_j += 1
			rows_index_i -= 1
		# link between first and second algorithm phases
		elif rows_index_i == 0 and movement_vector_for_read_QR_content == 'up':
			columns_index_j -= 1
			# result_bits_string += str(QR_content_part[rows_index_i][columns_index_j])
			result_bits_sequence_with_coordinates[(rows_index_i, columns_index_j)] = QR_content_part[rows_index_i][columns_index_j]
			columns_index_j -= 1
			result_bits_sequence_with_coordinates[(rows_index_i, columns_index_j)] = QR_content_part[rows_index_i][columns_index_j]
			# result_bits_string += str(QR_content_part[rows_index_i][columns_index_j])
			movement_vector_for_read_QR_content = 'down'
			# print('Changing vector of reading to BOTTOM!')

		
		# second phase - from up to down
		if rows_index_i < QR_row_max_index and columns_index_j % 2 != 0 and movement_vector_for_read_QR_content == 'down':
			columns_index_j -= 1
		elif rows_index_i < QR_row_max_index and columns_index_j % 2 == 0 and movement_vector_for_read_QR_content == 'down':
			columns_index_j += 1
			rows_index_i += 1
		# link from second -> first phase of algorithm
		elif rows_index_i == QR_row_max_index and movement_vector_for_read_QR_content == 'down':
			columns_index_j -= 1
			result_bits_sequence_with_coordinates[(rows_index_i, columns_index_j)] = QR_content_part[rows_index_i][columns_index_j]
			# result_bits_string += str(QR_content_part[rows_index_i][columns_index_j])
			columns_index_j -= 1
			movement_vector_for_read_QR_content = 'up'
			# print('Changing vector of reading to UP!')

		# other values - we don't need. length of bit sequence = 76
		if len(result_bits_sequence_with_coordinates) == 76:
			break

	# return result_bits_string[:-20] # return only data bits, without 'n' symbols
	return result_bits_sequence_with_coordinates

def get_modified_QR_data_coordinates_values(QR_coordinates_and_values = {(5, 5): 0}):
	new_QR_data_coordinates_values = {}
	rows_amount_to_add = 9
	columns_amount_to_add = 13
	for coordinates in QR_coordinates_and_values:
		new_coordinate_row = coordinates[0] + rows_amount_to_add
		new_coordinate_column = coordinates[1] + columns_amount_to_add
		new_QR_data_coordinates_values[(new_coordinate_row, new_coordinate_column)] = QR_coordinates_and_values[coordinates]

	return new_QR_data_coordinates_values


def get_QR_data_bit_sequence(QR_coordinates_and_values = {(5, 5): 0}):
	result_bit_sequence = ''
	for coordinates in QR_coordinates_and_values:
		if (coordinates[0] + coordinates[1]) % 2 == mask:
			bit_after_mask = (QR_coordinates_and_values[coordinates] - 1) ** 2
			result_bit_sequence += str(bit_after_mask) + str(QR_coordinates_and_values[coordinates])
		else:
			result_bit = QR_coordinates_and_values[coordinates]
			result_bit_sequence += str(0) + str(QR_coordinates_and_values[coordinates])

	return result_bit_sequence


content_part_of_QR_code = get_content_part_from_QR_code(example_of_QR_code)
show_matrix_in_pretty_format(content_part_of_QR_code)

QR_bits_coordinates_values = get_QR_content_coordinates_values(content_part_of_QR_code)
right_QR_bits_coordinates_values = get_modified_QR_data_coordinates_values(QR_bits_coordinates_values)
print(right_QR_bits_coordinates_values)

QR_bit_sequence = get_QR_data_bit_sequence(right_QR_bits_coordinates_values)
print('QR bit sequence:', QR_bit_sequence)
print('bits sequence length =', len(QR_bit_sequence))









