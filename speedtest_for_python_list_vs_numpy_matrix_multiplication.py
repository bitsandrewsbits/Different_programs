# implementation of speedtest for matrix multiplication
# python list matrix vs numpy array matrix
import random
import numpy as np
from datetime import datetime

matrix_sizes = [size for size in range(10, 10000, 1000)]

def get_py_list_matrix(size: int):
	return [[random.randint(0, 10000) for _ in range(size)] for _ in range(size)]

def py_list_matrix_multiplication(matrix_size: int):
	A = get_py_list_matrix(matrix_size)
	B = get_py_list_matrix(matrix_size)
	result_C = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]
	
	for i in range(len(A)):
  		k = 0
  		for j in range(len(A)):
  			result_C[i][j] = sum([A[i][j] * B[j][k] for j in range(len(A))])
  			k += 1
	return result_C

def numpy_array_matrix_multiplication(matrix_size: int):
	A = np.array(get_py_list_matrix(matrix_size))
	B = np.array(get_py_list_matrix(matrix_size))
	return A.dot(B)

def get_execution_delta_t(function_obj, matrix_size):
	t0 = datetime.now()
	function_obj(matrix_size)
	delta_t = datetime.now() - t0
	return delta_t

def execute_performance_test(matrix_sizes: list):
	print('Performance matrix Multiplication:')
	for matrix_size in matrix_sizes:
		dt_py_list_matrix_mult = get_execution_delta_t(py_list_matrix_multiplication, matrix_size)
		dt_numpy_array_matrix_mult = get_execution_delta_t(numpy_array_matrix_multiplication, matrix_size)

		print('\t\t\tPY-list_matrix dt\tNumpy Array matrix dt')
		print(f'Matrix size = {matrix_size}\t{dt_py_list_matrix_mult}\t\t{dt_numpy_array_matrix_mult}')

# testing
execute_performance_test(matrix_sizes)